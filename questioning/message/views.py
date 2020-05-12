from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from channels.layers import get_channel_layer
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async

from questioning.message.models import Message
from questioning.utils.helpers import ajax_required


class MessagesListView(LoginRequiredMixin, ListView):
    '''
    所有用户的私信列表
    '''
    model = Message
    # paginate_by = 10
    template_name = 'message/message_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MessagesListView, self).get_context_data(
            object_list=None, **kwargs)
        context['users_list'] = get_user_model().objects.filter(is_active=True).exclude(
            username=self.request.user.username
        ).order_by('-last_login')[:10]

        #最近互动的用户
        last_conversation = Message.objects.get_most_recent_conversation(
            self.request.user)
        context['active'] = last_conversation
        return context

    def get_queryset(self):
        '''最近私信互动的内容'''
        active_user = Message.objects.get_most_recent_conversation(
            self.request.user)
        return Message.objects.get_conversation(sender=active_user,
                                                recipient=self.request.user)

class ConversationListView(MessagesListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            object_list=None, **kwargs)
        context['active'] = self.kwargs['username']
        return context

    def get_queryset(self):
        active_user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return Message.objects.get_conversation(self.request.user, active_user)


@login_required
@ajax_required
@require_POST
def send_message(request):
    '''AJAX POST'''
    sender = request.user
    recipient_username = request.POST['to']
    recipient = get_user_model().objects.get(username=recipient_username)
    message = request.POST['message']
    if len(message.strip()) != 0 and sender != recipient:
        msg = Message.objects.create(
            sender=sender,
            recipient=recipient,
            message=message
        )
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'message': render_to_string('message/single_message.html', {'message': msg}),
            'sender': sender.username
        }
        async_to_sync(channel_layer.group_send)(recipient_username, payload)
        return render(request, 'message/single_message.html', {
            'message': msg
        })

    return HttpResponse()


@login_required
@ajax_required
@require_POST
def receiver_message(request):
    '''AJAX GET'''
    message_id = request.GET['message_id']
    msg = Message.objects.get(pk=message_id)
    return render(request, 'message/single_message.html', {
        'message': msg
    })
