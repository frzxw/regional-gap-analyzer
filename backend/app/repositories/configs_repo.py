"""
Configs repository - Data access for configuration data.
"""

from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db import get_database
from app.common.time import utc_now


class ConfigsRepository:
    """Repository for configuration data operations."""

    COLLECTION_NAME = "configs"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def get(self, key: str) -> Optional[Dict]:
        """Get a configuration value by key."""
        return await self.collection.find_one({"key": key})

    async def get_all(self) -> Dict[str, Any]:
        """Get all configuration values as a dictionary."""
        cursor = self.collection.find()
        configs = await cursor.to_list(length=100)
        return {c["key"]: c["value"] for c in configs}

    async def set(
        self,
        key: str,
        value: Any,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> bool:
        """Set a configuration value."""
        update_data = {
            "key": key,
            "value": value,
            "updated_at": utc_now(),
        }
        if description:
            update_data["description"] = description
        if updated_by:
            update_data["updated_by"] = updated_by

        result = await self.collection.update_one(
            {"key": key},
            {"$set": update_data},
            upsert=True,
        )
        return result.modified_count > 0 or result.upserted_id is not None

    async def delete(self, key: str) -> bool:
        """Delete a configuration value."""
        result = await self.collection.delete_one({"key": key})
        return result.deleted_count > 0

    async def get_scoring_config(self) -> Dict:
        """Get the complete scoring configuration."""
        config = await self.get("scoring_config")
        if config:
            return config["value"]
        # Return default config
        return {
            "category_weights": {
                "economic": 0.30,
                "infrastructure": 0.25,
                "health": 0.25,
                "education": 0.20,
            },
            "missing_data_strategy": "exclude",
            "min_indicators_required": 3,
        }

    async def set_scoring_config(self, config: Dict) -> bool:
        """Set the scoring configuration."""
        return await self.set(
            "scoring_config",
            config,
            description="Scoring weights and strategy configuration",
        )

    async def get_thresholds(self) -> Dict:
        """Get alert threshold configuration."""
        config = await self.get("thresholds")
        return config["value"] if config else {}

    async def set_thresholds(self, thresholds: Dict) -> bool:
        """Set alert threshold configuration."""
        return await self.set(
            "thresholds",
            thresholds,
            description="Alert threshold configuration",
        )


async def get_configs_repository() -> ConfigsRepository:
    """Factory function to get repository instance."""
    db = await get_database()
    return ConfigsRepository(db)
