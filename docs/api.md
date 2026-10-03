# API Contracts — Shop Platform

> This document will be filled in as each service API is built (Tasks 3–16).
> Gateway routes all traffic under `/api/v1/`.

## Gateway Base URL

`http://127.0.0.1:8000`

## Health Endpoints

| Endpoint | Service | Method | Response |
|----------|---------|--------|----------|
| `/api/v1/health/` | Gateway | GET | `{"service": "gateway", "status": "ok"}` |

*Per-service health endpoints and feature API contracts will be documented here as tasks are completed.*
