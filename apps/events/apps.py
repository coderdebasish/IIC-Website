"""
IIC-IEM Website – Events App
Event system, lifecycle, rich content, reports, galleries.
"""
from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.events'
    verbose_name = 'Events'
