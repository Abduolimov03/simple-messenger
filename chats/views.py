from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError

from .serializers import ChatMemberSerializer, ChatSerializer
from rest_framework import viewsets
from .models import ChatMember, Chat
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


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
                raise ValidationError({"user": "User not found"})

        chat = self.request.data.get('chat')
        if not chat:
            raise ValidationError({"chat": "Chat field is required"})
        try:
            chat = Chat.objects.get(id=chat)
        except Chat.DoesNotExist:
            raise ValidationError({"chat": "Chat not found"})
        serializer.save(user=user, chat=chat)


class AddMemberToChannel(viewsets.ModelViewSet):
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        try:
            chat = self.get_object()
        except Chat.DoesNotExist:
            return Response({"error":"Chat doese not exist"},status=status.HTTP_404_NOT_FOUND)
        serializer = ChatMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat=chat)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)