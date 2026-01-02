"""
Indicators router - API endpoints for indicator data.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query

from app.services import indicators_service
from app.models import IndicatorRecord, IndicatorCreate, IndicatorDefinition
from app.common.pagination import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/indicators", tags=["Indicators"])


@router.get("/", response_model=PaginatedResponse)
async def list_indicators(
    region_code: Optional[str] = Query(None, description="Filter by region"),
    indicator_code: Optional[str] = Query(None, description="Filter by indicator type"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List indicator records with optional filters.
    """
    filters = {}
    if region_code:
        filters["region_code"] = region_code
    if indicator_code:
        filters["indicator_code"] = indicator_code
    if year:
        filters["year"] = year

    items, total = await indicators_service.list_indicators(
        filters=filters, skip=skip, limit=limit
    )
    return PaginatedResponse(
        items=items, total=total, skip=skip, limit=limit
    )


@router.get("/definitions", response_model=List[IndicatorDefinition])
async def list_indicator_definitions():
    """
    Get list of all indicator definitions with metadata.
    """
    return await indicators_service.get_definitions()


@router.get("/region/{region_code}")
async def get_region_indicators(
    region_code: str,
    year: Optional[int] = None,
):
    """
    Get all indicators for a specific region.
    """
    indicators = await indicators_service.get_region_indicators(region_code, year)
    if not indicators:
        raise HTTPException(
            status_code=404,
            detail=f"No indicators found for region {region_code}",
        )
    return indicators


@router.get("/{indicator_code}/history")
async def get_indicator_history(
    indicator_code: str,
    region_code: Optional[str] = None,
    start_year: int = Query(2010, ge=1990),
    end_year: int = Query(2024, le=2030),
):
    """
    Get historical time series for an indicator.
    """
    history = await indicators_service.get_indicator_history(
        indicator_code, region_code, start_year, end_year
    )
    return {
        "indicator_code": indicator_code,
        "region_code": region_code,
        "start_year": start_year,
        "end_year": end_year,
        "data": history,
    }


@router.post("/", response_model=IndicatorRecord, status_code=201)
async def create_indicator(indicator: IndicatorCreate):
    """
    Create a new indicator record.
    """
    result = await indicators_service.create_indicator(indicator.model_dump())
    return result


@router.put("/{indicator_id}")
async def update_indicator(indicator_id: str, indicator: IndicatorCreate):
    """
    Update an existing indicator record.
    """
    result = await indicators_service.update_indicator(
        indicator_id, indicator.model_dump()
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Indicator {indicator_id} not found",
        )
    return result


@router.delete("/{indicator_id}", status_code=204)
async def delete_indicator(indicator_id: str):
    """
    Delete an indicator record.
    """
    deleted = await indicators_service.delete_indicator(indicator_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Indicator {indicator_id} not found",
        )
