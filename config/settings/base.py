from __future__ import annotations

import logging
import secrets
from datetime import timedelta
from pathlib import Path
from typing import Any, Final

import environ
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent
PRIMARY_ENV_FILE: Final[Path] = BASE_DIR / '.env'
SECONDARY_ENV_FILE: Final[Path] = BASE_DIR.parent / '.env'

load_dotenv(PRIMARY_ENV_FILE)

env = environ.Env()
for env_file in (PRIMARY_ENV_FILE, SECONDARY_ENV_FILE):
    if env_file.exists():
        env.read_env(env_file=str(env_file))

logging.captureWarnings(True)
logger = logging.getLogger(__name__)


def _load_secret_key() -> str:
    try:
        secret_key = env(
            'DJANGO_SECRET_KEY',
            default=secrets.token_urlsafe(64)
        )

    except Exception as e:
        logger.exception(
            'Unable to load DJANGO_SECRET_KEY from environment.',
            exc_info=e,
        )
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY could not be loaded from the environment.'
        ) from e

    if isinstance(secret_key, bytes):
        secret_key = secret_key.decode('utf-8', errors='ignore').strip()

    if not isinstance(secret_key, str):
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY must be a string value.'
        )

    secret_key = secret_key.strip()
    if not secret_key:
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY cannot be empty.'
        )

    return secret_key


SECRET_KEY: str = _load_secret_key()
DEBUG: bool = env.bool('DJANGO_DEBUG', default=False)

if not DEBUG and SECRET_KEY == 'unsafe-development-key':
    raise ImproperlyConfigured(
        'DJANGO_SECRET_KEY must be set when DEBUG is False.'
    )

ALLOWED_HOSTS: list[str] = env.list(
    'DJANGO_ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

ADMIN_SITE_TITLE: str = env(
    'ADMIN_SITE_TITLE', default='Job Board Admin Panel')
ADMIN_INDEX_TITLE: str = env(
    'ADMIN_INDEX_TITLE', default='Jhapson Administration')

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    'whitenoise.runserver_nostatic',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    # app
    'job_board',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE: str = 'en-us'
TIME_ZONE: str = 'UTC'
USE_I18N: bool = True
USE_TZ: bool = True

STATIC_URL: str = "/static/"

STATICFILES_DIRS: list[Path] = []
_static_dir = BASE_DIR / "static"
if _static_dir.exists():
    STATICFILES_DIRS.append(_static_dir)

STATIC_ROOT: Path = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL: str = env("AUTH_USER_MODEL", default="auth.User")

DEFAULT_FROM_EMAIL: str = env(
    "DEFAULT_FROM_EMAIL", default="noreply@example.com")
EMAIL_SUBJECT_PREFIX: str = env("EMAIL_SUBJECT_PREFIX", default="[Job Board] ")

REST_FRAMEWORK: dict[str, Any] = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 20,

    'EXCEPTION_HANDLER': 'job_board.exceptions.custom_exception_handler',

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'applications': '10/day',
    },

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

SIMPLE_JWT: dict[str, Any] = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

LOGGING: dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },

    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
