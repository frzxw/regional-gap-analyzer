"""
Service layer for persentase_penduduk_miskin (Poverty Rate) data operations.
"""

from typing import Optional
from app.db.client import get_database
from app.models.persentase_penduduk_miskin import PersentasePendudukMiskinRecord
from app.repositories.persentase_penduduk_miskin_repo import PersentasePendudukMiskinRepository


class PersentasePendudukMiskinService:
    """Business logic for poverty rate data operations."""

    async def get_all(self, province_id: Optional[str] = None, year: Optional[int] = None, skip: int = 0, limit: int = 10) -> tuple[list[PersentasePendudukMiskinRecord], int]:
        """Get all poverty rate records with optional filtering.
        
        Args:
            province_id: Optional province code to filter by
            year: Optional year to filter by
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            Tuple of (list of PersentasePendudukMiskinRecord, total count)
        """
        db = await get_database()
        repo = PersentasePendudukMiskinRepository(db)

        filters = {}
        if province_id:
            filters["province_id"] = province_id
        if year:
            filters["year"] = year

        records, total = await repo.find_all(filters, skip, limit)
        enriched_records = await self._enrich_records_with_province_names(records, repo)

        return enriched_records, total

    async def get_by_province(self, province_id: str, skip: int = 0, limit: int = 10) -> tuple[list[PersentasePendudukMiskinRecord], int]:
        """Get all records for a specific province.
        
        Args:
            province_id: Province code
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            Tuple of (list of PersentasePendudukMiskinRecord, total count)
        """
        db = await get_database()
        repo = PersentasePendudukMiskinRepository(db)

        records, total = await repo.find_by_province(province_id, skip, limit)
        enriched_records = await self._enrich_records_with_province_names(records, repo)

        return enriched_records, total

    async def get_by_year(self, year: int, skip: int = 0, limit: int = 10) -> tuple[list[PersentasePendudukMiskinRecord], int]:
        """Get all records for a specific year.
        
        Args:
            year: Year of data
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            Tuple of (list of PersentasePendudukMiskinRecord, total count)
        """
        db = await get_database()
        repo = PersentasePendudukMiskinRepository(db)

        records, total = await repo.find_by_year(year, skip, limit)
        enriched_records = await self._enrich_records_with_province_names(records, repo)

        return enriched_records, total

    async def _enrich_with_province_name(self, record: dict, repo: PersentasePendudukMiskinRepository) -> dict:
        """Add province name to record from provinces collection.
        
        Args:
            record: Raw database record
            repo: PersentasePendudukMiskinRepository instance
            
        Returns:
            Record with province_name added
        """
        province_name = await repo.get_province_name(record.get("province_id", ""))
        record["province_name"] = province_name
        return record

    async def _enrich_records_with_province_names(self, records: list, repo: PersentasePendudukMiskinRepository) -> list[PersentasePendudukMiskinRecord]:
        """Enrich multiple records with province names.
        
        Args:
            records: List of raw database records
            repo: PersentasePendudukMiskinRepository instance
            
        Returns:
            List of PersentasePendudukMiskinRecord models with province names
        """
        enriched = []
        for record in records:
            enriched_record = await self._enrich_with_province_name(record, repo)
            enriched.append(PersentasePendudukMiskinRecord(**enriched_record))

        return enriched

    # CRUD methods for new CRUD router
    async def get_by_province_and_year(self, province_id: str, year: int):
        """Get single record by province_id and year."""
        db = await get_database()
        repo = PersentasePendudukMiskinRepository(db)
        return await repo.find_by_province_and_year(province_id, year)

    async def create(self, data: dict):
        """Create new record."""
        db = await get_database()
        repo = PersentasePendudukMiskinRepository(db)
        return await repo.create(data)

    async def update(self, province_id: str, year: int, data: dict) -> bool:
        """Update existing record."""
        db = await get_database()
        repo = PersentasePendudukMiskinRepository(db)
        return await repo.update(province_id, year, data)

    async def delete(self, province_id: str, year: int) -> bool:
        """Delete record."""
        db = await get_database()
        repo = PersentasePendudukMiskinRepository(db)
        return await repo.delete(province_id, year)


# Singleton instance for dependency injection
persentase_penduduk_miskin_service = PersentasePendudukMiskinService()
