from messages.models import Message
from django.db import models
from datetime import timezone

# Create your models here.

class Media(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    )

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='message_media/')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.media_type} for message {self.message.id}"

