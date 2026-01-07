"""
Service for tingkat_pengangguran_terbuka business logic.
"""

from typing import Optional
from datetime import datetime
from app.repositories.tpt_repo import get_tpt_repository
from app.models.tpt_model import TingkatPengangguranTerbukaModel


class TPTService:
    """Service layer for tingkat_pengangguran_terbuka business logic."""

    async def get_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict], int]:
        """Get all TPT records with pagination."""
        skip = (page - 1) * page_size
        repo = await get_tpt_repository()
        return await repo.find_all(skip=skip, limit=page_size)

    async def get_by_province_and_year(
        self, province_id: str, tahun: int
    ) -> Optional[dict]:
        """Get TPT data by province and year."""
        repo = await get_tpt_repository()
        return await repo.find_by_province_and_year(province_id, tahun)

    async def get_by_province(self, province_id: str) -> list[dict]:
        """Get all TPT data for a province."""
        repo = await get_tpt_repository()
        return await repo.find_by_province(province_id)

    async def create(self, data_dict: dict) -> str:
        """Create new TPT record."""
        data = TingkatPengangguranTerbukaModel(**data_dict)
        repo = await get_tpt_repository()
        return await repo.create(data)

    async def update(
        self, province_id: str, tahun: int, update_data: dict
    ) -> bool:
        """Update TPT record."""
        update_data["updated_at"] = datetime.utcnow()
        repo = await get_tpt_repository()
        return await repo.update(province_id, tahun, update_data)

    async def delete(self, province_id: str, tahun: int) -> bool:
        """Delete TPT record."""
        repo = await get_tpt_repository()
        return await repo.delete(province_id, tahun)


tpt_service = TPTService()
