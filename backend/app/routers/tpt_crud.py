"""
Router for tingkat_pengangguran_terbuka (TPT) CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List

from app.services.tpt_service import tpt_service
from app.services.csv_import import TPTImportService
from app.models.tpt_model import (
    TPTCreateRequest,
    TPTUpdateRequest,
    TPTResponse,
)
from app.models.csv_import import CSVImportResponse

router = APIRouter(prefix="/tingkat-pengangguran-terbuka", tags=["Tingkat Pengangguran Terbuka"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class TPTListResponse(BaseModel):
    """Response model for list of TPT."""
    data: List[TPTResponse]
    total: int
    page: int
    page_size: int


@router.post(
    "/import-csv",
    response_model=CSVImportResponse,
    summary="Import Tingkat Pengangguran Terbuka from CSV"
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import TPT data from CSV file (skiprows=3)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await TPTImportService.import_csv(content, tahun, file.filename)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create TPT record",
)
async def create_tpt(
    data: TPTCreateRequest,
) -> MessageResponse:
    """Create new TPT record."""
    existing = await tpt_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await tpt_service.create(data.model_dump())

    return MessageResponse(
        message=f"TPT data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update TPT record",
)
async def update_tpt(
    province_id: str, tahun: int, update_data: TPTUpdateRequest
) -> MessageResponse:
    """Update TPT record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await tpt_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"TPT data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete TPT record",
)
async def delete_tpt(province_id: str, tahun: int) -> MessageResponse:
    """Delete TPT record."""
    success = await tpt_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"TPT data deleted for province_id '{province_id}', tahun {tahun}"
    )
