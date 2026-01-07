"""
API routes for pdrb_perkapita (GDP Per Capita) data.
"""

from typing import Optional
from fastapi import APIRouter, Query
from app.services.pdrb_perkapita_service import PdrbPerkapitaService
from app.models.pdrb_perkapita import PdrbPerkapitaListResponse

router = APIRouter(
    prefix="/pdrb-perkapita",
    tags=["PDRB Per Kapita"],
)


@router.get(
    "/",
    response_model=PdrbPerkapitaListResponse,
    summary="Get all GDP per capita data",
    description="Retrieve GDP per capita records with optional filtering by province and year",
)
async def list_pdrb_perkapita(
    province_id: Optional[str] = Query(None, description="Filter by province code"),
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get all GDP per capita records."""
    service = PdrbPerkapitaService()
    records, total = await service.get_all(province_id, year, skip, limit)

    return PdrbPerkapitaListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/province/{province_id}",
    response_model=PdrbPerkapitaListResponse,
    summary="Get GDP per capita by province",
    description="Retrieve all GDP per capita years for a specific province",
)
async def get_by_province(
    province_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get GDP per capita for a specific province."""
    service = PdrbPerkapitaService()
    records, total = await service.get_by_province(province_id, skip, limit)

    return PdrbPerkapitaListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/year/{year}",
    response_model=PdrbPerkapitaListResponse,
    summary="Get GDP per capita by year",
    description="Retrieve GDP per capita for all provinces in a specific year",
)
async def get_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),
):
    """Get GDP per capita for a specific year."""
    service = PdrbPerkapitaService()
    records, total = await service.get_by_year(year, skip, limit)

    return PdrbPerkapitaListResponse(
        data=records,
        total=total,
        skip=skip,
        limit=limit,
    )
