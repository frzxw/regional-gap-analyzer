"""
Health check router.
Provides endpoints for monitoring application health.
"""

from datetime import datetime, timezone
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


class HealthDetailedResponse(BaseModel):
    """Detailed health check response with metadata."""

    status: str
    database: str
    version: str
    timestamp: str


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


@router.get(
    "/health/full",
    response_model=HealthDetailedResponse,
    summary="Full health check with metadata",
    description="Returns complete health status with version and timestamp.",
)
async def health_check_full() -> HealthDetailedResponse:
    """
    Full health check with version info and timestamp.
    Useful for monitoring and debugging.
    """
    db_healthy = await ping_database()

    return HealthDetailedResponse(
        status="ok" if db_healthy else "degraded",
        database="connected" if db_healthy else "disconnected",
        version="0.1.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
