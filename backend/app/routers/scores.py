"""
Scores router - API endpoints for composite scores and rankings.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query

from app.services import scoring_service
from app.common.pagination import PaginatedResponse

router = APIRouter(prefix="/scores", tags=["Scores"])


@router.get("/")
async def list_scores(
    year: Optional[int] = Query(None, description="Filter by year"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List composite scores with optional year filter.
    """
    scores = await scoring_service.get_scores(year=year, skip=skip, limit=limit)
    return scores


@router.get("/rankings")
async def get_rankings(
    year: Optional[int] = Query(None, description="Year (latest if not specified)"),
    limit: int = Query(38, ge=1, le=100),
):
    """
    Get region rankings by composite score.
    """
    rankings = await scoring_service.get_rankings(year=year, limit=limit)
    return {
        "year": year or await scoring_service.get_latest_year(),
        "rankings": rankings,
    }


@router.get("/top-bottom")
async def get_top_bottom_regions(
    year: Optional[int] = None,
    count: int = Query(5, ge=1, le=10),
):
    """
    Get top and bottom performing regions.
    """
    top, bottom = await scoring_service.get_top_bottom(year=year, count=count)
    return {
        "year": year or await scoring_service.get_latest_year(),
        "top_performers": top,
        "bottom_performers": bottom,
    }


@router.get("/region/{region_code}")
async def get_region_score(
    region_code: str,
    year: Optional[int] = None,
):
    """
    Get score details for a specific region.
    """
    score = await scoring_service.get_region_score(region_code, year)
    if not score:
        raise HTTPException(
            status_code=404,
            detail=f"No score found for region {region_code}",
        )
    return score


@router.get("/region/{region_code}/history")
async def get_region_score_history(
    region_code: str,
    start_year: int = Query(2015, ge=1990),
    end_year: int = Query(2024, le=2030),
):
    """
    Get score history for a region over time.
    """
    history = await scoring_service.get_score_history(
        region_code, start_year, end_year
    )
    return {
        "region_code": region_code,
        "start_year": start_year,
        "end_year": end_year,
        "history": history,
    }


@router.get("/gap-analysis")
async def get_gap_analysis(
    year: Optional[int] = None,
):
    """
    Get gap analysis showing disparity between regions.
    """
    analysis = await scoring_service.calculate_gap_analysis(year)
    return analysis


@router.post("/recalculate")
async def recalculate_scores(
    year: Optional[int] = None,
    force: bool = Query(False, description="Force recalculation"),
):
    """
    Trigger score recalculation for a year.
    """
    result = await scoring_service.recalculate_scores(year=year, force=force)
    return result


@router.get("/years")
async def get_available_years():
    """
    Get list of years with available score data.
    """
    years = await scoring_service.get_available_years()
    return {"years": years}
