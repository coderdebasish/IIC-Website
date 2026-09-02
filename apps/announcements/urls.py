"""IIC-IEM – Announcements URLs"""
from django.urls import path
from . import views
app_name = 'announcements'
urlpatterns = [
    path('', views.announcement_list, name='list'),
    path('admin-panel/announcements/', views.admin_announcement_list, name='admin_list'),
    path('admin-panel/announcements/add/', views.admin_announcement_add, name='admin_add'),
    path('admin-panel/announcements/<int:pk>/edit/', views.admin_announcement_edit, name='admin_edit'),
    path('admin-panel/announcements/<int:pk>/toggle/', views.admin_announcement_toggle, name='admin_toggle'),
    path('admin-panel/announcements/<int:pk>/delete/', views.admin_announcement_delete, name='admin_delete'),
]
