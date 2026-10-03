"""
tests/test_settings_validator.py

Tests that the settings validator raises ImproperlyConfigured with a clear
message when required environment variables are missing.

Run from any service directory:
    python manage.py test tests.test_settings_validator
"""
import os
import unittest
from unittest.mock import patch
from django.core.exceptions import ImproperlyConfigured


class SettingsValidatorTests(unittest.TestCase):

    def _import_validator(self):
        """Import validator fresh (avoids module-level caching)."""
        import importlib
        import accounts.settings_validator as sv
        importlib.reload(sv)
        return sv

    def test_passes_when_all_required_vars_present(self):
        """validate_settings() succeeds when all required vars are set."""
        sv = self._import_validator()
        env = {
            "DJANGO_SECRET_KEY": "test-secret",
            "DB_NAME": "shop_accounts_db",
            "DB_USER": "shop_dev",
            "DB_PASSWORD": "ShopDev2026!",
        }
        with patch.dict(os.environ, env, clear=False):
            # Should not raise
            sv.validate_settings("accounts", sv.BASE_REQUIRED_VARS)

    def test_raises_on_missing_secret_key(self):
        """validate_settings() raises ImproperlyConfigured when DJANGO_SECRET_KEY is absent."""
        sv = self._import_validator()
        env = {
            "DB_NAME": "shop_accounts_db",
            "DB_USER": "shop_dev",
            "DB_PASSWORD": "ShopDev2026!",
        }
        # Remove SECRET_KEY from environment for this test
        clean_env = {k: v for k, v in os.environ.items() if k != "DJANGO_SECRET_KEY"}
        with patch.dict(os.environ, clean_env, clear=True):
            with self.assertRaises(ImproperlyConfigured) as ctx:
                sv.validate_settings("accounts", sv.BASE_REQUIRED_VARS)
        self.assertIn("DJANGO_SECRET_KEY", str(ctx.exception))
        self.assertIn("accounts", str(ctx.exception))

    def test_raises_on_missing_db_vars(self):
        """validate_settings() lists ALL missing DB vars in one error."""
        sv = self._import_validator()
        env = {"DJANGO_SECRET_KEY": "test-secret"}
        clean_env = {k: v for k, v in os.environ.items()
                     if k not in ("DB_NAME", "DB_USER", "DB_PASSWORD")}
        clean_env["DJANGO_SECRET_KEY"] = "test-secret"
        with patch.dict(os.environ, clean_env, clear=True):
            with self.assertRaises(ImproperlyConfigured) as ctx:
                sv.validate_settings("accounts", sv.BASE_REQUIRED_VARS)
        msg = str(ctx.exception)
        self.assertIn("DB_NAME", msg)
        self.assertIn("DB_USER", msg)
        self.assertIn("DB_PASSWORD", msg)

    def test_error_message_mentions_env_example(self):
        """Error message references .env.example to guide the developer."""
        sv = self._import_validator()
        clean_env = {}
        with patch.dict(os.environ, clean_env, clear=True):
            with self.assertRaises(ImproperlyConfigured) as ctx:
                sv.validate_settings("accounts", sv.BASE_REQUIRED_VARS)
        self.assertIn(".env.example", str(ctx.exception))

    def test_gateway_only_needs_secret_key(self):
        """Gateway validator only requires DJANGO_SECRET_KEY (no DB vars)."""
        sv = self._import_validator()
        env = {"DJANGO_SECRET_KEY": "test-gateway-secret"}
        with patch.dict(os.environ, env, clear=True):
            # Should not raise for gateway
            sv.validate_settings("gateway", sv.GATEWAY_REQUIRED_VARS)


if __name__ == "__main__":
    unittest.main()
