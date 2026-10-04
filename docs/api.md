# API Specification & Gateway Contracts — Shop Platform

## 1. Overview
The API Gateway operates at `http://127.0.0.1:8000` and serves as a unified entry point for all frontend requests. It routes traffic under `/api/v1/` to dedicated backend microservices.

---

## 2. Authentication & Profile Service (`/api/v1/auth/`, `/api/v1/profile/`)
**Target Microservice:** `accounts` (`http://127.0.0.1:8001`)

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/v1/auth/register/` | `POST` | No | Registers new user; returns auth token & profile payload. |
| `/api/v1/auth/login/` | `POST` | No | Authenticates username & password; returns DRF Token. |
| `/api/v1/auth/logout/` | `POST` | Yes | Invalidates and deletes current auth token. |
| `/api/v1/auth/me/` | `GET` | Yes | Returns current user details and profile info. |
| `/api/v1/profile/` | `GET`, `PATCH` | Yes | View or update user profile (full name, phone, avatar). |
| `/api/v1/profile/addresses/` | `GET`, `POST` | Yes | List or create shipping addresses owned by request user. |
| `/api/v1/profile/addresses/<id>/` | `GET`, `PATCH`, `DELETE` | Yes | Manage individual user-owned shipping address. |

---

## 3. Product Catalogue Service (`/api/v1/products/`, `/api/v1/categories/`)
**Target Microservice:** `catalogue` (`http://127.0.0.1:8002`)

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/v1/products/` | `GET` | No | List products with pagination, search, category filter, price range, and sorting. |
| `/api/v1/products/<id>/` | `GET` | No | Retrieve detailed product specs by ID. |
| `/api/v1/categories/` | `GET` | No | List all active product categories. |
| `/api/v1/admin/products/` | `POST`, `PATCH`, `DELETE` | Staff Only | Create, update, or soft-delete products. |
| `/api/v1/admin/categories/` | `POST`, `PATCH`, `DELETE` | Staff Only | Create or manage categories. |

---

## 4. Shopping Cart Service (`/api/v1/cart/`)
**Target Microservice:** `cart` (`http://127.0.0.1:8003`)

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/v1/cart/` | `GET` | Yes | Retrieve active shopping cart and item details. |
| `/api/v1/cart/items/` | `POST` | Yes | Add item or increase quantity in cart. |
| `/api/v1/cart/items/<id>/` | `PATCH`, `DELETE` | Yes | Update item quantity or remove from cart. |
| `/api/v1/cart/clear/` | `POST` | Yes | Empty all items from active cart. |

---

## 5. Wishlist Service (`/api/v1/wishlist/`)
**Target Microservice:** `wishlist` (`http://127.0.0.1:8004`)

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/v1/wishlist/` | `GET` | Yes | Retrieve user wishlist items. |
| `/api/v1/wishlist/items/` | `POST` | Yes | Add product to wishlist. |
| `/api/v1/wishlist/items/<id>/` | `DELETE` | Yes | Remove item from wishlist. |
| `/api/v1/wishlist/clear/` | `POST` | Yes | Clear all items from wishlist. |

---

## 6. Checkout & Orders Service (`/api/v1/checkout/`, `/api/v1/orders/`)
**Target Microservice:** `orders` (`http://127.0.0.1:8005`)

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/v1/checkout/preview/` | `POST` | Yes | Generate order preview with price snapshot & stock check. |
| `/api/v1/checkout/` | `POST` | Yes | Submit order from active cart items & clear cart. |
| `/api/v1/orders/` | `GET` | Yes | List customer order history. |
| `/api/v1/orders/<id>/` | `GET` | Yes | Retrieve order details & line items by ID. |
| `/api/v1/orders/<id>/cancel/` | `POST` | Yes | Cancel pending order. |
| `/api/v1/admin/orders/` | `GET` | Staff Only | Admin view of all platform orders. |
| `/api/v1/admin/orders/<id>/status/` | `PATCH` | Staff Only | Admin update order status (`PAID`, `SHIPPED`, `DELIVERED`). |

---

## 7. Payment Sandbox Service (`/api/v1/payments/`)
**Target Microservice:** `payments` (`http://127.0.0.1:8006`)

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/v1/payments/process/` | `POST` | Yes | Process payment sandbox simulation (`SUCCESS`/`FAIL`/`CANCEL`). |
| `/api/v1/payments/order/<order_id>/` | `GET` | Yes | View payment transaction history for an order. |

---

## 8. Customer Reviews Service (`/api/v1/reviews/`)
**Target Microservice:** `reviews` (`http://127.0.0.1:8007`)

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/v1/reviews/product/<product_id>/` | `GET` | No | Retrieve public approved reviews and aggregate ratings. |
| `/api/v1/reviews/` | `POST` | Yes | Submit customer review (1-5 star rating). |
| `/api/v1/reviews/<id>/` | `PATCH`, `DELETE` | Yes | Update or delete customer review. |
| `/api/v1/reviews/admin/<id>/` | `PATCH`, `DELETE` | Staff Only | Moderate review approval status. |
