from decimal import Decimal
from django.db import transaction
from django.db.models import Sum, Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError

from .models import Order, OrderItem, OrderStatus
from .serializers import OrderSerializer, CheckoutInputSerializer
from .service_clients import fetch_user_cart, clear_user_cart, verify_and_resolve_products


class CheckoutPreviewView(APIView):
    """
    POST /api/v1/checkout/preview/
    Generates an order preview by fetching the active cart, rechecking live inventory
    and prices with Catalogue service, and confirming address details.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_header = request.headers.get("Authorization")
        cart_data = fetch_user_cart(auth_header=auth_header, user_id=request.user.id)

        items = cart_data.get("items", [])
        if not items:
            return Response(
                {"cart": "Your shopping cart is empty. Add products to cart before checkout."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Re-check inventory stock and prices with Catalogue service
        verified_items = verify_and_resolve_products(items)

        total_amount = sum(item["line_total"] for item in verified_items)

        return Response({
            "shipping_address": serializer.validated_data,
            "items": [
                {
                    "product_id": item["product_id"],
                    "product_name": item["product_name"],
                    "product_sku": item["product_sku"],
                    "unit_price": str(item["unit_price"]),
                    "quantity": item["quantity"],
                    "line_total": str(item["line_total"]),
                }
                for item in verified_items
            ],
            "total_amount": str(total_amount),
            "status": "READY_FOR_CHECKOUT",
        }, status=status.HTTP_200_OK)


class CheckoutCreateOrderView(APIView):
    """
    POST /api/v1/checkout/
    Submits checkout, re-verifies inventory, creates pending order safely, and clears cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address_data = serializer.validated_data
        auth_header = request.headers.get("Authorization")

        # 1. Retrieve active cart
        cart_data = fetch_user_cart(auth_header=auth_header, user_id=request.user.id)
        cart_items = cart_data.get("items", [])

        if not cart_items:
            return Response(
                {"cart": "Your shopping cart is empty. Cannot place an empty order."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Re-verify inventory & price snapshots via Catalogue Service
        verified_items = verify_and_resolve_products(cart_items)

        # 3. Create Order & OrderItem snapshots within atomic transaction
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                status=OrderStatus.PENDING,
                shipping_full_name=address_data["shipping_full_name"],
                shipping_street_address=address_data["shipping_street_address"],
                shipping_city=address_data["shipping_city"],
                shipping_state=address_data["shipping_state"],
                shipping_postal_code=address_data["shipping_postal_code"],
                shipping_country=address_data["shipping_country"],
                shipping_phone=address_data.get("shipping_phone", ""),
            )

            total = Decimal("0.00")
            for item in verified_items:
                order_item = OrderItem(
                    order=order,
                    product_id=item["product_id"],
                    product_sku=item["product_sku"],
                    product_name=item["product_name"],
                    unit_price=item["unit_price"],
                    quantity=item["quantity"],
                )
                order_item.save()
                total += order_item.line_total

            order.total_amount = total
            order.save()

        # 4. Clear Cart after successful order placement
        clear_user_cart(auth_header=auth_header, user_id=request.user.id)

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
    """
    GET /api/v1/orders/
    Returns order history for current authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    """
    GET /api/v1/orders/<int:pk>/
    Returns specific order details with strict user ownership enforcement.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = Order.objects.filter(pk=pk, user=request.user).first()
        if not order:
            return Response(
                {"detail": "Order not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCancelView(APIView):
    """
    POST /api/v1/orders/<int:pk>/cancel/
    Allows customer to cancel an eligible order (PENDING or PAID status).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.filter(pk=pk, user=request.user).first()
        if not order:
            return Response(
                {"detail": "Order not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            order.transition_to(OrderStatus.CANCELLED)
        except ValidationError as err:
            return Response(err.detail, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderStatusUpdateView(APIView):
    """
    PATCH /api/v1/orders/<int:pk>/status/
    Updates order status validating state transitions.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        new_status = request.data.get("status")
        if not new_status or new_status not in OrderStatus.values:
            return Response(
                {"status": f"Invalid status choices: {OrderStatus.values}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.user.is_staff:
            order = Order.objects.filter(pk=pk).first()
        else:
            order = Order.objects.filter(pk=pk, user=request.user).first()

        if not order:
            return Response(
                {"detail": "Order not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            order.transition_to(new_status)
        except ValidationError as err:
            return Response(err.detail, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ── ADMIN OPERATIONS ─────────────────────────────────────────────────────────

class AdminAllOrdersView(APIView):
    """
    GET /api/v1/orders/admin/all/
    Admin-only endpoint returning all customer orders across the platform.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Order.objects.all()
        status_filter = request.query_params.get("status", "").strip()
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminOrderMetricsView(APIView):
    """
    GET /api/v1/orders/admin/metrics/
    Admin-only analytics metrics endpoint (total revenue, order counts, status breakdown).
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_orders = Order.objects.count()

        # Revenue from non-cancelled, non-pending paid/shipped/delivered orders
        fulfilled = Order.objects.filter(status__in=[OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED])
        total_revenue = fulfilled.aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")

        # Counts by status
        counts_by_status = {
            st: Order.objects.filter(status=st).count() for st in OrderStatus.values
        }

        return Response({
            "total_orders": total_orders,
            "total_revenue": str(total_revenue),
            "orders_by_status": counts_by_status,
        }, status=status.HTTP_200_OK)
