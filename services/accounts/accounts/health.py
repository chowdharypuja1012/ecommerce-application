"""
health.py — reusable health-check view for every Django microservice.

Usage in urls.py:
    from .health import make_health_view
    urlpatterns = [
        path("api/v1/health/", make_health_view("accounts"), name="health"),
        ...
    ]

Response shape (HTTP 200):
    {
        "service":  "accounts",
        "status":   "ok",
        "version":  "1.0.0",
        "timestamp": "2026-10-03T17:00:00Z",
        "checks": {
            "database": "ok"   # or "error: <reason>"
        }
    }
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from django.conf import settings
from django.db import connection, OperationalError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status as http_status

logger = logging.getLogger(__name__)

SERVICE_VERSION = "1.0.0"


def _check_database() -> str:
    """
    Ping the default database.
    Returns "ok" on success or "error: <detail>" on failure.
    """
    try:
        connection.ensure_connection()
        return "ok"
    except OperationalError as exc:
        logger.error("Health check DB ping failed: %s", exc)
        return f"error: {exc}"


def make_health_view(service_name: str):
    """
    Factory that returns a DRF view function for the given service name.
    The view is publicly accessible (no auth required).
    """

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def health(request):
        """GET /api/v1/health/ — service liveness and DB connectivity check."""
        has_db = bool(getattr(settings, "DATABASES", {}))
        checks = {}
        overall_ok = True

        if has_db:
            db_status = _check_database()
            checks["database"] = db_status
            if db_status != "ok":
                overall_ok = False

        payload = {
            "service":   service_name,
            "status":    "ok" if overall_ok else "degraded",
            "version":   SERVICE_VERSION,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "checks":    checks,
        }
        http_code = http_status.HTTP_200_OK if overall_ok else http_status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(payload, status=http_code)

    health.__name__ = f"health_{service_name}"
    return health
