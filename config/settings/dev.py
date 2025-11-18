from __future__ import annotations

import secrets
from datetime import timedelta
from typing import Any

from .base import *  # noqa: F403,F401

if not isinstance(SECRET_KEY, str) or not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(64)  # type: ignore[misc]

DEBUG: bool = True
ALLOWED_HOSTS: list[str] = ['127.0.0.1', 'localhost']

EMAIL_BACKEND: str = "django.core.mail.backends.console.EmailBackend"

DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATICFILES_STORAGE: str = "django.contrib.staticfiles.storage.StaticFilesStorage"

LOGIN_REDIRECT_URL: str = 'manager-dashboard'
LOGOUT_REDIRECT_URL: str = 'home'

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework_simplejwt.authentication.JWTAuthentication',
)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(minutes=30)
