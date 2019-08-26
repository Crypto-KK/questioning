import time
from datetime import datetime
from decimal import Decimal
from random import Random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.base import View, TemplateView
from rest_framework.response import Response

from questioning.utils.helpers import AuthorRequiredMixin, convert_rmb_to_money
from questioning.utils.alipay import AliPay
from questioning.utils.helpers import get_alipay_url
from questioning.trade.models import OrderInfo


class DepositView(LoginRequiredMixin, AuthorRequiredMixin, TemplateView):
    template_name = 'trade/deposit.html'


class ConfirmPayView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def post(self, request):
        order_sn = self.generate_order_sn(user=request.user)
        order_mount = request.POST.get('money', None)
        if not order_mount:
            return redirect(reverse('users:detail'))

        OrderInfo.objects.create(
            user=request.user,
            order_sn=order_sn,
            order_mount=order_mount,
        )
        url = get_alipay_url(order_sn, order_mount)

        return JsonResponse({
            'pay_url': url,
            'order_sn': order_sn
        })


    def generate_order_sn(self, user):
        ranstr = Random()
        order_sn = '{time_str}{userid}{ranstr}'.format(
            time_str=time.strftime('%Y%m%d%H%M%S'),
            userid=user.pk,
            ranstr=ranstr.randint(10, 99)
        )
        return order_sn


class AlipayView(LoginRequiredMixin, AuthorRequiredMixin, View):
    """
    支付宝支付
    get方法实现支付宝return_url，如果没有实现也无所谓，post同样可以更新状态
    post方法实现支付宝notify_url，异步更新

    支付宝返回的url如下：
    #http://127.0.0.1:8000/alipay/return/?
    # charset=utf-8&
    # out_trade_no=201902923423436&
    # method=alipay.trade.page.pay.return&
    # total_amount=1.00&
    # sign=CDBMY9NBsp4KICdQoBEVxGWobd0N8y4%2BU09stzUWwlNtLr7ZpELJdM5js20wXv%2FCPp0FGPbRW1YS9DRx0CnKJULZZMqysBUMH2FL39sS0Fgstgy1ydTs7ySXdHziJV0inI%2BDWAsebQqtjk5gQEweUstc%2B%2BnzjdgAulpvWzfJsbknS%2BqUfktSdF2ZOWGhr1CFlfsMFEDS2nzQv4K3E%2BNaeylkzUnRe9M1sjIL%2FYR0wVZ5A3OfHLPf9HzC2B8%2FLu4g7N5Vctkqp2aerDvIkN5SNmDnRGyjOt2b%2BOsLMqG4X0h6JSsrZT6Ln8PimsrkSOIGbj0gCqscx7BwZfmCQePlCw%3D%3D&
    # trade_no=2019082622001426981000041778&
    # auth_app_id=2016092600597838&
    # version=1.0&app_id=2016092600597838&
    # sign_type=RSA2&
    # seller_id=2088102177296610&
    # timestamp=2019-08-26+13%3A51%3A01
    """
    def dispatch(self, request, *args, **kwargs):
        self.alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=settings.APP_NOTIFY_URL,
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            debug=settings.ALIPAY_DEBUG,
            return_url=settings.RETURN_URL
        )
        #处理返回的url参数
        callback_data = {}
        for key, value in request.GET.items():
            callback_data[key] = value
        sign = callback_data.pop('sign', None)
        self.order_sn = callback_data.get('out_trade_no', None) #订单号
        self.trade_no = callback_data.get('trade_no', None) #支付宝订单号

        # 验证签名
        self.verify = self.alipay.verify(callback_data, sign)
        return super(AlipayView, self).dispatch(request, *args, **kwargs)


    def get(self, request):
        """处理支付宝return_url返回"""

        if self.verify:
            self.deposit()
            #返回个人中心页面
            return redirect(reverse('users:detail', kwargs={
                'username': request.user.username
            }))

    def post(self, request):
        """
        处理notify_url
        """
        if self.verify:
            self.deposit()

        return Response('success')

    def deposit(self):
        """充值操作

        1.更新用户的金币信息
        2.更新订单状态为交易成功
        """

        # 数据库中查询订单记录
        order = OrderInfo.objects.get(order_sn=self.order_sn)
        order.trade_no = self.trade_no  # 支付宝订单号

        # 把人民币转换成对应的金币
        rmb = order.order_mount
        money = convert_rmb_to_money(rmb)

        # 更新用户的金币
        order.user.money += Decimal(money)
        order.user.save()
        # 订单状态置为交易成功
        order.pay_status = 'TRADE_SUCCESS'
        order.save()


class PaySuccessView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def post(self, request):
        order_sn = request.POST['order_sn']

        order = OrderInfo.objects.get(order_sn=order_sn)
        if order:
            if order.pay_status == 'TRADE_SUCCESS':
                #支付成功
                return JsonResponse({
                    'status': 'ok'
                })

        return JsonResponse({
            'status': 'fail'
        })

