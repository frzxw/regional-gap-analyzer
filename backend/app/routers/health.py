"""
Health check router.
Provides endpoints for monitoring application health.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.db import ping_database

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    database: str


class HealthSimpleResponse(BaseModel):
    """Simple health check response."""

    status: str


@router.get(
    "/health",
    response_model=HealthSimpleResponse,
    summary="Basic health check",
    description="Returns basic health status of the API.",
)
async def health_check() -> HealthSimpleResponse:
    """
    Basic health check endpoint.
    Returns { "status": "ok" } if the API is running.
    """
    return HealthSimpleResponse(status="ok")


@router.get(
    "/health/detailed",
    response_model=HealthResponse,
    summary="Detailed health check",
    description="Returns detailed health status including database connectivity.",
)
async def health_check_detailed() -> HealthResponse:
    """
    Detailed health check including database status.
    """
    db_healthy = await ping_database()

    return HealthResponse(
        status="ok" if db_healthy else "degraded",
        database="connected" if db_healthy else "disconnected",
    )
