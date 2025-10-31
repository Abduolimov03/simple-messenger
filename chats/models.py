from django.db import models
from users.models import User
# from django.contrib.auth.models import User
from django.utils import timezone


class Chat(models.Model):
    CHAT_TYPES = (
        ('private', 'Private'),
        ('group', 'Group'),
        ('channel', 'Channel'),
    )

    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES)
    title = models.CharField(max_length=255, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_chats')
    created_at = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(User, through='ChatMember', related_name='chats')

    def __str__(self):
        return self.title or f"{self.chat_type} chat"


class ChatMember(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('owner', 'Owner'),
    )

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(default=timezone.now)
    is_muted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('chat', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.chat}"

