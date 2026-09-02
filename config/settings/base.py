"""
IIC-IEM Website – Base Settings
Shared configuration across all environments.
"""
import os
from pathlib import Path
from decouple import config, Csv

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root

# ─── Security ─────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ─── Application Definition ───────────────────────────────────────────────────
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'django_htmx',
    'django_ckeditor_5',
]

LOCAL_APPS = [
    'apps.users',
    'apps.core',
    'apps.events',
    'apps.certificates',
    'apps.council',
    'apps.achievements',
    'apps.gallery',
    'apps.announcements',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ─── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

# ─── URL Configuration ────────────────────────────────────────────────────────
ROOT_URLCONF = 'config.urls'

# ─── Templates ────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom context processor for site-wide settings
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

# ─── WSGI ─────────────────────────────────────────────────────────────────────
WSGI_APPLICATION = 'config.wsgi.application'

# ─── Database ─────────────────────────────────────────────────────────────────
import dj_database_url

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        cast=dj_database_url.parse
    )
}

# ─── Custom User Model ────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'users.CustomUser'

# ─── Password Validation ──────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Authentication ───────────────────────────────────────────────────────────
LOGIN_URL = '/admin-panel/login/'
LOGIN_REDIRECT_URL = '/admin-panel/'
LOGOUT_REDIRECT_URL = '/admin-panel/login/'

# ─── Internationalization ─────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ─── Static Files ─────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / config('STATIC_ROOT', default='staticfiles')

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# ─── Media Files ──────────────────────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / config('MEDIA_ROOT', default='media')

# ─── Default Primary Key ──────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── CKEditor 5 Configuration ─────────────────────────────────────────────────
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': [
                'heading', '|',
                'bold', 'italic', 'underline', 'strikethrough', '|',
                'link', '|',
                'bulletedList', 'numberedList', 'todoList', '|',
                'blockQuote', 'codeBlock', '|',
                'insertTable', '|',
                'imageUpload', 'mediaEmbed', '|',
                'outdent', 'indent', '|',
                'horizontalLine', 'pageBreak', '|',
                'undo', 'redo',
            ],
            'shouldNotGroupWhenFull': True,
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', 'imageTitle', '|',
                'imageStyle:inline', 'imageStyle:block', 'imageStyle:side', '|',
                'toggleImageCaption', 'linkImage',
            ],
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties'],
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'},
                {'model': 'heading4', 'view': 'h4', 'title': 'Heading 4', 'class': 'ck-heading_heading4'},
            ],
        },
        'height': 400,
        'width': '100%',
    },
    'minimal': {
        'toolbar': {
            'items': ['bold', 'italic', 'link', 'bulletedList', 'numberedList'],
        },
        'height': 200,
        'width': '100%',
    },
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = 'staff'
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'webp', 'pdf']
CKEDITOR_5_MAX_FILE_SIZE = 5  # MB

# ─── File Upload Security ─────────────────────────────────────────────────────
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
ALLOWED_DOCUMENT_TYPES = ['application/pdf']
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

# ─── Session Security ─────────────────────────────────────────────────────────
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 28800  # 8 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
