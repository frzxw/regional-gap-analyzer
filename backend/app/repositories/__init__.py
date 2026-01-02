"""Repositories module initialization."""

from app.repositories.region_repository import (
    RegionRepository,
    get_region_repository,
)

__all__ = ["RegionRepository", "get_region_repository"]
