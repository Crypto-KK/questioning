from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth import get_user_model

from questioning.utils.exceptions import InvalidUserInstanceException
from questioning.notifications.models import Notification


User = get_user_model()

class NotificationUnreadListView(LoginRequiredMixin, ListView):
    '''未读通知列表'''
    model = Notification

    def get_queryset(self):
        return self.request.user.notifications.unread()


@login_required
def get_latest_notifications(request):
    """获取最近未读的通知"""
    notifications = request.user.notifications.get_most_recent()
    return render(request, 'notifications/most_recent.html', {
        'notifications': notifications
    })


@login_required
def mark_as_read(request, pk):
    """根据pk"""
    notification = get_object_or_404(Notification, pk=pk)
    notification.mark_as_read()
    redirect_url = request.GET.get('next')
    messages.add_message(request, messages.SUCCESS,
                         f'通知{notification}标为已读')

    if redirect_url:
        return redirect(redirect_url)

    return redirect(reverse_lazy('notifications:unread'))

@login_required
def mark_all_as_read(request):
    '''已读'''
    request.user.notifications.mark_all_as_read()
    redirect_url = request.GET.get('next')
    messages.add_message(request, messages.SUCCESS,
                         f'用户{request.user.username}的所有通知已读')

    if redirect_url:
        return redirect(redirect_url)

    return redirect(reverse_lazy('notifications:unread'))


def push_notification(actor: User, recipient: User, verb: str,
                      action_object, **kwargs) -> None:
    """推送通知给特定用户

    :param actor: request.user
    :param recipient: User instance 一个或多个接受者
    :param verb: 类别
    :param action_object: 对象示例
    :param kwargs: key, id_value
    """
    if not isinstance(actor, User) and not isinstance(recipient, User):
        raise InvalidUserInstanceException("must be user instance")

    if recipient.username == action_object.user.username: #只通知接受者

        key = kwargs.get('key', 'notifications')
        id_value = kwargs.get('id_value', None)

        #记录通知内容
        Notification.objects.create(
            actor=actor,
            recipient=recipient,
            verb=verb,
            action_object=action_object
        )

        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': key,
            'actor_name': actor.username,
            'id_value': id_value
        }

        async_to_sync(channel_layer.group_send)("notifications", payload)

