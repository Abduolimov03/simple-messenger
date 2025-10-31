from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import ChatMemberViewset, ChatViewSet, AddMemberToChannel

router = DefaultRouter()
router.register(r'messages_chat', ChatMemberViewset, basename='message_chat')
router.register(r'chat_chat', ChatViewSet, basename='media_chat')
# router.register(r'add_member', AddMemberToChannel, basename='add_member')

urlpatterns = router.urls

urlpatterns += [
    # path('add_member/',AddMemberToChannel.as_view(),name='add_member')
]