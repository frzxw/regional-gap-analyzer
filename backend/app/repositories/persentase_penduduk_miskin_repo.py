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
