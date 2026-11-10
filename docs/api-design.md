# ServiceFind API Design (Planned)

The backend exposes a REST API built with FastAPI. Only `GET /health` is
implemented in Step 2; the remaining endpoints are planned for Step 3+.

## Base URL
- Local development: `http://localhost:8000`
- Docs (Swagger UI): `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Implemented endpoints (Step 2)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Welcome / root payload |
| `GET` | `/health` | Health check (returns `{"status":"healthy",...}`) |

## Planned endpoints (later steps)

### Authentication
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login, return access token |
| `POST` | `/auth/logout` | Logout / revoke token |

### Providers & Services
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/providers` | List service providers (with filters) |
| `GET` | `/providers/{id}` | Get provider detail |
| `GET` | `/services` | List services |
| `GET` | `/services/{id}` | Get service detail |
| `POST` | `/services` | Create a service (provider only) |
| `PUT` | `/services/{id}` | Update a service (provider only) |
| `DELETE` | `/services/{id}` | Delete a service (provider only) |

### Bookings
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/bookings` | List bookings (customer or provider scope) |
| `POST` | `/bookings` | Create a booking |
| `GET` | `/bookings/{id}` | Get booking detail |
| `PATCH` | `/bookings/{id}` | Update booking status |
| `DELETE` | `/bookings/{id}` | Cancel a booking |

### Reviews
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/reviews` | List reviews for a provider/service |
| `POST` | `/reviews` | Create a review |

### Favorites
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/favorites` | List customer favorites |
| `POST` | `/favorites` | Add a favorite |
| `DELETE` | `/favorites/{id}` | Remove a favorite |

## API conventions
- JSON request bodies and responses.
- Pydantic schemas validate all request payloads and shape responses.
- Standard HTTP status codes (200, 201, 400, 401, 403, 404, 409, 500).
- CORS configured in `backend/app/core/config.py` (permissive in dev).
- Bearer-token authentication (planned) via `Authorization` header.

## Error response shape (planned)
```json
{
  "detail": "Human-readable error message",
  "code": "ERROR_CODE"
}
```

## Notes
- MongoDB is not connected yet; repository layer is implemented in Step 3.
- No authentication middleware is applied yet.
