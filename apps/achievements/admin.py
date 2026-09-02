"""IIC-IEM – Achievements Admin"""
from django.contrib import admin
from .models import Achievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'is_featured']
    list_filter = ['category', 'is_featured']
    search_fields = ['title']
