from django.urls import path

from questioning.trade import views

app_name = 'trade'

urlpatterns = [
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('pay/', views.ConfirmPayView.as_view(), name='pay'),
    path('alipay/return/', views.AlipayView.as_view(), name='alipay'),
    path('pay/verify/', views.PaySuccessView.as_view(), name='verify'),

    path('orderinfo/', views.OrderInfoView.as_view(), name='orderinfo')
]
