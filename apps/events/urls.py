"""
IIC-IEM Website – Events URLs
"""
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # ── Public ──────────────────────────────────────────────────────────────
    path('', views.event_list, name='list'),
    path('<slug:slug>/', views.event_detail, name='detail'),

    # ── Admin Panel ──────────────────────────────────────────────────────────
    path('admin-panel/events/', views.admin_event_list, name='admin_list'),
    path('admin-panel/events/create/', views.admin_event_create, name='admin_create'),
    path('admin-panel/events/<int:pk>/', views.admin_event_detail, name='admin_detail'),
    path('admin-panel/events/<int:pk>/edit/', views.admin_event_edit, name='admin_edit'),
    path('admin-panel/events/<int:pk>/content/', views.admin_event_content, name='admin_content'),
    path('admin-panel/events/<int:pk>/stages/', views.admin_event_stages, name='admin_stages'),
    path('admin-panel/events/<int:pk>/stages/add/', views.admin_stage_add, name='admin_stage_add'),
    path('admin-panel/events/<int:pk>/stages/<int:stage_pk>/edit/', views.admin_stage_edit, name='admin_stage_edit'),
    path('admin-panel/events/<int:pk>/stages/<int:stage_pk>/delete/', views.admin_stage_delete, name='admin_stage_delete'),
    path('admin-panel/events/<int:pk>/stages/<int:stage_pk>/set-current/', views.admin_stage_set_current, name='admin_stage_set_current'),
    path('admin-panel/events/<int:pk>/report/', views.admin_event_report, name='admin_report'),
    path('admin-panel/events/<int:pk>/gallery/', views.admin_event_gallery, name='admin_gallery'),
    path('admin-panel/events/<int:pk>/gallery/upload/', views.admin_gallery_upload, name='admin_gallery_upload'),
    path('admin-panel/events/<int:pk>/gallery/<int:img_pk>/delete/', views.admin_gallery_image_delete, name='admin_gallery_image_delete'),
    path('admin-panel/events/<int:pk>/delete/', views.admin_event_delete, name='admin_delete'),
]
