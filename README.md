# Shop Platform — E-commerce Microservices

A portfolio-quality, full-stack e-commerce application built with Django REST Framework microservices and a React + TypeScript + Vite frontend.

## Architecture Overview

```
shop-platform/
├── gateway/          # API Gateway (Django DRF) — port 8000
├── services/
│   ├── accounts/     # Identity & Auth service — port 8001
│   ├── catalogue/    # Products & Categories — port 8002
│   ├── cart/         # Shopping Cart — port 8003
│   ├── wishlist/     # Wishlist — port 8004
│   ├── orders/       # Orders & Checkout — port 8005
│   ├── payments/     # Payment Sandbox — port 8006
│   └── reviews/      # Ratings & Reviews — port 8007
├── frontend/         # React + TypeScript + Vite — port 5173
└── docs/             # Architecture, API contracts, ERDs
```

**Frontend** calls only the **Gateway**. The Gateway proxies requests to the appropriate service. Each service owns its own PostgreSQL database.

---

## Prerequisites

| Tool | Required Version |
|---|---|
| Python | 3.12+ |
| pip | latest |
| Node.js | LTS (18+) |
| npm | 9+ |
| PostgreSQL | 15+ |
| Git | 2.x |

---

## First-Time Setup

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd shop-platform
```

### 2. PostgreSQL — create databases and user

Connect as the `postgres` superuser and run:

```sql
CREATE USER shop_dev WITH PASSWORD 'your-local-password';

CREATE DATABASE shop_accounts_db  OWNER shop_dev;
CREATE DATABASE shop_catalogue_db OWNER shop_dev;
CREATE DATABASE shop_cart_db      OWNER shop_dev;
CREATE DATABASE shop_wishlist_db  OWNER shop_dev;
CREATE DATABASE shop_orders_db    OWNER shop_dev;
CREATE DATABASE shop_payments_db  OWNER shop_dev;
CREATE DATABASE shop_reviews_db   OWNER shop_dev;

GRANT ALL PRIVILEGES ON DATABASE shop_accounts_db  TO shop_dev;
GRANT ALL PRIVILEGES ON DATABASE shop_catalogue_db TO shop_dev;
GRANT ALL PRIVILEGES ON DATABASE shop_cart_db      TO shop_dev;
GRANT ALL PRIVILEGES ON DATABASE shop_wishlist_db  TO shop_dev;
GRANT ALL PRIVILEGES ON DATABASE shop_orders_db    TO shop_dev;
GRANT ALL PRIVILEGES ON DATABASE shop_payments_db  TO shop_dev;
GRANT ALL PRIVILEGES ON DATABASE shop_reviews_db   TO shop_dev;
```

### 3. Configure each service

Each service has a `.env.example`. Copy it to `.env` and fill in real values:

```bash
# Repeat for each service: accounts, catalogue, cart, wishlist, orders, payments, reviews
cp services/accounts/.env.example services/accounts/.env

# Also for the gateway
cp gateway/.env.example gateway/.env
```

Edit each `.env` — **minimum required**:
- `DJANGO_SECRET_KEY` — generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `DB_PASSWORD` — your `shop_dev` PostgreSQL password

---

## Running Locally

Each service runs independently. Open a separate terminal for each.

### Gateway (port 8000)

```bash
cd gateway
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r ../requirements-base.txt
python manage.py check
python manage.py runserver 8000
```

### Services (ports 8001–8007)

```bash
# Example: accounts service on port 8001
cd services/accounts
python -m venv .venv
.\.venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

Repeat for each service with its own port:

| Service   | Port |
|-----------|------|
| accounts  | 8001 |
| catalogue | 8002 |
| cart      | 8003 |
| wishlist  | 8004 |
| orders    | 8005 |
| payments  | 8006 |
| reviews   | 8007 |

### Frontend (port 5173)

```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:5173**

---

## Running Tests

### Backend (per service)

```bash
cd services/accounts
python manage.py test
```

### Frontend

```bash
cd frontend
npm run test
```

### All Django checks at once

```bash
# From shop-platform root (with global django installed)
python scripts/gen_service_configs.py  # regenerate if needed
```

---

## Health Checks

Once all services are running:

```bash
curl http://127.0.0.1:8000/api/v1/health/   # Gateway
curl http://127.0.0.1:8001/api/v1/health/   # Accounts
curl http://127.0.0.1:8002/api/v1/health/   # Catalogue
# etc.
```

---

## Security Notes

- Never commit `.env` files — they are `.gitignore`'d
- Use `DB_PASSWORD` for local dev only — rotate before any deployment
- Payment service uses sandbox/simulation only — no real card data ever stored
- See `docs/architecture.md` for full security boundary documentation

---

## Documentation

| File | Contents |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | Service boundaries, context diagram, data ownership |
| [`docs/data-model.md`](docs/data-model.md) | Per-service ERDs |
| [`docs/api.md`](docs/api.md) | Gateway and service API contracts |
| [`docs/testing.md`](docs/testing.md) | Testing strategy and commands |
| [`docs/PROGRESS.md`](docs/PROGRESS.md) | Task completion log |

---

## Git Workflow

- One focused commit per approved task: `feat(catalogue): add product models and admin`
- Run tests before committing
- Log progress in `docs/PROGRESS.md`
