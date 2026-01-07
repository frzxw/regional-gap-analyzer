"""
Router for inflasi_tahunan CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List

from app.services.inflasi_tahunan_service import inflasi_tahunan_service
from app.models.inflasi_tahunan_model import (
    InflasiTahunanCreateRequest,
    InflasiTahunanUpdateRequest,
    InflasiTahunanResponse,
)

router = APIRouter(prefix="/inflasi-tahunan", tags=["Inflasi Tahunan"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class InflasiTahunanListResponse(BaseModel):
    """Response model for list of inflasi_tahunan."""
    data: List[InflasiTahunanResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=InflasiTahunanListResponse,
    summary="List all inflasi_tahunan records",
)
async def list_inflasi_tahunan(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> InflasiTahunanListResponse:
    """Get paginated list of inflasi_tahunan records."""
    records, total = await inflasi_tahunan_service.get_all(page, page_size)

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return InflasiTahunanListResponse(
        data=[InflasiTahunanResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[InflasiTahunanResponse],
    summary="Get inflasi_tahunan by province",
)
async def get_inflasi_tahunan_by_province(province_id: str) -> List[InflasiTahunanResponse]:
    """Get all inflasi_tahunan records for a specific province."""
    records = await inflasi_tahunan_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [InflasiTahunanResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}",
    response_model=InflasiTahunanResponse,
    summary="Get inflasi_tahunan by province and year",
)
async def get_inflasi_tahunan(province_id: str, tahun: int) -> InflasiTahunanResponse:
    """Get inflasi_tahunan data for specific province and year."""
    record = await inflasi_tahunan_service.get_by_province_and_year(province_id, tahun)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    if "_id" in record:
        record.pop("_id")

    return InflasiTahunanResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create inflasi_tahunan record",
)
async def create_inflasi_tahunan(
    data: InflasiTahunanCreateRequest,
) -> MessageResponse:
    """Create new inflasi_tahunan record."""
    existing = await inflasi_tahunan_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await inflasi_tahunan_service.create(data.model_dump())

    return MessageResponse(
        message=f"Inflasi tahunan data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update inflasi_tahunan record",
)
async def update_inflasi_tahunan(
    province_id: str, tahun: int, update_data: InflasiTahunanUpdateRequest
) -> MessageResponse:
    """Update inflasi_tahunan record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await inflasi_tahunan_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Inflasi tahunan data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete inflasi_tahunan record",
)
async def delete_inflasi_tahunan(province_id: str, tahun: int) -> MessageResponse:
    """Delete inflasi_tahunan record."""
    success = await inflasi_tahunan_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Inflasi tahunan data deleted for province_id '{province_id}', tahun {tahun}"
    )
