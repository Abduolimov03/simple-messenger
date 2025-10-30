from django.shortcuts import render
from rest_framework import viewsets, permissions
from users.models import User
from .models import Media, Message, MessageStatus
from .serializers import MediaSerilizer, MessageSerializer, MessageStatusSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        serializer.save(sender=user)
    # permission_classes = [permissions.AllowAny]
    #
    # def perform_create(self, serializer):
    #     serializer.save(sender=self.request.user)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerilizer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [IsAuthenticated]  # ← test uchun

    # def perform_create(self, serializer):
    #     user = self.request.user if self.request.user.is_authenticated else User.objects.first()
    #     serializer.save(sender=user)

    def perform_create(self, serializer):
        serializer.save()

class MessageStatusViewSet(viewsets.ModelViewSet):
    queryset = MessageStatus.objects.all()
    serializer_class = MessageStatusSerializer
    permission_classes = [permissions.AllowAny]

    


