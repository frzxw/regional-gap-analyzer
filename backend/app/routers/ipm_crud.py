"""
Router for indeks_pembangunan_manusia (IPM) CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List

from app.services.ipm_service import ipm_service
from app.models.ipm_model import (
    IPMCreateRequest,
    IPMUpdateRequest,
    IPMResponse,
)

router = APIRouter(prefix="/indeks-pembangunan-manusia", tags=["Indeks Pembangunan Manusia"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class IPMListResponse(BaseModel):
    """Response model for list of IPM."""
    data: List[IPMResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=IPMListResponse,
    summary="List all IPM records",
)
async def list_ipm(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> IPMListResponse:
    """Get paginated list of IPM records."""
    records, total = await ipm_service.get_all(page, page_size)

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return IPMListResponse(
        data=[IPMResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[IPMResponse],
    summary="Get IPM by province",
)
async def get_ipm_by_province(province_id: str) -> List[IPMResponse]:
    """Get all IPM records for a specific province."""
    records = await ipm_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [IPMResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}",
    response_model=IPMResponse,
    summary="Get IPM by province and year",
)
async def get_ipm(province_id: str, tahun: int) -> IPMResponse:
    """Get IPM data for specific province and year."""
    record = await ipm_service.get_by_province_and_year(province_id, tahun)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    if "_id" in record:
        record.pop("_id")

    return IPMResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create IPM record",
)
async def create_ipm(
    data: IPMCreateRequest,
) -> MessageResponse:
    """Create new IPM record."""
    existing = await ipm_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await ipm_service.create(data.model_dump())

    return MessageResponse(
        message=f"IPM data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update IPM record",
)
async def update_ipm(
    province_id: str, tahun: int, update_data: IPMUpdateRequest
) -> MessageResponse:
    """Update IPM record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await ipm_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"IPM data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete IPM record",
)
async def delete_ipm(province_id: str, tahun: int) -> MessageResponse:
    """Delete IPM record."""
    success = await ipm_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"IPM data deleted for province_id '{province_id}', tahun {tahun}"
    )
