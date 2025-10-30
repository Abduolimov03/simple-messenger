from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DeviceViewSet, CustomTokenObtainPairView, LogoutView, RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'register',RegisterView, basename='register')
router.register(r'login',LoginView, basename='login')
router.register(r'token',CustomTokenObtainPairView, basename='token')
router.register(r'logout',LogoutView, basename='logout')

urlpatterns = [
    path('', include(router.urls)),
]
