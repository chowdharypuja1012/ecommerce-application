from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Wishlist, WishlistItem
from .serializers import WishlistSerializer
from .catalogue_service import fetch_product_details


def get_or_create_user_wishlist(user) -> Wishlist:
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    return wishlist


class WishlistDetailView(APIView):
    """
    GET /api/v1/wishlist/
    Retrieves current user's active wishlist with resolved product details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = get_or_create_user_wishlist(request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddWishlistItemView(APIView):
    """
    POST /api/v1/wishlist/items/
    Body: {"product_id": int}
    Adds a product to user's wishlist. Enforces unique product entries.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id or not isinstance(product_id, int):
            return Response(
                {"product_id": "Valid integer product_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Resolve product via Catalogue service (verifies existence)
        prod_info = fetch_product_details(product_id)
        if not prod_info:
            return Response(
                {"product_id": f"Product #{product_id} could not be resolved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        wishlist = get_or_create_user_wishlist(request.user)

        # Check for existing entry to prevent duplicates
        if WishlistItem.objects.filter(wishlist=wishlist, product_id=product_id).exists():
            return Response(
                {"product_id": "Product is already in your wishlist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                WishlistItem.objects.create(wishlist=wishlist, product_id=product_id)
        except IntegrityError:
            return Response(
                {"product_id": "Product is already in your wishlist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveWishlistItemView(APIView):
    """
    DELETE /api/v1/wishlist/items/<int:pk>/
    Removes item from user's wishlist by item ID.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        wishlist = get_or_create_user_wishlist(request.user)
        item = WishlistItem.objects.filter(pk=pk, wishlist=wishlist).first()
        if not item:
            return Response(
                {"detail": "Wishlist item not found or does not belong to user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        item.delete()
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveWishlistItemByProductView(APIView):
    """
    DELETE /api/v1/wishlist/items/by-product/<int:product_id>/
    Removes item from user's wishlist by product ID.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        wishlist = get_or_create_user_wishlist(request.user)
        item = WishlistItem.objects.filter(product_id=product_id, wishlist=wishlist).first()
        if not item:
            return Response(
                {"detail": "Product is not in your wishlist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        item.delete()
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClearWishlistView(APIView):
    """
    POST /api/v1/wishlist/clear/
    Removes all items from current user's wishlist.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wishlist = get_or_create_user_wishlist(request.user)
        wishlist.items.all().delete()
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
