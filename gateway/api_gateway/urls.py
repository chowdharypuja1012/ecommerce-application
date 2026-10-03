from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(request):
    """Gateway health check — GET /api/v1/health/"""
    return Response({"service": "gateway", "status": "ok"})


urlpatterns = [
    path("api/v1/health/", health, name="gateway-health"),
    # Upstream proxy routes will be added in Task 3
]
