from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class AuthenticationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/v1/auth/register/"
        self.login_url = "/api/v1/auth/login/"
        self.logout_url = "/api/v1/auth/logout/"
        self.me_url = "/api/v1/auth/me/"

    def test_user_registration_success(self):
        payload = {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "StrongPassword123!",
            "full_name": "John Doe",
            "phone_number": "+1234567890",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn("token", data)
        self.assertEqual(data["user"]["username"], "johndoe")
        self.assertEqual(data["profile"]["full_name"], "John Doe")

        # Verify DB user and token creation
        user = User.objects.get(username="johndoe")
        self.assertTrue(user.check_password("StrongPassword123!"))
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_user_registration_duplicate_username_fails(self):
        User.objects.create_user(username="existinguser", email="existing@example.com", password="Password123!")
        payload = {
            "username": "existinguser",
            "email": "new@example.com",
            "password": "Password123!",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_weak_password_fails(self):
        payload = {
            "username": "weakuser",
            "email": "weak@example.com",
            "password": "123",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        User.objects.create_user(username="testuser", email="test@example.com", password="MySecurePassword123!")
        payload = {"username": "testuser", "password": "MySecurePassword123!"}
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("token", data)
        self.assertEqual(data["user"]["username"], "testuser")

    def test_user_login_invalid_credentials_fails(self):
        User.objects.create_user(username="testuser", email="test@example.com", password="MySecurePassword123!")
        payload = {"username": "testuser", "password": "WrongPassword!"}
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_deletes_token(self):
        user = User.objects.create_user(username="logoutuser", email="logout@example.com", password="Password123!")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=user).exists())

    def test_me_endpoint_requires_auth(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_endpoint_authenticated_success(self):
        user = User.objects.create_user(username="meuser", email="me@example.com", password="Password123!")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["user"]["username"], "meuser")
