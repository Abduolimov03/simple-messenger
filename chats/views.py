from django.shortcuts import render
from django.http import HttpResponse
from .serializers import ChatMemberSerializer, ChatSerializer
from rest_framework import viewsets
from .models import ChatMember, Chat
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

class ChatMemberViewset(viewsets.ModelViewSet):
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [IsAuthenticated]