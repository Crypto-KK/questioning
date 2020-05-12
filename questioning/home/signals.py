from django.dispatch import receiver
from django.db.models.signals import post_save

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from questioning.home.models import Item


@receiver(post_save, sender=Item)
def item_save(sender, instance=None, created=False, **kwargs):
    """新增动态时，首页出现通知"""
    # channel_layer = get_channel_layer()
    # payload = {
    #     'type': 'receive',
    #     'key': 'home_new',
    #     'actor_name': instance.user.username
    # }
    # async_to_sync(channel_layer.group_send)('notifications', payload)
    pass
