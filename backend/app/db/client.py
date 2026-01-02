"""
MongoDB client connection using Motor (async driver).
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.settings import get_settings

# Global client instance
_client: AsyncIOMotorClient | None = None
_database: AsyncIOMotorDatabase | None = None


async def get_database() -> AsyncIOMotorDatabase:
    """
    Get the MongoDB database instance.
    Creates connection if not exists.
    """
    global _client, _database

    if _database is None:
        settings = get_settings()
        _client = AsyncIOMotorClient(settings.mongo_uri)
        _database = _client[settings.mongo_db]

    return _database


async def close_database() -> None:
    """Close the MongoDB connection."""
    global _client, _database

    if _client is not None:
        _client.close()
        _client = None
        _database = None


async def ping_database() -> bool:
    """
    Check if database connection is healthy.
    Returns True if connected, False otherwise.
    """
    try:
        db = await get_database()
        await db.command("ping")
        return True
    except Exception:
        return False
