from django.contrib import admin
from .models import Message, Media, MessageStatus
# Register your models here.

admin.site.register(Message)
admin.site.register(Media)
admin.site.register(MessageStatus)

