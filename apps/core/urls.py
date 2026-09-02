"""
IIC-IEM Website – Core URLs (Public: homepage, about, contact)
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # Admin settings management
    path('admin-panel/settings/', views.admin_settings, name='admin_settings'),
    path('admin-panel/settings/about/', views.admin_settings_about, name='admin_settings_about'),
]
