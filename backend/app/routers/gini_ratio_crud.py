"""
Router for gini_ratio CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import List

from app.services.gini_ratio_service import gini_ratio_service
from app.services.csv_import import GiniRatioImportService
from app.models.gini_ratio_model import (
    GiniRatioCreateRequest,
    GiniRatioUpdateRequest,
    GiniRatioResponse,
)
from app.models.csv_import import CSVImportResponse

router = APIRouter(prefix="/gini-ratio", tags=["Gini Ratio"])


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class GiniRatioListResponse(BaseModel):
    """Response model for list of gini_ratio."""
    data: List[GiniRatioResponse]
    total: int
    page: int
    page_size: int


@router.get(
    "",
    response_model=GiniRatioListResponse,
    summary="List all gini_ratio data",
)
async def list_gini_ratio(
    tahun: int = Query(None, description="Filter by year"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Page size"),
) -> GiniRatioListResponse:
    """Get list of gini_ratio data with optional year filter."""
    data = await gini_ratio_service.list_all(tahun=tahun, page=page, page_size=page_size)
    total = await gini_ratio_service.count(tahun=tahun)
    return GiniRatioListResponse(
        data=data,
        total=total,
        page=page,
        page_size=page_size,
    )

@router.post(
    "/import-csv",
    response_model=CSVImportResponse,
    summary="Import Gini Ratio from CSV"
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to import"),
    tahun: int = Query(..., description="Year of the data")
) -> CSVImportResponse:
    """Import Gini Ratio data from CSV file (skiprows=4)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    return await GiniRatioImportService.import_csv(content, tahun, file.filename)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create gini_ratio record",
)
async def create_gini_ratio(
    data: GiniRatioCreateRequest,
) -> MessageResponse:
    """Create new gini_ratio record."""
    existing = await gini_ratio_service.get_by_province_and_year(
        data.province_id, data.tahun
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data for province_id '{data.province_id}' and tahun {data.tahun} already exists",
        )

    await gini_ratio_service.create(data.model_dump())

    return MessageResponse(
        message=f"Gini ratio data created for province_id '{data.province_id}', tahun {data.tahun}"
    )


@router.put(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Update gini_ratio record",
)
async def update_gini_ratio(
    province_id: str, tahun: int, update_data: GiniRatioUpdateRequest
) -> MessageResponse:
    """Update gini_ratio record."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    success = await gini_ratio_service.update(province_id, tahun, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Gini ratio data updated for province_id '{province_id}', tahun {tahun}"
    )


@router.delete(
    "/{province_id}/{tahun}",
    response_model=MessageResponse,
    summary="Delete gini_ratio record",
)
async def delete_gini_ratio(province_id: str, tahun: int) -> MessageResponse:
    """Delete gini_ratio record."""
    success = await gini_ratio_service.delete(province_id, tahun)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data not found for province_id '{province_id}' and tahun {tahun}",
        )

    return MessageResponse(
        message=f"Gini ratio data deleted for province_id '{province_id}', tahun {tahun}"
    )
