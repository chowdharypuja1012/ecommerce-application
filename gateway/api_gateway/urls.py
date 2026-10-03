"""
API Gateway — URL routing.

All client-facing routes are under /api/v1/.
Internal service endpoints are NOT publicly exposed.

Proxy routes forward to upstream services; authentication and
service-specific routing happens inside each service.
"""
from django.urls import path, re_path
from .health import gateway_health
from .proxy import proxy_view

urlpatterns = [
    # ── Gateway health (shallow: just gateway; deep: ?deep=1 pings all services)
    path("api/v1/health/", gateway_health, name="gateway-health"),

    # ── Accounts service  (auth, registration, profile, addresses)
    re_path(r"^api/v1/auth/(?P<rest>.*)$",     proxy_view("ACCOUNTS_SERVICE_URL"),  name="proxy-auth"),
    re_path(r"^api/v1/profile/(?P<rest>.*)$",  proxy_view("ACCOUNTS_SERVICE_URL"),  name="proxy-profile"),

    # ── Catalogue service  (products, categories)
    re_path(r"^api/v1/catalogue/(?P<rest>.*)$", proxy_view("CATALOGUE_SERVICE_URL"), name="proxy-catalogue"),

    # ── Cart service
    re_path(r"^api/v1/cart/(?P<rest>.*)$",      proxy_view("CART_SERVICE_URL"),      name="proxy-cart"),

    # ── Wishlist service
    re_path(r"^api/v1/wishlist/(?P<rest>.*)$",  proxy_view("WISHLIST_SERVICE_URL"),  name="proxy-wishlist"),

    # ── Orders service  (checkout + order history)
    re_path(r"^api/v1/orders/(?P<rest>.*)$",    proxy_view("ORDERS_SERVICE_URL"),    name="proxy-orders"),
    re_path(r"^api/v1/checkout/(?P<rest>.*)$",  proxy_view("ORDERS_SERVICE_URL"),    name="proxy-checkout"),

    # ── Payments service
    re_path(r"^api/v1/payments/(?P<rest>.*)$",  proxy_view("PAYMENTS_SERVICE_URL"),  name="proxy-payments"),

    # ── Reviews service
    re_path(r"^api/v1/reviews/(?P<rest>.*)$",   proxy_view("REVIEWS_SERVICE_URL"),   name="proxy-reviews"),
]
