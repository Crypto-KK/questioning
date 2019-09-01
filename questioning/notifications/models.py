import uuid

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.core import serializers

from questioning.utils.models import CreatedUpdatedMixin


@python_2_unicode_compatible
class NotificationQuerySet(models.query.QuerySet):

    def unread(self):
        return self.filter(unread=True)

    def read(self):
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """标记所有已读
        :param recipient --接收者
        """
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        return qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """标记所有未读
        :param recipient --接收者
        """
        qs = self.read()
        if recipient:
            qs = qs.filter(recipient=recipient)
        return qs.update(unread=True)

    def get_most_recent(self, recipient=None):
        """获取最近五条通知
        :param recipient: 接收者
        """
        qs = self.unread()[:5]
        if recipient:
            qs = qs.filter(recipient=recipient)[:5]
        return qs

    def serialize_latest_notifications(self, recipient=None):
        """序列化成JSON格式
        :param recipient: 接收者
        """
        qs = self.get_most_recent(recipient)
        return serializers.serialize('json', qs)


@python_2_unicode_compatible
class Notification(CreatedUpdatedMixin, models.Model):
    """"""
    NOTIFICATION_TYPE = (
        ('L', '赞了'),
        ('C', '评论了'),
        ('A', '回答了'),
        ('W', '接受了回答'),
        ('R', '回复了'),
    )

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_actor',
                              on_delete=models.CASCADE, verbose_name='触发者')

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                  related_name='notifications', on_delete=models.CASCADE)
    unread = models.BooleanField(default=True, db_index=True, verbose_name='是否未读')
    verb = models.CharField(max_length=1, choices=NOTIFICATION_TYPE)
    content_type = models.ForeignKey(ContentType, related_name='notify_action_object',
                                     null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    action_object = GenericForeignKey()
    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name
        ordering = ('-created_at', )

    def __str__(self):
        if self.action_object:
            return f'{self.actor} {self.get_verb_display()} {self.action_object}'
        return f'{self.actor} {self.get_verb_display()}'
