import os
import sys
import pytest
from unittest.mock import AsyncMock, patch

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import DatabaseConfig
from database.postgres import Database


@pytest.fixture
def db_config():
    return DatabaseConfig(
        {
            "host": "localhost",
            "port": 5432,
            "user": "testuser",
            "password": "testpass",
            "database": "testdb",
        }
    )


@pytest.fixture
def db(db_config):
    return Database(db_config)


@pytest.mark.asyncio
async def test_connect_to_db(db):
    with patch("asyncpg.connect", new_callable=AsyncMock) as mock_connect:
        await db.connect_to_db()
        mock_connect.assert_called_once_with(
            host=db.db_config.host,
            port=db.db_config.port,
            user=db.db_config.user,
            password=db.db_config.password,
            database=db.db_config.database,
        )
        assert db.connection is not None


@pytest.mark.asyncio
async def test_disconnect(db):
    with patch("asyncpg.connect", new_callable=AsyncMock) as mock_connect:
        mock_connection = mock_connect.return_value
        await db.connect_to_db()
        await db.disconnect()
        mock_connection.close.assert_awaited_once()
        assert db.connection is None


@pytest.mark.asyncio
async def test_execute_query_select(db):
    with patch("asyncpg.connect", new_callable=AsyncMock) as mock_connect:
        mock_connection = mock_connect.return_value
        mock_connection.fetch = AsyncMock(return_value=[{"id": 1, "text": "test"}])

        await db.connect_to_db()
        result = await db.execute_query("SELECT * FROM test_table WHERE id = $1", 1)

        mock_connection.fetch.assert_awaited_once_with(
            "SELECT * FROM test_table WHERE id = $1", 1
        )
        assert result == [{"id": 1, "text": "test"}]


@pytest.mark.asyncio
async def test_execute_query_non_select(db):
    with patch("asyncpg.connect", new_callable=AsyncMock) as mock_connect:
        mock_connection = mock_connect.return_value
        mock_connection.execute = AsyncMock(return_value="Query executed")

        await db.connect_to_db()
        result = await db.execute_query(
            "INSERT INTO test_table (id, text) VALUES ($1, $2)", 1, "test"
        )

        mock_connection.execute.assert_awaited_once_with(
            "INSERT INTO test_table (id, text) VALUES ($1, $2)", 1, "test"
        )
        assert result == "Query executed"
