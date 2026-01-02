"""Routers module initialization."""

from app.routers.health import router as health_router
from app.routers.regions import router as regions_router

__all__ = ["health_router", "regions_router"]
