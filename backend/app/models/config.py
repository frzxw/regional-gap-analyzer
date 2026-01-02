"""
Config models for scoring configuration.
"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


class CategoryWeight(BaseModel):
    """Weight for a scoring category."""

    category: str
    weight: float = Field(..., ge=0, le=1, description="Weight (0-1)")
    enabled: bool = True


class IndicatorWeight(BaseModel):
    """Weight for an individual indicator."""

    indicator_key: str
    weight: float = Field(..., ge=0, le=1)
    inverse: bool = Field(
        default=False, description="True if lower values are better"
    )
    enabled: bool = True


class ThresholdConfig(BaseModel):
    """Threshold configuration for alerts."""

    indicator_key: str
    low_threshold: Optional[float] = None
    high_threshold: Optional[float] = None
    severity: str = "medium"


class ScoringConfig(BaseModel):
    """Complete scoring configuration."""

    category_weights: List[CategoryWeight]
    indicator_weights: List[IndicatorWeight]
    missing_data_strategy: str = Field(
        default="exclude",
        description="Strategy: exclude, mean_impute, zero, last_known",
    )
    min_indicators_required: int = Field(
        default=3, description="Minimum indicators to compute score"
    )


class ConfigItem(BaseModel):
    """Generic configuration item."""

    key: str = Field(..., description="Configuration key")
    value: Any = Field(..., description="Configuration value")
    description: Optional[str] = None


class ConfigResponse(ConfigItem):
    """Response model for configuration."""

    updated_at: datetime
    updated_by: Optional[str] = None


class ConfigUpdate(BaseModel):
    """Request model for updating configuration."""

    value: Any
    description: Optional[str] = None


class ScoringConfigResponse(BaseModel):
    """Full scoring configuration response."""

    category_weights: Dict[str, float]
    indicator_weights: Dict[str, Dict[str, Any]]
    thresholds: List[ThresholdConfig]
    missing_data_strategy: str
    updated_at: datetime


class ScoringConfigUpdate(BaseModel):
    """Request to update scoring configuration."""

    category_weights: Optional[Dict[str, float]] = None
    indicator_weights: Optional[Dict[str, Dict[str, Any]]] = None
    thresholds: Optional[List[ThresholdConfig]] = None
    missing_data_strategy: Optional[str] = None
