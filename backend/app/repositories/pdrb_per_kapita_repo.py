"""
Repository for pdrb_per_kapita collection.
"""

from typing import Optional
from app.db.client import get_database
from app.models.pdrb_per_kapita_model import PDRBPerKapitaModel


class PDRBPerKapitaRepository:
    """Repository for pdrb_per_kapita MongoDB operations."""

    def __init__(self):
        self.collection_name = "pdrb_per_kapita"

    @property
    async def collection(self):
        """Get the MongoDB collection."""
        db = await get_database()
        return db[self.collection_name]

    async def find_all(self, skip: int = 0, limit: int = 20) -> tuple[list[dict], int]:
        """Get all pdrb_per_kapita records with pagination."""
        coll = await self.collection
        cursor = coll.find().skip(skip).limit(limit)
        records = await cursor.to_list(length=limit)
        total = await coll.count_documents({})
        return records, total

    async def find_by_province_year_indikator(
        self, province_id: str, tahun: int, indikator: str
    ) -> Optional[dict]:
        """Find pdrb_per_kapita by province_id, tahun, and indikator."""
        coll = await self.collection
        return await coll.find_one({"province_id": province_id, "tahun": tahun, "indikator": indikator})

    async def find_by_province(self, province_id: str) -> list[dict]:
        """Find all pdrb_per_kapita records for a province."""
        coll = await self.collection
        cursor = coll.find({"province_id": province_id})
        return await cursor.to_list(length=None)

    async def create(self, data: PDRBPerKapitaModel) -> str:
        """Create a new pdrb_per_kapita record."""
        coll = await self.collection
        result = await coll.insert_one(data.model_dump())
        return str(result.inserted_id)

    async def update(self, province_id: str, tahun: int, indikator: str, update_data: dict) -> bool:
        """Update pdrb_per_kapita by province_id, tahun, and indikator."""
        coll = await self.collection
        result = await coll.update_one(
            {"province_id": province_id, "tahun": tahun, "indikator": indikator}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete(self, province_id: str, tahun: int, indikator: str) -> bool:
        """Delete pdrb_per_kapita by province_id, tahun, and indikator."""
        coll = await self.collection
        result = await coll.delete_one({"province_id": province_id, "tahun": tahun, "indikator": indikator})
        return result.deleted_count > 0


_repository_instance = None


async def get_pdrb_per_kapita_repository() -> PDRBPerKapitaRepository:
    """Get or create repository instance."""
    global _repository_instance
    if _repository_instance is None:
        _repository_instance = PDRBPerKapitaRepository()
    return _repository_instance
