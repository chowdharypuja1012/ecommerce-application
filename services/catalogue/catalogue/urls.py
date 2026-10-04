from django.contrib import admin
from django.urls import path
from .health import make_health_view
from .views import (
    CategoryDetailView,
    CategoryListView,
    ProductDetailView,
    ProductListView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("catalogue"), name="health"),

    # Category endpoints
    path("api/v1/categories/", CategoryListView.as_view(), name="category-list"),
    path("api/v1/categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"),

    # Product endpoints
    path("api/v1/products/", ProductListView.as_view(), name="product-list"),
    path("api/v1/products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),

    # Catalogue-prefixed routes for gateway proxies
    path("api/v1/catalogue/categories/", CategoryListView.as_view(), name="catalogue-category-list"),
    path("api/v1/catalogue/categories/<slug:slug>/", CategoryDetailView.as_view(), name="catalogue-category-detail"),
    path("api/v1/catalogue/products/", ProductListView.as_view(), name="catalogue-product-list"),
    path("api/v1/catalogue/products/<slug:slug>/", ProductDetailView.as_view(), name="catalogue-product-detail"),
]
