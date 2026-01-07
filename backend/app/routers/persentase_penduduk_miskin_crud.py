"""
Router for persentase_penduduk_miskin CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List

from app.services.persentase_penduduk_miskin_service import persentase_penduduk_miskin_service
from app.models.persentase_penduduk_miskin_model import (
    PersentasePendudukMiskinCreateRequest,
    PersentasePendudukMiskinUpdateRequest,
    PersentasePendudukMiskinResponse,
)

router = APIRouter(prefix="/persentase-penduduk-miskin", tags=["Persentase Penduduk Miskin"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class PersentasePendudukMiskinListResponse(BaseModel):
    """Response model for list of persentase_penduduk_miskin."""
    data: List[PersentasePendudukMiskinResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=PersentasePendudukMiskinListResponse,
    summary="List all persentase_penduduk_miskin records",
)
async def list_persentase_penduduk_miskin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> PersentasePendudukMiskinListResponse:
    """Get paginated list of persentase_penduduk_miskin records."""
    records, total = await persentase_penduduk_miskin_service.get_all(page, page_size)

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return PersentasePendudukMiskinListResponse(
        data=[PersentasePendudukMiskinResponse(**r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/province/{province_id}",
    response_model=List[PersentasePendudukMiskinResponse],
    summary="Get persentase_penduduk_miskin by province",
)
async def get_persentase_penduduk_miskin_by_province(province_id: str) -> List[PersentasePendudukMiskinResponse]:
    """Get all persentase_penduduk_miskin records for a specific province."""
    records = await persentase_penduduk_miskin_service.get_by_province(province_id)

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for province_id '{province_id}'",
        )

    for record in records:
        if "_id" in record:
            record.pop("_id")

    return [PersentasePendudukMiskinResponse(**r) for r in records]


@router.get(
    "/{province_id}/{tahun}",
    response_model=PersentasePendudukMiskinResponse,
    summary="Get persentase_penduduk_miskin by province and year",
)
async def get_persentase_penduduk_miskin(province_id: str, tahun: int) -> PersentasePendudukMiskinResponse:
    """Get persentase_penduduk_miskin data for specific province and year."""
    record = await persentase_penduduk_miskin_service.get_by_province_and_year(province_id, tahun)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    if "_id" in record:
        record.pop("_id")

    return PersentasePendudukMiskinResponse(**record)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create persentase_penduduk_miskin record",
)
async def create_persentase_penduduk_miskin(
    data: PersentasePendudukMiskinCreateRequest,
) -> MessageResponse:
    """Create new persentase_penduduk_miskin record."""
    existing = await persentase_penduduk_miskin_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await persentase_penduduk_miskin_service.create(data.model_dump())

    return MessageResponse(
        message=f"Persentase penduduk miskin data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update persentase_penduduk_miskin record",
)
async def update_persentase_penduduk_miskin(
    province_id: str, tahun: int, update_data: PersentasePendudukMiskinUpdateRequest
) -> MessageResponse:
    """Update persentase_penduduk_miskin record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await persentase_penduduk_miskin_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Persentase penduduk miskin data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete persentase_penduduk_miskin record",
)
async def delete_persentase_penduduk_miskin(province_id: str, tahun: int) -> MessageResponse:
    """Delete persentase_penduduk_miskin record."""
    success = await persentase_penduduk_miskin_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Persentase penduduk miskin data deleted for province_id '{province_id}', tahun {tahun}"
    )
