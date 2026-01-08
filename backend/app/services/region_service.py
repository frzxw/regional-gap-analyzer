"""
Region service - Business logic for region operations.
"""

from typing import Optional

from app.repositories import get_region_repository
from app.models import RegionModel


class RegionService:
    """Service layer for region business logic."""

    async def get_all_regions(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict], int]:
        """
        Get all regions with pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Tuple of (regions list, total count)
        """
        skip = (page - 1) * page_size
        repo = await get_region_repository()
        return await repo.find_all(skip=skip, limit=page_size)

    async def get_region_by_code(self, code: str) -> Optional[dict]:
        """Get a single region by its code."""
        repo = await get_region_repository()
        return await repo.find_by_code(code)

    async def create_region(self, region_data: dict) -> str:
        """
        Create a new region.

        Args:
            region_data: Region data dictionary (GeoJSON Feature format with nested properties)

        Returns:
            Created region ID
        """
        # Extract properties from GeoJSON structure if present
        if "properties" in region_data:
            properties = region_data.get("properties", {})
            flattened_data = {
                "id": region_data.get("id"),
                "KODE_PROV": properties.get("KODE_PROV"),
                "PROVINSI": properties.get("PROVINSI"),
                "geometry": region_data.get("geometry"),
            }
            region = RegionModel(**flattened_data)
        else:
            # Backward compatibility: flat structure
            region = RegionModel(**region_data)
        
        repo = await get_region_repository()
        return await repo.create(region)

    async def update_region(self, code: str, update_data: dict) -> bool:
        """Update a region by code."""
        repo = await get_region_repository()
        return await repo.update(code, update_data)

    async def delete_region(self, code: str) -> bool:
        """Delete a region by code."""
        repo = await get_region_repository()
        return await repo.delete(code)


# Singleton instance
region_service = RegionService()
