"""
Router for persentase_penduduk_miskin CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List

from app.services.persentase_penduduk_miskin_service import persentase_penduduk_miskin_service
from app.services.csv_import import PersentasePendudukMiskinImportService
from app.models.persentase_penduduk_miskin_model import (
    PersentasePendudukMiskinCreateRequest,
    PersentasePendudukMiskinUpdateRequest,
    PersentasePendudukMiskinResponse,
)
from app.models.csv_import import CSVImportResponse

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


@router.post(
    "/import-csv",
    response_model=CSVImportResponse,
    summary="Import Persentase Penduduk Miskin from CSV"
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import Persentase Penduduk Miskin data from CSV file (skiprows=4)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await PersentasePendudukMiskinImportService.import_csv(content, tahun)


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
