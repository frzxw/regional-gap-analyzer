"""
Alert models for API request/response.
"""

from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


AlertType = Literal["threshold", "trend", "anomaly", "missing_data"]
AlertSeverity = Literal["low", "medium", "high", "critical"]
AlertStatus = Literal["open", "acknowledged", "resolved"]


class AlertBase(BaseModel):
    """Base alert fields."""

    region_code: str = Field(..., description="Province code")
    alert_type: AlertType = Field(..., description="Type of alert")
    severity: AlertSeverity = Field(..., description="Alert severity level")
    indicator_key: Optional[str] = Field(None, description="Related indicator")
    message: str = Field(..., description="Human-readable alert message")


class AlertCreate(AlertBase):
    """Request model for creating an alert."""

    metadata: Optional[dict] = Field(None, description="Additional context data")


class AlertUpdate(BaseModel):
    """Request model for updating an alert."""

    status: Optional[AlertStatus] = None
    notes: Optional[str] = None


class AlertResponse(AlertBase):
    """Response model for an alert."""

    id: str
    status: AlertStatus = "open"
    metadata: Optional[dict] = None
    notes: Optional[str] = None
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AlertSummary(BaseModel):
    """Summary of alerts for dashboard."""

    total: int
    by_severity: dict  # {severity: count}
    by_status: dict  # {status: count}
    by_type: dict  # {type: count}


class AlertFilter(BaseModel):
    """Filter parameters for alert queries."""

    region_code: Optional[str] = None
    alert_type: Optional[AlertType] = None
    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    indicator_key: Optional[str] = None


class AlertAcknowledge(BaseModel):
    """Request to acknowledge an alert."""

    notes: Optional[str] = Field(None, description="Acknowledgement notes")


class AlertResolve(BaseModel):
    """Request to resolve an alert."""

    resolution_notes: str = Field(..., description="Resolution description")


class AlertBulkAction(BaseModel):
    """Bulk action on multiple alerts."""

    alert_ids: List[str]
    action: Literal["acknowledge", "resolve"]
    notes: Optional[str] = None


class GenerateAlertsRequest(BaseModel):
    """Request to generate alerts based on current data."""

    year: Optional[int] = Field(None, description="Year to check (latest if None)")
    region_codes: Optional[List[str]] = Field(None, description="Specific regions")
    alert_types: Optional[List[AlertType]] = Field(
        None, description="Types to generate"
    )


class GenerateAlertsResponse(BaseModel):
    """Response from alert generation."""

    alerts_created: int
    alerts_by_severity: dict
    regions_affected: int
