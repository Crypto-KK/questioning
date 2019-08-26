from django.urls import path

from questioning.trade import views

app_name = 'trade'

urlpatterns = [
    path('deposit/', views.DepositView.as_view(), name='deposit'),

]
