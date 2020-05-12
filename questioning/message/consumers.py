import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MessageConsumer(AsyncWebsocketConsumer):
    """消息功能"""

    async def connect(self):
        if self.scope['user'].is_anonymous:
            #匿名用户
            await self.close()
        else:
            #加入聊天组
            await self.channel_layer.group_add(
                self.scope['user'].username,
                self.channel_name
            )
            await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        #接受私信
        await self.send(text_data=json.dumps(text_data))

    async def disconnect(self, code):
        #离开聊天组
        await self.channel_layer.group_discard(
            self.scope['user'].username,
            self.channel_name
        )
