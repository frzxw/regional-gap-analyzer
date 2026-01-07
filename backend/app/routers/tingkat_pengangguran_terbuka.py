"""
API routes for tingkat_pengangguran_terbuka (Open Unemployment Rate) data.
"""

from typing import Optional
from fastapi import APIRouter, Query
from app.services.tingkat_pengangguran_terbuka_service import TingkatPengangguranTerbukaService
from app.models.tingkat_pengangguran_terbuka import TingkatPengangguranTerbukaListResponse

router = APIRouter(
    prefix="/tingkat-pengangguran-terbuka",
    tags=["Tingkat Pengangguran Terbuka"],
)


@router.get(
    "/",
    response_model=TingkatPengangguranTerbukaListResponse,
    summary="Get all unemployment rate data",
    description="Retrieve unemployment rate records with optional filtering by province and year",
)
async def list_tingkat_pengangguran_terbuka(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get all unemployment rate records."""
    service = TingkatPengangguranTerbukaService()
    records, total = await service.get_all(province_id, year, skip, limit)

    return TingkatPengangguranTerbukaListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/province/{province_id}",
    response_model=TingkatPengangguranTerbukaListResponse,
    summary="Get unemployment rate by province",
    description="Retrieve all unemployment rate years for a specific province",
)
async def get_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get unemployment rate for a specific province."""
    service = TingkatPengangguranTerbukaService()
    records, total = await service.get_by_province(province_id, skip, limit)

    return TingkatPengangguranTerbukaListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/year/{year}",
    response_model=TingkatPengangguranTerbukaListResponse,
    summary="Get unemployment rate by year",
    description="Retrieve unemployment rate for all provinces in a specific year",
)
async def get_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get unemployment rate for a specific year."""
    service = TingkatPengangguranTerbukaService()
    records, total = await service.get_by_year(year, skip, limit)

    return TingkatPengangguranTerbukaListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )
