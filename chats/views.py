from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError

from .serializers import ChatMemberSerializer, ChatSerializer
from rest_framework import viewsets
from .models import ChatMember, Chat
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny



class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [AllowAny]

class ChatMemberViewset(viewsets.ModelViewSet):
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        elif 'user' in self.request.data:
            from users.models import User
            try:
                user = User.objects.get(id=self.request.data['user'])
            except User.DoesNotExist:
                raise ValidationError({"user": "Foydalanuvchi topilmadi"})
        serializer.save(user=user)
