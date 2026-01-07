"""
API routes for inflasi_tahunan (Annual Inflation) data.
"""

from typing import Optional
from fastapi import APIRouter, Query
from app.services.inflasi_tahunan_service import InflasiTahunanService
from app.models.inflasi_tahunan import InflasiTahunanListResponse

router = APIRouter(
    prefix="/inflasi-tahunan",
    tags=["Inflasi Tahunan"],
)


@router.get(
    "/",
    response_model=InflasiTahunanListResponse,
    summary="Get all annual inflation data",
    description="Retrieve annual inflation records with optional filtering by province and year",
)
async def list_inflasi_tahunan(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get all annual inflation records."""
    service = InflasiTahunanService()
    records, total = await service.get_all(province_id, year, skip, limit)

    return InflasiTahunanListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/province/{province_id}",
    response_model=InflasiTahunanListResponse,
    summary="Get annual inflation by province",
    description="Retrieve all annual inflation years for a specific province",
)
async def get_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get annual inflation for a specific province."""
    service = InflasiTahunanService()
    records, total = await service.get_by_province(province_id, skip, limit)

    return InflasiTahunanListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/year/{year}",
    response_model=InflasiTahunanListResponse,
    summary="Get annual inflation by year",
    description="Retrieve annual inflation for all provinces in a specific year",
)
async def get_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get annual inflation for a specific year."""
    service = InflasiTahunanService()
    records, total = await service.get_by_year(year, skip, limit)

    return InflasiTahunanListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )
