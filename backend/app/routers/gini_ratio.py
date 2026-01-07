"""
Gini Ratio router - API endpoints for gini ratio data.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from app.services.gini_ratio_service import GiniRatioService
from app.models.gini_ratio import (
    GiniRatioRecord,
    GiniRatioListResponse,
)

router = APIRouter(prefix="/gini-ratio", tags=["Gini Ratio"])


@router.get("/", response_model=GiniRatioListResponse)
async def list_gini_ratio(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    List all gini ratio records with optional filters.
    
    - **province_id**: Filter by specific province (e.g., "11", "12")
    - **year**: Filter by specific year (e.g., 2025)
    - **skip**: Pagination offset
    - **limit**: Pagination limit (max 100)
    """
    try:
        service = GiniRatioService()
        items, total = await service.get_all_gini_ratio(
            province_id=province_id,
            year=year,
            skip=skip,
            limit=limit,
        )
        return GiniRatioListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/province/{province_id}", response_model=GiniRatioListResponse)
async def get_gini_ratio_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    Get all gini ratio records for a specific province.
    
    - **province_id**: Province code (e.g., "11", "12")
    """
    try:
        service = GiniRatioService()
        items, total = await service.get_gini_ratio_by_province(
            province_id=province_id,
            skip=skip,
            limit=limit,
        )
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No gini ratio records found for province {province_id}",
            )
        return GiniRatioListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/year/{year}", response_model=GiniRatioListResponse)
async def get_gini_ratio_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    Get all gini ratio records for a specific year across all provinces.
    
    - **year**: Year (e.g., 2025)
    """
    try:
        service = GiniRatioService()
        items, total = await service.get_gini_ratio_by_year(
            year=year,
            skip=skip,
            limit=limit,
        )
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No gini ratio records found for year {year}",
            )
        return GiniRatioListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
