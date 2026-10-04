"""
Gateway settings — reads all config from environment variables.
Copy .env.example → .env and fill in values before running.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "api_gateway",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Security Headers & Production SSL Configurations
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False") == "True"
SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False") == "True"
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "False") == "True"


ROOT_URLCONF = "api_gateway.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]

WSGI_APPLICATION = "api_gateway.wsgi.application"

# Gateway has no own database — it only proxies to services
DATABASES = {}

# CORS — narrow allowlist; never use CORS_ALLOW_ALL_ORIGINS=True in any environment
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS", "http://localhost:5173"
).split(",")
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "x-correlation-id",
    "x-csrftoken",
]
# Expose correlation ID to clients so they can reference it in bug reports
CORS_EXPOSE_HEADERS = ["X-Correlation-ID"]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "200/min",
        "user": "1000/min",
        "auth": "20/min",
    },
}

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"

# ── Upstream service URLs (used by proxy views) ──────────────────────────────
ACCOUNTS_SERVICE_URL  = os.environ.get("ACCOUNTS_SERVICE_URL",  "http://127.0.0.1:8001")
CATALOGUE_SERVICE_URL = os.environ.get("CATALOGUE_SERVICE_URL", "http://127.0.0.1:8002")
CART_SERVICE_URL      = os.environ.get("CART_SERVICE_URL",      "http://127.0.0.1:8003")
WISHLIST_SERVICE_URL  = os.environ.get("WISHLIST_SERVICE_URL",  "http://127.0.0.1:8004")
ORDERS_SERVICE_URL    = os.environ.get("ORDERS_SERVICE_URL",    "http://127.0.0.1:8005")
PAYMENTS_SERVICE_URL  = os.environ.get("PAYMENTS_SERVICE_URL",  "http://127.0.0.1:8006")
REVIEWS_SERVICE_URL   = os.environ.get("REVIEWS_SERVICE_URL",   "http://127.0.0.1:8007")

# -- Startup validation -- fails clearly if required env vars are missing ------
from .settings_validator import validate_settings, GATEWAY_REQUIRED_VARS
validate_settings('gateway', GATEWAY_REQUIRED_VARS)

