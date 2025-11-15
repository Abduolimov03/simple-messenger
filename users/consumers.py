import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()


class UserStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.user_group_name = f"user_{self.username}"

        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

        await self.set_user_online_status(True)

        await self.channel_layer.group_send(
            self.user_group_name,
            {
                "type": "user_status",
                "status": "online",
                "username": self.username,
            }
        )

    async def disconnect(self, close_code):

        await self.set_user_online_status(False)

        await self.channel_layer.group_send(
            self.user_group_name,
            {
                "type": "user_status",
                "status": "offline",
                "username": self.username,
                "last_seen": now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def user_status(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def set_user_online_status(self, is_online):
        try:
            user = User.objects.get(username=self.username)
            profile = user.profile
            profile.is_online = is_online
            if not is_online:
                profile.last_seen = now()
            profile.save()
        except User.DoesNotExist:
            pass
