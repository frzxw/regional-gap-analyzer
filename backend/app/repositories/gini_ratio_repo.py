"""
Gini Ratio repository - Data access for gini ratio data.
"""

from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.db import get_database


class GiniRatioRepository:
    """Repository for gini ratio data operations."""

    COLLECTION_NAME = "gini_ratio"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def find_all(
        self,
        filters: Optional[Dict] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Dict], int]:
        """Find all gini ratio records with filters and pagination."""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def find_by_province(
        self, province_id: str, skip: int = 0, limit: int = 100
    ) -> tuple[List[Dict], int]:
        """Find all gini ratio records for a province."""
        query = {"province_id": province_id}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("tahun", -1)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def find_by_year(
        self, year: int, skip: int = 0, limit: int = 100
    ) -> tuple[List[Dict], int]:
        """Find all gini ratio records for a specific year."""
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

    # CRUD methods for new CRUD router
    async def find_by_province_and_year(
        self, province_id: str, year: int
    ) -> Optional[Dict]:
        """Find single record by province_id and year."""
        query = {"province_id": province_id, "tahun": year}
        record = await self.collection.find_one(query)
        return record

    async def create(self, data: Dict) -> Dict:
        """Create new record."""
        result = await self.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return data

    async def update(self, province_id: str, year: int, data: Dict) -> bool:
        """Update existing record."""
        query = {"province_id": province_id, "tahun": year}
        # Remove fields that shouldn't be updated
        update_data = {k: v for k, v in data.items() if k not in ["province_id", "tahun"]}
        if not update_data:
            return False
        result = await self.collection.update_one(query, {"$set": update_data})
        return result.modified_count > 0

    async def delete(self, province_id: str, year: int) -> bool:
        """Delete record."""
        query = {"province_id": province_id, "tahun": year}
        result = await self.collection.delete_one(query)
        return result.deleted_count > 0
