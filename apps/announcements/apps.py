"""
IIC-IEM Website – Announcements App
Site-wide announcements with publish control.
"""
from django.apps import AppConfig


class AnnouncementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.announcements'
    verbose_name = 'Announcements'
