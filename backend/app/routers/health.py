"""Health-check routers.

Provides:
- ``GET /health`` — service health status (no database probe).
- ``GET /health/database`` — verifies MongoDB connectivity via ``ping``.

The database endpoint never exposes credentials or sensitive connection
details; it only reports whether the server responded to the ping.
"""

from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.database import ping_database

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Health check",
    description="Return the service health status. No database connection is "
    "validated here.",
)
async def health_check() -> dict:
    """Return the service health status."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION,
    }


@router.get(
    "/health/database",
    summary="Database health check",
    description="Verify MongoDB connectivity using a ping command. Returns a "
    "clear success or failure status without exposing connection details.",
)
async def database_health() -> dict:
    """Return the database connectivity status."""
    connected = await ping_database()
    if connected:
        return {
            "status": "healthy",
            "database": {
                "connected": True,
                "name": settings.DATABASE_NAME,
            },
        }
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "status": "unhealthy",
            "database": {
                "connected": False,
                "name": settings.DATABASE_NAME,
            },
        },
    )
