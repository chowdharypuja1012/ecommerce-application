"""
Generates settings.py and .env.example for all 7 Django microservices.
Run from shop-platform root: python scripts/gen_service_configs.py
"""
import os, pathlib, textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent

SERVICES = [
    {"name": "accounts",  "port": 8001, "db": "shop_accounts_db"},
    {"name": "catalogue", "port": 8002, "db": "shop_catalogue_db"},
    {"name": "cart",      "port": 8003, "db": "shop_cart_db"},
    {"name": "wishlist",  "port": 8004, "db": "shop_wishlist_db"},
    {"name": "orders",    "port": 8005, "db": "shop_orders_db"},
    {"name": "payments",  "port": 8006, "db": "shop_payments_db"},
    {"name": "reviews",   "port": 8007, "db": "shop_reviews_db"},
]

SETTINGS_TEMPLATE = '''\
"""
{name} service settings — reads all config from environment variables.
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
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "{name}",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "{name}.urls"

TEMPLATES = [
    {{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {{
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        }},
    }},
]

WSGI_APPLICATION = "{name}.wsgi.application"

DATABASES = {{
    "default": {{
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {{"connect_timeout": 5}},
    }}
}}

AUTH_PASSWORD_VALIDATORS = [
    {{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}},
    {{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}},
    {{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"}},
    {{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}},
]

REST_FRAMEWORK = {{
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}}

# CORS — internal service; only allow gateway
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS", "http://127.0.0.1:8000"
).split(",")

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
'''

ENV_TEMPLATE = '''\
# {name} service environment variables
# Copy this file to .env and fill in real values — never commit .env

DJANGO_SECRET_KEY=replace-with-a-long-random-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# PostgreSQL connection for this service only
DB_NAME={db}
DB_USER=shop_dev
DB_PASSWORD=replace-with-shop-dev-password
DB_HOST=127.0.0.1
DB_PORT=5432

# CORS — allow only the gateway
CORS_ALLOWED_ORIGINS=http://127.0.0.1:8000
'''

URLS_TEMPLATE = '''\
from django.contrib import admin
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(request):
    """Service health check — GET /api/v1/health/"""
    return Response({{"service": "{name}", "status": "ok"}})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", health, name="health"),
    # Feature routes added in later tasks
]
'''

REQUIREMENTS_TEMPLATE = '''\
-r ../../requirements-base.txt
'''

for svc in SERVICES:
    name = svc["name"]
    db   = svc["db"]
    svc_dir   = ROOT / "services" / name
    inner_dir = svc_dir / name      # Django inner package dir

    # settings.py
    (inner_dir / "settings.py").write_text(
        SETTINGS_TEMPLATE.format(name=name), encoding="utf-8"
    )
    print(f"  Written: services/{name}/{name}/settings.py")

    # urls.py
    (inner_dir / "urls.py").write_text(
        URLS_TEMPLATE.format(name=name), encoding="utf-8"
    )
    print(f"  Written: services/{name}/{name}/urls.py")

    # .env.example
    (svc_dir / ".env.example").write_text(
        ENV_TEMPLATE.format(name=name, db=db), encoding="utf-8"
    )
    print(f"  Written: services/{name}/.env.example")

    # requirements.txt
    (svc_dir / "requirements.txt").write_text(
        REQUIREMENTS_TEMPLATE, encoding="utf-8"
    )
    print(f"  Written: services/{name}/requirements.txt")

print("\nAll service configs generated!")
