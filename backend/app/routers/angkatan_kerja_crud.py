"""
Router for angkatan_kerja (Labor Force) CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.services.angkatan_kerja_service import angkatan_kerja_service
from app.services.csv_import import AngkatanKerjaImportService
from app.models.angkatan_kerja import (
    AngkatanKerjaCreateRequest,
    AngkatanKerjaUpdateRequest,
    AngkatanKerjaResponse,
)
from app.models.csv_import import CSVImportResponse

router = APIRouter(prefix="/angkatan-kerja", tags=["Angkatan Kerja"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class AngkatanKerjaListResponse(BaseModel):
    """Response model for list of angkatan_kerja."""
    data: List[AngkatanKerjaResponse]
    total: int
    page: int
    page_size: int


# ===== ENDPOINTS =====


@router.post(
    "/import-csv",
    response_model=CSVImportResponse,
    summary="Import Angkatan Kerja from CSV"
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import Angkatan Kerja data from CSV file (skiprows=4)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await AngkatanKerjaImportService.import_csv(content, tahun)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create angkatan_kerja record",
)
async def create_angkatan_kerja(
    data: AngkatanKerjaCreateRequest,
) -> MessageResponse:
    """Create new angkatan_kerja record."""
    # Check if record already exists
    existing = await angkatan_kerja_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    # Create record
    await angkatan_kerja_service.create(data.model_dump())

    return MessageResponse(
        message=f"Angkatan kerja data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update angkatan_kerja record",
)
async def update_angkatan_kerja(
    province_id: str, tahun: int, update_data: AngkatanKerjaUpdateRequest
) -> MessageResponse:
    """Update angkatan_kerja record."""
    # Prepare update dict (only non-None fields)
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await angkatan_kerja_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Angkatan kerja data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete angkatan_kerja record",
)
async def delete_angkatan_kerja(province_id: str, tahun: int) -> MessageResponse:
    """Delete angkatan_kerja record."""
    success = await angkatan_kerja_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Angkatan kerja data deleted for province_id '{province_id}', tahun {tahun}"
    )
