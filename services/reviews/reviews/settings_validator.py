"""
settings_validator.py — validates required environment variables at startup.

Import this at the bottom of every service's settings.py:
    from .settings_validator import validate_settings
    validate_settings(SERVICE_NAME, REQUIRED_VARS)

Raises django.core.exceptions.ImproperlyConfigured with a clear message
listing ALL missing variables — not just the first one.
"""
import os
from django.core.exceptions import ImproperlyConfigured


def validate_settings(service_name: str, required_vars: list[str]) -> None:
    """
    Check that all required env vars are set and non-empty.
    Raises ImproperlyConfigured if any are missing.
    """
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        missing_list = "\n  - ".join(missing)
        raise ImproperlyConfigured(
            f"\n\n[{service_name}] Missing required environment variables:\n"
            f"  - {missing_list}\n\n"
            f"Copy .env.example → .env in the service directory and fill in all values.\n"
            f"Never commit the .env file to source control.\n"
        )


# Required vars shared by every Django service that has a database
BASE_REQUIRED_VARS: list[str] = [
    "DJANGO_SECRET_KEY",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
]

# Required vars for the gateway (no database)
GATEWAY_REQUIRED_VARS: list[str] = [
    "DJANGO_SECRET_KEY",
]
