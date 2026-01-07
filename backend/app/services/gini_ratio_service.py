"""
Gini Ratio service - Business logic for gini ratio operations.
"""

from typing import Optional, List, Dict

from app.repositories.gini_ratio_repo import GiniRatioRepository
from app.db import get_database
from app.common.errors import NotFoundError


class GiniRatioService:
    """Service layer for gini ratio business logic."""

    async def _enrich_with_province_name(self, record: Dict) -> Dict:
        """Enrich record with province name from provinces collection."""
        db = await get_database()
        repo = GiniRatioRepository(db)
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

    async def get_all_gini_ratio(
        self,
        province_id: Optional[str] = None,
        year: Optional[int] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[List[Dict], int]:
        """
        Get all gini ratio records with optional filters.
        
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
        repo = GiniRatioRepository(db)
        items, total = await repo.find_all(filters=filters, skip=skip, limit=limit)
        items = await self._enrich_records_with_province_names(items)
        return items, total

    async def get_gini_ratio_by_province(
        self, province_id: str, skip: int = 0, limit: int = 50
    ) -> tuple[List[Dict], int]:
        """
        Get all gini ratio records for a province.
        
        Args:
            province_id: Province code
            skip: Number of records to skip
            limit: Number of records to return
            
        Returns:
            Tuple of (records, total_count)
        """
        db = await get_database()
        repo = GiniRatioRepository(db)
        items, total = await repo.find_by_province(province_id, skip=skip, limit=limit)
        items = await self._enrich_records_with_province_names(items)
        return items, total

    async def get_gini_ratio_by_year(
        self, year: int, skip: int = 0, limit: int = 50
    ) -> tuple[List[Dict], int]:
        """
        Get all gini ratio records for a specific year.
        
        Args:
            year: Year
            skip: Number of records to skip
            limit: Number of records to return
            
        Returns:
            Tuple of (records, total_count)
        """
        db = await get_database()
        repo = GiniRatioRepository(db)
        items, total = await repo.find_by_year(year, skip=skip, limit=limit)
        items = await self._enrich_records_with_province_names(items)
        return items, total

    # CRUD methods for new CRUD router
    async def get_by_province_and_year(
        self, province_id: str, year: int
    ) -> Optional[Dict]:
        """Get single record by province_id and year."""
        db = await get_database()
        repo = GiniRatioRepository(db)
        record = await repo.find_by_province_and_year(province_id, year)
        if record:
            record = await self._enrich_with_province_name(record)
        return record

    async def create(self, data: Dict) -> Dict:
        """Create new record."""
        db = await get_database()
        repo = GiniRatioRepository(db)
        result = await repo.create(data)
        return result

    async def update(self, province_id: str, year: int, data: Dict) -> bool:
        """Update existing record."""
        db = await get_database()
        repo = GiniRatioRepository(db)
        success = await repo.update(province_id, year, data)
        return success

    async def delete(self, province_id: str, year: int) -> bool:
        """Delete record."""
        db = await get_database()
        repo = GiniRatioRepository(db)
        success = await repo.delete(province_id, year)
        return success

    async def list_all(
        self, tahun: Optional[int] = None, page: int = 1, page_size: int = 50
    ) -> List[Dict]:
        """List all records with optional year filter."""
        skip = (page - 1) * page_size
        items, _ = await self.get_all_gini_ratio(year=tahun, skip=skip, limit=page_size)
        return items

    async def count(self, tahun: Optional[int] = None) -> int:
        """Count records with optional year filter."""
        _, total = await self.get_all_gini_ratio(year=tahun, skip=0, limit=1)
        return total


# Singleton instance for dependency injection
gini_ratio_service = GiniRatioService()
