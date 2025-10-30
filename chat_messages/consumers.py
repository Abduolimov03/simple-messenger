import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from django.utils.timezone import now

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Kanalga ulanish
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_username = data["sender"]
        receiver_username = data["receiver"]

        await self.save_message(sender_username, receiver_username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_username,
                "receiver": receiver_username,
                "timestamp": now().strftime("%H:%M:%S"),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @staticmethod
    async def save_message(sender_username, receiver_username, message):
        try:
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver_username)
            Message.objects.create(
                sender=sender, receiver=receiver, content=message
            )
        except User.DoesNotExist:
            pass
