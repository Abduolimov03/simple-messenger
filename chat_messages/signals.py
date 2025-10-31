from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, MessageStatus
from chats.models import ChatMember

@receiver(post_save, sender=Message)
def create_message_statuses(sender, instance, created, **kwargs):
    if created:
        members = ChatMember.objects.filter(chat=instance.chat)
        for member in members:
            MessageStatus.objects.create(
                message=instance,
                user=member.user,
                is_read=(member.user==instance.sender)
            )
