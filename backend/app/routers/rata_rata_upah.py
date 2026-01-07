"""
API routes for rata_rata_upah (Average Net Wage) data.
"""

from typing import Optional
from fastapi import APIRouter, Query
from app.services.rata_rata_upah_service import RataRataUpahService
from app.models.rata_rata_upah import RataRataUpahBersihListResponse

router = APIRouter(
    prefix="/rata-rata-upah",
    tags=["Rata-rata Upah Bersih"],
)


@router.get(
    "/",
    response_model=RataRataUpahBersihListResponse,
    summary="Get all average net wage data",
    description="Retrieve average net wage records with optional filtering by province and year",
)
async def list_rata_rata_upah(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get all average net wage records."""
    service = RataRataUpahService()
    records, total = await service.get_all(province_id, year, skip, limit)

    return RataRataUpahBersihListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/province/{province_id}",
    response_model=RataRataUpahBersihListResponse,
    summary="Get average net wage by province",
    description="Retrieve all average net wage years for a specific province",
)
async def get_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get average net wage for a specific province."""
    service = RataRataUpahService()
    records, total = await service.get_by_province(province_id, skip, limit)

    return RataRataUpahBersihListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/year/{year}",
    response_model=RataRataUpahBersihListResponse,
    summary="Get average net wage by year",
    description="Retrieve average net wage for all provinces in a specific year",
)
async def get_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get average net wage for a specific year."""
    service = RataRataUpahService()
    records, total = await service.get_by_year(year, skip, limit)

    return RataRataUpahBersihListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )
