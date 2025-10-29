from django.contrib import admin
from .models import User, Device

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'phone_number', 'is_online', 'last_seen']

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'device_name', 'platform', 'ip_address', 'login_time', 'last_active']
