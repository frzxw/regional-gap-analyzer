"""
Labor Force repository - Data access for labor force data.
"""

from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.db import get_database


class LaborForceRepository:
    """Repository for labor force (angkatan_kerja) data operations."""

    COLLECTION_NAME = "angkatan_kerja"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def find_all(
        self,
        filters: Optional[Dict] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Dict], int]:
        """Find all labor force records with filters and pagination."""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def find_by_id(self, record_id: str) -> Optional[Dict]:
        """Find labor force record by ID."""
        try:
            return await self.collection.find_one({"_id": ObjectId(record_id)})
        except Exception:
            return None

    async def find_by_province_and_year(
        self, province_id: str, year: int
    ) -> Optional[Dict]:
        """Find labor force record for specific province and year."""
        return await self.collection.find_one({
            "province_id": province_id,
            "tahun": year,
        })

    async def find_by_province(
        self, province_id: str, skip: int = 0, limit: int = 100
    ) -> tuple[List[Dict], int]:
        """Find all labor force records for a province."""
        query = {"province_id": province_id}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("tahun", -1)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def find_by_year(
        self, year: int, skip: int = 0, limit: int = 100
    ) -> tuple[List[Dict], int]:
        """Find all labor force records for a specific year."""
        query = {"tahun": year}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("province_id", 1)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def get_available_years(self) -> List[int]:
        """Get list of years with labor force data."""
        pipeline = [
            {"$group": {"_id": "$tahun"}},
            {"$sort": {"_id": -1}}
        ]
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        return sorted([doc["_id"] for doc in results], reverse=True)

    async def get_provinces(self) -> List[str]:
        """Get list of provinces with labor force data."""
        pipeline = [
            {"$group": {"_id": "$province_id"}},
            {"$sort": {"_id": 1}}
        ]
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        return [doc["_id"] for doc in results]

    async def get_province_name(self, province_id: str) -> Optional[str]:
        """Get province name from provinces collection."""
        try:
            provinces_collection = self.db["provinces"]
            province = await provinces_collection.find_one({"properties.id": province_id})
            if province:
                # Try different possible field names
                if "properties" in province and "PROVINSI" in province["properties"]:
                    return province["properties"]["PROVINSI"]
                elif "PROVINSI" in province:
                    return province["PROVINSI"]
            return None
        except Exception as e:
            print(f"Error getting province name: {e}")
            return None
