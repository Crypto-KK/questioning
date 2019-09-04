from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.views.generic import ListView, DeleteView

from questioning.utils.helpers import ajax_required, AuthorRequiredMixin

from questioning.notifications.models import Notification


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
