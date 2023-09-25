# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Room 
import json
from asgiref.sync import async_to_sync
class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
    
        user_id = await self.get_user_id(self.scope["user"].id) 
        if user_id:
            self.room_id = self.scope['url_route']['kwargs']['room_id']
            self.room_group_name = f"room_{self.room_id}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        user = self.scope["user"]
        if user.is_authenticated:
            sender_username = user.username
        else:
            sender_username = "Guest"

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'run_game',
                'payload': text_data,
            }
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                 'message': f"{sender_username}: {text_data}",
        })
        
        

    async def run_game(self,event):
        data = event['payload'] 
        data = json.loads(data)
        print("hi",data['data'])
        self.send(text_data= json.dumps({ 
            'payload'  : data['data']
        }))

    async def chat_message(self, event):
    
        message = event['message']
        await self.send(text_data=message)

    


    @database_sync_to_async
    def get_user_id(self, user_id):
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            return user.id
        except User.DoesNotExist:
            return None
