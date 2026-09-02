import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.council.models import CouncilYear

def seed():
    years_data = [
        {'year_label': '2025-2026', 'is_current': True, 'description': 'Academic Session 2025-2026'},
        {'year_label': '2024-2025', 'is_current': False, 'description': 'Academic Session 2024-2025'},
        {'year_label': '2023-2024', 'is_current': False, 'description': 'Academic Session 2023-2024'},
    ]
    for data in years_data:
        obj, created = CouncilYear.objects.get_or_create(
            year_label=data['year_label'],
            defaults={'is_current': data['is_current'], 'description': data['description']}
        )
        if created:
            print(f"Created CouncilYear: {obj.year_label}")
        else:
            print(f"CouncilYear exists: {obj.year_label}")

if __name__ == '__main__':
    seed()
