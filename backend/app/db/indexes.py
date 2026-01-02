"""
Database index definitions.
Creates indexes at application startup.
"""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.logging import get_logger

logger = get_logger(__name__)


async def create_indexes(db: AsyncIOMotorDatabase) -> None:
    """
    Create all required indexes for the database collections.

    Args:
        db: MongoDB database instance
    """
    logger.info("Creating database indexes...")

    # Regions collection
    await db.regions.create_index("code", unique=True)
    await db.regions.create_index("bps_code")
    await db.regions.create_index("name")

    # Indicators collection
    await db.indicators.create_index([
        ("region_code", 1),
        ("indicator_key", 1),
        ("year", -1)
    ])
    await db.indicators.create_index("category")
    await db.indicators.create_index("year")
    await db.indicators.create_index("source_id")

    # Scores collection
    await db.scores.create_index([
        ("region_code", 1),
        ("year", -1)
    ], unique=True)
    await db.scores.create_index("year")
    await db.scores.create_index([("composite_score", -1)])
    await db.scores.create_index("rank")

    # Alerts collection
    await db.alerts.create_index("region_code")
    await db.alerts.create_index("status")
    await db.alerts.create_index("severity")
    await db.alerts.create_index([("created_at", -1)])
    await db.alerts.create_index([
        ("region_code", 1),
        ("status", 1)
    ])

    # Sources collection
    await db.sources.create_index("name")
    await db.sources.create_index("download_date")

    # Configs collection
    await db.configs.create_index("key", unique=True)

    # Import batches collection
    await db.import_batches.create_index([("created_at", -1)])
    await db.import_batches.create_index("status")

    logger.info("Database indexes created successfully")
