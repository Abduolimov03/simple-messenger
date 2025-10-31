from django.shortcuts import render
from django.http import HttpResponse
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