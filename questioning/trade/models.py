from __future__ import unicode_literals

import time
from random import Random

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from questioning.trade import ORDER_STATUS
from questioning.utils.models import CreatedUpdatedMixin

@python_2_unicode_compatible
class OrderInfo(CreatedUpdatedMixin, models.Model):
    '''
    充值订单详情
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付订单号')

    pay_status = models.CharField(choices=ORDER_STATUS, max_length=40, verbose_name='订单状态', default='paying')
    order_mount = models.DecimalField(verbose_name="充值金额", max_digits=10,
                                decimal_places=2, default=0.00)
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    class Meta:
        verbose_name = "充值订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        '''保存到数据库时生成订单号'''
        ranstr = Random()
        order_sn = '{time_str}{userid}{ranstr}'.format(
            time_str=time.strftime('%Y%m%d%H%M%S'),
            userid=self.user.pk,
            ranstr=ranstr.randint(10, 99)
        )
        self.order_sn = order_sn
        super().save(force_insert=False, force_update=False, using=None,
             update_fields=None)
