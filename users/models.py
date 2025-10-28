from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    phone_number = models.CharField(max_length=14, unique=True)
    bio = models.TextField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photo/', null=True, blank=True, default='default_photo/')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username or self.phone_number

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=120)
    platform = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    login_time = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.device_name} - {self.platform}"

