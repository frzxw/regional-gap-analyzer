"""
Router for angkatan_kerja (Labor Force) CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.services.angkatan_kerja_service import angkatan_kerja_service
from app.models.angkatan_kerja import (
    AngkatanKerjaCreateRequest,
    AngkatanKerjaUpdateRequest,
    AngkatanKerjaResponse,
)

router = APIRouter(prefix="/angkatan-kerja", tags=["Angkatan Kerja"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class AngkatanKerjaListResponse(BaseModel):
    """Response model for list of angkatan_kerja."""
    data: List[AngkatanKerjaResponse]
    total: int
    page: int
    page_size: int


# ===== ENDPOINTS =====


@router.get(
    "",
    response_model=AngkatanKerjaListResponse,
    summary="List all angkatan_kerja records",
)
async def list_angkatan_kerja(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> AngkatanKerjaListResponse:
    """Get paginated list of angkatan_kerja records."""
    records, total = await angkatan_kerja_service.get_all(page, page_size)

    # Remove _id from each record
    for record in records:
        if "_id" in record:
            record.pop("_id")

    return AngkatanKerjaListResponse(
        data=[AngkatanKerjaResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[AngkatanKerjaResponse],
    summary="Get angkatan_kerja by province",
)
async def get_angkatan_kerja_by_province(province_id: str) -> List[AngkatanKerjaResponse]:
    """Get all angkatan_kerja records for a specific province."""
    records = await angkatan_kerja_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    # Remove _id
    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [AngkatanKerjaResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}",
    response_model=AngkatanKerjaResponse,
    summary="Get angkatan_kerja by province and year",
)
async def get_angkatan_kerja(province_id: str, tahun: int) -> AngkatanKerjaResponse:
    """Get angkatan_kerja data for specific province and year."""
    record = await angkatan_kerja_service.get_by_province_and_year(province_id, tahun)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    if "_id" in record:
        record.pop("_id")

    return AngkatanKerjaResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create angkatan_kerja record",
)
async def create_angkatan_kerja(
    data: AngkatanKerjaCreateRequest,
) -> MessageResponse:
    """Create new angkatan_kerja record."""
    # Check if record already exists
    existing = await angkatan_kerja_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    # Create record
    await angkatan_kerja_service.create(data.model_dump())

    return MessageResponse(
        message=f"Angkatan kerja data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update angkatan_kerja record",
)
async def update_angkatan_kerja(
    province_id: str, tahun: int, update_data: AngkatanKerjaUpdateRequest
) -> MessageResponse:
    """Update angkatan_kerja record."""
    # Prepare update dict (only non-None fields)
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await angkatan_kerja_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Angkatan kerja data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete angkatan_kerja record",
)
async def delete_angkatan_kerja(province_id: str, tahun: int) -> MessageResponse:
    """Delete angkatan_kerja record."""
    success = await angkatan_kerja_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Angkatan kerja data deleted for province_id '{province_id}', tahun {tahun}"
    )
