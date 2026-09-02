"""
IIC-IEM Website – Development Settings
Extends base.py with development-specific configuration.
"""
from .base import *

# ─── Core ─────────────────────────────────────────────────────────────────────
DEBUG = True
SECRET_KEY = config('SECRET_KEY', default='dev-insecure-key-change-in-production-!!!!')

# ─── Development Database ─────────────────────────────────────────────────────
# Using SQLite by default for quick local development startup.
# Switch to PostgreSQL by commenting out this block and setting DB_* in .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL (uncomment when PostgreSQL is ready):
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', default='iic_iem_db'),
#         'USER': config('DB_USER', default='postgres'),
#         'PASSWORD': config('DB_PASSWORD', default=''),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }

# ─── Static & Media ───────────────────────────────────────────────────────────
# Override to use simpler static storage in development
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# ─── Email (console backend in dev) ───────────────────────────────────────────
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)

# ─── Debug Toolbar (optional) ─────────────────────────────────────────────────
try:
    import debug_toolbar  # noqa
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']
except ImportError:
    pass

# ─── CORS / Security relaxation for development ───────────────────────────────
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
