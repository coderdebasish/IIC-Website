"""
IIC-IEM Website – Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ── Public Website ───────────────────────────────────────────────────────
    path('', include('apps.core.urls', namespace='core')),
    path('events/', include('apps.events.urls', namespace='events')),
    path('council/', include('apps.council.urls', namespace='council')),
    path('achievements/', include('apps.achievements.urls', namespace='achievements')),
    path('gallery/', include('apps.gallery.urls', namespace='gallery')),
    path('certificates/', include('apps.certificates.urls', namespace='certificates')),
    path('announcements/', include('apps.announcements.urls', namespace='announcements')),

    # ── Admin Panel (Custom) ─────────────────────────────────────────────────
    path('admin-panel/', include('apps.users.urls', namespace='users')),

    # ── CKEditor 5 (file uploads) ────────────────────────────────────────────
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # ── Django Admin (superuser emergency access) ─────────────────────────────
    path('django-admin/', admin.site.urls),
]

# ── Serve Media Files in Development ────────────────────────────────────────
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
