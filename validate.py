"""
Quick validation script — run this to check if the project structure is correct.
Usage: python validate.py
"""
import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

errors = []

print("=== IIC-IEM Project Validation ===\n")

# 1. Check Python version
print(f"Python: {sys.version.split()[0]}")

# 2. Check Django
try:
    import django
    print(f"Django: {django.__version__}")
except ImportError as e:
    errors.append(f"Django not installed: {e}")

# 3. Check key packages
packages = {
    'decouple': 'python-decouple',
    'psycopg2': 'psycopg2-binary',
    'PIL': 'Pillow',
    'whitenoise': 'whitenoise',
    'django_htmx': 'django-htmx',
    'pandas': 'pandas',
    'openpyxl': 'openpyxl',
    'django_ckeditor_5': 'django-ckeditor-5',
}
for module, package in packages.items():
    try:
        __import__(module)
        print(f"  [OK] {package}")
    except ImportError:
        errors.append(f"Missing package: {package}")
        print(f"  [MISSING] {package}")

# 4. Try Django setup
print("\n--- Django Setup ---")
try:
    django.setup()
    print("  [OK] Django configured")
except Exception as e:
    errors.append(f"Django setup failed: {e}")
    print(f"  [ERROR] Django setup: {e}")

# 5. Check apps can be imported
print("\n--- App Imports ---")
apps = ['apps.users', 'apps.core', 'apps.events', 'apps.certificates',
        'apps.council', 'apps.achievements', 'apps.gallery', 'apps.announcements']
for app in apps:
    try:
        __import__(f"{app}.models")
        print(f"  [OK] {app}")
    except Exception as e:
        errors.append(f"App error {app}: {e}")
        print(f"  [ERROR] {app}: {e}")

print("\n--- Summary ---")
if errors:
    print(f"  {len(errors)} error(s) found:")
    for err in errors:
        print(f"    - {err}")
    sys.exit(1)
else:
    print("  All checks passed!")
    print("\nNext step: Set up PostgreSQL and run:")
    print("  python manage.py migrate")
    print("  python manage.py createsuperuser")
    print("  python manage.py runserver")
