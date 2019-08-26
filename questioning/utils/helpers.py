from functools import wraps

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.exceptions import PermissionDenied

from utils.alipay import AliPay


def ajax_required(func):
    '''
    验证是否为ajax请求
    :param func:
    :return:
    '''
    @wraps(func)
    def _wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('ajax required')
        return func(request, *args, **kwargs)

    return _wrapper


class AuthorRequiredMixin(View):
    '''
    验证是否为作者
    '''
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.username != self.request.user.username:
            raise PermissionDenied()
        return super(AuthorRequiredMixin, self).dispatch(request, *args, **kwargs)


def get_alipay_url(order_sn, order_mount):
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,
        app_notify_url=settings.APP_NOTIFY_URL,
        app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
        alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
        debug=settings.ALIPAY_DEBUG,
        return_url=settings.RETURN_URL
    )

    url = alipay.direct_pay(
        subject=order_sn,
        out_trade_no=order_sn,
        total_amount=order_mount,
    )
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    return re_url


def convert_rmb_to_money(rmb:float) -> float:
    """
    把人民币转换成对应的金币
    ￥5 = 50金币 ￥10 = 120金币 ￥50 = 600金币 ￥100 = 1500金币
    :param rmb: float
    """
    d = {
        5: 50.00,
        10: 120.00,
        50: 600.00,
        100: 1500.00
    }
    money = 0.00
    if rmb not in d:
        money = rmb * 10
    else:
        money = d[rmb]

    return money
