"""
Labor Force service - Business logic for labor force operations.
"""

from typing import Optional, List, Dict

from app.repositories.labor_force_repo import LaborForceRepository
from app.db import get_database
from app.common.errors import NotFoundError


class LaborForceService:
    """Service layer for labor force business logic."""

    async def _enrich_with_province_name(self, record: Dict) -> Dict:
        """Enrich record with province name from provinces collection."""
        db = await get_database()
        repo = LaborForceRepository(db)
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

    async def get_all_labor_force(
        self,
        province_id: Optional[str] = None,
        year: Optional[int] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[List[Dict], int]:
        """
        Get all labor force records with optional filters.
        
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
        repo = LaborForceRepository(db)
        items, total = await repo.find_all(filters=filters, skip=skip, limit=limit)
        items = await self._enrich_records_with_province_names(items)
        return items, total

    async def get_labor_force_by_id(self, record_id: str) -> Dict:
        """
        Get a single labor force record by ID.
        
        Args:
            record_id: Document ID
            
        Returns:
            Labor force record
            
        Raises:
            NotFoundError: If record not found
        """
        db = await get_database()
        repo = LaborForceRepository(db)
        record = await repo.find_by_id(record_id)
        if not record:
            raise NotFoundError("Labor Force Record", record_id)
        record = await self._enrich_with_province_name(record)
        return record

    async def get_labor_force_by_province_year(
        self, province_id: str, year: int
    ) -> Dict:
        """
        Get labor force record for specific province and year.
        
        Args:
            province_id: Province code
            year: Year
            
        Returns:
            Labor force record
            
        Raises:
            NotFoundError: If record not found
        """
        db = await get_database()
        repo = LaborForceRepository(db)
        record = await repo.find_by_province_and_year(province_id, year)
        if not record:
            raise NotFoundError(
                "Labor Force Record",
                f"province_id={province_id}, year={year}"
            )
        record = await self._enrich_with_province_name(record)
        return record

    async def get_labor_force_by_province(
        self, province_id: str, skip: int = 0, limit: int = 50
    ) -> tuple[List[Dict], int]:
        """
        Get all labor force records for a province.
        
        Args:
            province_id: Province code
            skip: Number of records to skip
            limit: Number of records to return
            
        Returns:
            Tuple of (records, total_count)
        """
        db = await get_database()
        repo = LaborForceRepository(db)
        items, total = await repo.find_by_province(province_id, skip=skip, limit=limit)
        items = await self._enrich_records_with_province_names(items)
        return items, total

    async def get_labor_force_by_year(
        self, year: int, skip: int = 0, limit: int = 50
    ) -> tuple[List[Dict], int]:
        """
        Get all labor force records for a specific year.
        
        Args:
            year: Year
            skip: Number of records to skip
            limit: Number of records to return
            
        Returns:
            Tuple of (records, total_count)
        """
        db = await get_database()
        repo = LaborForceRepository(db)
        items, total = await repo.find_by_year(year, skip=skip, limit=limit)
        items = await self._enrich_records_with_province_names(items)
        return items, total

    async def get_available_years(self) -> List[int]:
        """
        Get list of years with labor force data.
        
        Returns:
            List of years in descending order
        """
        db = await get_database()
        repo = LaborForceRepository(db)
        return await repo.get_available_years()

    async def get_provinces(self) -> List[str]:
        """
        Get list of provinces with labor force data.
        
        Returns:
            List of province codes in ascending order
        """
        db = await get_database()
        repo = LaborForceRepository(db)
        return await repo.get_provinces()
