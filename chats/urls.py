from rest_framework.routers import DefaultRouter

from .views import ChatMemberViewset, ChatViewSet

router = DefaultRouter()
router.register(r'messages_chat', ChatMemberViewset, basename='message_chat')
router.register(r'chat_chat', ChatViewSet, basename='media_chat')

urlpatterns = router.urls
