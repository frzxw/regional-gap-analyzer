"""
Router for rata_rata_upah_bersih CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List

from app.services.rata_rata_upah_bersih_service import rata_rata_upah_bersih_service
from app.services.csv_import import RataRataUpahImportService
from app.models.rata_rata_upah_bersih_model import (
    RataRataUpahBersihCreateRequest,
    RataRataUpahBersihUpdateRequest,
    RataRataUpahBersihResponse,
)
from app.models.csv_import import CSVImportResponse

router = APIRouter(prefix="/rata-rata-upah", tags=["Rata-rata Upah Bersih"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class RataRataUpahBersihListResponse(BaseModel):
    """Response model for list of rata_rata_upah_bersih."""
    data: List[RataRataUpahBersihResponse]
    total: int
    page: int
    page_size: int


@router.post(
    "/import-csv",
    response_model=CSVImportResponse,
    summary="Import Rata-rata Upah Bersih from CSV"
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import Rata-rata Upah Bersih data from CSV file (skiprows=4)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await RataRataUpahImportService.import_csv(content, tahun)


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
