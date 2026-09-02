"""
IIC-IEM Website – Certificates URLs
"""
from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    # ── Public ──────────────────────────────────────────────────────────────
    path('', views.certificate_verify_page, name='verify'),
    path('verify/', views.certificate_verify_api, name='verify_api'),  # HTMX endpoint

    # ── Admin Panel ──────────────────────────────────────────────────────────
    path('admin-panel/certificates/', views.admin_certificate_list, name='admin_list'),
    path('admin-panel/certificates/add/', views.admin_certificate_add, name='admin_add'),
    path('admin-panel/certificates/<int:pk>/edit/', views.admin_certificate_edit, name='admin_edit'),
    path('admin-panel/certificates/<int:pk>/revoke/', views.admin_certificate_revoke, name='admin_revoke'),
    path('admin-panel/certificates/import/', views.admin_certificate_import, name='admin_import'),
    path('admin-panel/certificates/import/history/', views.admin_import_history, name='admin_import_history'),
]
