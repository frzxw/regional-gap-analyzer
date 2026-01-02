"""
Indicators repository - Data access for indicator data.
"""

from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.db import get_database
from app.common.time import utc_now


class IndicatorsRepository:
    """Repository for indicator data operations."""

    COLLECTION_NAME = "indicators"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def find_all(
        self,
        filters: Optional[Dict] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Dict], int]:
        """Find indicators with filters and pagination."""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def find_by_id(self, indicator_id: str) -> Optional[Dict]:
        """Find indicator by ID."""
        return await self.collection.find_one({"_id": ObjectId(indicator_id)})

    async def find_by_region_and_year(
        self, region_code: str, year: int
    ) -> List[Dict]:
        """Find all indicators for a region and year."""
        cursor = self.collection.find({
            "region_code": region_code,
            "year": year,
        })
        return await cursor.to_list(length=100)

    async def find_by_key_and_year(
        self, indicator_key: str, year: int
    ) -> List[Dict]:
        """Find indicator values across all regions."""
        cursor = self.collection.find({
            "indicator_key": indicator_key,
            "year": year,
        })
        return await cursor.to_list(length=100)

    async def create(self, indicator_data: Dict) -> str:
        """Create a new indicator."""
        indicator_data["created_at"] = utc_now()
        result = await self.collection.insert_one(indicator_data)
        return str(result.inserted_id)

    async def create_many(self, indicators: List[Dict]) -> List[str]:
        """Bulk create indicators."""
        now = utc_now()
        for ind in indicators:
            ind["created_at"] = now
        result = await self.collection.insert_many(indicators)
        return [str(id) for id in result.inserted_ids]

    async def update(self, indicator_id: str, update_data: Dict) -> bool:
        """Update an indicator."""
        update_data["updated_at"] = utc_now()
        result = await self.collection.update_one(
            {"_id": ObjectId(indicator_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete(self, indicator_id: str) -> bool:
        """Delete an indicator."""
        result = await self.collection.delete_one({"_id": ObjectId(indicator_id)})
        return result.deleted_count > 0

    async def delete_by_source(self, source_id: str) -> int:
        """Delete all indicators from a source."""
        result = await self.collection.delete_many({"source_id": source_id})
        return result.deleted_count

    async def get_available_years(self) -> List[int]:
        """Get list of years with data."""
        years = await self.collection.distinct("year")
        return sorted(years, reverse=True)

    async def get_categories(self) -> List[str]:
        """Get list of indicator categories."""
        return await self.collection.distinct("category")


async def get_indicators_repository() -> IndicatorsRepository:
    """Factory function to get repository instance."""
    db = await get_database()
    return IndicatorsRepository(db)
