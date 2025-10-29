from rest_framework import serializers
from .models import Chat
from chats.models import ChatMember
# from users.models import User

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'chat_type', 'title', 'creator', 'members']
        read_only_fields = ['created_at']

class ChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = ['id', 'chat', 'role', 'is_muted']
        read_only_fields = ['joined_at']