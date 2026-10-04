from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from accounts.models import Address, Profile

User = get_user_model()


class ProfileAndAddressOwnershipTest(TestCase):
    def setUp(self):
        self.client_a = APIClient()
        self.user_a = User.objects.create_user(
            username="usera", email="usera@example.com", password="Password123!"
        )
        self.token_a = Token.objects.create(user=self.user_a)
        self.client_a.credentials(HTTP_AUTHORIZATION=f"Token {self.token_a.key}")

        self.client_b = APIClient()
        self.user_b = User.objects.create_user(
            username="userb", email="userb@example.com", password="Password123!"
        )
        self.token_b = Token.objects.create(user=self.user_b)
        self.client_b.credentials(HTTP_AUTHORIZATION=f"Token {self.token_b.key}")

        # Create Address owned by User A
        self.address_a = Address.objects.create(
            user=self.user_a,
            title="User A Home",
            street_address="123 Main St",
            city="New York",
            postal_code="10001",
            country="USA",
            is_default=True,
        )

    def test_profile_retrieval_and_update(self):
        response = self.client_a.get("/api/v1/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["user"]["username"], "usera")

        # Update profile
        update_payload = {"full_name": "Alice Smith", "phone_number": "+1999888777"}
        patch_response = self.client_a.patch("/api/v1/profile/", update_payload, format="json")
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()["full_name"], "Alice Smith")

    def test_address_create_and_default_toggle(self):
        payload = {
            "title": "Work",
            "street_address": "456 Office Blvd",
            "city": "New York",
            "postal_code": "10002",
            "country": "USA",
            "is_default": True,
        }
        response = self.client_a.post("/api/v1/profile/addresses/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_address_id = response.json()["id"]

        # Verify new address is default and old address is no longer default
        self.address_a.refresh_from_db()
        self.assertFalse(self.address_a.is_default)
        new_address = Address.objects.get(id=new_address_id)
        self.assertTrue(new_address.is_default)

    def test_strict_address_ownership_user_b_cannot_access_user_a_address(self):
        # User B tries to GET User A's address detail
        url = f"/api/v1/profile/addresses/{self.address_a.id}/"
        response_get = self.client_b.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        # User B tries to PUT User A's address detail
        response_put = self.client_b.put(url, {"street_address": "Hacked St"}, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

        # User B tries to DELETE User A's address detail
        response_delete = self.client_b.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

        # Verify User A's address remains unchanged
        self.address_a.refresh_from_db()
        self.assertEqual(self.address_a.street_address, "123 Main St")

    def test_unauthenticated_access_rejected(self):
        anon_client = APIClient()
        self.assertEqual(anon_client.get("/api/v1/profile/").status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(anon_client.get("/api/v1/profile/addresses/").status_code, status.HTTP_401_UNAUTHORIZED)
