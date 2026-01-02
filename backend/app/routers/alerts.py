"""
Alerts router - API endpoints for inequality alerts.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Body

from app.services import alerts_service
from app.models import Alert
from app.common.pagination import PaginatedResponse

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/")
async def list_alerts(
    region_code: Optional[str] = Query(None, description="Filter by region"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List alerts with optional filters.
    """
    filters = {}
    if region_code:
        filters["region_code"] = region_code
    if severity:
        filters["severity"] = severity
    if status:
        filters["status"] = status

    alerts, total = await alerts_service.list_alerts(
        filters=filters, skip=skip, limit=limit
    )
    return PaginatedResponse(items=alerts, total=total, skip=skip, limit=limit)


@router.get("/active")
async def get_active_alerts(
    region_code: Optional[str] = None,
    limit: int = Query(20, ge=1, le=50),
):
    """
    Get currently active (unacknowledged) alerts.
    """
    alerts = await alerts_service.get_active_alerts(region_code, limit)
    return {"alerts": alerts, "count": len(alerts)}


@router.get("/summary")
async def get_alerts_summary():
    """
    Get summary of alerts by severity and region.
    """
    summary = await alerts_service.get_alerts_summary()
    return summary


@router.get("/{alert_id}")
async def get_alert(alert_id: str):
    """
    Get a specific alert by ID.
    """
    alert = await alerts_service.get_alert(alert_id)
    if not alert:
        raise HTTPException(
            status_code=404,
            detail=f"Alert {alert_id} not found",
        )
    return alert


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    acknowledged_by: str = Body(..., embed=True),
    notes: Optional[str] = Body(None, embed=True),
):
    """
    Acknowledge an alert.
    """
    result = await alerts_service.acknowledge_alert(
        alert_id, acknowledged_by, notes
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Alert {alert_id} not found",
        )
    return result


@router.post("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: str,
    resolved_by: str = Body(..., embed=True),
    resolution_notes: Optional[str] = Body(None, embed=True),
):
    """
    Mark an alert as resolved.
    """
    result = await alerts_service.resolve_alert(
        alert_id, resolved_by, resolution_notes
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Alert {alert_id} not found",
        )
    return result


@router.post("/generate")
async def generate_alerts(
    year: Optional[int] = Query(None, description="Year to generate alerts for"),
):
    """
    Generate alerts based on current data and thresholds.
    """
    result = await alerts_service.generate_alerts(year)
    return {
        "generated": result.get("created", 0),
        "updated": result.get("updated", 0),
        "message": "Alert generation completed",
    }


@router.delete("/{alert_id}", status_code=204)
async def delete_alert(alert_id: str):
    """
    Delete an alert.
    """
    deleted = await alerts_service.delete_alert(alert_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Alert {alert_id} not found",
        )
