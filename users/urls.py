from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DeviceViewSet, CustomTokenObtainPairView, LogoutView, RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'register', RegisterView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    # path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
]
