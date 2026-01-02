"""
Indicator models for API request/response.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.common.time import utc_now


class IndicatorBase(BaseModel):
    """Base indicator fields."""

    region_code: str = Field(..., description="Province code (e.g., ID-JK)")
    category: str = Field(
        ..., description="Category: economic, infrastructure, health, education"
    )
    indicator_key: str = Field(..., description="Indicator identifier")
    value: float = Field(..., description="Indicator value")
    unit: str = Field(..., description="Unit of measurement")
    year: int = Field(..., ge=1900, le=2100, description="Data year")


class IndicatorCreate(IndicatorBase):
    """Request model for creating an indicator."""

    source_id: Optional[str] = Field(None, description="Reference to data source")


class IndicatorUpdate(BaseModel):
    """Request model for updating an indicator."""

    value: Optional[float] = None
    unit: Optional[str] = None
    source_id: Optional[str] = None


class IndicatorResponse(IndicatorBase):
    """Response model for an indicator."""

    id: str = Field(..., description="Unique identifier")
    source_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IndicatorBulkCreate(BaseModel):
    """Request model for bulk indicator creation."""

    indicators: List[IndicatorCreate]
    source_id: Optional[str] = None


class IndicatorFilter(BaseModel):
    """Filter parameters for indicator queries."""

    region_code: Optional[str] = None
    category: Optional[str] = None
    indicator_key: Optional[str] = None
    year: Optional[int] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None


class IndicatorTimeSeries(BaseModel):
    """Time series data for a single indicator."""

    indicator_key: str
    region_code: str
    unit: str
    data_points: List[dict]  # [{year: int, value: float}]


class IndicatorComparison(BaseModel):
    """Comparison of an indicator across regions."""

    indicator_key: str
    year: int
    unit: str
    regions: List[dict]  # [{region_code: str, value: float, rank: int}]
