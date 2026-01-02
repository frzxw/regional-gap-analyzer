"""
Regional Gap Analyzer API
Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import get_settings
from app.db import close_database
from app.routers import health_router, regions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    settings = get_settings()
    print(f"Starting Regional Gap Analyzer API...")
    print(f"Debug mode: {settings.debug}")
    print(f"MongoDB: {settings.mongo_db}")

    yield

    # Shutdown
    print("Shutting down...")
    await close_database()


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title="Regional Gap Analyzer API",
        description="Regional Inequality Analysis System - Province-level scoring and visualization",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(regions_router, prefix="/api/v1")

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
