import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    """通知应用"""

    async def connect(self):
        #建立连接
        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_add('notifications', self.channel_name)
            await self.accept()

        else: #未登录用户
            await self.close()


    async def receive(self, text_data=None, bytes_data=None):
        """返回给前端"""
        await self.send(text_data=json.dumps(text_data))


    async def disconnect(self, code):
        """断开连接"""
        self.channel_layer.group_discard("notifications", self.channel_name)

