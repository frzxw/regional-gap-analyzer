"""
Region repository - Data access layer for regions.
Handles all MongoDB operations for region data.
"""

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db import get_database
from app.models import RegionModel


class RegionRepository:
    """Repository for region data operations."""

    COLLECTION_NAME = "regions"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def find_all(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[dict], int]:
        """
        Find all regions with pagination.

        Args:
            skip: Number of documents to skip
            limit: Maximum documents to return

        Returns:
            Tuple of (list of regions, total count)
        """
        cursor = self.collection.find().skip(skip).limit(limit)
        regions = await cursor.to_list(length=limit)
        total = await self.collection.count_documents({})
        return regions, total

    async def find_by_code(self, code: str) -> Optional[dict]:
        """Find a region by its code."""
        return await self.collection.find_one({"code": code})

    async def find_by_id(self, region_id: str) -> Optional[dict]:
        """Find a region by its MongoDB _id."""
        from bson import ObjectId

        return await self.collection.find_one({"_id": ObjectId(region_id)})

    async def create(self, region: RegionModel) -> str:
        """
        Create a new region.

        Returns:
            The inserted document ID as string.
        """
        result = await self.collection.insert_one(region.model_dump())
        return str(result.inserted_id)

    async def update(self, code: str, update_data: dict) -> bool:
        """
        Update a region by code.

        Returns:
            True if document was modified, False otherwise.
        """
        result = await self.collection.update_one(
            {"code": code}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete(self, code: str) -> bool:
        """
        Delete a region by code.

        Returns:
            True if document was deleted, False otherwise.
        """
        result = await self.collection.delete_one({"code": code})
        return result.deleted_count > 0


async def get_region_repository() -> RegionRepository:
    """Factory function to get region repository instance."""
    db = await get_database()
    return RegionRepository(db)
