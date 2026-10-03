# Testing Strategy — Shop Platform

## Test Levels

| Level | What it verifies | When to run | Tools |
|-------|-----------------|-------------|-------|
| Unit | Model/service/business rules, validation, totals, state transitions | Every backend logic task | `pytest` / Django test runner |
| API/Integration | HTTP status, schema, auth, permissions, DB behavior, error cases | Every API/backend task | Django `APIClient` / `pytest` |
| Frontend component | Rendering, user actions, form validation, loading/error/empty states | Every UI task | Vitest + React Testing Library |
| End-to-end | Critical user journey across frontend, API and database | After checkout, before deployment | Playwright |
| Manual smoke | Start services, browse, authenticate, cart, sandbox order | At task boundaries and final handover | Manual |

## Running Tests

### Backend (any service)
```bash
cd services/<name>
python manage.py test
```

### Frontend
```bash
cd frontend
npm run test
```

### All Django system checks
```bash
# From each service directory:
python manage.py check
```

## Rules
- A green test suite is necessary but not sufficient — review diffs and verify acceptance criteria manually.
- Never use production credentials or real payment details in tests.
- Never skip or weaken a failing test to get a pass — fix the root cause.
