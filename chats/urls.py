from rest_framework.routers import DefaultRouter

from .views import ChatMemberViewset, ChatViewSet

router = DefaultRouter()
router.register(r'messages', ChatMemberViewset, basename='message')
router.register(r'chat', ChatViewSet, basename='media')

urlpatterns = router.urls
