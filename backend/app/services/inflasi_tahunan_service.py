"""
Service layer for inflasi_tahunan (Annual Inflation) data operations.
"""

from typing import Optional
from app.db.client import get_database
from app.models.inflasi_tahunan import InflasiTahunanRecord
from app.repositories.inflasi_tahunan_repo import InflasiTahunanRepository


class InflasiTahunanService:
    """Business logic for annual inflation data operations."""

    async def get_all(self, province_id: Optional[str] = None, year: Optional[int] = None, skip: int = 0, limit: int = 10) -> tuple[list[InflasiTahunanRecord], int]:
        """Get all annual inflation records with optional filtering.
        
        Args:
            province_id: Optional province code to filter by
            year: Optional year to filter by
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            Tuple of (list of InflasiTahunanRecord, total count)
        """
        db = await get_database()
        repo = InflasiTahunanRepository(db)

        filters = {}
        if province_id:
            filters["province_id"] = province_id
        if year:
            filters["year"] = year

        records, total = await repo.find_all(filters, skip, limit)
        enriched_records = await self._enrich_records_with_province_names(records, repo)

        return enriched_records, total

    async def get_by_province(self, province_id: str, skip: int = 0, limit: int = 10) -> tuple[list[InflasiTahunanRecord], int]:
        """Get all records for a specific province.
        
        Args:
            province_id: Province code
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            Tuple of (list of InflasiTahunanRecord, total count)
        """
        db = await get_database()
        repo = InflasiTahunanRepository(db)

        records, total = await repo.find_by_province(province_id, skip, limit)
        enriched_records = await self._enrich_records_with_province_names(records, repo)

        return enriched_records, total

    async def get_by_year(self, year: int, skip: int = 0, limit: int = 10) -> tuple[list[InflasiTahunanRecord], int]:
        """Get all records for a specific year.
        
        Args:
            year: Year of data
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            Tuple of (list of InflasiTahunanRecord, total count)
        """
        db = await get_database()
        repo = InflasiTahunanRepository(db)

        records, total = await repo.find_by_year(year, skip, limit)
        enriched_records = await self._enrich_records_with_province_names(records, repo)

        return enriched_records, total

    async def _enrich_with_province_name(self, record: dict, repo: InflasiTahunanRepository) -> dict:
        """Add province name to record from provinces collection.
        
        Args:
            record: Raw database record
            repo: InflasiTahunanRepository instance
            
        Returns:
            Record with province_name added
        """
        province_name = await repo.get_province_name(record.get("province_id", ""))
        record["province_name"] = province_name
        return record

    async def _enrich_records_with_province_names(self, records: list, repo: InflasiTahunanRepository) -> list[InflasiTahunanRecord]:
        """Enrich multiple records with province names.
        
        Args:
            records: List of raw database records
            repo: InflasiTahunanRepository instance
            
        Returns:
            List of InflasiTahunanRecord models with province names
        """
        enriched = []
        for record in records:
            enriched_record = await self._enrich_with_province_name(record, repo)
            enriched.append(InflasiTahunanRecord(**enriched_record))

        return enriched
