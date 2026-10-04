# Production Deployment & Operations Guide — Shop Platform

## 1. Overview
The **Shop Platform** is a containerized microservices application comprising 8 backend services (Django REST Framework + PostgreSQL) and a React TypeScript Vite frontend.

### Service Topology & Ports
| Service Name | Internal Port | Primary Purpose | Database |
|--------------|---------------|-----------------|----------|
| **API Gateway** | `8000` | Public Reverse Proxy & Routing | None (Stateless) |
| **Accounts** | `8001` | User Auth, Profiles & Addresses | `accounts_db` |
| **Catalogue** | `8002` | Products, Stock & Categories | `catalogue_db` |
| **Cart** | `8003` | Shopping Cart & Items | `cart_db` |
| **Wishlist** | `8004` | Customer Wishlist | `wishlist_db` |
| **Orders** | `8005` | Checkout Orchestration & Orders | `orders_db` |
| **Payments** | `8006` | Payment Sandbox Processing | `payments_db` |
| **Reviews** | `8007` | Customer Reviews & Ratings | `reviews_db` |
| **Frontend** | `5173` / `80` | React TS Vite Web Application | — |

---

## 2. Environment Variables & Secret Provisioning

Production settings strictly require secrets supplied by the host environment. **Never commit `.env` files containing production credentials to source control.**

### Mandatory Environment Variables per Backend Service
```bash
# Core Django Config
DJANGO_SECRET_KEY="<production-random-50-character-secret-key>"
DEBUG=False
ALLOWED_HOSTS="127.0.0.1,localhost,api.yourdomain.com"
CORS_ALLOWED_ORIGINS="https://yourdomain.com"

# Production SSL & HSTS Security Settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Database Configuration (PostgreSQL)
DB_NAME="<service_db_name>"
DB_USER="<postgres_user>"
DB_PASSWORD="<postgres_password>"
DB_HOST="<postgres_host>"
DB_PORT=5432
```

---

## 3. Database Migration Strategy

Database migrations must run independently for each service prior to spawning application processes.

### Pre-Deployment Migration Commands
```bash
# Run for each microservice directory
cd services/accounts && python manage.py migrate --noinput
cd services/catalogue && python manage.py migrate --noinput
cd services/cart && python manage.py migrate --noinput
cd services/wishlist && python manage.py migrate --noinput
cd services/orders && python manage.py migrate --noinput
cd services/payments && python manage.py migrate --noinput
cd services/reviews && python manage.py migrate --noinput
```

---

## 4. Static Assets & Frontend Build

### Building the Production Frontend
```bash
cd shop-platform/frontend
npm install
npm run build
```
This produces static bundle assets in `shop-platform/frontend/dist/`. Serve `dist/` via NGINX, Cloudflare Pages, AWS S3 + CloudFront, or Vercel.

---

## 5. Container Orchestration & Health Checks

Each microservice exposes an automated health check endpoint used by Docker/Kubernetes readiness probes:

```bash
# Gateway & Microservice Health Probes
GET /api/v1/health/
```

### Expected Health Response:
```json
{
  "status": "healthy",
  "service": "catalogue",
  "timestamp": "2026-10-04T16:53:00Z"
}
```

---

## 6. Pre-Flight Deployment Checklist
- [x] Execute `python manage.py check --deploy` across all services.
- [x] Ensure `DEBUG=False` in production environment.
- [x] Verify SSL/TLS certificates on API Gateway reverse proxy.
- [x] Confirm CORS origin allowlist restricts non-whitelisted origins.
- [x] Run full automated unit and E2E test suites prior to deployment.
