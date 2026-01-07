"""
Router for gini_ratio CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List

from app.services.gini_ratio_service import gini_ratio_service
from app.models.gini_ratio_model import (
    GiniRatioCreateRequest,
    GiniRatioUpdateRequest,
    GiniRatioResponse,
)

router = APIRouter(prefix="/gini-ratio", tags=["Gini Ratio"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class GiniRatioListResponse(BaseModel):
    """Response model for list of gini_ratio."""
    data: List[GiniRatioResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=GiniRatioListResponse,
    summary="List all gini_ratio records",
)
async def list_gini_ratio(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> GiniRatioListResponse:
    """Get paginated list of gini_ratio records."""
    records, total = await gini_ratio_service.get_all(page, page_size)

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return GiniRatioListResponse(
        data=[GiniRatioResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[GiniRatioResponse],
    summary="Get gini_ratio by province",
)
async def get_gini_ratio_by_province(province_id: str) -> List[GiniRatioResponse]:
    """Get all gini_ratio records for a specific province."""
    records = await gini_ratio_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [GiniRatioResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}",
    response_model=GiniRatioResponse,
    summary="Get gini_ratio by province and year",
)
async def get_gini_ratio(province_id: str, tahun: int) -> GiniRatioResponse:
    """Get gini_ratio data for specific province and year."""
    record = await gini_ratio_service.get_by_province_and_year(province_id, tahun)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    if "_id" in record:
        record.pop("_id")

    return GiniRatioResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create gini_ratio record",
)
async def create_gini_ratio(
    data: GiniRatioCreateRequest,
) -> MessageResponse:
    """Create new gini_ratio record."""
    existing = await gini_ratio_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await gini_ratio_service.create(data.model_dump())

    return MessageResponse(
        message=f"Gini ratio data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update gini_ratio record",
)
async def update_gini_ratio(
    province_id: str, tahun: int, update_data: GiniRatioUpdateRequest
) -> MessageResponse:
    """Update gini_ratio record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await gini_ratio_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Gini ratio data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete gini_ratio record",
)
async def delete_gini_ratio(province_id: str, tahun: int) -> MessageResponse:
    """Delete gini_ratio record."""
    success = await gini_ratio_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Gini ratio data deleted for province_id '{province_id}', tahun {tahun}"
    )
