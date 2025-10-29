from rest_framework import serializers
from .models import Message, Media, MessageStatus
from users.serializers import UserSerializer


class MediaSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'media_type', 'uploaded_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    media = MediaSerilizer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'chat', 'sender', 'content', 'sent_at',
            'is_edited', 'is_deleted', 'reply_to', 'media'
        ]

class MessageStatusSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MessageStatus
        fields = [
            'id', 'message', 'user', 'is_read', 'read_at'
        ]