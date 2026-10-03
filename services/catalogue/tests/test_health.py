from django.test import TestCase, Client


class CatalogueHealthTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_endpoint_returns_200(self):
        response = self.client.get("/api/v1/health/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"], "catalogue")
