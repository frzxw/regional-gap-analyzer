"""
Service for angkatan_kerja business logic.
"""

from typing import Optional
from datetime import datetime
from app.repositories.angkatan_kerja_repo import get_angkatan_kerja_repository
from app.models.angkatan_kerja import AngkatanKerjaModel


class AngkatanKerjaService:
    """Service layer for angkatan_kerja business logic."""

    async def get_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict], int]:
        """
        Get all angkatan_kerja records with pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Tuple of (records list, total count)
        """
        skip = (page - 1) * page_size
        repo = await get_angkatan_kerja_repository()
        return await repo.find_all(skip=skip, limit=page_size)

    async def get_by_province_and_year(
        self, province_id: str, tahun: int
    ) -> Optional[dict]:
        """Get angkatan_kerja data by province and year."""
        repo = await get_angkatan_kerja_repository()
        return await repo.find_by_province_and_year(province_id, tahun)

    async def get_by_province(self, province_id: str) -> list[dict]:
        """Get all angkatan_kerja data for a province."""
        repo = await get_angkatan_kerja_repository()
        return await repo.find_by_province(province_id)

    async def create(self, data_dict: dict) -> str:
        """
        Create new angkatan_kerja record.

        Args:
            data_dict: Data dictionary

        Returns:
            Created record ID
        """
        data = AngkatanKerjaModel(**data_dict)
        repo = await get_angkatan_kerja_repository()
        return await repo.create(data)

    async def update(
        self, province_id: str, tahun: int, update_data: dict
    ) -> bool:
        """Update angkatan_kerja record."""
        update_data["updated_at"] = datetime.utcnow()
        repo = await get_angkatan_kerja_repository()
        return await repo.update(province_id, tahun, update_data)

    async def delete(self, province_id: str, tahun: int) -> bool:
        """Delete angkatan_kerja record."""
        repo = await get_angkatan_kerja_repository()
        return await repo.delete(province_id, tahun)


# Singleton instance
angkatan_kerja_service = AngkatanKerjaService()
