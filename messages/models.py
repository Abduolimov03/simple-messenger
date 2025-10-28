from datetime import timezone
from django.db import models
from chats.models import Chat
from users.models import User

# Create your models here.

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(default=timezone.now)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}" if self.content else "Media message"
    

class MessageStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('message', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.message.id} ({'read' if self.is_read else 'unread'})"