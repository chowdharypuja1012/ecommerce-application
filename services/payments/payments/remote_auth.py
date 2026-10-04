import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

logger = logging.getLogger(__name__)
User = get_user_model()


class RemoteTokenAuthentication(BaseAuthentication):
    """
    Microservice token authentication backend for Payments service.
    Validates token against the Accounts Service via HTTP and syncs the local User model.
    """
    keyword = "Token"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        if auth[0].lower() not in (b"token", b"bearer"):
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Invalid token header. No credentials provided.")
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed("Invalid token header. Token string should not contain spaces.")

        try:
            token_key = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed("Invalid token header. Token string should not contain invalid characters.")

        return self.authenticate_credentials(token_key)

    def authenticate_credentials(self, key: str):
        try:
            from rest_framework.authtoken.models import Token
            token_obj = Token.objects.select_related("user").filter(key=key).first()
            if token_obj and token_obj.user and token_obj.user.is_active:
                return (token_obj.user, token_obj)
        except Exception:
            pass

        accounts_url = getattr(settings, "ACCOUNTS_SERVICE_URL", "http://127.0.0.1:8001")
        url = f"{accounts_url.rstrip('/')}/api/v1/auth/me/"

        try:
            resp = requests.get(url, headers={"Authorization": f"Token {key}"}, timeout=4)
            if resp.status_code in (401, 403):
                raise exceptions.AuthenticationFailed("Invalid or expired token.")
            if not resp.ok:
                logger.error("Accounts service returned HTTP %s during auth check: %s", resp.status_code, resp.text)
                raise exceptions.AuthenticationFailed("Authentication service temporarily unavailable.")

            data = resp.json()
            user_data = data.get("user")
            if not user_data or "id" not in user_data:
                raise exceptions.AuthenticationFailed("Invalid user profile returned from authentication service.")

            user, _ = User.objects.get_or_create(
                id=user_data["id"],
                defaults={
                    "username": user_data.get("username", f"user_{user_data['id']}"),
                    "email": user_data.get("email", ""),
                    "is_active": True,
                }
            )
            if user.username != user_data.get("username", user.username):
                user.username = user_data.get("username", user.username)
                user.save(update_fields=["username"])

            return (user, key)
        except requests.RequestException as exc:
            logger.error("Failed to connect to Accounts service for token validation: %s", exc)
            raise exceptions.AuthenticationFailed("Authentication service is temporarily unreachable.")

    def authenticate_header(self, request):
        return self.keyword
