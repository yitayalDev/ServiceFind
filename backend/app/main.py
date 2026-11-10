"""ServiceFind FastAPI application entry point.

Creates the FastAPI application, registers routers, and exposes the ASGI app
used by Uvicorn.

MongoDB is connected via FastAPI lifespan handlers defined in
``app.database.mongodb``. No authentication is implemented yet (deferred to
a later step).
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import close_db, connect_db
from app.routers import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan.

    Startup: connect to MongoDB Atlas.
    Shutdown: close the MongoDB client cleanly.
    """
    await connect_db()
    yield
    await close_db()


def create_app() -> FastAPI:
    """Application factory.

    Builds and configures the FastAPI application instance. Keeping the app
    construction in a function makes it easy to create separate instances for
    testing and for different deployment environments.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Service Finder backend API built with Python FastAPI.",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS is permissive for local development. Tighten allow_origins before
    # any production deployment.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers (no prefix; the health router defines its own paths)
    app.include_router(health.router, tags=["health"])

    @app.get("/", tags=["root"], summary="Root / welcome")
    async def root() -> dict:
        return {
            "message": "ServiceFind API",
            "version": settings.VERSION,
            "status": "running",
            "docs": "/docs",
        }

    return app


# Module-level ASGI application instance for Uvicorn (`uvicorn app.main:app`).
app = create_app()
