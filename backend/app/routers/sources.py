"""
Sources router - API endpoints for data source management.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from app.services import imports_service
from app.repositories import get_sources_repository
from app.models import DataSource
from app.common.pagination import PaginatedResponse

router = APIRouter(prefix="/sources", tags=["Data Sources"])


@router.get("/")
async def list_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List all data sources.
    """
    repo = await get_sources_repository()
    sources = await repo.find_all(skip=skip, limit=limit)
    total = await repo.count()
    return PaginatedResponse(items=sources, total=total, skip=skip, limit=limit)


@router.get("/{source_id}")
async def get_source(source_id: str):
    """
    Get a specific data source by ID.
    """
    repo = await get_sources_repository()
    source = await repo.find_by_id(source_id)
    if not source:
        raise HTTPException(
            status_code=404,
            detail=f"Source {source_id} not found",
        )
    return source


@router.post("/", status_code=201)
async def create_source(source: DataSource):
    """
    Create a new data source record.
    """
    repo = await get_sources_repository()
    result = await repo.create(source.model_dump())
    return result


@router.put("/{source_id}")
async def update_source(source_id: str, source: DataSource):
    """
    Update a data source.
    """
    repo = await get_sources_repository()
    result = await repo.update(source_id, source.model_dump())
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Source {source_id} not found",
        )
    return result


@router.delete("/{source_id}", status_code=204)
async def delete_source(source_id: str):
    """
    Delete a data source.
    """
    repo = await get_sources_repository()
    deleted = await repo.delete(source_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Source {source_id} not found",
        )


@router.get("/{source_id}/indicators")
async def get_source_indicators(source_id: str):
    """
    Get all indicators from a specific source.
    """
    repo = await get_sources_repository()
    source = await repo.find_by_id(source_id)
    if not source:
        raise HTTPException(
            status_code=404,
            detail=f"Source {source_id} not found",
        )

    # Get indicators linked to this source
    from app.repositories import get_indicators_repository
    indicators_repo = await get_indicators_repository()
    indicators = await indicators_repo.find_by_source(source_id)

    return {
        "source": source,
        "indicators": indicators,
        "count": len(indicators),
    }
