"""
Router for pdrb_per_kapita CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List

from app.services.pdrb_per_kapita_service import pdrb_per_kapita_service
from app.services.csv_import import PDRBImportService
from app.models.pdrb_per_kapita_model import (
    PDRBPerKapitaCreateRequest,
    PDRBPerKapitaUpdateRequest,
    PDRBPerKapitaResponse,
)
from app.models.csv_import import CSVImportResponse

router = APIRouter(prefix="/pdrb-per-kapita", tags=["PDRB Per Kapita"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class PDRBPerKapitaListResponse(BaseModel):
    """Response model for list of pdrb_per_kapita."""
    data: List[PDRBPerKapitaResponse]
    total: int
    page: int
    page_size: int


@router.post(
    "/import-csv-adhb",
    response_model=CSVImportResponse,
    summary="Import PDRB Per Kapita ADHB from CSV"
)
async def import_csv_adhb(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import PDRB Per Kapita ADHB data from CSV file (no skiprows)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await PDRBImportService.import_adhb(content, tahun)


@router.post(
    "/import-csv-adhk",
    response_model=CSVImportResponse,
    summary="Import PDRB Per Kapita ADHK from CSV"
)
async def import_csv_adhk(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import PDRB Per Kapita ADHK data from CSV file (no skiprows)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await PDRBImportService.import_adhk(content, tahun)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create PDRB per kapita record",
)
async def create_pdrb_per_kapita(
    data: PDRBPerKapitaCreateRequest,
) -> MessageResponse:
    """Create new pdrb_per_kapita record."""
    existing = await pdrb_per_kapita_service.get_by_province_year_indikator(
        data.province_id, data.tahun, data.indikator
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}', tahun {data.tahun}, indikator '{data.indikator}' already exists",
        )

    await pdrb_per_kapita_service.create(data.model_dump())

    return MessageResponse(
        message=f"PDRB per kapita data created for province_id '{data.province_id}', tahun {data.tahun}, indikator '{data.indikator}'"
    )


@router.put(
    "/{province_id}/{tahun}/{indikator}",
    response_model=MessageResponse,
    summary="Update PDRB per kapita record",
)
async def update_pdrb_per_kapita(
    province_id: str, tahun: int, indikator: str, update_data: PDRBPerKapitaUpdateRequest
) -> MessageResponse:
    """Update pdrb_per_kapita record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await pdrb_per_kapita_service.update(province_id, tahun, indikator, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}', tahun {tahun}, indikator '{indikator}'",
        )

    return MessageResponse(
        message=f"PDRB per kapita data updated for province_id '{province_id}', tahun {tahun}, indikator '{indikator}'"
    )


@router.delete(
    "/{province_id}/{tahun}/{indikator}",
    response_model=MessageResponse,
    summary="Delete PDRB per kapita record",
)
async def delete_pdrb_per_kapita(province_id: str, tahun: int, indikator: str) -> MessageResponse:
    """Delete pdrb_per_kapita record."""
    success = await pdrb_per_kapita_service.delete(province_id, tahun, indikator)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}', tahun {tahun}, indikator '{indikator}'",
        )

    return MessageResponse(
        message=f"PDRB per kapita data deleted for province_id '{province_id}', tahun {tahun}, indikator '{indikator}'"
    )
