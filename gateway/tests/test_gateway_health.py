"""
tests/test_gateway_health.py — API tests for the gateway health endpoint.

Verifies:
- GET /api/v1/health/ returns 200 with correct shape
- CORS headers are present for allowed origins
- No broad CORS (CORS_ALLOW_ALL_ORIGINS is False)
- Shallow health check returns empty checks dict
- POST returns 405
"""
from django.test import TestCase, override_settings, RequestFactory
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status


class GatewayHealthTests(TestCase):
    # Gateway has no database — disable test DB creation
    databases = set()

    def setUp(self):
        self.client = APIClient()

    def test_gateway_health_200(self):
        """Gateway health returns HTTP 200."""
        response = self.client.get("/api/v1/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_gateway_health_body_shape(self):
        """Response has service=gateway, status, version, timestamp, checks."""
        response = self.client.get("/api/v1/health/")
        data = response.json()
        self.assertEqual(data["service"], "gateway")
        self.assertIn(data["status"], ["ok", "degraded"])
        self.assertIn("version", data)
        self.assertIn("timestamp", data)
        self.assertIn("checks", data)

    def test_gateway_health_no_auth_required(self):
        """Health endpoint is public."""
        response = APIClient().get("/api/v1/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_gateway_health_shallow_checks_empty(self):
        """Shallow health (no ?deep=1) returns empty checks dict."""
        response = self.client.get("/api/v1/health/")
        data = response.json()
        self.assertEqual(data["checks"], {})

    def test_cors_not_allow_all_origins(self):
        """CORS_ALLOW_ALL_ORIGINS is never True."""
        from django.conf import settings
        self.assertFalse(getattr(settings, "CORS_ALLOW_ALL_ORIGINS", False))

    def test_cors_header_present_for_allowed_origin(self):
        """CORS Access-Control-Allow-Origin returned for an allowed origin."""
        with override_settings(CORS_ALLOWED_ORIGINS=["http://localhost:5173"]):
            response = self.client.get(
                "/api/v1/health/",
                HTTP_ORIGIN="http://localhost:5173",
            )
        self.assertIn("Access-Control-Allow-Origin", response)
        self.assertEqual(
            response["Access-Control-Allow-Origin"],
            "http://localhost:5173",
        )

    def test_cors_header_absent_for_disallowed_origin(self):
        """CORS Access-Control-Allow-Origin NOT returned for unknown origin."""
        with override_settings(CORS_ALLOWED_ORIGINS=["http://localhost:5173"]):
            response = self.client.get(
                "/api/v1/health/",
                HTTP_ORIGIN="http://evil.example.com",
            )
        self.assertNotIn("Access-Control-Allow-Origin", response)

    def test_gateway_health_only_accepts_get(self):
        """POST to gateway health returns 405."""
        response = self.client.post("/api/v1/health/", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_timestamp_ends_with_z(self):
        """Timestamp is UTC and ends with Z."""
        response = self.client.get("/api/v1/health/")
        data = response.json()
        self.assertTrue(data["timestamp"].endswith("Z"))
