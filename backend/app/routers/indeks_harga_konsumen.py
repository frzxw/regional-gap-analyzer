"""
Indeks Harga Konsumen router - API endpoints for consumer price index data.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from app.services.indeks_harga_konsumen_service import IndeksHargaKonsumenService
from app.models.indeks_harga_konsumen import (
    IndeksHargaKonsumenRecord,
    IndeksHargaKonsumenListResponse,
)

router = APIRouter(prefix="/indeks-harga-konsumen", tags=["Indeks Harga Konsumen"])


@router.get("/", response_model=IndeksHargaKonsumenListResponse)
async def list_indeks_harga_konsumen(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    List all consumer price index records with optional filters.
    
    - **province_id**: Filter by specific province (e.g., "11", "12")
    - **year**: Filter by specific year (e.g., 2024)
    - **skip**: Pagination offset
    - **limit**: Pagination limit (max 100)
    """
    try:
        service = IndeksHargaKonsumenService()
        items, total = await service.get_all_indeks_harga_konsumen(
            province_id=province_id,
            year=year,
            skip=skip,
            limit=limit,
        )
        return IndeksHargaKonsumenListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/province/{province_id}", response_model=IndeksHargaKonsumenListResponse)
async def get_indeks_harga_konsumen_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    Get all consumer price index records for a specific province.
    
    - **province_id**: Province code (e.g., "11", "12")
    """
    try:
        service = IndeksHargaKonsumenService()
        items, total = await service.get_indeks_harga_konsumen_by_province(
            province_id=province_id,
            skip=skip,
            limit=limit,
        )
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No consumer price index records found for province {province_id}",
            )
        return IndeksHargaKonsumenListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/year/{year}", response_model=IndeksHargaKonsumenListResponse)
async def get_indeks_harga_konsumen_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
):
    """
    Get all consumer price index records for a specific year across all provinces.
    
    - **year**: Year (e.g., 2024)
    """
    try:
        service = IndeksHargaKonsumenService()
        items, total = await service.get_indeks_harga_konsumen_by_year(
            year=year,
            skip=skip,
            limit=limit,
        )
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No consumer price index records found for year {year}",
            )
        return IndeksHargaKonsumenListResponse(
            data=items,
            total=total,
            skip=skip,
            limit=limit,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
