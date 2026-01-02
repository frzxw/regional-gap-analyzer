"""
Configs router - API endpoints for system configuration.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from app.repositories import get_configs_repository
from app.models import Config

router = APIRouter(prefix="/configs", tags=["Configuration"])


@router.get("/")
async def list_configs():
    """
    List all configuration entries.
    """
    repo = await get_configs_repository()
    configs = await repo.find_all()
    return {"configs": configs}


@router.get("/{key}")
async def get_config(key: str):
    """
    Get a specific configuration value.
    """
    repo = await get_configs_repository()
    config = await repo.find_by_key(key)
    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Config key '{key}' not found",
        )
    return config


@router.put("/{key}")
async def set_config(key: str, config: Config):
    """
    Set or update a configuration value.
    """
    repo = await get_configs_repository()
    result = await repo.upsert(key, config.model_dump())
    return result


@router.delete("/{key}", status_code=204)
async def delete_config(key: str):
    """
    Delete a configuration entry.
    """
    repo = await get_configs_repository()
    deleted = await repo.delete_by_key(key)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Config key '{key}' not found",
        )


# Convenience endpoints for common configs

@router.get("/weights/indicators")
async def get_indicator_weights():
    """
    Get current indicator weights for scoring.
    """
    repo = await get_configs_repository()
    config = await repo.find_by_key("indicator_weights")
    if not config:
        # Return defaults
        return {
            "HDI": 0.25,
            "POVERTY_RATE": 0.20,
            "GRDP_CAPITA": 0.20,
            "GINI": 0.15,
            "UNEMPLOYMENT": 0.10,
            "LITERACY": 0.10,
        }
    return config.get("value", {})


@router.put("/weights/indicators")
async def set_indicator_weights(weights: dict):
    """
    Update indicator weights for scoring.
    """
    # Validate weights sum to 1.0
    total = sum(weights.values())
    if abs(total - 1.0) > 0.01:
        raise HTTPException(
            status_code=400,
            detail=f"Weights must sum to 1.0, got {total}",
        )

    repo = await get_configs_repository()
    result = await repo.upsert("indicator_weights", {
        "key": "indicator_weights",
        "value": weights,
        "description": "Indicator weights for composite score calculation",
    })
    return result


@router.get("/thresholds/alerts")
async def get_alert_thresholds():
    """
    Get alert threshold configuration.
    """
    repo = await get_configs_repository()
    config = await repo.find_by_key("alert_thresholds")
    if not config:
        # Return defaults
        return {
            "critical_score": 30,
            "warning_score": 50,
            "rank_drop_critical": 5,
            "rank_drop_warning": 3,
        }
    return config.get("value", {})


@router.put("/thresholds/alerts")
async def set_alert_thresholds(thresholds: dict):
    """
    Update alert threshold configuration.
    """
    repo = await get_configs_repository()
    result = await repo.upsert("alert_thresholds", {
        "key": "alert_thresholds",
        "value": thresholds,
        "description": "Thresholds for alert generation",
    })
    return result
