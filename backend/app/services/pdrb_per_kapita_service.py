"""
Service for pdrb_per_kapita business logic.
"""

from typing import Optional
from datetime import datetime
from app.repositories.pdrb_per_kapita_repo import get_pdrb_per_kapita_repository
from app.models.pdrb_per_kapita_model import PDRBPerKapitaModel


class PDRBPerKapitaService:
    """Service layer for pdrb_per_kapita business logic."""

    async def get_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict], int]:
        """Get all pdrb_per_kapita records with pagination."""
        skip = (page - 1) * page_size
        repo = await get_pdrb_per_kapita_repository()
        return await repo.find_all(skip=skip, limit=page_size)

    async def get_by_province_year_indikator(
        self, province_id: str, tahun: int, indikator: str
    ) -> Optional[dict]:
        """Get pdrb_per_kapita data by province, year, and indikator."""
        repo = await get_pdrb_per_kapita_repository()
        return await repo.find_by_province_year_indikator(province_id, tahun, indikator)

    async def get_by_province(self, province_id: str) -> list[dict]:
        """Get all pdrb_per_kapita data for a province."""
        repo = await get_pdrb_per_kapita_repository()
        return await repo.find_by_province(province_id)

    async def create(self, data_dict: dict) -> str:
        """Create new pdrb_per_kapita record."""
        data = PDRBPerKapitaModel(**data_dict)
        repo = await get_pdrb_per_kapita_repository()
        return await repo.create(data)

    async def update(
        self, province_id: str, tahun: int, indikator: str, update_data: dict
    ) -> bool:
        """Update pdrb_per_kapita record."""
        update_data["updated_at"] = datetime.utcnow()
        repo = await get_pdrb_per_kapita_repository()
        return await repo.update(province_id, tahun, indikator, update_data)

    async def delete(self, province_id: str, tahun: int, indikator: str) -> bool:
        """Delete pdrb_per_kapita record."""
        repo = await get_pdrb_per_kapita_repository()
        return await repo.delete(province_id, tahun, indikator)


pdrb_per_kapita_service = PDRBPerKapitaService()
