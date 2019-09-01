from django.urls import path

from questioning.message import views

app_name = 'messager'

urlpatterns = [
    path('', views.MessagesListView.as_view(), name='messages_list'),
    path('send-message/', views.send_message, name='send_message'),
    path('receive-message/', views.receiver_message, name='receive_message'),
    path('<username>/', views.ConversationListView.as_view(), name='conversation_detail'),
]
