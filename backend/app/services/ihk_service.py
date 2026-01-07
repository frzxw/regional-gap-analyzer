"""
Service for indeks_harga_konsumen business logic.
"""

from typing import Optional
from datetime import datetime
from app.repositories.ihk_repo import get_ihk_repository
from app.models.ihk_model import IndeksHargaKonsumenModel


class IHKService:
    """Service layer for indeks_harga_konsumen business logic."""

    async def get_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict], int]:
        """Get all IHK records with pagination."""
        skip = (page - 1) * page_size
        repo = await get_ihk_repository()
        return await repo.find_all(skip=skip, limit=page_size)

    async def get_by_province_and_year(
        self, province_id: str, tahun: int
    ) -> Optional[dict]:
        """Get IHK data by province and year."""
        repo = await get_ihk_repository()
        return await repo.find_by_province_and_year(province_id, tahun)

    async def get_by_province(self, province_id: str) -> list[dict]:
        """Get all IHK data for a province."""
        repo = await get_ihk_repository()
        return await repo.find_by_province(province_id)

    async def create(self, data_dict: dict) -> str:
        """Create new IHK record."""
        data = IndeksHargaKonsumenModel(**data_dict)
        repo = await get_ihk_repository()
        return await repo.create(data)

    async def update(
        self, province_id: str, tahun: int, update_data: dict
    ) -> bool:
        """Update IHK record."""
        update_data["updated_at"] = datetime.utcnow()
        repo = await get_ihk_repository()
        return await repo.update(province_id, tahun, update_data)

    async def delete(self, province_id: str, tahun: int) -> bool:
        """Delete IHK record."""
        repo = await get_ihk_repository()
        return await repo.delete(province_id, tahun)


ihk_service = IHKService()
