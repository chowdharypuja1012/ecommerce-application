# Data Model & Entity-Relationship Diagrams — Shop Platform

## 1. Data Ownership Architecture & Isolation
The application strictly enforces **Database-per-Service** isolation. No database shares tables or relationships with another microservice.

- **Accounts Service** owns User identity, Profile extensions, and Shipping Addresses.
- **Catalogue Service** owns Category taxonomies and Product specifications.
- **Cart Service** owns active Shopping Carts and line items.
- **Wishlist Service** owns customer Wishlist items.
- **Orders Service** owns Order headers and Order Line Items (snapshotting product price/name/SKU at checkout time).
- **Payments Service** owns Sandbox Payment Transactions and idempotency tokens.
- **Reviews Service** owns Product Reviews, Rating scores (1-5), and moderation status.

---

## 2. Microservice Entity-Relationship Diagrams (ERDs)

### Accounts Microservice Schema (`accounts_db`)

```mermaid
erDiagram
    User ||--o| Profile : "has one"
    User ||--o{ Address : "owns many"

    User {
        int id PK
        string username
        string email
        string password
        boolean is_staff
        datetime date_joined
    }

    Profile {
        int id PK
        int user_id FK
        string full_name
        string phone_number
        string avatar_url
        datetime created_at
    }

    Address {
        int id PK
        int user_id FK
        string title
        string street_address
        string city
        string state
        string postal_code
        string country
        boolean is_default
    }
```

---

### Catalogue Microservice Schema (`catalogue_db`)

```mermaid
erDiagram
    Category ||--o{ Product : "contains"

    Category {
        int id PK
        string name
        string slug
        string description
        boolean is_active
    }

    Product {
        int id PK
        int category_id FK
        string name
        string slug
        string sku
        decimal price
        int stock
        string description
        string image_url
        boolean is_active
        datetime created_at
    }
```

---

### Cart Microservice Schema (`cart_db`)

```mermaid
erDiagram
    Cart ||--o{ CartItem : "contains"

    Cart {
        int id PK
        int user_id
        datetime created_at
        datetime updated_at
    }

    CartItem {
        int id PK
        int cart_id FK
        int product_id
        int quantity
        datetime added_at
    }
```

---

### Orders Microservice Schema (`orders_db`)

```mermaid
erDiagram
    Order ||--o{ OrderItem : "contains"

    Order {
        int id PK
        int user_id
        string order_number
        string status
        decimal total_amount
        string shipping_full_name
        string shipping_street_address
        string shipping_city
        string shipping_state
        string shipping_postal_code
        string shipping_country
        datetime created_at
    }

    OrderItem {
        int id PK
        int order_id FK
        int product_id
        string product_sku
        string product_name
        decimal unit_price
        int quantity
        decimal line_total
    }
```

---

### Payments Microservice Schema (`payments_db`)

```mermaid
erDiagram
    PaymentTransaction {
        int id PK
        int order_id
        string transaction_reference
        string idempotency_key
        decimal amount
        string currency
        string payment_method
        string status
        string provider_status_code
        datetime created_at
    }
```

---

### Reviews Microservice Schema (`reviews_db`)

```mermaid
erDiagram
    ProductReview {
        int id PK
        int user_id
        string username
        int product_id
        int rating
        string title
        string comment
        boolean is_approved
        datetime created_at
    }
```
