"""
Indeks Harga Konsumen repository - Data access for consumer price index data.
"""

from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.db import get_database


class IndeksHargaKonsumenRepository:
    """Repository for consumer price index data operations."""

    COLLECTION_NAME = "indeks_harga_konsumen"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def find_all(
        self,
        filters: Optional[Dict] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Dict], int]:
        """Find all consumer price index records with filters and pagination."""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def find_by_province(
        self, province_id: str, skip: int = 0, limit: int = 100
    ) -> tuple[List[Dict], int]:
        """Find all consumer price index records for a province."""
        query = {"province_id": province_id}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("tahun", -1)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def find_by_year(
        self, year: int, skip: int = 0, limit: int = 100
    ) -> tuple[List[Dict], int]:
        """Find all consumer price index records for a specific year."""
        query = {"tahun": year}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("province_id", 1)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def get_province_name(self, province_id: str) -> Optional[str]:
        """Get province name from provinces collection."""
        try:
            provinces_collection = self.db["provinces"]
            province = await provinces_collection.find_one({"properties.id": province_id})
            if province:
                if "properties" in province and "PROVINSI" in province["properties"]:
                    return province["properties"]["PROVINSI"]
                elif "PROVINSI" in province:
                    return province["PROVINSI"]
            return None
        except Exception as e:
            print(f"Error getting province name: {e}")
            return None
