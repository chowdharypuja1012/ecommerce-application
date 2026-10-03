from django.contrib import admin
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(request):
    """Service health check — GET /api/v1/health/"""
    return Response({"service": "accounts", "status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", health, name="health"),
    # Feature routes added in later tasks
]
