"""
Indeks Pembangunan Manusia service - Business logic for human development index operations.
"""

from typing import Optional, List, Dict

from app.repositories.indeks_pembangunan_manusia_repo import IndeksPembangunanManusiaRepository
from app.db import get_database
from app.common.errors import NotFoundError


class IndeksPembangunanManusiaService:
    """Service layer for human development index business logic."""

    async def _enrich_with_province_name(self, record: Dict) -> Dict:
        """Enrich record with province name from provinces collection."""
        db = await get_database()
        repo = IndeksPembangunanManusiaRepository(db)
        province_id = record.get("province_id")
        if province_id:
            province_name = await repo.get_province_name(province_id)
            record["province_name"] = province_name
        return record

    async def _enrich_records_with_province_names(self, records: List[Dict]) -> List[Dict]:
        """Enrich multiple records with province names."""
        enriched = []
        for record in records:
            enriched_record = await self._enrich_with_province_name(record)
            enriched.append(enriched_record)
        return enriched

    async def get_all_indeks_pembangunan_manusia(
        self,
        province_id: Optional[str] = None,
        year: Optional[int] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[List[Dict], int]:
        """
        Get all human development index records with optional filters.
        
        Args:
            province_id: Filter by province code
            year: Filter by year
            skip: Number of records to skip
            limit: Number of records to return
            
        Returns:
            Tuple of (records, total_count)
        """
        filters = {}
        if province_id:
            filters["province_id"] = province_id
        if year:
            filters["tahun"] = year

        db = await get_database()
        repo = IndeksPembangunanManusiaRepository(db)
        items, total = await repo.find_all(filters=filters, skip=skip, limit=limit)
        items = await self._enrich_records_with_province_names(items)
        return items, total

    async def get_indeks_pembangunan_manusia_by_province(
        self, province_id: str, skip: int = 0, limit: int = 50
    ) -> tuple[List[Dict], int]:
        """
        Get all human development index records for a province.
        
        Args:
            province_id: Province code
            skip: Number of records to skip
            limit: Number of records to return
            
        Returns:
            Tuple of (records, total_count)
        """
        db = await get_database()
        repo = IndeksPembangunanManusiaRepository(db)
        items, total = await repo.find_by_province(province_id, skip=skip, limit=limit)
        items = await self._enrich_records_with_province_names(items)
        return items, total

    async def get_indeks_pembangunan_manusia_by_year(
        self, year: int, skip: int = 0, limit: int = 50
    ) -> tuple[List[Dict], int]:
        """
        Get all human development index records for a specific year.
        
        Args:
            year: Year
            skip: Number of records to skip
            limit: Number of records to return
            
        Returns:
            Tuple of (records, total_count)
        """
        db = await get_database()
        repo = IndeksPembangunanManusiaRepository(db)
        items, total = await repo.find_by_year(year, skip=skip, limit=limit)
        items = await self._enrich_records_with_province_names(items)
        return items, total
