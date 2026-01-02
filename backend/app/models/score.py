"""
Score models for API request/response.
"""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class ScoreBase(BaseModel):
    """Base score fields."""

    region_code: str = Field(..., description="Province code")
    year: int = Field(..., ge=1900, le=2100, description="Scoring year")


class CategoryScores(BaseModel):
    """Scores by category."""

    economic: Optional[float] = Field(None, ge=0, le=100)
    infrastructure: Optional[float] = Field(None, ge=0, le=100)
    health: Optional[float] = Field(None, ge=0, le=100)
    education: Optional[float] = Field(None, ge=0, le=100)


class ScoreCreate(ScoreBase):
    """Request model for creating a score (internal use)."""

    economic_score: Optional[float] = Field(None, ge=0, le=100)
    infrastructure_score: Optional[float] = Field(None, ge=0, le=100)
    health_score: Optional[float] = Field(None, ge=0, le=100)
    education_score: Optional[float] = Field(None, ge=0, le=100)
    composite_score: Optional[float] = Field(None, ge=0, le=100)


class ScoreResponse(ScoreBase):
    """Response model for a score."""

    id: str
    economic_score: Optional[float] = None
    infrastructure_score: Optional[float] = None
    health_score: Optional[float] = None
    education_score: Optional[float] = None
    composite_score: Optional[float] = None
    rank: Optional[int] = None
    rank_delta: Optional[int] = Field(
        None, description="Change from previous period (positive = improved)"
    )
    computed_at: datetime

    class Config:
        from_attributes = True


class ScoreSummary(BaseModel):
    """Summary score for a region (lightweight)."""

    region_code: str
    region_name: str
    year: int
    composite_score: float
    rank: int
    rank_delta: Optional[int] = None


class ScoreRanking(BaseModel):
    """Ranking list response."""

    year: int
    rankings: List[ScoreSummary]
    total_regions: int


class ScoreComparison(BaseModel):
    """Side-by-side score comparison."""

    year: int
    regions: List[ScoreResponse]


class ScoreTrend(BaseModel):
    """Score trend over time for a region."""

    region_code: str
    region_name: str
    data_points: List[Dict]  # [{year, composite_score, rank}]


class ScoreDrivers(BaseModel):
    """Score breakdown showing contributing factors."""

    region_code: str
    year: int
    composite_score: float
    category_contributions: Dict[str, float]  # category -> weighted contribution
    top_indicators: List[Dict]  # [{indicator_key, score, weight, contribution}]
    bottom_indicators: List[Dict]


class RecomputeRequest(BaseModel):
    """Request to recompute scores."""

    year: Optional[int] = Field(None, description="Year to recompute (all if None)")
    region_codes: Optional[List[str]] = Field(
        None, description="Specific regions (all if None)"
    )
    force: bool = Field(
        default=False, description="Force recompute even if no changes"
    )


class RecomputeResponse(BaseModel):
    """Response from recompute operation."""

    status: str
    regions_updated: int
    year: Optional[int]
    computed_at: datetime
