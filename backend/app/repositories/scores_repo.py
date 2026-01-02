"""
Scores repository - Data access for computed scores.
"""

from typing import Optional, List, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.db import get_database
from app.common.time import utc_now


class ScoresRepository:
    """Repository for score data operations."""

    COLLECTION_NAME = "scores"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def find_all(
        self,
        year: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Dict], int]:
        """Find scores with optional year filter."""
        query = {"year": year} if year else {}
        cursor = (
            self.collection.find(query)
            .sort("rank", 1)
            .skip(skip)
            .limit(limit)
        )
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def find_by_id(self, score_id: str) -> Optional[Dict]:
        """Find score by ID."""
        return await self.collection.find_one({"_id": ObjectId(score_id)})

    async def find_by_region_and_year(
        self, region_code: str, year: int
    ) -> Optional[Dict]:
        """Find score for specific region and year."""
        return await self.collection.find_one({
            "region_code": region_code,
            "year": year,
        })

    async def find_by_region(
        self, region_code: str, limit: int = 10
    ) -> List[Dict]:
        """Find all scores for a region (time series)."""
        cursor = (
            self.collection.find({"region_code": region_code})
            .sort("year", -1)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)

    async def find_rankings(self, year: int) -> List[Dict]:
        """Get rankings for a specific year."""
        cursor = (
            self.collection.find({"year": year})
            .sort("rank", 1)
        )
        return await cursor.to_list(length=100)

    async def upsert(self, region_code: str, year: int, score_data: Dict) -> str:
        """Create or update score for region/year."""
        score_data["computed_at"] = utc_now()
        result = await self.collection.update_one(
            {"region_code": region_code, "year": year},
            {"$set": score_data},
            upsert=True,
        )
        if result.upserted_id:
            return str(result.upserted_id)
        doc = await self.find_by_region_and_year(region_code, year)
        return str(doc["_id"]) if doc else ""

    async def update_ranks(self, year: int, rankings: List[Dict]) -> int:
        """Bulk update ranks for a year."""
        updated = 0
        for rank_data in rankings:
            result = await self.collection.update_one(
                {"region_code": rank_data["region_code"], "year": year},
                {"$set": {
                    "rank": rank_data["rank"],
                    "rank_delta": rank_data.get("rank_delta"),
                }},
            )
            updated += result.modified_count
        return updated

    async def delete_by_year(self, year: int) -> int:
        """Delete all scores for a year."""
        result = await self.collection.delete_many({"year": year})
        return result.deleted_count

    async def get_available_years(self) -> List[int]:
        """Get list of years with scores."""
        years = await self.collection.distinct("year")
        return sorted(years, reverse=True)

    async def get_latest_year(self) -> Optional[int]:
        """Get the most recent year with scores."""
        years = await self.get_available_years()
        return years[0] if years else None


async def get_scores_repository() -> ScoresRepository:
    """Factory function to get repository instance."""
    db = await get_database()
    return ScoresRepository(db)
