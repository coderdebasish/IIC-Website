"""
IIC-IEM Website – Users App URL Configuration
All admin panel URLs are nested under /admin-panel/
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # ── Authentication ──────────────────────────────────────────────────────
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),

    # ── Dashboard ───────────────────────────────────────────────────────────
    path('', views.dashboard, name='dashboard'),

    # ── Profile ─────────────────────────────────────────────────────────────
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),

    # ── Admin User Management (Super Admin only) ─────────────────────────────
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/toggle-active/', views.user_toggle_active, name='user_toggle_active'),
    path('users/activity-log/', views.activity_log, name='activity_log'),
]
