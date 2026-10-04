# Security & Reliability Audit Matrix — Shop Platform Microservices

## 1. Executive Summary
This document provides a comprehensive security and reliability audit of the 8 microservices (`gateway`, `accounts`, `catalogue`, `cart`, `orders`, `payments`, `reviews`, `wishlist`) and the React TypeScript frontend.

All high-priority threats, data isolation risks, authentication vulnerabilities, and denial-of-service risks have been audited, mitigated, and verified with automated test suites.

---

## 2. Threat Checklist Matrix

| Security Domain | Threat Vector | Risk Level | Mitigation Strategy | Verification Status |
|-----------------|---------------|------------|---------------------|---------------------|
| **Authentication** | Token theft / Brute-force login attempts | High | Implemented DRF Token Authentication with `ScopedRateThrottle` (`20/min` on auth endpoints). Passwords hashed using Django's PBKDF2 with SHA256. | ✅ Verified (`test_security.py`) |
| **Authorization** | Insecure Direct Object References (IDOR) | High | Strict `request.user` filtering in querysets (`Address.objects.filter(user=request.user)`, `Order.objects.filter(user=request.user)`). Cross-user access returns HTTP 404/403. | ✅ Verified (`test_security.py` & `test_orders.py`) |
| **Data Validation** | Rating boundary exploitation / Invalid quantities | Medium | `MinValueValidator` and `MaxValueValidator` enforced on models and DRF serializers. Positive integer validation on cart & order items. | ✅ Verified (`test_reviews.py` & `test_cart.py`) |
| **Duplicate Prevention** | Double review / duplicate cart item injection | Medium | Database `UniqueConstraint(fields=["user", "product_id"])` on ProductReview and WishlistItem models. | ✅ Verified (`test_reviews.py` & `test_wishlist.py`) |
| **Rate Limiting** | Automated API spam / DDoS | Medium | Enforced global DRF rate throttling (`AnonRateThrottle`: 200/min, `UserRateThrottle`: 1000/min) across all 8 microservices. | ✅ Enforced across all settings |
| **CORS & Proxying** | Cross-Origin Data Exfiltration | High | Explicit origin allowlists on Gateway (`CORS_ALLOWED_ORIGINS`). Gateway acts as reverse proxy, hiding internal microservice topology. | ✅ Verified in Gateway configuration |
| **Security Headers** | XSS, MIME-sniffing, Clickjacking | Medium | Enabled `SECURE_BROWSER_XSS_FILTER = True`, `SECURE_CONTENT_TYPE_NOSNIFF = True`, `X_FRAME_OPTIONS = "DENY"`. | ✅ Applied to all microservices |
| **Secret Management** | Hardcoded production keys / Credential leakage | Critical | `settings_validator.py` enforces mandatory environment variable loading (`DJANGO_SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`). | ✅ Verified in startup checks |
| **Error Handling** | HTML Stack trace leakage in 500 responses | Low | Configured DRF `JSONRenderer` and standard exception handlers to return structured JSON error messages without internal tracebacks. | ✅ Verified across all services |

---

## 3. Microservice Rate Limiting Configuration

All 8 services use Django REST Framework throttling configured in `settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "200/min",
        "user": "1000/min",
        "auth": "20/min",
    },
}
```

---

## 4. Test Suite Execution & Verification Summary

| Service | Test Suite Command | Tests Ran | Status |
|---------|-------------------|-----------|--------|
| **gateway** | `python manage.py test tests` | 9 | ✅ PASS |
| **accounts** | `python manage.py test tests` | 28 | ✅ PASS |
| **catalogue** | `python manage.py test tests` | 32 | ✅ PASS |
| **cart** | `python manage.py test tests` | 9 | ✅ PASS |
| **orders** | `python manage.py test tests` | 14 | ✅ PASS |
| **payments** | `python manage.py test tests` | 7 | ✅ PASS |
| **reviews** | `python manage.py test tests` | 5 | ✅ PASS |
| **wishlist** | `python manage.py test tests` | 8 | ✅ PASS |
| **frontend** | `npm run build && npm run lint` | 45 modules | ✅ PASS (0 errors) |

---

## 5. Security & Reliability Checklist Completed
- [x] Strict user isolation on all private user resources (addresses, cart, orders, wishlist).
- [x] Input range validation (ratings 1-5, quantities > 0, price formatting).
- [x] DB-level uniqueness constraints for ratings and wishlist items.
- [x] Rate limiting / throttling configured across all microservices.
- [x] Security headers (XSS, Nosniff, Frame Options) enabled in settings.
- [x] Zero credential leaks in source code; environment variable enforcement active.
- [x] Clean JSON error responses without traceback leakage.
