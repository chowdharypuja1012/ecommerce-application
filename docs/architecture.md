# Architecture — Shop Platform Microservices

## 1. Context Diagram

```
                        ┌─────────────────┐
                        │    Browser /    │
                        │  React Frontend │  :5173
                        └────────┬────────┘
                                 │ HTTP REST (JSON)
                                 ▼
                        ┌─────────────────┐
                        │   API Gateway   │  :8000
                        │  (Django DRF)   │
                        └──┬──┬──┬──┬──┬─┘
              ┌────────────┘  │  │  │  └──────────────┐
              ▼               ▼  │  ▼                 ▼
       ┌──────────┐  ┌──────────┐│┌──────────┐ ┌──────────┐
       │ Accounts │  │Catalogue ││ │  Cart    │ │ Wishlist │
       │  :8001   │  │  :8002   ││ │  :8003   │ │  :8004   │
       └──────────┘  └──────────┘│└──────────┘ └──────────┘
                                 │
              ┌──────────────────┼──────────────┐
              ▼                  ▼               ▼
       ┌──────────┐      ┌──────────┐    ┌──────────┐
       │  Orders  │      │ Payments │    │ Reviews  │
       │  :8005   │      │  :8006   │    │  :8007   │
       └──────────┘      └──────────┘    └──────────┘
```

**Rule**: The frontend talks **only** to the Gateway. Internal services are not publicly exposed.

---

## 2. Service Responsibility Matrix

| Service   | Owns | Public via Gateway | Internal Calls Made To |
|-----------|------|--------------------|------------------------|
| **Accounts** | Users, profiles, addresses, auth tokens | `/api/v1/auth/`, `/api/v1/profile/` | None |
| **Catalogue** | Categories, products, stock levels, images | `/api/v1/catalogue/` | None |
| **Cart** | Active carts, cart items | `/api/v1/cart/` | Catalogue (price/stock validation) |
| **Wishlist** | Saved product lists per user | `/api/v1/wishlist/` | Catalogue (product details) |
| **Orders** | Order records, order items (snapshots), status lifecycle | `/api/v1/orders/` | Catalogue, Cart, Payments |
| **Payments** | Sandbox payment sessions, provider references, payment status | `/api/v1/payments/` | Orders (status update) |
| **Reviews** | Ratings, review text, moderation status | `/api/v1/reviews/` | Accounts (eligibility), Orders (purchase check) |
| **Gateway** | Routing, CORS, request correlation | All `/api/v1/*` | All services (proxy) |

---

## 3. Data Ownership

**Rule**: Each service owns its database exclusively. No service may directly read or write another service's database. Cross-service data is exchanged via REST API calls only.

| Service   | Database            | Key Tables (to be defined in Tasks 4–16) |
|-----------|---------------------|------------------------------------------|
| Accounts  | `shop_accounts_db`  | `users`, `profiles`, `addresses` |
| Catalogue | `shop_catalogue_db` | `categories`, `products`, `product_images` |
| Cart      | `shop_cart_db`      | `carts`, `cart_items` |
| Wishlist  | `shop_wishlist_db`  | `wishlists`, `wishlist_items` |
| Orders    | `shop_orders_db`    | `orders`, `order_items` (price/SKU snapshots) |
| Payments  | `shop_payments_db`  | `payment_sessions`, `payment_events` |
| Reviews   | `shop_reviews_db`   | `reviews`, `ratings` |

---

## 4. Local Development Topology

| Component   | Port  | Command |
|-------------|-------|---------|
| Gateway     | 8000  | `cd gateway && python manage.py runserver 8000` |
| Accounts    | 8001  | `cd services/accounts && python manage.py runserver 8001` |
| Catalogue   | 8002  | `cd services/catalogue && python manage.py runserver 8002` |
| Cart        | 8003  | `cd services/cart && python manage.py runserver 8003` |
| Wishlist    | 8004  | `cd services/wishlist && python manage.py runserver 8004` |
| Orders      | 8005  | `cd services/orders && python manage.py runserver 8005` |
| Payments    | 8006  | `cd services/payments && python manage.py runserver 8006` |
| Reviews     | 8007  | `cd services/reviews && python manage.py runserver 8007` |
| Frontend    | 5173  | `cd frontend && npm run dev` |
| PostgreSQL  | 5432  | System service (auto-start) |

---

## 5. Microservice Rules

1. **Database isolation**: Never share ORM models or directly query another service's DB.
2. **No distributed transactions**: Use clear order/payment states, idempotent operations, retries with limits, and compensating actions.
3. **Timeouts**: Define timeouts and safe error handling for every remote call.
4. **Correlation IDs**: Add request IDs to logs for tracing.
5. **Authorization**: Keep authentication identity verifiable across services; enforce authorization *inside* each service.
6. **Contract tests**: Use contract tests to detect breaking API changes between services.

---

## 6. Failure & Idempotency Rules

- Cart and Order operations must be idempotent (safe to retry).
- Checkout must re-validate price and stock from the Catalogue service at the moment of order creation.
- Payment callbacks must be idempotent — duplicate callbacks must not double-charge or create duplicate order records.
- If a service is unreachable, the gateway returns a structured error (503) — never a raw exception.
