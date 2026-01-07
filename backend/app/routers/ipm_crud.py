"""
Router for indeks_pembangunan_manusia (IPM) CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List

from app.services.ipm_service import ipm_service
from app.services.csv_import import IPMImportService
from app.models.ipm_model import (
    IPMCreateRequest,
    IPMUpdateRequest,
    IPMResponse,
)
from app.models.csv_import import CSVImportResponse

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


@router.post(
    "/import-csv",
    response_model=CSVImportResponse,
    summary="Import Indeks Pembangunan Manusia from CSV"
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import IPM data from CSV file (skiprows=2)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await IPMImportService.import_csv(content, tahun)


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
