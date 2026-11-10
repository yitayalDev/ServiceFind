"""Custom application exceptions.

Reserved for future use (e.g. ServiceNotFoundError, BookingConflictError).
Includes database-related exceptions used by ``app.database.mongodb``.
"""


class ServiceFindError(Exception):
    """Base exception for the ServiceFind application."""


class DatabaseConfigurationError(ServiceFindError):
    """Raised when MongoDB configuration is missing or invalid."""


class DatabaseConnectionError(ServiceFindError):
    """Raised when the MongoDB client cannot reach the database."""


class DatabaseError(ServiceFindError):
    """Raised for general MongoDB operation failures."""
