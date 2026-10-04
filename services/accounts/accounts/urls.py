from django.contrib import admin
from django.urls import path
from .health import make_health_view
from .views import (
    AddressDetailView,
    AddressListCreateView,
    CurrentUserView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("accounts"), name="health"),

    # Auth routes
    path("api/v1/auth/register/", RegisterView.as_view(), name="auth-register"),
    path("api/v1/auth/login/", LoginView.as_view(), name="auth-login"),
    path("api/v1/auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("api/v1/auth/me/", CurrentUserView.as_view(), name="auth-me"),

    # Profile & Address routes
    path("api/v1/profile/", ProfileView.as_view(), name="profile-detail"),
    path("api/v1/profile/addresses/", AddressListCreateView.as_view(), name="address-list-create"),
    path("api/v1/profile/addresses/<int:pk>/", AddressDetailView.as_view(), name="address-detail"),
]
