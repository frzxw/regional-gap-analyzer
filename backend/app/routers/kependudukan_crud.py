"""
Router for kependudukan CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List

from app.services.kependudukan_service import kependudukan_service
from app.models.kependudukan_model import (
    KependudukanCreateRequest,
    KependudukanUpdateRequest,
    KependudukanResponse,
)

router = APIRouter(prefix="/kependudukan", tags=["Kependudukan"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class KependudukanListResponse(BaseModel):
    """Response model for list of kependudukan."""
    data: List[KependudukanResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=KependudukanListResponse,
    summary="List all kependudukan records",
)
async def list_kependudukan(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> KependudukanListResponse:
    """Get paginated list of kependudukan records."""
    records, total = await kependudukan_service.get_all(page, page_size)

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return KependudukanListResponse(
        data=[KependudukanResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[KependudukanResponse],
    summary="Get kependudukan by province",
)
async def get_kependudukan_by_province(province_id: str) -> List[KependudukanResponse]:
    """Get all kependudukan records for a specific province."""
    records = await kependudukan_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [KependudukanResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}",
    response_model=KependudukanResponse,
    summary="Get kependudukan by province and year",
)
async def get_kependudukan(province_id: str, tahun: int) -> KependudukanResponse:
    """Get kependudukan data for specific province and year."""
    record = await kependudukan_service.get_by_province_and_year(province_id, tahun)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    if "_id" in record:
        record.pop("_id")

    return KependudukanResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create kependudukan record",
)
async def create_kependudukan(
    data: KependudukanCreateRequest,
) -> MessageResponse:
    """Create new kependudukan record."""
    existing = await kependudukan_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await kependudukan_service.create(data.model_dump())

    return MessageResponse(
        message=f"Kependudukan data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update kependudukan record",
)
async def update_kependudukan(
    province_id: str, tahun: int, update_data: KependudukanUpdateRequest
) -> MessageResponse:
    """Update kependudukan record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await kependudukan_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Kependudukan data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete kependudukan record",
)
async def delete_kependudukan(province_id: str, tahun: int) -> MessageResponse:
    """Delete kependudukan record."""
    success = await kependudukan_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Kependudukan data deleted for province_id '{province_id}', tahun {tahun}"
    )
