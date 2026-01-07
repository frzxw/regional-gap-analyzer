"""
Repository for angkatan_kerja collection.
"""

from typing import Optional
from app.db.client import get_database
from app.models.angkatan_kerja import AngkatanKerjaModel


class AngkatanKerjaRepository:
    """Repository for angkatan_kerja MongoDB operations."""

    def __init__(self):
        self.collection_name = "angkatan_kerja"

    @property
    async def collection(self):
        """Get the MongoDB collection."""
        db = await get_database()
        return db[self.collection_name]

    async def find_all(self, skip: int = 0, limit: int = 20) -> tuple[list[dict], int]:
        """
        Get all angkatan_kerja records with pagination.

        Returns:
            Tuple of (records list, total count)
        """
        coll = await self.collection
        cursor = coll.find().skip(skip).limit(limit)
        records = await cursor.to_list(length=limit)
        total = await coll.count_documents({})
        return records, total

    async def find_by_province_and_year(
        self, province_id: str, tahun: int
    ) -> Optional[dict]:
        """Find angkatan_kerja by province_id and tahun."""
        coll = await self.collection
        return await coll.find_one({"province_id": province_id, "tahun": tahun})

    async def find_by_province(self, province_id: str) -> list[dict]:
        """Find all angkatan_kerja records for a province."""
        coll = await self.collection
        cursor = coll.find({"province_id": province_id})
        return await cursor.to_list(length=None)

    async def create(self, data: AngkatanKerjaModel) -> str:
        """
        Create a new angkatan_kerja record.

        Returns:
            The inserted document ID as string.
        """
        coll = await self.collection
        result = await coll.insert_one(data.model_dump())
        return str(result.inserted_id)

    async def update(self, province_id: str, tahun: int, update_data: dict) -> bool:
        """
        Update angkatan_kerja by province_id and tahun.

        Returns:
            True if document was modified, False otherwise.
        """
        coll = await self.collection
        result = await coll.update_one(
            {"province_id": province_id, "tahun": tahun}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete(self, province_id: str, tahun: int) -> bool:
        """
        Delete angkatan_kerja by province_id and tahun.

        Returns:
            True if document was deleted, False otherwise.
        """
        coll = await self.collection
        result = await coll.delete_one({"province_id": province_id, "tahun": tahun})
        return result.deleted_count > 0


# Singleton instance getter
_repository_instance = None


async def get_angkatan_kerja_repository() -> AngkatanKerjaRepository:
    """Get or create repository instance."""
    global _repository_instance
    if _repository_instance is None:
        _repository_instance = AngkatanKerjaRepository()
    return _repository_instance
