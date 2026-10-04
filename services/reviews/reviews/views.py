from django.db import IntegrityError, transaction
from django.db.models import Avg, Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import ProductReview
from .serializers import ProductReviewSerializer


class ProductReviewListView(APIView):
    """
    GET /api/v1/reviews/product/<int:product_id>/
    Public endpoint returning approved customer reviews and aggregate rating metrics.
    """
    permission_classes = [AllowAny]

    def get(self, request, product_id):
        reviews = ProductReview.objects.filter(product_id=product_id, is_approved=True)

        total_reviews = reviews.count()
        avg_rating = round(reviews.aggregate(avg=Avg("rating"))["avg"] or 0.0, 1)

        distribution = {
            "5": reviews.filter(rating=5).count(),
            "4": reviews.filter(rating=4).count(),
            "3": reviews.filter(rating=3).count(),
            "2": reviews.filter(rating=2).count(),
            "1": reviews.filter(rating=1).count(),
        }

        serializer = ProductReviewSerializer(reviews, many=True)

        return Response({
            "product_id": product_id,
            "average_rating": avg_rating,
            "total_reviews": total_reviews,
            "rating_distribution": distribution,
            "reviews": serializer.data,
        }, status=status.HTTP_200_OK)


class CreateProductReviewView(APIView):
    """
    POST /api/v1/reviews/
    Enforces 1 to 5 rating range validation and duplicate review prevention per user/product.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        rating = request.data.get("rating")

        if not product_id or not isinstance(product_id, int):
            return Response(
                {"product_id": "Valid integer product_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if rating is None or not isinstance(rating, int) or rating < 1 or rating > 5:
            return Response(
                {"rating": "Rating must be an integer between 1 and 5 stars."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Duplicate review check
        if ProductReview.objects.filter(user=request.user, product_id=product_id).exists():
            return Response(
                {"detail": "You have already submitted a review for this product."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                review = ProductReview.objects.create(
                    user=request.user,
                    product_id=product_id,
                    rating=rating,
                    title=request.data.get("title", "").strip(),
                    comment=request.data.get("comment", "").strip(),
                    is_approved=True,
                )
        except IntegrityError:
            return Response(
                {"detail": "You have already submitted a review for this product."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserReviewDetailView(APIView):
    """
    PATCH / DELETE /api/v1/reviews/<int:pk>/
    Allows authenticated customer to update or delete their own review.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        review = ProductReview.objects.filter(pk=pk, user=request.user).first()
        if not review:
            return Response({"detail": "Review not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        rating = request.data.get("rating")
        if rating is not None:
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                return Response(
                    {"rating": "Rating must be an integer between 1 and 5 stars."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            review.rating = rating

        if "title" in request.data:
            review.title = request.data["title"].strip()
        if "comment" in request.data:
            review.comment = request.data["comment"].strip()

        review.save()
        serializer = ProductReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        review = ProductReview.objects.filter(pk=pk, user=request.user).first()
        if not review:
            return Response({"detail": "Review not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        review.delete()
        return Response({"detail": "Review deleted successfully."}, status=status.HTTP_200_OK)


class AdminReviewModerationView(APIView):
    """
    PATCH / DELETE /api/v1/reviews/admin/<int:pk>/
    Admin-only workflow for moderating reviews (approving/flagging/deleting).
    """
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        review = ProductReview.objects.filter(pk=pk).first()
        if not review:
            return Response({"detail": "Review not found."}, status=status.HTTP_404_NOT_FOUND)

        if "is_approved" in request.data:
            review.is_approved = bool(request.data["is_approved"])
            review.save(update_fields=["is_approved"])

        serializer = ProductReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        review = ProductReview.objects.filter(pk=pk).first()
        if not review:
            return Response({"detail": "Review not found."}, status=status.HTTP_404_NOT_FOUND)

        review.delete()
        return Response({"detail": "Review deleted by admin moderation."}, status=status.HTTP_200_OK)
