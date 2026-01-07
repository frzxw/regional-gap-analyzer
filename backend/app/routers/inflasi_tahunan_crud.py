"""
Router for inflasi_tahunan CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List

from app.services.inflasi_tahunan_service import inflasi_tahunan_service
from app.services.csv_import import InflasiTahunanImportService
from app.models.inflasi_tahunan_model import (
    InflasiTahunanCreateRequest,
    InflasiTahunanUpdateRequest,
    InflasiTahunanResponse,
)
from app.models.csv_import import CSVImportResponse

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


@router.post(
    "/import-csv",
    response_model=CSVImportResponse,
    summary="Import Inflasi Tahunan from CSV"
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import Inflasi Tahunan data from CSV file (skiprows=3)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await InflasiTahunanImportService.import_csv(content, tahun)


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
