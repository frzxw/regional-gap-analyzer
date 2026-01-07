"""
Indeks Pembangunan Manusia router - API endpoints for human development index data.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from app.services.indeks_pembangunan_manusia_service import IndeksPembangunanManusiaService
from app.models.indeks_pembangunan_manusia import (
    IndeksPembangunanManusiaRecord,
    IndeksPembangunanManusiaListResponse,
)

router = APIRouter(prefix="/indeks-pembangunan-manusia", tags=["Indeks Pembangunan Manusia"])


@router.get("/", response_model=IndeksPembangunanManusiaListResponse)
async def list_indeks_pembangunan_manusia(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    List all human development index records with optional filters.
    
    - **province_id**: Filter by specific province (e.g., "11", "12")
    - **year**: Filter by specific year (e.g., 2020)
    - **skip**: Pagination offset
    - **limit**: Pagination limit (max 100)
    """
    try:
        service = IndeksPembangunanManusiaService()
        items, total = await service.get_all_indeks_pembangunan_manusia(
            province_id=province_id,
            year=year,
            skip=skip,
            limit=limit,
        )
        return IndeksPembangunanManusiaListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/province/{province_id}", response_model=IndeksPembangunanManusiaListResponse)
async def get_indeks_pembangunan_manusia_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    Get all human development index records for a specific province.
    
    - **province_id**: Province code (e.g., "11", "12")
    """
    try:
        service = IndeksPembangunanManusiaService()
        items, total = await service.get_indeks_pembangunan_manusia_by_province(
            province_id=province_id,
            skip=skip,
            limit=limit,
        )
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No human development index records found for province {province_id}",
            )
        return IndeksPembangunanManusiaListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/year/{year}", response_model=IndeksPembangunanManusiaListResponse)
async def get_indeks_pembangunan_manusia_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    Get all human development index records for a specific year across all provinces.
    
    - **year**: Year (e.g., 2020)
    """
    try:
        service = IndeksPembangunanManusiaService()
        items, total = await service.get_indeks_pembangunan_manusia_by_year(
            year=year,
            skip=skip,
            limit=limit,
        )
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No human development index records found for year {year}",
            )
        return IndeksPembangunanManusiaListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
