from django.dispatch import receiver
from django.db.models.signals import post_save

from questioning.trade.models import OrderInfo, AccountDetail
from questioning.trade import Status

@receiver(post_save, sender=OrderInfo)
def finish_deposit(sender, instance=None, created=False, **kwargs):
    """完成充值后，写入到流水中"""

    if not created: #第一次created交易状态是待支付，所以这里不是created
        if instance.pay_status == Status.TRADE_SUCCESS.value:
            # 充值成功
            AccountDetail.objects.create(
                user=instance.user,
                mount=instance.order_mount,
                current_money=instance.user.money,
                description="在线充值"
            )

