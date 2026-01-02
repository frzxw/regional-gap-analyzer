"""
Alerts service - Business logic for alert operations.
"""

from typing import Optional, List, Dict

from app.repositories import (
    get_alerts_repository,
    get_indicators_repository,
    get_configs_repository,
)
from app.common import NotFoundError
from app.logging import get_logger

logger = get_logger(__name__)


class AlertsService:
    """Service layer for alert business logic."""

    async def get_all_alerts(
        self,
        filters: Optional[Dict] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[List[Dict], int]:
        """Get all alerts with filters and pagination."""
        skip = (page - 1) * page_size
        repo = await get_alerts_repository()
        return await repo.find_all(filters=filters, skip=skip, limit=page_size)

    async def get_alert_by_id(self, alert_id: str) -> Dict:
        """Get a single alert by ID."""
        repo = await get_alerts_repository()
        alert = await repo.find_by_id(alert_id)
        if not alert:
            raise NotFoundError("Alert", alert_id)
        return alert

    async def get_alerts_for_region(
        self, region_code: str, status: Optional[str] = None
    ) -> List[Dict]:
        """Get alerts for a specific region."""
        repo = await get_alerts_repository()
        return await repo.find_by_region(region_code, status)

    async def get_open_alerts(self, limit: int = 50) -> List[Dict]:
        """Get all open alerts, sorted by severity."""
        repo = await get_alerts_repository()
        return await repo.find_open_alerts(limit)

    async def get_alert_summary(self) -> Dict:
        """Get summary statistics for alerts."""
        repo = await get_alerts_repository()
        return await repo.get_summary()

    async def create_alert(self, alert_data: Dict) -> str:
        """Create a new alert."""
        repo = await get_alerts_repository()
        return await repo.create(alert_data)

    async def acknowledge_alert(
        self, alert_id: str, notes: Optional[str] = None
    ) -> bool:
        """Acknowledge an alert."""
        repo = await get_alerts_repository()
        acknowledged = await repo.acknowledge(alert_id, notes)
        if not acknowledged:
            raise NotFoundError("Alert", alert_id)
        return True

    async def resolve_alert(self, alert_id: str, notes: str) -> bool:
        """Resolve an alert."""
        repo = await get_alerts_repository()
        resolved = await repo.resolve(alert_id, notes)
        if not resolved:
            raise NotFoundError("Alert", alert_id)
        return True

    async def generate_alerts(
        self,
        year: Optional[int] = None,
        region_codes: Optional[List[str]] = None,
    ) -> Dict:
        """Generate alerts based on current data and thresholds."""
        logger.info(f"Generating alerts for year={year}, regions={region_codes}")

        configs_repo = await get_configs_repository()
        thresholds = await configs_repo.get_thresholds()

        alerts_to_create = []
        regions_affected = set()

        # TODO: Implement alert generation logic
        # 1. Check threshold violations
        # 2. Check trend anomalies
        # 3. Check missing data
        # 4. Check outliers

        if alerts_to_create:
            repo = await get_alerts_repository()
            await repo.create_many(alerts_to_create)

        return {
            "alerts_created": len(alerts_to_create),
            "alerts_by_severity": {},
            "regions_affected": len(regions_affected),
        }


# Singleton instance
alerts_service = AlertsService()
