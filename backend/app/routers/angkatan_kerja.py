"""
Angkatan Kerja (Labor Force) router - API endpoints for labor force data.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from app.services.labor_force_service import LaborForceService
from app.models.labor_force import (
    LaborForceRecord,
    LaborForceResponse,
    LaborForceListResponse,
)
from app.common.errors import NotFoundError

router = APIRouter(prefix="/angkatan-kerja", tags=["Angkatan Kerja"])


@router.get("/", response_model=LaborForceListResponse)
async def list_angkatan_kerja(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    List all angkatan kerja records with optional filters.
    
    - **province_id**: Filter by specific province (e.g., "11", "12")
    - **year**: Filter by specific year (e.g., 2025)
    - **skip**: Pagination offset
    - **limit**: Pagination limit (max 100)
    """
    try:
        service = LaborForceService()
        items, total = await service.get_all_labor_force(
            province_id=province_id,
            year=year,
            skip=skip,
            limit=limit,
        )
        return LaborForceListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/province/{province_id}", response_model=LaborForceListResponse)
async def get_angkatan_kerja_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    Get all angkatan kerja records for a specific province.
    
    - **province_id**: Province code (e.g., "11", "12")
    """
    try:
        service = LaborForceService()
        items, total = await service.get_labor_force_by_province(
            province_id=province_id,
            skip=skip,
            limit=limit,
        )
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No angkatan kerja records found for province {province_id}",
            )
        return LaborForceListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/year/{year}", response_model=LaborForceListResponse)
async def get_angkatan_kerja_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    Get all angkatan kerja records for a specific year across all provinces.
    
    - **year**: Year (e.g., 2025)
    """
    try:
        service = LaborForceService()
        items, total = await service.get_labor_force_by_year(
            year=year,
            skip=skip,
            limit=limit,
        )
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No angkatan kerja records found for year {year}",
            )
        return LaborForceListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
