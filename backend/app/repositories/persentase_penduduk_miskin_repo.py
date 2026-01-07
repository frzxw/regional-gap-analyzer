"""
Repository for persentase_penduduk_miskin (Poverty Rate) collection.
"""

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId


class PersentasePendudukMiskinRepository:
    """Data access layer for poverty rate data."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize repository with database connection.
        
        Args:
            db: AsyncIOMotorDatabase instance
        """
        self.db = db

    async def find_all(self, filters: dict, skip: int = 0, limit: int = 10) -> tuple[list, int]:
        """Find all poverty rate records with optional filters.
        
        Args:
            filters: Dictionary with optional keys: province_id, year
            skip: Number of records to skip (default: 0)
            limit: Maximum records to return (default: 10)
            
        Returns:
            Tuple of (records list, total count)
        """
        collection = self.db["persentase_penduduk_miskin"]
        query = {}

        if "province_id" in filters and filters["province_id"]:
            query["province_id"] = filters["province_id"]

        if "year" in filters and filters["year"]:
            query["tahun"] = filters["year"]

        records = await collection.find(query).skip(skip).limit(limit).to_list(None)
        total = await collection.count_documents(query)

        return records, total

    async def find_by_province(self, province_id: str, skip: int = 0, limit: int = 10) -> tuple[list, int]:
        """Find all records for a specific province.
        
        Args:
            province_id: Province code
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            Tuple of (records list, total count)
        """
        collection = self.db["persentase_penduduk_miskin"]
        query = {"province_id": province_id}

        records = await collection.find(query).skip(skip).limit(limit).to_list(None)
        total = await collection.count_documents(query)

        return records, total

    async def find_by_year(self, year: int, skip: int = 0, limit: int = 10) -> tuple[list, int]:
        """Find all records for a specific year.
        
        Args:
            year: Year of data
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            Tuple of (records list, total count)
        """
        collection = self.db["persentase_penduduk_miskin"]
        query = {"tahun": year}

        records = await collection.find(query).skip(skip).limit(limit).to_list(None)
        total = await collection.count_documents(query)

        return records, total

    async def get_province_name(self, province_id: str) -> Optional[str]:
        """Get province name from provinces collection.
        
        Args:
            province_id: Province code
            
        Returns:
            Province name if found, None otherwise
        """
        provinces_collection = self.db["provinces"]
        province = await provinces_collection.find_one({"properties.id": province_id})

        if province:
            if "properties" in province and "PROVINSI" in province["properties"]:
                return province["properties"]["PROVINSI"]

        return None

    # CRUD methods for new CRUD router
    async def find_by_province_and_year(self, province_id: str, year: int):
        """Find single record by province_id and year."""
        collection = self.db["persentase_penduduk_miskin"]
        query = {"province_id": province_id, "tahun": year}
        return await collection.find_one(query)

    async def create(self, data: dict):
        """Create new record."""
        collection = self.db["persentase_penduduk_miskin"]
        result = await collection.insert_one(data)
        data["_id"] = result.inserted_id
        return data

    async def update(self, province_id: str, year: int, data: dict) -> bool:
        """Update existing record."""
        collection = self.db["persentase_penduduk_miskin"]
        query = {"province_id": province_id, "tahun": year}
        update_data = {k: v for k, v in data.items() if k not in ["province_id", "tahun"]}
        if not update_data:
            return False
        result = await collection.update_one(query, {"$set": update_data})
        return result.modified_count > 0

    async def delete(self, province_id: str, year: int) -> bool:
        """Delete record."""
        collection = self.db["persentase_penduduk_miskin"]
        query = {"province_id": province_id, "tahun": year}
        result = await collection.delete_one(query)
        return result.deleted_count > 0
