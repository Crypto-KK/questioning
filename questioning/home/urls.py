from django.urls import path
from questioning.home import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeList.as_view(), name='list'),
]
