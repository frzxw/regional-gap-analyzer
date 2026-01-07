"""
API routes for kependudukan (Population) data.
"""

from typing import Optional
from fastapi import APIRouter, Query
from app.services.kependudukan_service import KependudukanService
from app.models.kependudukan import KependudukanListResponse

router = APIRouter(
    prefix="/kependudukan",
    tags=["Kependudukan"],
)


@router.get(
    "/",
    response_model=KependudukanListResponse,
    summary="Get all population data",
    description="Retrieve population records with optional filtering by province and year",
)
async def list_kependudukan(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get all population records."""
    service = KependudukanService()
    records, total = await service.get_all(province_id, year, skip, limit)

    return KependudukanListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/province/{province_id}",
    response_model=KependudukanListResponse,
    summary="Get population by province",
    description="Retrieve all population years for a specific province",
)
async def get_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get population for a specific province."""
    service = KependudukanService()
    records, total = await service.get_by_province(province_id, skip, limit)

    return KependudukanListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/year/{year}",
    response_model=KependudukanListResponse,
    summary="Get population by year",
    description="Retrieve population for all provinces in a specific year",
)
async def get_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get population for a specific year."""
    service = KependudukanService()
    records, total = await service.get_by_year(year, skip, limit)

    return KependudukanListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )
