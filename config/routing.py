from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from questioning.message.consumers import MessageConsumer

#self.scope['protocol'] 获取协议
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/<str:username>/', MessageConsumer)
            ])
        )
    ),
    #http自动加载
})
