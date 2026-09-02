"""
IIC-IEM Website – Users App Admin Registration
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminActivityLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('IIC Admin Fields', {
            'fields': ('role', 'profile_photo', 'bio', 'last_login_ip'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('IIC Admin Fields', {
            'fields': ('email', 'role'),
        }),
    )


@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = ['admin_user', 'action', 'model_name', 'object_repr', 'ip_address', 'created_at']
    list_filter = ['action', 'model_name']
    search_fields = ['admin_user__username', 'model_name', 'object_repr']
    readonly_fields = ['admin_user', 'action', 'model_name', 'object_id', 'object_repr', 'details', 'ip_address', 'created_at']
    ordering = ['-created_at']
