from decimal import Decimal

from django.dispatch import receiver
from django.db.models.signals import post_save

from questioning.articles.models import Article
from questioning.trade.models import AccountDetail


@receiver(post_save, sender=Article)
def article_save(sender, instance=None, created=False, **kwargs):
    """保存文章时，新增首页内容"""
    instance.home_items.update_or_create(
        user=instance.user
    )

    #创建文章时，用户金币 + 1
    if created:
        instance.user.money += Decimal(0.1)

        # 账户流水变动
        AccountDetail.objects.create(
            user=instance.user,
            mount=Decimal(0.1),
            current_money=instance.user.money,
            description="发表一篇文章"
        )
