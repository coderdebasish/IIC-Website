"""
IIC-IEM Website – Council URLs
"""
from django.urls import path
from . import views

app_name = 'council'

urlpatterns = [
    # ── Public ──────────────────────────────────────────────────────────────
    path('', views.council_current, name='current'),
    path('<str:year_label>/', views.council_by_year, name='by_year'),

    # ── Admin Panel ──────────────────────────────────────────────────────────
    path('admin-panel/council/', views.admin_council_list, name='admin_list'),
    path('admin-panel/council/years/add/', views.admin_year_add, name='admin_year_add'),
    path('admin-panel/council/years/<int:pk>/edit/', views.admin_year_edit, name='admin_year_edit'),
    path('admin-panel/council/members/add/', views.admin_member_add, name='admin_member_add'),
    path('admin-panel/council/members/<int:pk>/edit/', views.admin_member_edit, name='admin_member_edit'),
    path('admin-panel/council/members/<int:pk>/delete/', views.admin_member_delete, name='admin_member_delete'),
]
