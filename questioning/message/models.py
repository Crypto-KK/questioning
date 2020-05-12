import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from questioning.utils.models import CreatedUpdatedMixin


class MessageQuerySet(models.query.QuerySet):
    def get_conversation(self, sender, recipient):
        '''用户的私信会话'''
        qs_one = self.filter(sender=sender, recipient=recipient).select_related('sender', 'recipient')  #a给b
        qs_two = self.filter(sender=recipient, recipient=sender).select_related('sender', 'recipient')  #b给a

        return qs_one.union(qs_two).order_by('created_at')  #时间排序

    def get_most_recent_conversation(self, recipient):
        '''最近一次私信的用户'''
        try:
            qs_sent = self.filter(sender=recipient).select_related('sender', 'recipient') #当前用户发送的消息
            qs_received = self.filter(recipient=recipient).select_related('sender', 'recipient')#当前登录用户接受的消息

            qs = qs_sent.union(qs_received).latest('created_at')#最后一条消息

            # 如果登录用户有发送消息，返回消息的接受者
            if qs.sender == recipient:
                return qs.recipient

            # 发送者

            return qs.sender
        except self.model.DoesNotExist:
            #返回当前用户
            return get_user_model().objects.get(username=recipient.username)


@python_2_unicode_compatible
class Message(CreatedUpdatedMixin, models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                               verbose_name='uid')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages',
                               blank=True, null=True, on_delete=models.SET_NULL,
                               verbose_name='发送者')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages',
                                  blank=True, null=True, on_delete=models.SET_NULL,
                                  verbose_name='接受者')
    message = models.TextField(blank=True, null=True, verbose_name='内容')
    unread = models.BooleanField(default=True, db_index=True, verbose_name='是否未读')

    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = verbose_name
        ordering = ('-created_at', )

    def __str__(self):
        return self.message

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
