"""
Regions router - CRUD operations for regional data.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime

from app.services.region_service import region_service

router = APIRouter(prefix="/regions", tags=["Regions"])


# ===== Request/Response Models =====


class GeometryModel(BaseModel):
    """GeoJSON geometry model."""
    type: str = Field(..., description="Geometry type (Polygon, MultiPolygon, etc.)")
    coordinates: List[Any] = Field(..., description="Geometry coordinates array")


class PropertiesModel(BaseModel):
    """Properties object from GeoJSON."""
    id: Optional[str] = Field(None, description="Province ID (may duplicate top-level id)")
    KODE_PROV: Optional[str] = Field(None, description="Kode provinsi BPS")
    PROVINSI: Optional[str] = Field(None, description="Nama provinsi")
    is_national: Optional[bool] = Field(None, description="Flag for national-level data")
    
    class Config:
        extra = "allow"  # Allow additional fields not defined in the model


class RegionBase(BaseModel):
    """Base model for region data (sesuai format indonesia-38.json)."""

    id: str = Field(..., description="ID unik region")
    type: Optional[str] = Field(None, description="GeoJSON type (Feature)")
    properties: PropertiesModel = Field(..., description="Properties containing KODE_PROV and PROVINSI")
    geometry: Optional[GeometryModel] = Field(None, description="GeoJSON geometry object")


class RegionCreateRequest(RegionBase):
    """Request model for creating a region."""

    class Config:
        json_schema_extra = {
            "example": {
                "id": "31",
                "type": "Feature",
                "properties": {
                    "KODE_PROV": "31",
                    "PROVINSI": "DKI Jakarta"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[106.7, -6.1], [106.9, -6.1], [106.9, -6.3], [106.7, -6.3], [106.7, -6.1]]]
                }
            }
        }


class RegionUpdateRequest(BaseModel):
    """Request model for updating a region - ONLY allows updating PROVINSI (province name)."""

    PROVINSI: str = Field(..., description="Nama provinsi (sesuai format indonesia-38.json)")

    class Config:
        json_schema_extra = {
            "example": {
                "PROVINSI": "DKI Jakarta"
            }
        }


class RegionResponse(RegionBase):
    """Response model for a region."""

    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "31",
                "type": "Feature",
                "properties": {
                    "KODE_PROV": "31",
                    "PROVINSI": "DKI Jakarta"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[106.7, -6.1], [106.9, -6.1], [106.9, -6.3], [106.7, -6.3], [106.7, -6.1]]]
                },
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }


class RegionsListResponse(BaseModel):
    """Response model for list of regions."""

    regions: list[RegionResponse]
    total: int
    page: int
    page_size: int


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str


# ===== Endpoints =====


@router.get(
    "",
    response_model=RegionsListResponse,
    summary="List all regions",
    description="Returns a paginated list of all regions.",
)
async def list_regions(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> RegionsListResponse:
    """
    List all regions with pagination.

    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page

    Returns:
        Paginated list of regions with total count
    """
    regions, total = await region_service.get_all_regions(page=page, page_size=page_size)

    # Convert _id to string for response
    for region in regions:
        if "_id" in region:
            region["id"] = str(region.pop("_id"))

    return RegionsListResponse(
        regions=[RegionResponse(**r) for r in regions],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{region_code}",
    response_model=RegionResponse,
    summary="Get region by code",
    description="Returns a single region by its code.",
)
async def get_region(region_code: str) -> RegionResponse:
    """
    Get a single region by code.

    Args:
        region_code: The region code (e.g., 'ID-JK')

    Returns:
        Region data

    Raises:
        404: Region not found
    """
    region = await region_service.get_region_by_code(region_code)

    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Region with code '{region_code}' not found",
        )

    # Convert _id to string for response
    if "_id" in region:
        region.pop("_id")

    return RegionResponse(**region)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new region",
    description="Creates a new region with the provided data.",
)
async def create_region(region_data: RegionCreateRequest) -> MessageResponse:
    """
    Create a new region.

    Args:
        region_data: Region data to create

    Returns:
        Success message with created region code

    Raises:
        409: Region with the same code already exists
    """
    # Check if region already exists
    existing = await region_service.get_region_by_code(region_data.properties.KODE_PROV)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Region with KODE_PROV '{region_data.properties.KODE_PROV}' already exists",
        )

    # Create the region
    await region_service.create_region(region_data.model_dump())

    return MessageResponse(message=f"Region '{region_data.properties.KODE_PROV}' (PROVINSI: '{region_data.properties.PROVINSI}') created successfully")


@router.put(
    "/{region_code}",
    response_model=MessageResponse,
    summary="Update a region",
    description="Updates an existing region by its code.",
)
async def update_region(
    region_code: str, update_data: RegionUpdateRequest
) -> MessageResponse:
    """
    Update an existing region - HANYA BISA MENGUPDATE NAMA PROVINSI (PROVINSI field).
    
    Sesuai prinsip data integrity, field lain seperti KODE_PROV dan geometry
    tidak boleh diubah karena berasal dari sumber data resmi (BPS).

    Args:
        region_code: The KODE_PROV to update
        update_data: Hanya field PROVINSI yang bisa diupdate

    Returns:
        Success message

    Raises:
        404: Region not found
    """
    # Hanya ambil field PROVINSI dan tambahkan updated_at
    update_dict = {
        "PROVINSI": update_data.PROVINSI,
        "updated_at": datetime.utcnow()
    }

    # Update the region
    success = await region_service.update_region(region_code, update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Region with KODE_PROV '{region_code}' not found",
        )

    return MessageResponse(message=f"Region '{region_code}' (PROVINSI: '{update_data.PROVINSI}') updated successfully")


@router.delete(
    "/{region_code}",
    response_model=MessageResponse,
    summary="Delete a region",
    description="Deletes a region by its code.",
)
async def delete_region(region_code: str) -> MessageResponse:
    """
    Delete a region.

    Args:
        region_code: The region code to delete

    Returns:
        Success message

    Raises:
        404: Region not found
    """
    success = await region_service.delete_region(region_code)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Region with code '{region_code}' not found",
        )

    return MessageResponse(message=f"Region '{region_code}' deleted successfully")
