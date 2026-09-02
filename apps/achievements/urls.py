"""IIC-IEM – Achievements URLs"""
from django.urls import path
from . import views
app_name = 'achievements'
urlpatterns = [
    path('', views.achievement_list, name='list'),
    path('admin-panel/achievements/', views.admin_achievement_list, name='admin_list'),
    path('admin-panel/achievements/add/', views.admin_achievement_add, name='admin_add'),
    path('admin-panel/achievements/<int:pk>/edit/', views.admin_achievement_edit, name='admin_edit'),
    path('admin-panel/achievements/<int:pk>/delete/', views.admin_achievement_delete, name='admin_delete'),
]
