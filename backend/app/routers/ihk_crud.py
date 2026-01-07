"""
Router for indeks_harga_konsumen (IHK) CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List

from app.services.ihk_service import ihk_service
from app.services.csv_import import IHKImportService
from app.models.ihk_model import (
    IHKCreateRequest,
    IHKUpdateRequest,
    IHKResponse,
)
from app.models.csv_import import CSVImportResponse

router = APIRouter(prefix="/indeks-harga-konsumen", tags=["Indeks Harga Konsumen"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class IHKListResponse(BaseModel):
    """Response model for list of IHK."""
    data: List[IHKResponse]
    total: int
    page: int
    page_size: int


@router.post(
    "/import-csv",
    response_model=CSVImportResponse,
    summary="Import Indeks Harga Konsumen from CSV"
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import IHK data from CSV file (skiprows=3)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await IHKImportService.import_csv(content, tahun)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create IHK record",
)
async def create_ihk(
    data: IHKCreateRequest,
) -> MessageResponse:
    """Create new IHK record."""
    existing = await ihk_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await ihk_service.create(data.model_dump())

    return MessageResponse(
        message=f"IHK data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update IHK record",
)
async def update_ihk(
    province_id: str, tahun: int, update_data: IHKUpdateRequest
) -> MessageResponse:
    """Update IHK record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await ihk_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"IHK data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete IHK record",
)
async def delete_ihk(province_id: str, tahun: int) -> MessageResponse:
    """Delete IHK record."""
    success = await ihk_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"IHK data deleted for province_id '{province_id}', tahun {tahun}"
    )
