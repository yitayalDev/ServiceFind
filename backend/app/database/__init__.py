"""Database module.

Provides the async MongoDB client (Motor's AsyncIOMotorClient, built on PyMongo)
and FastAPI lifespan handlers for startup/shutdown.

Import the shared database handle with::

    from app.database import db, get_database

MongoDB is connected at application startup via the lifespan registered in
``app.main`` and disconnected at shutdown. The client is created once and
reused (singleton) to avoid creating multiple clients unnecessarily.
"""

from app.database.mongodb import (
    connect_db,
    close_db,
    get_database,
    ping_database,
    db,
)

__all__ = [
    "db",
    "connect_db",
    "close_db",
    "get_database",
    "ping_database",
]
