"""
IIC-IEM Website – Council App
Council members and council years management.
"""
from django.apps import AppConfig


class CouncilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.council'
    verbose_name = 'Council Members'
