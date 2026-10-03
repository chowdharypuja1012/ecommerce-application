"""
Gateway health view — checks gateway itself and all upstream services.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status as http_status

logger = logging.getLogger(__name__)

SERVICE_VERSION = "1.0.0"

UPSTREAM_SERVICES = {
    "accounts":  "ACCOUNTS_SERVICE_URL",
    "catalogue": "CATALOGUE_SERVICE_URL",
    "cart":      "CART_SERVICE_URL",
    "wishlist":  "WISHLIST_SERVICE_URL",
    "orders":    "ORDERS_SERVICE_URL",
    "payments":  "PAYMENTS_SERVICE_URL",
    "reviews":   "REVIEWS_SERVICE_URL",
}


def _ping_service(name: str, base_url: str) -> str:
    """Ping a service's health endpoint. Returns 'ok' or 'error: <reason>'."""
    try:
        resp = requests.get(
            f"{base_url.rstrip('/')}/api/v1/health/",
            timeout=2,
        )
        if resp.status_code == 200:
            return "ok"
        return f"error: HTTP {resp.status_code}"
    except Exception as exc:
        return f"error: {exc}"


@api_view(["GET"])
@permission_classes([AllowAny])
def gateway_health(request):
    """
    GET /api/v1/health/
    Returns gateway status. Set ?deep=1 to also ping all upstream services.
    """
    deep = request.query_params.get("deep") == "1"
    checks: dict[str, str] = {}
    overall_ok = True

    if deep:
        for name, setting_key in UPSTREAM_SERVICES.items():
            base_url = getattr(settings, setting_key, "")
            if not base_url:
                checks[name] = "error: not configured"
                overall_ok = False
            else:
                result = _ping_service(name, base_url)
                checks[name] = result
                if result != "ok":
                    overall_ok = False

    payload = {
        "service":   "gateway",
        "status":    "ok" if overall_ok else "degraded",
        "version":   SERVICE_VERSION,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks":    checks,
    }
    http_code = (
        http_status.HTTP_200_OK
        if overall_ok
        else http_status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return Response(payload, status=http_code)
