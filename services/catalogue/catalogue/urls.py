from django.contrib import admin
from django.urls import path
from .health import make_health_view
from .views import (
    CategoryDetailView,
    CategoryListView,
    ProductDetailView,
    ProductListView,
    AdminProductCreateView,
    AdminProductUpdateDeleteView,
    AdminLowStockAlertsView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("catalogue"), name="health"),

    # Public Category endpoints
    path("api/v1/categories/", CategoryListView.as_view(), name="category-list"),
    path("api/v1/categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"),

    # Public Product endpoints
    path("api/v1/products/", ProductListView.as_view(), name="product-list"),
    path("api/v1/products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),

    # Catalogue-prefixed routes for gateway proxies
    path("api/v1/catalogue/categories/", CategoryListView.as_view(), name="catalogue-category-list"),
    path("api/v1/catalogue/categories/<slug:slug>/", CategoryDetailView.as_view(), name="catalogue-category-detail"),
    path("api/v1/catalogue/products/", ProductListView.as_view(), name="catalogue-product-list"),
    path("api/v1/catalogue/products/<slug:slug>/", ProductDetailView.as_view(), name="catalogue-product-detail"),

    # Admin Protected Routes
    path("api/v1/catalogue/admin/products/", AdminProductCreateView.as_view(), name="catalogue-admin-product-create"),
    path("api/v1/catalogue/admin/products/<int:pk>/", AdminProductUpdateDeleteView.as_view(), name="catalogue-admin-product-update-delete"),
    path("api/v1/catalogue/admin/inventory/low-stock/", AdminLowStockAlertsView.as_view(), name="catalogue-admin-low-stock"),
]
