"""
Service for rata_rata_upah_bersih business logic.
"""

from typing import Optional
from datetime import datetime
from app.repositories.rata_rata_upah_bersih_repo import get_rata_rata_upah_bersih_repository
from app.models.rata_rata_upah_bersih_model import RataRataUpahBersihModel


class RataRataUpahBersihService:
    """Service layer for rata_rata_upah_bersih business logic."""

    async def get_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict], int]:
        """Get all rata_rata_upah_bersih records with pagination."""
        skip = (page - 1) * page_size
        repo = await get_rata_rata_upah_bersih_repository()
        return await repo.find_all(skip=skip, limit=page_size)

    async def get_by_province_and_year(
        self, province_id: str, tahun: int
    ) -> Optional[dict]:
        """Get rata_rata_upah_bersih data by province and year."""
        repo = await get_rata_rata_upah_bersih_repository()
        return await repo.find_by_province_and_year(province_id, tahun)

    async def get_by_province(self, province_id: str) -> list[dict]:
        """Get all rata_rata_upah_bersih data for a province."""
        repo = await get_rata_rata_upah_bersih_repository()
        return await repo.find_by_province(province_id)

    async def create(self, data_dict: dict) -> str:
        """Create new rata_rata_upah_bersih record."""
        data = RataRataUpahBersihModel(**data_dict)
        repo = await get_rata_rata_upah_bersih_repository()
        return await repo.create(data)

    async def update(
        self, province_id: str, tahun: int, update_data: dict
    ) -> bool:
        """Update rata_rata_upah_bersih record."""
        update_data["updated_at"] = datetime.utcnow()
        repo = await get_rata_rata_upah_bersih_repository()
        return await repo.update(province_id, tahun, update_data)

    async def delete(self, province_id: str, tahun: int) -> bool:
        """Delete rata_rata_upah_bersih record."""
        repo = await get_rata_rata_upah_bersih_repository()
        return await repo.delete(province_id, tahun)


rata_rata_upah_bersih_service = RataRataUpahBersihService()
