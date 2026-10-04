from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import Address

class SecurityAndIsolationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="secuser1", password="SecurePassword123!")
        self.user2 = User.objects.create_user(username="secuser2", password="SecurePassword123!")

        self.address1 = Address.objects.create(
            user=self.user1,
            title="Home",
            street_address="123 Security St",
            city="Cyber City",
            postal_code="10001",
            country="USA"
        )
        self.address2 = Address.objects.create(
            user=self.user2,
            title="Office",
            street_address="456 Isolation Ave",
            city="Cyber City",
            postal_code="10002",
            country="USA"
        )

    def test_user_cannot_access_or_modify_other_user_address(self):
        """Verify strict authorization isolation between users."""
        self.client.force_authenticate(user=self.user1)

        # Attempting to retrieve user2's address should return 404 (or 403)
        response = self.client.get(f"/api/v1/profile/addresses/{self.address2.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Attempting to delete user2's address should be prevented
        response = self.client.delete(f"/api/v1/profile/addresses/{self.address2.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Confirm address2 still exists in database
        self.assertTrue(Address.objects.filter(id=self.address2.id).exists())

    def test_unauthenticated_request_rejected(self):
        """Verify unauthenticated requests to protected profile endpoints return 401."""
        response = self.client.get("/api/v1/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
