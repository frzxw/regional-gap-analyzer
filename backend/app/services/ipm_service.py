"""
Service for indeks_pembangunan_manusia business logic.
"""

from typing import Optional
from datetime import datetime
from app.repositories.ipm_repo import get_ipm_repository
from app.models.ipm_model import IndeksPembangunanManusiaModel


class IPMService:
    """Service layer for indeks_pembangunan_manusia business logic."""

    async def get_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict], int]:
        """Get all IPM records with pagination."""
        skip = (page - 1) * page_size
        repo = await get_ipm_repository()
        return await repo.find_all(skip=skip, limit=page_size)

    async def get_by_province_and_year(
        self, province_id: str, tahun: int
    ) -> Optional[dict]:
        """Get IPM data by province and year."""
        repo = await get_ipm_repository()
        return await repo.find_by_province_and_year(province_id, tahun)

    async def get_by_province(self, province_id: str) -> list[dict]:
        """Get all IPM data for a province."""
        repo = await get_ipm_repository()
        return await repo.find_by_province(province_id)

    async def create(self, data_dict: dict) -> str:
        """Create new IPM record."""
        data = IndeksPembangunanManusiaModel(**data_dict)
        repo = await get_ipm_repository()
        return await repo.create(data)

    async def update(
        self, province_id: str, tahun: int, update_data: dict
    ) -> bool:
        """Update IPM record."""
        update_data["updated_at"] = datetime.utcnow()
        repo = await get_ipm_repository()
        return await repo.update(province_id, tahun, update_data)

    async def delete(self, province_id: str, tahun: int) -> bool:
        """Delete IPM record."""
        repo = await get_ipm_repository()
        return await repo.delete(province_id, tahun)


ipm_service = IPMService()
