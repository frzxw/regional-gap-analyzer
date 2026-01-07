"""Routers module initialization."""

from app.routers.health import router as health_router
from app.routers.regions import router as regions_router
from app.routers.angkatan_kerja import router as angkatan_kerja_router
from app.routers.gini_ratio import router as gini_ratio_router

__all__ = ["health_router", "regions_router", "angkatan_kerja_router", "gini_ratio_router"]
