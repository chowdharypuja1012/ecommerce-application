from django.contrib import admin
from django.urls import path
from .health import make_health_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("catalogue"), name="health"),
    # Feature routes added in later tasks
]
