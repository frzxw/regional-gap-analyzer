"""
Repository for indeks_pembangunan_manusia collection.
"""

from typing import Optional
from app.db.client import get_database
from app.models.ipm_model import IndeksPembangunanManusiaModel


class IPMRepository:
    """Repository for indeks_pembangunan_manusia MongoDB operations."""

    def __init__(self):
        self.collection_name = "indeks_pembangunan_manusia"

    @property
    async def collection(self):
        """Get the MongoDB collection."""
        db = await get_database()
        return db[self.collection_name]

    async def find_all(self, skip: int = 0, limit: int = 20) -> tuple[list[dict], int]:
        """Get all IPM records with pagination."""
        coll = await self.collection
        cursor = coll.find().skip(skip).limit(limit)
        records = await cursor.to_list(length=limit)
        total = await coll.count_documents({})
        return records, total

    async def find_by_province_and_year(
        self, province_id: str, tahun: int
    ) -> Optional[dict]:
        """Find IPM by province_id and tahun."""
        coll = await self.collection
        return await coll.find_one({"province_id": province_id, "tahun": tahun})

    async def find_by_province(self, province_id: str) -> list[dict]:
        """Find all IPM records for a province."""
        coll = await self.collection
        cursor = coll.find({"province_id": province_id})
        return await cursor.to_list(length=None)

    async def create(self, data: IndeksPembangunanManusiaModel) -> str:
        """Create a new IPM record."""
        coll = await self.collection
        result = await coll.insert_one(data.model_dump())
        return str(result.inserted_id)

    async def update(self, province_id: str, tahun: int, update_data: dict) -> bool:
        """Update IPM by province_id and tahun."""
        coll = await self.collection
        result = await coll.update_one(
            {"province_id": province_id, "tahun": tahun}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete(self, province_id: str, tahun: int) -> bool:
        """Delete IPM by province_id and tahun."""
        coll = await self.collection
        result = await coll.delete_one({"province_id": province_id, "tahun": tahun})
        return result.deleted_count > 0


_repository_instance = None


async def get_ipm_repository() -> IPMRepository:
    """Get or create repository instance."""
    global _repository_instance
    if _repository_instance is None:
        _repository_instance = IPMRepository()
    return _repository_instance
