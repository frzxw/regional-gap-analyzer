"""
Router for kependudukan CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List

from app.services.kependudukan_service import kependudukan_service
from app.services.csv_import import KependudukanImportService
from app.models.kependudukan_model import (
    KependudukanCreateRequest,
    KependudukanUpdateRequest,
    KependudukanResponse,
)
from app.models.csv_import import CSVImportResponse

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


@router.post(
    "/import-csv",
    response_model=CSVImportResponse,
    summary="Import Kependudukan from CSV"
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import Kependudukan data from CSV file (no skiprows)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await KependudukanImportService.import_csv(content, tahun)


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
