"""
Router for indeks_harga_konsumen (IHK) CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List

from app.services.ihk_service import ihk_service
from app.models.ihk_model import (
    IHKCreateRequest,
    IHKUpdateRequest,
    IHKResponse,
)

router = APIRouter(prefix="/indeks-harga-konsumen", tags=["Indeks Harga Konsumen"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class IHKListResponse(BaseModel):
    """Response model for list of IHK."""
    data: List[IHKResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=IHKListResponse,
    summary="List all IHK records",
)
async def list_ihk(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> IHKListResponse:
    """Get paginated list of IHK records."""
    records, total = await ihk_service.get_all(page, page_size)

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return IHKListResponse(
        data=[IHKResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[IHKResponse],
    summary="Get IHK by province",
)
async def get_ihk_by_province(province_id: str) -> List[IHKResponse]:
    """Get all IHK records for a specific province."""
    records = await ihk_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [IHKResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}",
    response_model=IHKResponse,
    summary="Get IHK by province and year",
)
async def get_ihk(province_id: str, tahun: int) -> IHKResponse:
    """Get IHK data for specific province and year."""
    record = await ihk_service.get_by_province_and_year(province_id, tahun)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    if "_id" in record:
        record.pop("_id")

    return IHKResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create IHK record",
)
async def create_ihk(
    data: IHKCreateRequest,
) -> MessageResponse:
    """Create new IHK record."""
    existing = await ihk_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await ihk_service.create(data.model_dump())

    return MessageResponse(
        message=f"IHK data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update IHK record",
)
async def update_ihk(
    province_id: str, tahun: int, update_data: IHKUpdateRequest
) -> MessageResponse:
    """Update IHK record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await ihk_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"IHK data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete IHK record",
)
async def delete_ihk(province_id: str, tahun: int) -> MessageResponse:
    """Delete IHK record."""
    success = await ihk_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"IHK data deleted for province_id '{province_id}', tahun {tahun}"
    )
