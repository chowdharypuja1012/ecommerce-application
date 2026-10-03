"""
proxy.py — lightweight HTTP reverse proxy for the API Gateway.

Forwards incoming requests to the appropriate upstream service,
injecting/forwarding X-Correlation-ID for distributed tracing.

Usage in urls.py:
    from .proxy import proxy_view
    path("api/v1/auth/<path:rest>", proxy_view("ACCOUNTS_SERVICE_URL"), name="proxy-accounts"),
"""
from __future__ import annotations

import logging
import uuid
from typing import Any

import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status as http_status

logger = logging.getLogger(__name__)

# Headers that must NOT be forwarded upstream (hop-by-hop)
_HOP_BY_HOP = frozenset({
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade",
    "host",  # upstream host will differ
})

# Timeout for upstream calls (connect_timeout, read_timeout)
_UPSTREAM_TIMEOUT = (3, 10)


def _get_correlation_id(request: Request) -> str:
    """Return existing correlation ID from header or generate a new one."""
    return request.META.get("HTTP_X_CORRELATION_ID") or str(uuid.uuid4())


def _forward_headers(request: Request, correlation_id: str) -> dict[str, str]:
    """Build the header dict to send to the upstream service."""
    headers: dict[str, str] = {}
    for key, value in request.META.items():
        if key.startswith("HTTP_"):
            header_name = key[5:].replace("_", "-").lower()
            if header_name not in _HOP_BY_HOP:
                headers[header_name] = value
        elif key == "CONTENT_TYPE":
            headers["content-type"] = value
        elif key == "CONTENT_LENGTH" and value:
            headers["content-length"] = value
    headers["x-correlation-id"] = correlation_id
    return headers


def _upstream_error_response(service_key: str, error: Exception) -> Response:
    """Return a structured 503 when an upstream service is unreachable."""
    logger.error("Upstream %s unreachable: %s", service_key, error)
    return Response(
        {
            "error": "service_unavailable",
            "detail": f"The {service_key.lower().replace('_service_url', '')} service is temporarily unavailable.",
        },
        status=http_status.HTTP_503_SERVICE_UNAVAILABLE,
    )


def proxy_view(service_setting_key: str):
    """
    Factory returning a catch-all DRF view that proxies requests to an upstream service.

    Args:
        service_setting_key: settings attribute name, e.g. "ACCOUNTS_SERVICE_URL"

    The view matches any path suffix via the `rest` URL capture group:
        path("api/v1/auth/<path:rest>", proxy_view("ACCOUNTS_SERVICE_URL"))
    """

    @api_view(["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
    @permission_classes([AllowAny])
    def _proxy(request: Request, rest: str = "") -> Response:
        base_url: str = getattr(settings, service_setting_key, "")
        if not base_url:
            logger.error("Settings key %s is not configured.", service_setting_key)
            return Response(
                {"error": "misconfigured_gateway", "detail": "Gateway routing error."},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        correlation_id = _get_correlation_id(request)
        upstream_path = request.path  # preserve the full original path
        upstream_url = f"{base_url.rstrip('/')}/{upstream_path.lstrip('/')}"

        if request.META.get("QUERY_STRING"):
            upstream_url += f"?{request.META['QUERY_STRING']}"

        headers = _forward_headers(request, correlation_id)
        body: Any = request.body if request.method not in ("GET", "HEAD", "DELETE") else None

        logger.info(
            "[%s] GW → %s %s",
            correlation_id, request.method, upstream_url
        )

        try:
            upstream_response = requests.request(
                method=request.method,
                url=upstream_url,
                headers=headers,
                data=body,
                timeout=_UPSTREAM_TIMEOUT,
                allow_redirects=False,
            )
        except requests.exceptions.ConnectionError as exc:
            return _upstream_error_response(service_setting_key, exc)
        except requests.exceptions.Timeout as exc:
            logger.error("[%s] Upstream %s timed out: %s", correlation_id, service_setting_key, exc)
            return Response(
                {"error": "upstream_timeout", "detail": "The upstream service did not respond in time."},
                status=http_status.HTTP_504_GATEWAY_TIMEOUT,
            )

        # Strip hop-by-hop headers from the upstream response
        response_headers = {
            k: v for k, v in upstream_response.headers.items()
            if k.lower() not in _HOP_BY_HOP
        }
        response_headers["X-Correlation-ID"] = correlation_id

        try:
            data = upstream_response.json()
        except ValueError:
            data = upstream_response.text

        response = Response(data, status=upstream_response.status_code)
        for key, value in response_headers.items():
            response[key] = value
        return response

    _proxy.__name__ = f"proxy_{service_setting_key.lower()}"
    return _proxy
