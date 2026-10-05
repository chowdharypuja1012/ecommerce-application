# AGENTS.md — Sweet Sentiments Setup & Execution Instructions for AI Agents

> **Quick Summary for AI Agents**: This repository contains the **Sweet Sentiments** boutique lifestyle e-commerce application. It has a React+TypeScript frontend, a Django API Gateway, and 7 Django microservices.

## 🚀 1-Step Complete Bootstrap
To bootstrap this repository on a fresh machine:
```bash
python scripts/bootstrap_all.py
```
This single command automatically:
1. Installs Python dependencies (`requirements.txt`).
2. Installs Frontend dependencies (`frontend/package.json`).
3. Runs database migrations for all 7 microservices (using zero-configuration SQLite fallback, or PostgreSQL if configured).
4. Seeds all 21 boutique products + 6 categories with high-resolution image links.
5. Sets up superuser admin accounts (`admin` / `admin123`).

---

## 🧭 Microservices & Port Map

| Component | Path | Port | Run Command |
| :--- | :--- | :---: | :--- |
| **API Gateway** | `gateway/` | `8000` | `python gateway/manage.py runserver 8000` |
| **Accounts** | `services/accounts/` | `8001` | `python services/accounts/manage.py runserver 8001` |
| **Catalogue** | `services/catalogue/` | `8002` | `python services/catalogue/manage.py runserver 8002` |
| **Cart** | `services/cart/` | `8003` | `python services/cart/manage.py runserver 8003` |
| **Wishlist** | `services/wishlist/` | `8004` | `python services/wishlist/manage.py runserver 8004` |
| **Orders** | `services/orders/` | `8005` | `python services/orders/manage.py runserver 8005` |
| **Payments** | `services/payments/` | `8006` | `python services/payments/manage.py runserver 8006` |
| **Reviews** | `services/reviews/` | `8007` | `python services/reviews/manage.py runserver 8007` |
| **Frontend** | `frontend/` | `5173` | `cd frontend && npm run dev` |

---

## 🗄️ Database & Environment Notes
* **Zero Database Server Needed**: The application is configured with an automated SQLite fallback. If `DB_NAME` is absent in the environment or if `DB_ENGINE=sqlite`, every service uses `db.sqlite3`.
* **Product Images**: All 21 product images are located in `frontend/public/images/products/` and tracked in Git. No external cloud storage is needed.

See `AGENT_SETUP_GUIDE.md` for full documentation.
