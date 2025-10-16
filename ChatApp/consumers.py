import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ChatApp.models import Message, Room  # adjust imports if needed

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"room_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = data.get('sender')
        message = data.get('message')

        # Optional: save message
        # await self.save_message(sender, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender,
                'message': message
            }
        )

    async def chat_message(self, event):
        sender = event['sender']
        message = event['message']

        await self.send(text_data=json.dumps({
            'sender': sender,
            'message': message
        }))

    # Optional save function if needed
    @database_sync_to_async
    def save_message(self, sender, message):
        room = Room.objects.get(name=self.room_name)
        return Message.objects.create(sender=sender, content=message, room=room)
