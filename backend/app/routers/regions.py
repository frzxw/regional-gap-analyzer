"""
Regions router - CRUD operations for regional data.
TODO: Implement full CRUD operations.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/regions", tags=["Regions"])


class RegionBase(BaseModel):
    """Base model for region data."""

    code: str
    name: str
    province: str


class RegionResponse(RegionBase):
    """Response model for a region."""

    id: str


class RegionsListResponse(BaseModel):
    """Response model for list of regions."""

    regions: list[RegionResponse]
    total: int


# TODO: Implement the following endpoints:
# - GET /regions - List all regions with pagination
# - GET /regions/{region_id} - Get single region by ID
# - POST /regions - Create new region
# - PUT /regions/{region_id} - Update region
# - DELETE /regions/{region_id} - Delete region
# - GET /regions/{region_id}/scores - Get scoring data for region


@router.get(
    "",
    response_model=RegionsListResponse,
    summary="List all regions",
    description="Returns a list of all regions. TODO: Add pagination and filtering.",
)
async def list_regions() -> RegionsListResponse:
    """
    List all regions.
    TODO: Implement database query with pagination.
    """
    # Stub response - replace with actual database query
    return RegionsListResponse(regions=[], total=0)


@router.get(
    "/{region_id}",
    response_model=RegionResponse | None,
    summary="Get region by ID",
    description="Returns a single region by its ID.",
)
async def get_region(region_id: str) -> RegionResponse | None:
    """
    Get a single region by ID.
    TODO: Implement database query.
    """
    # Stub - replace with actual database query
    return None
