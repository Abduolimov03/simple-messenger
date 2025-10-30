from datetime import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from .models import User, Device
from .serializers import UserSerializer, RegisterSerializer, DeviceSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import generics
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(datail=False, method=['get'], permission_classes = [permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)



class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        class CustomTokenObtainPairView(TokenObtainPairView):
            serializer_class = CustomTokenObtainPairSerializer

            def post(self, request, *args, **kwargs):
                response = super().post(request, *args, **kwargs)
                if response.status_code == 200:
                    try:
                        user = User.objects.get(username=request.data.get('username'))
                        user.is_online = True
                        user.last_seen = timezone.now()
                        user.save(update_fields=['is_online', 'last_seen'])
                    except Exception:
                        pass
                return response


        class LogoutView(APIView):
            permission_classes = (permissions.IsAuthenticated,)

            def post(self, request):

                refresh_token = request.data.get("refresh")
                if not refresh_token:
                    return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception as e:
                    return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

                request.user.is_online = False
                request.user.last_seen = timezone.now()
                request.user.save(update_fields=['is_online', 'last_seen'])
                return Response(status=status.HTTP_205_RESET_CONTENT)

    
