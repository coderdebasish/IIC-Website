"""
IIC-IEM Website – Gallery App
General photo albums and images.
"""
from django.apps import AppConfig


class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gallery'
    verbose_name = 'Gallery'
