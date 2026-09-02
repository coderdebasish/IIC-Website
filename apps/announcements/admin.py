"""IIC-IEM – Announcements Admin"""
from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_active', 'show_on_home', 'created_at']
    list_filter = ['is_active', 'priority', 'show_on_home']
    search_fields = ['title']
