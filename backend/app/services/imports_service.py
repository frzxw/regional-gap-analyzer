"""
Imports service - Business logic for data import operations.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime

from app.repositories import (
    get_indicators_repository,
    get_sources_repository,
)
from app.common import ValidationError
from app.common.time import utc_now
from app.logging import get_logger

logger = get_logger(__name__)


class ImportBatch:
    """Represents a batch import operation."""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.started_at = utc_now()
        self.records_processed = 0
        self.records_created = 0
        self.records_updated = 0
        self.records_failed = 0
        self.errors: List[Dict] = []
        self.status = "in_progress"

    def to_dict(self) -> Dict:
        return {
            "source_name": self.source_name,
            "started_at": self.started_at,
            "records_processed": self.records_processed,
            "records_created": self.records_created,
            "records_updated": self.records_updated,
            "records_failed": self.records_failed,
            "errors": self.errors[:100],  # Limit errors
            "status": self.status,
        }


class ImportsService:
    """Service layer for data import operations."""

    async def import_indicators(
        self,
        indicators: List[Dict],
        source_name: str,
        source_id: Optional[str] = None,
        upsert: bool = True,
    ) -> Dict:
        """
        Import a batch of indicators.

        Args:
            indicators: List of indicator data
            source_name: Name of the data source
            source_id: Optional source document ID
            upsert: If True, update existing records

        Returns:
            Import summary
        """
        batch = ImportBatch(source_name)
        logger.info(f"Starting import batch: {source_name} ({len(indicators)} records)")

        repo = await get_indicators_repository()

        for idx, indicator in enumerate(indicators):
            batch.records_processed += 1
            try:
                # Validate
                self._validate_indicator(indicator)

                # Add source reference
                if source_id:
                    indicator["source_id"] = source_id

                # Create record
                await repo.create(indicator)
                batch.records_created += 1

            except Exception as e:
                batch.records_failed += 1
                batch.errors.append({
                    "row": idx,
                    "error": str(e),
                    "data": indicator,
                })
                logger.warning(f"Import error at row {idx}: {e}")

        batch.status = "completed" if batch.records_failed == 0 else "completed_with_errors"
        logger.info(
            f"Import complete: {batch.records_created} created, "
            f"{batch.records_failed} failed"
        )

        return batch.to_dict()

    async def create_source_and_import(
        self,
        source_data: Dict,
        indicators: List[Dict],
    ) -> Dict:
        """Create a source record and import indicators."""
        sources_repo = await get_sources_repository()

        # Create source record
        source_id = await sources_repo.create(source_data)
        logger.info(f"Created source: {source_id}")

        # Import indicators
        result = await self.import_indicators(
            indicators=indicators,
            source_name=source_data["name"],
            source_id=source_id,
        )

        result["source_id"] = source_id
        return result

    async def rollback_import(self, source_id: str) -> Dict:
        """
        Rollback an import by deleting all indicators from a source.

        Args:
            source_id: Source document ID

        Returns:
            Rollback summary
        """
        logger.info(f"Rolling back import for source: {source_id}")

        indicators_repo = await get_indicators_repository()
        deleted_count = await indicators_repo.delete_by_source(source_id)

        sources_repo = await get_sources_repository()
        await sources_repo.delete(source_id)

        logger.info(f"Rollback complete: {deleted_count} indicators deleted")

        return {
            "source_id": source_id,
            "indicators_deleted": deleted_count,
            "status": "rolled_back",
        }

    def _validate_indicator(self, indicator: Dict) -> None:
        """Validate indicator data for import."""
        required_fields = ["region_code", "indicator_key", "value", "year"]
        for field in required_fields:
            if field not in indicator:
                raise ValidationError(f"Missing required field: {field}")

        if not isinstance(indicator.get("year"), int):
            raise ValidationError("Year must be an integer")

        if indicator.get("value") is None:
            raise ValidationError("Value cannot be None")


# Singleton instance
imports_service = ImportsService()
