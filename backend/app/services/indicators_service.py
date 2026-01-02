"""
Indicators service - Business logic for indicator operations.
"""

from typing import Optional, List, Dict

from app.repositories import get_indicators_repository
from app.common import NotFoundError, ValidationError


class IndicatorsService:
    """Service layer for indicator business logic."""

    VALID_CATEGORIES = ["economic", "infrastructure", "health", "education"]

    async def get_all_indicators(
        self,
        filters: Optional[Dict] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[List[Dict], int]:
        """Get all indicators with filters and pagination."""
        skip = (page - 1) * page_size
        repo = await get_indicators_repository()
        return await repo.find_all(filters=filters, skip=skip, limit=page_size)

    async def get_indicator_by_id(self, indicator_id: str) -> Dict:
        """Get a single indicator by ID."""
        repo = await get_indicators_repository()
        indicator = await repo.find_by_id(indicator_id)
        if not indicator:
            raise NotFoundError("Indicator", indicator_id)
        return indicator

    async def get_indicators_for_region(
        self, region_code: str, year: int
    ) -> List[Dict]:
        """Get all indicators for a region and year."""
        repo = await get_indicators_repository()
        return await repo.find_by_region_and_year(region_code, year)

    async def create_indicator(self, indicator_data: Dict) -> str:
        """Create a new indicator."""
        self._validate_indicator(indicator_data)
        repo = await get_indicators_repository()
        return await repo.create(indicator_data)

    async def create_indicators_bulk(self, indicators: List[Dict]) -> List[str]:
        """Bulk create indicators."""
        for ind in indicators:
            self._validate_indicator(ind)
        repo = await get_indicators_repository()
        return await repo.create_many(indicators)

    async def update_indicator(
        self, indicator_id: str, update_data: Dict
    ) -> bool:
        """Update an indicator."""
        repo = await get_indicators_repository()
        existing = await repo.find_by_id(indicator_id)
        if not existing:
            raise NotFoundError("Indicator", indicator_id)
        return await repo.update(indicator_id, update_data)

    async def delete_indicator(self, indicator_id: str) -> bool:
        """Delete an indicator."""
        repo = await get_indicators_repository()
        deleted = await repo.delete(indicator_id)
        if not deleted:
            raise NotFoundError("Indicator", indicator_id)
        return True

    async def get_available_years(self) -> List[int]:
        """Get years with indicator data."""
        repo = await get_indicators_repository()
        return await repo.get_available_years()

    async def get_time_series(
        self, region_code: str, indicator_key: str
    ) -> List[Dict]:
        """Get time series for an indicator in a region."""
        repo = await get_indicators_repository()
        # TODO: Implement time series query
        return []

    def _validate_indicator(self, data: Dict) -> None:
        """Validate indicator data."""
        if data.get("category") not in self.VALID_CATEGORIES:
            raise ValidationError(
                f"Invalid category. Must be one of: {self.VALID_CATEGORIES}",
                field="category",
            )
        if data.get("value") is None:
            raise ValidationError("Value is required", field="value")


# Singleton instance
indicators_service = IndicatorsService()
