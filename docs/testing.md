# Comprehensive Testing Strategy & Verification Guide — Shop Platform

## 1. Overview & Test Matrix
The project implements a multi-layered automated testing suite covering unit tests, integration tests, contract tests, and end-to-end (E2E) customer journey verification.

| Test Level | Scope & Target | Execution Command | Count / Coverage |
|------------|----------------|-------------------|------------------|
| **Gateway Unit** | Proxy routing, CORS, Health check | `python manage.py test tests` | 9 Tests |
| **Accounts Unit & Security** | Auth, Profile, Addresses, Rate Limiting, Ownership Isolation | `python manage.py test tests` | 28 Tests |
| **Catalogue Unit & Admin** | Products, Categories, Stock, Filtering, Admin Operations | `python manage.py test tests` | 32 Tests |
| **Cart Unit** | Cart Items, Quantity updates, Total calculation | `python manage.py test tests` | 9 Tests |
| **Orders & Checkout Unit** | Checkout snapshotting, Status transitions, History | `python manage.py test tests` | 14 Tests |
| **Payments Sandbox Unit** | Transaction simulation, Idempotency keys | `python manage.py test tests` | 7 Tests |
| **Reviews & Ratings Unit** | Rating validation (1-5), Duplicate prevention, Aggregates | `python manage.py test tests` | 5 Tests |
| **Wishlist Unit** | Wishlist items, Clear, Unique constraints | `python manage.py test tests` | 8 Tests |
| **Frontend Clients & E2E** | Full 9-step customer journey (Browse -> Auth -> Cart -> Wishlist -> Address -> Checkout -> Payment -> History -> Review) | `npx tsx src/api/e2eCustomerJourney.test.ts` | 9 Steps Verified |
| **Frontend Production Build** | TypeScript build check & Vite bundling | `npm run build` | 0 Errors |
| **Frontend Linting** | Oxlint code quality verification | `npm run lint` | 0 Errors |

---

## 2. Automated Test Execution Commands

### Running All Backend Django Test Suites
```bash
# Run in each respective service directory:
cd gateway && python manage.py test tests
cd services/accounts && python manage.py test tests
cd services/catalogue && python manage.py test tests
cd services/cart && python manage.py test tests
cd services/orders && python manage.py test tests
cd services/payments && python manage.py test tests
cd services/reviews && python manage.py test tests
cd services/wishlist && python manage.py test tests
```

### Running Frontend Tests & E2E Integration Suite
```bash
cd shop-platform/frontend

# Client API unit tests
npx tsx src/api/authClient.test.ts
npx tsx src/api/catalogueClient.test.ts
npx tsx src/api/cartClient.test.ts
npx tsx src/api/ordersClient.test.ts
npx tsx src/api/paymentsClient.test.ts
npx tsx src/api/reviewsClient.test.ts
npx tsx src/api/wishlistClient.test.ts

# Full 9-Step E2E Customer Journey Integration Test
npx tsx src/api/e2eCustomerJourney.test.ts

# Production build and linter
npm run build
npm run lint
```
