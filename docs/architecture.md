# ServiceFind Architecture

## Overview
ServiceFind is a professional Service Finder mobile application built with a
decoupled, full-stack architecture:

- **Frontend:** Flutter (Dart) mobile app, web-capable, developed in GitHub
  Codespaces.
- **Backend:** Python FastAPI REST API.
- **Database:** MongoDB Atlas (planned, connected in Step 3).
- **Dev environment:** GitHub Codespaces devcontainer (Flutter, Dart, Python,
  Chromium, Git all inside the container).

## High-level diagram

```
+---------------------+      HTTPS/JSON       +---------------------------+
|  Flutter (mobile)   | <==================> |  FastAPI backend          |
|  (mobile/lib/)      |                      |  (backend/app/)           |
+---------------------+                      +---------------------------+
                                                   |
                                                   | MongoDB wire protocol
                                                   v
                                          +----------------+
                                          | MongoDB Atlas  |
                                          | (Step 3)       |
                                          +----------------+
```

## Layer responsibilities

### Frontend (`mobile/`)
- `lib/main.dart` — application entry point.
- `lib/app/` — app shell (theme, routes).
- `lib/core/` — shared utilities, constants, extensions.
- `lib/config/` — API endpoints, environment flags.
- `lib/models/` — data models consumed by the UI.
- `lib/services/` — API client, storage services.
- `lib/providers/` — state management (Riverpod/Provider/Bloc).
- `lib/widgets/` — reusable UI widgets.
- `lib/features/` — feature-based modules (authentication, home, categories,
  search, service_details, bookings, favorites, reviews, profile,
  notifications). Each feature owns its UI and logic.

### Backend (`backend/`)
- `app/main.py` — FastAPI application factory + ASGI app.
- `app/core/` — configuration (Pydantic settings), custom exceptions.
- `app/database/` — MongoDB client (placeholder; connected Step 3).
- `app/models/` — domain models.
- `app/schemas/` — request/response Pydantic schemas.
- `app/routers/` — API route definitions (`health` implemented here).
- `app/services/` — business logic.
- `app/repositories/` — data-access layer (Step 3).
- `app/middleware/` — custom middleware.
- `app/utils/` — shared helpers.
- `tests/` — pytest suite.

## Architectural principles
1. **Separation of concerns:** frontend, backend, and database are independent
   layers communicating over HTTP/JSON (frontend ↔ backend) and the MongoDB
   wire protocol (backend ↔ Atlas).
2. **Clean backend layers:** routers delegate to services, services delegate to
   repositories, repositories talk to the database. This keeps business logic
   testable without a database.
3. **Feature-based frontend:** each user-facing capability lives in its own
   folder under `lib/features/`, keeping the codebase navigable as it grows.
4. **Environment parity:** Flutter, Dart, Python, and tooling all run inside
   the GitHub Codespaces container — nothing is required on the host machine.
5. **Deferred dependencies:** MongoDB and authentication are intentionally not
   implemented in Step 2 so the foundation can be verified first.

## Tech stack
| Layer | Technology | Version |
|-------|-----------|---------|
| Mobile framework | Flutter | 3.47.8 |
| Mobile language | Dart | 3.13.7 |
| Backend framework | FastAPI | 0.162.3 |
| Backend language | Python | 3.14.2 |
| ASGI server | Uvicorn | 0.54.0 |
| Database | MongoDB Atlas | Step 3 |
| Dev environment | GitHub Codespaces devcontainer | — |
