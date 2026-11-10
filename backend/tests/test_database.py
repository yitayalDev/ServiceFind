"""Tests for the MongoDB connection module using mocks.

No real MongoDB Atlas connection is made; all client interactions are mocked.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.config import settings
from app.core.exceptions import (
    DatabaseConfigurationError,
    DatabaseConnectionError,
)
import app.database.mongodb as mongodb_mod


class TestConnectDb:
    """Tests for connect_db()."""

    @pytest.mark.asyncio
    async def test_connect_db_missing_uri(self):
        """connect_db() raises DatabaseConfigurationError when MONGODB_URI is empty."""
        mongodb_mod._client = None
        mongodb_mod._database = None
        with patch.object(settings, "MONGODB_URI", ""):
            with pytest.raises(DatabaseConfigurationError):
                await mongodb_mod.connect_db()
        assert mongodb_mod._client is None
        assert mongodb_mod._database is None

    @pytest.mark.asyncio
    async def test_connect_db_invalid_uri(self):
        """connect_db() raises DatabaseConfigurationError for a malformed URI."""
        mongodb_mod._client = None
        mongodb_mod._database = None
        from pymongo.errors import ConfigurationError

        fake_client = MagicMock()
        fake_client.admin.command = AsyncMock(side_effect=ConfigurationError("bad uri"))
        with patch.object(settings, "MONGODB_URI", "mongodb+srv://bad"):
            with patch(
                "app.database.mongodb.AsyncIOMotorClient", return_value=fake_client
            ):
                with pytest.raises(DatabaseConfigurationError):
                    await mongodb_mod.connect_db()
        assert mongodb_mod._client is None

    @pytest.mark.asyncio
    async def test_connect_db_timeout(self):
        """connect_db() raises DatabaseConnectionError on server selection timeout."""
        mongodb_mod._client = None
        mongodb_mod._database = None
        from pymongo.errors import ServerSelectionTimeoutError

        fake_client = MagicMock()
        fake_client.admin.command = AsyncMock(
            side_effect=ServerSelectionTimeoutError("timeout")
        )
        with patch.object(settings, "MONGODB_URI", "mongodb+srv://example.net"):
            with patch(
                "app.database.mongodb.AsyncIOMotorClient", return_value=fake_client
            ):
                with pytest.raises(DatabaseConnectionError):
                    await mongodb_mod.connect_db()
        assert mongodb_mod._client is None

    @pytest.mark.asyncio
    async def test_connect_db_success(self):
        """connect_db() sets the client and database on successful ping."""
        mongodb_mod._client = None
        mongodb_mod._database = None
        fake_client = MagicMock()
        fake_client.admin.command = AsyncMock(return_value={"ok": 1})
        fake_client.__getitem__ = MagicMock(return_value="fake-database")

        with patch.object(settings, "MONGODB_URI", "mongodb+srv://example.net"):
            with patch(
                "app.database.mongodb.AsyncIOMotorClient", return_value=fake_client
            ):
                await mongodb_mod.connect_db()

        assert mongodb_mod._client is fake_client
        assert mongodb_mod._database == "fake-database"
        fake_client.admin.command.assert_awaited_once_with("ping")

    @pytest.mark.asyncio
    async def test_close_db(self):
        """close_db() clears the client and database."""
        mongodb_mod._client = MagicMock()
        mongodb_mod._database = MagicMock()
        await mongodb_mod.close_db()
        mongodb_mod._client.close.assert_called_once()
        assert mongodb_mod._client is None
        assert mongodb_mod._database is None


class TestPingDatabase:
    """Tests for ping_database()."""

    @pytest.mark.asyncio
    async def test_ping_database_true(self):
        """ping_database() returns True when ping succeeds."""
        mongodb_mod._client = MagicMock()
        mongodb_mod._client.admin.command = AsyncMock(return_value={"ok": 1})
        assert await mongodb_mod.ping_database() is True

    @pytest.mark.asyncio
    async def test_ping_database_false(self):
        """ping_database() returns False when ping raises."""
        mongodb_mod._client = MagicMock()
        mongodb_mod._client.admin.command = AsyncMock(side_effect=Exception("down"))
        assert await mongodb_mod.ping_database() is False

    @pytest.mark.asyncio
    async def test_ping_database_no_client(self):
        """ping_database() returns False when no client exists."""
        mongodb_mod._client = None
        assert await mongodb_mod.ping_database() is False


class TestGetDatabase:
    """Tests for get_database()."""

    def test_get_database_connected(self):
        """get_database() returns the database when connected."""
        mongodb_mod._database = "connected-db"
        assert mongodb_mod.get_database() == "connected-db"

    def test_get_database_not_connected(self):
        """get_database() raises DatabaseConnectionError when not connected."""
        mongodb_mod._database = None
        with pytest.raises(DatabaseConnectionError):
            mongodb_mod.get_database()
