"""
tests/test_health.py — API tests for the health endpoint.

Verifies:
- GET /api/v1/health/ returns HTTP 200
- Response body has required fields: service, status, version, timestamp, checks
- Status is 'ok' when DB is reachable
- No authentication required (public endpoint)
- Response content-type is application/json
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch


class HealthEndpointTests(TestCase):
    """Tests for GET /api/v1/health/"""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("health")

    def test_health_returns_200(self):
        """Health endpoint returns HTTP 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_content_type_is_json(self):
        """Response content-type is application/json."""
        response = self.client.get(self.url)
        self.assertIn("application/json", response["Content-Type"])

    def test_health_body_has_required_fields(self):
        """Response body contains service, status, version, timestamp, checks."""
        response = self.client.get(self.url)
        data = response.json()
        self.assertIn("service", data)
        self.assertIn("status", data)
        self.assertIn("version", data)
        self.assertIn("timestamp", data)
        self.assertIn("checks", data)

    def test_health_status_is_ok_with_good_db(self):
        """Status is 'ok' when database is reachable."""
        response = self.client.get(self.url)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["checks"].get("database"), "ok")

    def test_health_no_auth_required(self):
        """Health endpoint is accessible without authentication."""
        unauthenticated = APIClient()  # no credentials
        response = unauthenticated.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_returns_503_when_db_fails(self):
        """Status is 'degraded' and HTTP 503 when database is unreachable."""
        with patch(
            "accounts.health._check_database",
            return_value="error: connection refused",
        ):
            response = self.client.get(self.url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(data["status"], "degraded")
        self.assertIn("error", data["checks"]["database"])

    def test_health_version_is_string(self):
        """Version field is a non-empty string."""
        response = self.client.get(self.url)
        data = response.json()
        self.assertIsInstance(data["version"], str)
        self.assertTrue(len(data["version"]) > 0)

    def test_health_timestamp_format(self):
        """Timestamp is in ISO-8601 UTC format (ends with Z)."""
        response = self.client.get(self.url)
        data = response.json()
        self.assertTrue(data["timestamp"].endswith("Z"), data["timestamp"])

    def test_health_only_accepts_get(self):
        """POST to health endpoint returns 405 Method Not Allowed."""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
