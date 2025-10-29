from django.shortcuts import render
from django.http import HttpResponse
from .serializers import ChatMemberSerializer, ChatSerializer
from rest_framework import viewsets
from .models import ChatMember, Chat

# Create your views here.


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class ChatMemberViewset(viewsets.ModelViewSet):
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer