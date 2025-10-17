import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ChatApp.models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Debug: log connection attempt
        print(f"[ChatConsumer] connect attempt: scope={self.scope.get('path', '')}")
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        print(f"[ChatConsumer] connected to {self.room_name} channel_name={self.channel_name}")
        
    async def disconnect(self, close_code):
        print(f"[ChatConsumer] disconnect: room={getattr(self, 'room_name', None)} code={close_code}")
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        print(f"[ChatConsumer] receive raw: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json

        event = {
            'type': 'send_message',
            'message': message,
        }

        await self.channel_layer.group_send(self.room_name, event)


    async def send_message(self, event):
        data = event['message']
        # Do not save to database, just broadcast
        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        payload = json.dumps({'message': response_data})
        print(f"[ChatConsumer] sending payload: {payload}")
        # Save message in DB for persistence
        await self.create_message(data)
        await self.send(text_data=payload)

    @database_sync_to_async
    def create_message(self, data):
        try:
            get_room_by_name = Room.objects.get(room_name=data.get('room_name'))
        except Room.DoesNotExist:
            get_room_by_name = Room.objects.create(room_name=data.get('room_name'))
        Message.objects.create(room=get_room_by_name, sender=data.get('sender'), message=data.get('message'))
        
