from rest_framework import serializers
from .models import Device, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'bio', 'profile_photo', 'is_online', 'last_seen']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'user', 'device_name', 'platform', 'ip_address', 'login_time', 'last_active']

