"""MongoDB Atlas connection module.

Uses Motor's ``AsyncIOMotorClient`` (the asynchronous MongoDB driver built on
PyMongo) for non-blocking database access inside FastAPI's async event loop.

Responsibilities:
- Create a single, reusable MongoDB client (singleton) at startup.
- Verify connectivity with a ``ping`` command.
- Expose ``get_database()`` so routers/services can obtain the database handle.
- Close the client cleanly at shutdown.

Never log or return the connection URI, credentials, or any part of it.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

from app.core.config import settings
from app.core.exceptions import (
    DatabaseConfigurationError,
    DatabaseConnectionError,
)

# Singleton client and database handle. Created once at startup, closed at
# shutdown. Reused across all requests to avoid multiple clients.
_client: AsyncIOMotorClient | None = None
_database = None


async def connect_db() -> None:
    """Initialize the MongoDB client and verify connectivity.

    Intended to be registered as a FastAPI lifespan startup handler.
    Raises ``DatabaseConfigurationError`` if ``MONGODB_URI`` is not set, or
    ``DatabaseConnectionError`` if the server cannot be reached within the
    configured timeout.
    """
    global _client, _database

    if not settings.MONGODB_URI:
        raise DatabaseConfigurationError(
            "MONGODB_URI environment variable is not configured. "
            "Copy backend/.env.example to backend/.env and set MONGODB_URI."
        )

    try:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=settings.MONGODB_TIMEOUT_MS,
        )
        _database = _client[settings.DATABASE_NAME]

        # Verify connectivity with a lightweight ping command.
        await _client.admin.command("ping")
    except ConfigurationError as exc:
        _client = None
        _database = None
        raise DatabaseConfigurationError(
            f"Invalid MongoDB connection string: {exc}"
        ) from exc
    except ServerSelectionTimeoutError as exc:
        _client = None
        _database = None
        raise DatabaseConnectionError(
            "Could not reach MongoDB within the configured timeout."
        ) from exc
    except Exception as exc:  # noqa: BLE001 - any unexpected failure must surface
        _client = None
        _database = None
        raise DatabaseConnectionError(
            "Unexpected error while connecting to MongoDB."
        ) from exc


async def close_db() -> None:
    """Close the MongoDB client.

    Intended to be registered as a FastAPI lifespan shutdown handler.
    Safe to call even if ``connect_db`` was never called or already failed.
    """
    global _client, _database
    if _client is not None:
        _client.close()
        _client = None
        _database = None


def get_database():
    """Return the connected database instance.

    Raises ``DatabaseConnectionError`` if the database is not connected.
    """
    if _database is None:
        raise DatabaseConnectionError(
            "Database is not connected. Ensure connect_db() ran at startup."
        )
    return _database


# Backwards-compatible module-level handle (``from app.database import db``).
db = _database


async def ping_database() -> bool:
    """Ping MongoDB to verify connectivity.

    Returns ``True`` if the server responds to a ping, ``False`` otherwise.
    Never raises; used by the ``/health/database`` endpoint.
    """
    if _client is None:
        return False
    try:
        await _client.admin.command("ping")
        return True
    except Exception:  # noqa: BLE001 - health check must never crash
        return False
