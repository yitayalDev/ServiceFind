# ServiceFind Database Design (Planned)

MongoDB Atlas is **not connected yet** (Step 3). This document describes the
planned collections, documents, and relationships so the backend repositories
(Step 3) can be implemented against a stable schema.

## Planned collections

### `users`
Stores application users (customers and service providers).

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Primary key |
| `email` | String | Unique login email |
| `password_hash` | String | Bcrypt/argon2 hash (auth step) |
| `full_name` | String | Display name |
| `role` | Enum | `customer` \| `provider` |
| `phone` | String | Contact phone |
| `profile_picture_url` | String | Avatar URL |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last-update timestamp |

**Indexes:** unique index on `email`.

### `service_providers`
Provider profiles linked to a `users` document.

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Primary key |
| `user_id` | ObjectId | Ref → `users._id` |
| `business_name` | String | Provider business name |
| `categories` | [String] | Service categories offered |
| `bio` | String | Provider description |
| `rating` | Double | Average rating (0–5) |
| `is_available` | Boolean | Accepting new bookings |
| `created_at` | DateTime | |

**Indexes:** `user_id` (unique), `categories`.

### `services`
Individual services offered by providers.

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Primary key |
| `provider_id` | ObjectId | Ref → `service_providers._id` |
| `title` | String | Service title |
| `description` | String | Service description |
| `category` | String | Service category |
| `price` | Decimal128 | Price (currency minor units or decimal) |
| `currency` | String | ISO currency code (e.g. `USD`) |
| `duration_minutes` | Int | Expected duration |
| `is_active` | Boolean | Visible to customers |
| `created_at` | DateTime | |

**Indexes:** `provider_id`, `category`, `is_active`.

### `service_requests` (bookings)
Customer bookings of a provider's service.

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Primary key |
| `customer_id` | ObjectId | Ref → `users._id` |
| `provider_id` | ObjectId | Ref → `service_providers._id` |
| `service_id` | ObjectId | Ref → `services._id` |
| `status` | Enum | `pending` \| `confirmed` \| `completed` \| `cancelled` |
| `scheduled_at` | DateTime | Appointment time |
| `price_paid` | Decimal128 | Amount charged |
| `created_at` | DateTime | |

**Indexes:** `customer_id`, `provider_id`, `status`, `scheduled_at`.

### `reviews`
Customer reviews of completed services.

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Primary key |
| `booking_id` | ObjectId | Ref → `service_requests._id` |
| `customer_id` | ObjectId | Ref → `users._id` |
| `provider_id` | ObjectId | Ref → `service_providers._id` |
| `rating` | Int | 1–5 stars |
| `comment` | String | Review text |
| `created_at` | DateTime | |

**Indexes:** `provider_id`, `booking_id` (unique).

### `favorites`
Customer-favorited providers or services.

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Primary key |
| `customer_id` | ObjectId | Ref → `users._id` |
| `provider_id` | ObjectId | Ref → `service_providers._id` (optional) |
| `service_id` | ObjectId | Ref → `services._id` (optional) |
| `created_at` | DateTime | |

**Indexes:** `customer_id`.

## Relationships summary
- `users` 1↔1 `service_providers` (providers are also users)
- `service_providers` 1→N `services`
- `service_providers` 1→N `service_requests`
- `users` (customer) 1→N `service_requests`
- `services` 1→N `service_requests`
- `service_requests` 1→1 `reviews`
- `users` 1→N `reviews`
- `service_providers` 1→N `reviews`
- `users` 1→N `favorites`

## Notes
- All timestamps stored as UTC `DateTime`.
- ObjectId references used for relationships (no joins in MongoDB; application
  layer resolves related documents).
- Connection string and database name live in `backend/.env.example`
  (`MONGODB_URL`, `MONGODB_DB_NAME`); the client is instantiated in Step 3.
