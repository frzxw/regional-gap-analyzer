"""
Router for tingkat_pengangguran_terbuka (TPT) CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List

from app.services.tpt_service import tpt_service
from app.models.tpt_model import (
    TPTCreateRequest,
    TPTUpdateRequest,
    TPTResponse,
)

router = APIRouter(prefix="/tingkat-pengangguran-terbuka", tags=["Tingkat Pengangguran Terbuka"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class TPTListResponse(BaseModel):
    """Response model for list of TPT."""
    data: List[TPTResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=TPTListResponse,
    summary="List all TPT records",
)
async def list_tpt(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> TPTListResponse:
    """Get paginated list of TPT records."""
    records, total = await tpt_service.get_all(page, page_size)

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return TPTListResponse(
        data=[TPTResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[TPTResponse],
    summary="Get TPT by province",
)
async def get_tpt_by_province(province_id: str) -> List[TPTResponse]:
    """Get all TPT records for a specific province."""
    records = await tpt_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [TPTResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}",
    response_model=TPTResponse,
    summary="Get TPT by province and year",
)
async def get_tpt(province_id: str, tahun: int) -> TPTResponse:
    """Get TPT data for specific province and year."""
    record = await tpt_service.get_by_province_and_year(province_id, tahun)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    if "_id" in record:
        record.pop("_id")

    return TPTResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create TPT record",
)
async def create_tpt(
    data: TPTCreateRequest,
) -> MessageResponse:
    """Create new TPT record."""
    existing = await tpt_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await tpt_service.create(data.model_dump())

    return MessageResponse(
        message=f"TPT data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update TPT record",
)
async def update_tpt(
    province_id: str, tahun: int, update_data: TPTUpdateRequest
) -> MessageResponse:
    """Update TPT record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await tpt_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"TPT data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete TPT record",
)
async def delete_tpt(province_id: str, tahun: int) -> MessageResponse:
    """Delete TPT record."""
    success = await tpt_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"TPT data deleted for province_id '{province_id}', tahun {tahun}"
    )
