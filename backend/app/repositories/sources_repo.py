"""
Sources repository - Data access for data sources.
"""

from typing import Optional, List, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.db import get_database
from app.common.time import utc_now


class SourcesRepository:
    """Repository for source data operations."""

    COLLECTION_NAME = "sources"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def find_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Dict], int]:
        """Find all sources with pagination."""
        cursor = (
            self.collection.find()
            .sort("download_date", -1)
            .skip(skip)
            .limit(limit)
        )
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents({})
        return items, total

    async def find_by_id(self, source_id: str) -> Optional[Dict]:
        """Find source by ID."""
        return await self.collection.find_one({"_id": ObjectId(source_id)})

    async def find_by_name(self, name: str) -> Optional[Dict]:
        """Find source by name."""
        return await self.collection.find_one({"name": name})

    async def create(self, source_data: Dict) -> str:
        """Create a new source."""
        source_data["created_at"] = utc_now()
        result = await self.collection.insert_one(source_data)
        return str(result.inserted_id)

    async def update(self, source_id: str, update_data: Dict) -> bool:
        """Update a source."""
        update_data["updated_at"] = utc_now()
        result = await self.collection.update_one(
            {"_id": ObjectId(source_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete(self, source_id: str) -> bool:
        """Delete a source."""
        result = await self.collection.delete_one({"_id": ObjectId(source_id)})
        return result.deleted_count > 0

    async def get_indicator_sources(self, indicator_key: str) -> List[Dict]:
        """Get sources that provide a specific indicator."""
        cursor = self.collection.find({"indicators": indicator_key})
        return await cursor.to_list(length=50)


async def get_sources_repository() -> SourcesRepository:
    """Factory function to get repository instance."""
    db = await get_database()
    return SourcesRepository(db)
