"""Application configuration.

Uses pydantic-settings so values can be overridden via environment variables
or a ``.env`` file without changing code. MongoDB settings are declared here;
the database connection is established in ``app.database.mongodb`` via the
FastAPI lifespan (see ``app/main.py``).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "servicefind-api"
    VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    CORS_ORIGINS: list[str] = ["*"]

    # MongoDB Atlas connection (see backend/.env.example)
    # Left empty by default so the app can start without a database; connect_db()
    # raises DatabaseConfigurationError if this is not set before use.
    MONGODB_URI: str = ""
    DATABASE_NAME: str = "servicefind"

    # Server selection timeout in milliseconds for the MongoDB client.
    MONGODB_TIMEOUT_MS: int = 5000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
