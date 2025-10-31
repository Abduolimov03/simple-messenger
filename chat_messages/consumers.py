import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message, MessageStatus
from django.utils.timezone import now

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):

        data = json.loads(text_data)

        if data.get("event") == "typing_start":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_event",
                    "username": data.get("username"),
                    "status": "start",
                },
            )
            return

        if data.get("event") == "typing_stop":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_event",
                    "username": data.get("username"),
                    "status": "stop",
                },
            )
            return

        if data.get("event") == "mark_read":
            message_id = data.get("message_id")
            username = data.get("username")
            try:
                user = User.objects.get(username=username)
                msg_status = MessageStatus.objects.get(message_id=message_id, user=user)
                msg_status.is_read = True
                msg_status.read_at = now()
                msg_status.save()

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "read_update",
                        "message_id": message_id,
                        "username": username,
                        "read_at": msg_status.read_at.strftime("%H:%M:%S"),
                    },
                )
            except (User.DoesNotExist, MessageStatus.DoesNotExist):
                pass
            return

        message = data.get("message")
        sender_username = data.get("sender")
        receiver_username = data.get("receiver")

        await self.save_message(sender_username, receiver_username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_username,
                "receiver": receiver_username,
                "timestamp": now().strftime("%H:%M:%S"),
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing_event(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "event": "typing",
                    "username": event["username"],
                    "status": event["status"],
                }
            )
        )

    async def read_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "event": "read_update",
                    "message_id": event["message_id"],
                    "username": event["username"],
                    "read_at": event["read_at"],
                }
            )
        )

    @staticmethod
    async def save_message(sender_username, receiver_username, message):
        try:
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver_username)
            msg = Message.objects.create(sender=sender, receiver=receiver, content=message)
            MessageStatus.objects.create(message=msg, user=receiver)
        except User.DoesNotExist:
            pass
