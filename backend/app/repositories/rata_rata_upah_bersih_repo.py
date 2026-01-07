"""
Repository for rata_rata_upah_bersih collection.
"""

from typing import Optional
from app.db.client import get_database
from app.models.rata_rata_upah_bersih_model import RataRataUpahBersihModel


class RataRataUpahBersihRepository:
    """Repository for rata_rata_upah_bersih MongoDB operations."""

    def __init__(self):
        self.collection_name = "rata_rata_upah_bersih"

    @property
    async def collection(self):
        """Get the MongoDB collection."""
        db = await get_database()
        return db[self.collection_name]

    async def find_all(self, skip: int = 0, limit: int = 20) -> tuple[list[dict], int]:
        """Get all rata_rata_upah_bersih records with pagination."""
        coll = await self.collection
        cursor = coll.find().skip(skip).limit(limit)
        records = await cursor.to_list(length=limit)
        total = await coll.count_documents({})
        return records, total

    async def find_by_province_and_year(
        self, province_id: str, tahun: int
    ) -> Optional[dict]:
        """Find rata_rata_upah_bersih by province_id and tahun."""
        coll = await self.collection
        return await coll.find_one({"province_id": province_id, "tahun": tahun})

    async def find_by_province(self, province_id: str) -> list[dict]:
        """Find all rata_rata_upah_bersih records for a province."""
        coll = await self.collection
        cursor = coll.find({"province_id": province_id})
        return await cursor.to_list(length=None)

    async def create(self, data: RataRataUpahBersihModel) -> str:
        """Create a new rata_rata_upah_bersih record."""
        coll = await self.collection
        result = await coll.insert_one(data.model_dump())
        return str(result.inserted_id)

    async def update(self, province_id: str, tahun: int, update_data: dict) -> bool:
        """Update rata_rata_upah_bersih by province_id and tahun."""
        coll = await self.collection
        result = await coll.update_one(
            {"province_id": province_id, "tahun": tahun}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete(self, province_id: str, tahun: int) -> bool:
        """Delete rata_rata_upah_bersih by province_id and tahun."""
        coll = await self.collection
        result = await coll.delete_one({"province_id": province_id, "tahun": tahun})
        return result.deleted_count > 0


_repository_instance = None


async def get_rata_rata_upah_bersih_repository() -> RataRataUpahBersihRepository:
    """Get or create repository instance."""
    global _repository_instance
    if _repository_instance is None:
        _repository_instance = RataRataUpahBersihRepository()
    return _repository_instance
