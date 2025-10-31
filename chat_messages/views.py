from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

from users.models import User
from .models import Media, Message, MessageStatus
from .serializers import MediaSerilizer, MessageSerializer, MessageStatusSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from log.log import setup_logger

logger = setup_logger('chat_messages')


class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):

        user = self.request.user
        if not user.is_authenticated:
            user = User.objects.first()  # test uchun vaqtincha

        message = serializer.save(sender=user)
        logger.info(f"New message created: ID={message.id}, Sender={user.username}")
        return message

    @action(detail=True, methods=['patch'], url_path='mark_read')
    def mark_read(self, request, pk=None):

        message = self.get_object()
        user = request.user

        if not user.is_authenticated:
            user = User.objects.first()

        try:
            status_obj, created = MessageStatus.objects.get_or_create(
                message=message,
                user=user,
                defaults={'is_read': True, 'read_at': timezone.now()}
            )

            if not created and not status_obj.is_read:
                status_obj.is_read = True
                status_obj.read_at = timezone.now()
                status_obj.save()

            logger.info(f"Message ID={message.id} marked as read by {user.username}")

            return Response(
                {'message': f'Message {message.id} marked as read'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Error marking message as read: {str(e)}")
            return Response(
                {'error': 'Failed to mark message as read'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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

    


