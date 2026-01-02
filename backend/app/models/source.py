"""
Source models for tracking data provenance.
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


class SourceBase(BaseModel):
    """Base source fields."""

    name: str = Field(..., description="Source name (e.g., 'BPS SUSENAS 2024')")
    url: Optional[str] = Field(None, description="Download URL")
    description: Optional[str] = Field(None, description="Source description")


class SourceCreate(SourceBase):
    """Request model for creating a source."""

    download_date: date = Field(..., description="Date data was downloaded")
    coverage_years: List[int] = Field(..., description="Years covered")
    indicators: List[str] = Field(..., description="Indicator keys from source")
    notes: Optional[str] = None


class SourceUpdate(BaseModel):
    """Request model for updating a source."""

    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class SourceResponse(SourceBase):
    """Response model for a source."""

    id: str
    download_date: date
    coverage_years: List[int]
    indicators: List[str]
    notes: Optional[str] = None
    record_count: Optional[int] = Field(
        None, description="Number of records from this source"
    )
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SourceSummary(BaseModel):
    """Lightweight source summary."""

    id: str
    name: str
    download_date: date
    indicator_count: int
    coverage_years: List[int]
