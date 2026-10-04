from django.contrib import admin
from django.urls import path
from .health import make_health_view
from .views import (
    ProductReviewListView,
    CreateProductReviewView,
    UserReviewDetailView,
    AdminReviewModerationView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("reviews"), name="health"),
    path("api/v1/reviews/", CreateProductReviewView.as_view(), name="review-create"),
    path("api/v1/reviews/product/<int:product_id>/", ProductReviewListView.as_view(), name="review-product-list"),
    path("api/v1/reviews/<int:pk>/", UserReviewDetailView.as_view(), name="review-user-detail"),
    path("api/v1/reviews/admin/<int:pk>/", AdminReviewModerationView.as_view(), name="review-admin-moderation"),
]
