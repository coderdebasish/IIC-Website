"""
IIC-IEM Website – Core App
Site settings, homepage, about, contact pages.
"""
import os
import shutil
from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Core / Site Settings'

    def ready(self):
        """Auto-sync logos and seed default Council Academic Years on app ready."""
        try:
            base_dir = settings.BASE_DIR
            logo_src = os.path.join(base_dir, 'Logo')
            if os.path.exists(logo_src):
                dest_dir = os.path.join(base_dir, 'static', 'images', 'logos')
                os.makedirs(dest_dir, exist_ok=True)
                for item in os.listdir(logo_src):
                    src_file = os.path.join(logo_src, item)
                    if os.path.isfile(src_file):
                        shutil.copy(src_file, os.path.join(dest_dir, item))

            # Auto-seed Council Years if missing
            from apps.council.models import CouncilYear
            if not CouncilYear.objects.exists():
                CouncilYear.objects.create(year_label='2025-2026', is_current=True, description='Academic Session 2025-2026')
                CouncilYear.objects.create(year_label='2024-2025', is_current=False, description='Academic Session 2024-2025')
                CouncilYear.objects.create(year_label='2023-2024', is_current=False, description='Academic Session 2023-2024')
        except Exception:
            pass
