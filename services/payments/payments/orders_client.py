import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def notify_order_payment_status(order_id: int, status: str, auth_header: str = None) -> bool:
    """
    Notifies Orders Service of payment completion (updates order status to 'PAID' or 'CANCELLED').
    Uses local DB update fallback if Orders models are available locally in same environment runner.
    """
    # 1. Local DB Fallback (for monolithic test environment)
    try:
        from orders.models import Order as LocalOrder, OrderStatus
        order = LocalOrder.objects.filter(id=order_id).first()
        if order:
            if status == "SUCCESS":
                order.transition_to(OrderStatus.PAID)
            elif status == "CANCELLED":
                order.transition_to(OrderStatus.CANCELLED)
            return True
    except ImportError:
        pass

    # 2. HTTP Request to Orders Microservice
    orders_url = getattr(settings, "ORDERS_SERVICE_URL", "http://127.0.0.1:8004")
    url = f"{orders_url}/api/v1/orders/{order_id}/status/"

    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header

    target_status = "PAID" if status == "SUCCESS" else "CANCELLED" if status == "CANCELLED" else "PENDING"

    try:
        response = requests.patch(url, json={"status": target_status}, headers=headers, timeout=4)
        if not response.ok:
            logger.warning("Orders service responded with error on payment status sync: %s", response.text)
            return False
        return True
    except requests.RequestException as exc:
        logger.error("Failed to notify Orders service of payment: %s", exc)
        return False
