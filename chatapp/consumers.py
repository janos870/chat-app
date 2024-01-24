from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import ChatMessage, ChatRoom
from django.contrib.auth.models import User

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.channel_name,
            self.room_group_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']     
        chatroom = data['chatroom']

        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chatroom': chatroom
            }
        )

        await self.save_message(username, chatroom, message)
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chatroom = event['chatroom']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chatroom': chatroom,
        }))

    @sync_to_async
    def save_message(self, username, chatroom, message):
        user = User.objects.get(username=username)
        chatroom = ChatRoom.objects.get(slug=chatroom)
        ChatMessage.objects.create(user=user, chatroom=chatroom, message=message)
