"""
API routes for persentase_penduduk_miskin (Poverty Rate) data.
"""

from typing import Optional
from fastapi import APIRouter, Query
from app.services.persentase_penduduk_miskin_service import PersentasePendudukMiskinService
from app.models.persentase_penduduk_miskin import PersentasePendudukMiskinListResponse

router = APIRouter(
    prefix="/persentase-penduduk-miskin",
    tags=["Persentase Penduduk Miskin"],
)


@router.get(
    "/",
    response_model=PersentasePendudukMiskinListResponse,
    summary="Get all poverty rate data",
    description="Retrieve poverty rate records with optional filtering by province and year",
)
async def list_persentase_penduduk_miskin(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get all poverty rate records."""
    service = PersentasePendudukMiskinService()
    records, total = await service.get_all(province_id, year, skip, limit)

    return PersentasePendudukMiskinListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/province/{province_id}",
    response_model=PersentasePendudukMiskinListResponse,
    summary="Get poverty rate by province",
    description="Retrieve all poverty rate years for a specific province",
)
async def get_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get poverty rate for a specific province."""
    service = PersentasePendudukMiskinService()
    records, total = await service.get_by_province(province_id, skip, limit)

    return PersentasePendudukMiskinListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/year/{year}",
    response_model=PersentasePendudukMiskinListResponse,
    summary="Get poverty rate by year",
    description="Retrieve poverty rate for all provinces in a specific year",
)
async def get_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get poverty rate for a specific year."""
    service = PersentasePendudukMiskinService()
    records, total = await service.get_by_year(year, skip, limit)

    return PersentasePendudukMiskinListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )
