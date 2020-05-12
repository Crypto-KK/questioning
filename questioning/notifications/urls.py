from django.urls import path

from questioning.notifications import views

app_name = "notifications"

urlpatterns = [
    path('', views.NotificationUnreadListView.as_view(), name='unread'),
    path('mark-as-read/<str:pk>/', views.mark_as_read,name='mark_as_read'),
    path('mark-all-read/', views.mark_all_as_read,name='mark_all_read'),
    path('latest-notifications/', views.get_latest_notifications, name='latest_notifications')
]
