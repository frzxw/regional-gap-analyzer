"""
Router for rata_rata_upah_bersih CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List

from app.services.rata_rata_upah_bersih_service import rata_rata_upah_bersih_service
from app.models.rata_rata_upah_bersih_model import (
    RataRataUpahBersihCreateRequest,
    RataRataUpahBersihUpdateRequest,
    RataRataUpahBersihResponse,
)

router = APIRouter(prefix="/rata-rata-upah-bersih", tags=["Rata-Rata Upah Bersih"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class RataRataUpahBersihListResponse(BaseModel):
    """Response model for list of rata_rata_upah_bersih."""
    data: List[RataRataUpahBersihResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=RataRataUpahBersihListResponse,
    summary="List all rata_rata_upah_bersih records",
)
async def list_rata_rata_upah_bersih(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> RataRataUpahBersihListResponse:
    """Get paginated list of rata_rata_upah_bersih records."""
    records, total = await rata_rata_upah_bersih_service.get_all(page, page_size)

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return RataRataUpahBersihListResponse(
        data=[RataRataUpahBersihResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[RataRataUpahBersihResponse],
    summary="Get rata_rata_upah_bersih by province",
)
async def get_rata_rata_upah_bersih_by_province(province_id: str) -> List[RataRataUpahBersihResponse]:
    """Get all rata_rata_upah_bersih records for a specific province."""
    records = await rata_rata_upah_bersih_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [RataRataUpahBersihResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}",
    response_model=RataRataUpahBersihResponse,
    summary="Get rata_rata_upah_bersih by province and year",
)
async def get_rata_rata_upah_bersih(province_id: str, tahun: int) -> RataRataUpahBersihResponse:
    """Get rata_rata_upah_bersih data for specific province and year."""
    record = await rata_rata_upah_bersih_service.get_by_province_and_year(province_id, tahun)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    if "_id" in record:
        record.pop("_id")

    return RataRataUpahBersihResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create rata_rata_upah_bersih record",
)
async def create_rata_rata_upah_bersih(
    data: RataRataUpahBersihCreateRequest,
) -> MessageResponse:
    """Create new rata_rata_upah_bersih record."""
    existing = await rata_rata_upah_bersih_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await rata_rata_upah_bersih_service.create(data.model_dump())

    return MessageResponse(
        message=f"Rata-rata upah bersih data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update rata_rata_upah_bersih record",
)
async def update_rata_rata_upah_bersih(
    province_id: str, tahun: int, update_data: RataRataUpahBersihUpdateRequest
) -> MessageResponse:
    """Update rata_rata_upah_bersih record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await rata_rata_upah_bersih_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Rata-rata upah bersih data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete rata_rata_upah_bersih record",
)
async def delete_rata_rata_upah_bersih(province_id: str, tahun: int) -> MessageResponse:
    """Delete rata_rata_upah_bersih record."""
    success = await rata_rata_upah_bersih_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Rata-rata upah bersih data deleted for province_id '{province_id}', tahun {tahun}"
    )
