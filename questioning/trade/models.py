from __future__ import unicode_literals

import uuid

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from questioning.trade import ORDER_STATUS
from questioning.utils.models import CreatedUpdatedMixin
from questioning.utils.helpers import convert_rmb_to_money

@python_2_unicode_compatible
class OrderInfo(CreatedUpdatedMixin, models.Model):
    '''
    充值订单详情
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付流水号')

    pay_status = models.CharField(choices=ORDER_STATUS, max_length=40, verbose_name='订单状态', default='paying')
    order_mount = models.DecimalField(verbose_name="充值金额", max_digits=10,
                                decimal_places=2, default=0.00)


    class Meta:
        verbose_name = "充值订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn

    def get_money(self):
        """获取实际金币的数量"""
        return convert_rmb_to_money(self.order_mount.to_integral())


@python_2_unicode_compatible
class AccountDetail(CreatedUpdatedMixin, models.Model):
    """
    消费金币的流水记录
    """
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                               editable=False, verbose_name='uid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    mount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2,
                                verbose_name='金额变化')
    current_money = models.DecimalField(default=0.00, max_digits=10, decimal_places=2,
                                verbose_name='当前金币')
    description = models.CharField(max_length=255, verbose_name='说明')


    class Meta:
        verbose_name = '账户明细'
        verbose_name_plural = verbose_name
