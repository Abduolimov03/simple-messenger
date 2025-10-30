from rest_framework import serializers
from .models import Device, User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True, validators=[validate_password])
    password2 = serializers.CharField(write_only = True, required = True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'bio', 'profile_photo', 'is_online', 'last_seen', 'password', 'password2']

    def create(self, validate_data):
        password = validate_data.pop('password')
        user = User(**validate_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'bio', 'profile_photo', 'is_online', 'last_seen']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'user', 'device_name', 'platform', 'ip_address', 'login_time', 'last_active']

