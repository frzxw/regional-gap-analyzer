"""
Router for pdrb_per_kapita CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List

from app.services.pdrb_per_kapita_service import pdrb_per_kapita_service
from app.models.pdrb_per_kapita_model import (
    PDRBPerKapitaCreateRequest,
    PDRBPerKapitaUpdateRequest,
    PDRBPerKapitaResponse,
)

router = APIRouter(prefix="/pdrb-per-kapita", tags=["PDRB Per Kapita"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class PDRBPerKapitaListResponse(BaseModel):
    """Response model for list of pdrb_per_kapita."""
    data: List[PDRBPerKapitaResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=PDRBPerKapitaListResponse,
    summary="List all PDRB per kapita records",
)
async def list_pdrb_per_kapita(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> PDRBPerKapitaListResponse:
    """Get paginated list of pdrb_per_kapita records."""
    records, total = await pdrb_per_kapita_service.get_all(page, page_size)

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return PDRBPerKapitaListResponse(
        data=[PDRBPerKapitaResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[PDRBPerKapitaResponse],
    summary="Get PDRB per kapita by province",
)
async def get_pdrb_per_kapita_by_province(province_id: str) -> List[PDRBPerKapitaResponse]:
    """Get all pdrb_per_kapita records for a specific province."""
    records = await pdrb_per_kapita_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [PDRBPerKapitaResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}/{indikator}",
    response_model=PDRBPerKapitaResponse,
    summary="Get PDRB per kapita by province, year, and indikator",
)
async def get_pdrb_per_kapita(province_id: str, tahun: int, indikator: str) -> PDRBPerKapitaResponse:
    """Get pdrb_per_kapita data for specific province, year, and indikator."""
    record = await pdrb_per_kapita_service.get_by_province_year_indikator(province_id, tahun, indikator)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}', tahun {tahun}, indikator '{indikator}'",
        )

    if "_id" in record:
        record.pop("_id")

    return PDRBPerKapitaResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create PDRB per kapita record",
)
async def create_pdrb_per_kapita(
    data: PDRBPerKapitaCreateRequest,
) -> MessageResponse:
    """Create new pdrb_per_kapita record."""
    existing = await pdrb_per_kapita_service.get_by_province_year_indikator(
        data.province_id, data.tahun, data.indikator
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}', tahun {data.tahun}, indikator '{data.indikator}' already exists",
        )

    await pdrb_per_kapita_service.create(data.model_dump())

    return MessageResponse(
        message=f"PDRB per kapita data created for province_id '{data.province_id}', tahun {data.tahun}, indikator '{data.indikator}'"
    )


@router.put(
    "/{province_id}/{tahun}/{indikator}",
    response_model=MessageResponse,
    summary="Update PDRB per kapita record",
)
async def update_pdrb_per_kapita(
    province_id: str, tahun: int, indikator: str, update_data: PDRBPerKapitaUpdateRequest
) -> MessageResponse:
    """Update pdrb_per_kapita record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await pdrb_per_kapita_service.update(province_id, tahun, indikator, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}', tahun {tahun}, indikator '{indikator}'",
        )

    return MessageResponse(
        message=f"PDRB per kapita data updated for province_id '{province_id}', tahun {tahun}, indikator '{indikator}'"
    )


@router.delete(
    "/{province_id}/{tahun}/{indikator}",
    response_model=MessageResponse,
    summary="Delete PDRB per kapita record",
)
async def delete_pdrb_per_kapita(province_id: str, tahun: int, indikator: str) -> MessageResponse:
    """Delete pdrb_per_kapita record."""
    success = await pdrb_per_kapita_service.delete(province_id, tahun, indikator)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}', tahun {tahun}, indikator '{indikator}'",
        )

    return MessageResponse(
        message=f"PDRB per kapita data deleted for province_id '{province_id}', tahun {tahun}, indikator '{indikator}'"
    )
