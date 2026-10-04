import logging
from decimal import Decimal
from typing import Any, Dict, Optional
import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def fetch_and_validate_product(product_id: int, requested_quantity: int) -> Dict[str, Any]:
    """
    Retrieves live product details from the Catalogue service.
    Validates:
    1. Product existence & active flag (is_active=True).
    2. Live unit price (prevents price tampering by ignoring client-sent prices).
    3. Stock availability (requested_quantity <= available_stock).

    Returns dict containing: id, sku, name, unit_price, stock.
    Raises rest_framework.exceptions.ValidationError on validation failure.
    """
    if requested_quantity < 1:
        raise ValidationError({"quantity": "Quantity must be a positive integer >= 1."})

    # Try direct database query if catalogue models are available locally in same environment
    try:
        from catalogue.models import Product as LocalProduct
        prod = LocalProduct.objects.filter(id=product_id, is_active=True).first()
        if prod:
            if requested_quantity > prod.stock:
                raise ValidationError({
                    "quantity": f"Requested quantity ({requested_quantity}) exceeds available stock ({prod.stock})."
                })
            return {
                "id": prod.id,
                "sku": prod.sku,
                "name": prod.name,
                "unit_price": prod.price,
                "stock": prod.stock,
            }
    except ImportError:
        pass

    # Fallback to HTTP request to Catalogue Service / Gateway
    catalogue_url = getattr(settings, "CATALOGUE_SERVICE_URL", "http://127.0.0.1:8002")
    url = f"{catalogue_url}/api/v1/products/{product_id}/"

    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 404:
            raise ValidationError({"product_id": "Product not found or currently inactive."})
        if not response.ok:
            raise ValidationError({"product_id": "Failed to verify product with Catalogue service."})

        data = response.json()
        if not data.get("is_active", True):
            raise ValidationError({"product_id": "This product is currently inactive and cannot be added to cart."})

        stock = int(data.get("stock", 0))
        if requested_quantity > stock:
            raise ValidationError({
                "quantity": f"Requested quantity ({requested_quantity}) exceeds available stock ({stock})."
            })

        return {
            "id": int(data["id"]),
            "sku": data["sku"],
            "name": data["name"],
            "unit_price": Decimal(str(data["price"])),
            "stock": stock,
        }
    except requests.RequestException as exc:
        logger.error("Error communicating with Catalogue service: %s", exc)
        # If catalogue HTTP is unreachable during test or service isolation, fallback to mock/local check
        raise ValidationError({"product_id": "Catalogue service is temporarily unavailable."})
