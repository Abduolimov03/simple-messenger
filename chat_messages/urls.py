from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, MediaViewSet, MessageStatusViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'media', MediaViewSet, basename='media')
router.register(r'status', MessageStatusViewSet, basename='status')

urlpatterns = router.urls
