"""
Django settings for config project.
Production-friendly settings for Render, with local development fallback.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key: set SECRET_KEY in Render Environment Variables.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-development-only-change-me"
)

# DEBUG should be False in production.
DEBUG = os.environ.get("DEBUG", "False").strip().lower() in ("1", "true", "yes")

# Render supplies RENDER_EXTERNAL_HOSTNAME for deployed web services.
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
allowed_hosts_env = os.environ.get("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
if allowed_hosts_env:
    ALLOWED_HOSTS.extend(
        host.strip() for host in allowed_hosts_env.split(",") if host.strip()
    )
# Allow Render subdomains if a specific hostname is not yet configured.
if not DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = [".onrender.com"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "users",
    "jobs",
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
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database:
# Set DATABASE_URL to a Render PostgreSQL connection URL in production.
# If DATABASE_URL is absent, SQLite is used (not recommended for shared production data).
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if DATABASE_URL:
    try:
        import dj_database_url
    except ImportError as exc:
        raise ImportError(
            "DATABASE_URL is set but dj-database-url is not installed. "
            "Add dj-database-url to requirements.txt."
        ) from exc

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
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
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Render serves the app over HTTPS in production.
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Preserve the project's existing email setting.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
