from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Media, Message, MessageStatus
from .serializers import MediaSerilizer, MessageSerializer, MessageStatusSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerilizer
    permission_classes = [permissions.IsAuthenticated]

class MessageStatusViewSet(viewsets.ModelViewSet):
    queryset = MessageStatus.objects.all()
    serializer_class = MessageStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    


