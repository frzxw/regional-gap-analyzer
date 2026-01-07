"""
Models for unemployment rate analysis, scoring, and alerts.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class SeverityLevel(str, Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TrendDirection(str, Enum):
    """Trend direction indicators."""
    IMPROVING = "improving"  # Pengangguran menurun
    STABLE = "stable"
    WORSENING = "worsening"  # Pengangguran meningkat


class UnemploymentScore(BaseModel):
    """Scoring model for unemployment rate."""
    
    rate: float = Field(..., description="Unemployment rate percentage")
    score: int = Field(..., ge=0, le=100, description="Score 0-100 (higher is better)")
    category: str = Field(..., description="Category: Excellent/Good/Fair/Poor/Critical")
    severity: SeverityLevel = Field(..., description="Severity level")
    
    class Config:
        use_enum_values = True


class TrendAnalysis(BaseModel):
    """Trend analysis between years."""
    
    year_from: int
    year_to: int
    rate_from: float
    rate_to: float
    change_absolute: float = Field(..., description="Absolute change in percentage points")
    change_percentage: float = Field(..., description="Percentage change")
    direction: TrendDirection
    is_significant: bool = Field(..., description="Whether change is significant (>0.5 percentage points)")
    
    class Config:
        use_enum_values = True


class Alert(BaseModel):
    """Alert for problematic regions."""
    
    type: str = Field(..., description="Alert type")
    severity: SeverityLevel
    message: str = Field(..., description="Alert message")
    recommendation: Optional[str] = Field(None, description="Recommended action")
    
    class Config:
        use_enum_values = True


class ProvinceAnalysis(BaseModel):
    """Complete analysis for a province."""
    
    province_id: str
    province_name: str
    year: int
    unemployment_rate: float
    score: UnemploymentScore
    trend: Optional[TrendAnalysis] = None
    alerts: List[Alert] = []
    rank: Optional[int] = Field(None, description="Ranking among all provinces (1 is best)")
    percentile: Optional[float] = Field(None, description="Percentile ranking")


class RegionalGapAnalysis(BaseModel):
    """Regional inequality analysis response."""
    
    year: int
    national_average: float
    provinces: List[ProvinceAnalysis]
    total_provinces: int
    critical_provinces: int = Field(..., description="Number of provinces with critical unemployment")
    high_risk_provinces: int = Field(..., description="Number of provinces with high unemployment")
    gap_index: float = Field(..., description="Inequality gap index (0-1, higher means more inequality)")
    summary: str = Field(..., description="Summary of findings")
    status: str = "success"


class ComparisonAnalysis(BaseModel):
    """Year-over-year comparison analysis."""
    
    year_from: int
    year_to: int
    provinces_improved: int
    provinces_worsened: int
    provinces_stable: int
    biggest_improvement: Optional[ProvinceAnalysis] = None
    biggest_decline: Optional[ProvinceAnalysis] = None
    status: str = "success"
