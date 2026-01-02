"""
Alerts repository - Data access for alerts.
"""

from typing import Optional, List, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.db import get_database
from app.common.time import utc_now


class AlertsRepository:
    """Repository for alert data operations."""

    COLLECTION_NAME = "alerts"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def find_all(
        self,
        filters: Optional[Dict] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Dict], int]:
        """Find alerts with filters and pagination."""
        query = filters or {}
        cursor = (
            self.collection.find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return items, total

    async def find_by_id(self, alert_id: str) -> Optional[Dict]:
        """Find alert by ID."""
        return await self.collection.find_one({"_id": ObjectId(alert_id)})

    async def find_by_region(
        self, region_code: str, status: Optional[str] = None
    ) -> List[Dict]:
        """Find alerts for a specific region."""
        query = {"region_code": region_code}
        if status:
            query["status"] = status
        cursor = self.collection.find(query).sort("created_at", -1)
        return await cursor.to_list(length=100)

    async def find_open_alerts(self, limit: int = 50) -> List[Dict]:
        """Find all open alerts."""
        cursor = (
            self.collection.find({"status": "open"})
            .sort([("severity", -1), ("created_at", -1)])
            .limit(limit)
        )
        return await cursor.to_list(length=limit)

    async def create(self, alert_data: Dict) -> str:
        """Create a new alert."""
        alert_data["created_at"] = utc_now()
        alert_data["status"] = "open"
        result = await self.collection.insert_one(alert_data)
        return str(result.inserted_id)

    async def create_many(self, alerts: List[Dict]) -> List[str]:
        """Bulk create alerts."""
        now = utc_now()
        for alert in alerts:
            alert["created_at"] = now
            alert["status"] = "open"
        result = await self.collection.insert_many(alerts)
        return [str(id) for id in result.inserted_ids]

    async def acknowledge(self, alert_id: str, notes: Optional[str] = None) -> bool:
        """Acknowledge an alert."""
        result = await self.collection.update_one(
            {"_id": ObjectId(alert_id)},
            {"$set": {
                "status": "acknowledged",
                "acknowledged_at": utc_now(),
                "notes": notes,
            }},
        )
        return result.modified_count > 0

    async def resolve(self, alert_id: str, notes: str) -> bool:
        """Resolve an alert."""
        result = await self.collection.update_one(
            {"_id": ObjectId(alert_id)},
            {"$set": {
                "status": "resolved",
                "resolved_at": utc_now(),
                "resolution_notes": notes,
            }},
        )
        return result.modified_count > 0

    async def get_summary(self) -> Dict:
        """Get alert summary statistics."""
        pipeline = [
            {"$group": {
                "_id": None,
                "total": {"$sum": 1},
                "by_severity": {"$push": "$severity"},
                "by_status": {"$push": "$status"},
                "by_type": {"$push": "$alert_type"},
            }},
        ]
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        if not result:
            return {"total": 0, "by_severity": {}, "by_status": {}, "by_type": {}}

        data = result[0]
        return {
            "total": data["total"],
            "by_severity": self._count_values(data["by_severity"]),
            "by_status": self._count_values(data["by_status"]),
            "by_type": self._count_values(data["by_type"]),
        }

    @staticmethod
    def _count_values(values: List[str]) -> Dict[str, int]:
        """Count occurrences of each value."""
        counts = {}
        for v in values:
            counts[v] = counts.get(v, 0) + 1
        return counts


async def get_alerts_repository() -> AlertsRepository:
    """Factory function to get repository instance."""
    db = await get_database()
    return AlertsRepository(db)
