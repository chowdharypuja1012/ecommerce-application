# 🌸 Sweet Sentiments — AI Agent & Developer Setup Guide

Welcome to **Sweet Sentiments** (formerly *ruja*), an aesthetic boutique e-commerce platform crafted with a React + TypeScript frontend, an API Gateway, and 7 Django REST microservices.

This guide provides automated and step-by-step instructions so any **AI Agent** or **Developer** can clone this repository onto a fresh machine, install dependencies, seed the full product catalogue with images, and start all services with zero friction.

---

## 🏗️ Architecture & Port Map

| Component | Directory | Port | Technology | Purpose |
| :--- | :--- | :---: | :--- | :--- |
| **Frontend** | `frontend/` | `5173` | React, Vite, TypeScript, Lucide | Aesthetic boutique UI, Cart, Wishlist, Auth modal |
| **API Gateway** | `gateway/` | `8000` | Django, Requests proxy | Routes client traffic to microservices |
| **Accounts** | `services/accounts/` | `8001` | Django REST Framework | User registration, token auth, profile |
| **Catalogue** | `services/catalogue/` | `8002` | Django REST Framework | 6 categories, 21 boutique products, stock |
| **Cart** | `services/cart/` | `8003` | Django REST Framework | User shopping cart management |
| **Wishlist** | `services/wishlist/` | `8004` | Django REST Framework | User wishlist with reactive backend sync |
| **Orders** | `services/orders/` | `8005` | Django REST Framework | Checkout and order tracking |
| **Payments** | `services/payments/` | `8006` | Django REST Framework | Payment processing simulation |
| **Reviews** | `services/reviews/` | `8007` | Django REST Framework | Product ratings and reviews |

---

## ⚡ Quick Start: Automated 1-Click Bootstrap

Run the included automated bootstrap script from the project root (`shop-platform`):

```bash
# 1. Run the Python bootstrap script
python scripts/bootstrap_all.py
```

### What `bootstrap_all.py` automatically does:
1. Validates Python (3.10+) and Node.js (18+) environments.
2. Installs backend dependencies (`pip install -r requirements.txt`).
3. Installs frontend dependencies (`npm install` inside `frontend/`).
4. Runs database migrations for all 7 microservices.
5. Seeds the **full catalogue** (6 categories + 21 high-res lifestyle products).
6. Creates default superuser accounts (`admin` / `admin123`).

---

## 🗄️ Database Strategy: Zero-Config SQLite Fallback vs PostgreSQL

### Database Compatibility:
* **SQLite (Default / Zero-Config)**: 
  Each microservice automatically falls back to an embedded SQLite database (`BASE_DIR / 'db.sqlite3'`) if `DB_NAME` is not defined or if `DB_ENGINE=sqlite`. **No database installation, credentials, or server setup is required.**
* **PostgreSQL (Optional / Production)**: 
  If you have PostgreSQL running, specify credentials in your environment or `.env` file:
  ```env
  DB_NAME=shop_db
  DB_USER=postgres
  DB_PASSWORD=postgres
  DB_HOST=127.0.0.1
  DB_PORT=5432
  ```

> [!NOTE]
> **Why not H2 Database?**  
> H2 is a Java-only embedded database engine. Since the backend services are built in Python/Django, **SQLite** is the standard zero-configuration embedded database. It provides identical zero-setup convenience while having 100% native Django ORM support.

---

## 🖼️ Product Catalogue & Image Assets

* **100% Self-Contained**: All 21 high-resolution lifestyle product images and 6 category banners are committed directly to the Git repository in `frontend/public/images/`.
* **Relative Serving**: The database seed script points directly to local relative paths (e.g. `/images/products/the-little-journal-blush-pink.jpg`). Vite serves them automatically from the root on `http://localhost:5173`.
* **Zero External Cloud Dependencies**: No AWS S3, Cloudinary, or external CDN accounts are required.

---

## 🛠️ Step-by-Step Manual Setup

If you prefer running commands manually instead of the automated bootstrap:

### 1. Backend Dependencies & Migrations
```bash
# Install root requirements
pip install -r requirements.txt

# Run migrations across all services
python services/accounts/manage.py migrate
python services/catalogue/manage.py migrate
python services/cart/manage.py migrate
python services/wishlist/manage.py migrate
python services/orders/manage.py migrate
python services/payments/manage.py migrate
python services/reviews/manage.py migrate
```

### 2. Seed Catalogue & Admin Accounts
```bash
# Seed 21 boutique products and 6 categories
python services/catalogue/manage.py seed_data

# Create superuser accounts (admin / admin123)
python setup_admins.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cd ..
```

---

## 🚀 Starting All Services

To run the complete application, open separate terminal windows (or use background processes) and run:

```bash
# Gateway & Services
python gateway/manage.py runserver 8000
python services/accounts/manage.py runserver 8001
python services/catalogue/manage.py runserver 8002
python services/cart/manage.py runserver 8003
python services/wishlist/manage.py runserver 8004
python services/orders/manage.py runserver 8005
python services/payments/manage.py runserver 8006
python services/reviews/manage.py runserver 8007

# Frontend (in a separate terminal)
cd frontend
npm run dev
```

The store will be available at: **`http://localhost:5173`**  
The API Gateway will be available at: **`http://localhost:8000`**

---

## 🔑 Default Credentials

| Role | Username | Password | Access Port / Admin UI |
| :--- | :--- | :--- | :--- |
| **Superuser / Admin** | `admin` | `admin123` | `http://localhost:8002/admin/` (Catalogue) |
| **Superuser / Admin** | `admin` | `admin123` | `http://localhost:8001/admin/` (Accounts) |
| **Superuser / Admin** | `admin` | `admin123` | `http://localhost:8005/admin/` (Orders) |
| **Superuser / Admin** | `admin` | `admin123` | `http://localhost:8007/admin/` (Reviews) |

---

## 🩺 Health Check & Verification

You can verify that all services are operational by checking the gateway health endpoint:
* **Gateway Status**: `http://localhost:8000/api/health/` (or `http://localhost:8000/health/`)
* **Catalogue API**: `http://localhost:8000/api/products/` (returns 21 products)
* **Categories API**: `http://localhost:8000/api/categories/` (returns 6 categories)
