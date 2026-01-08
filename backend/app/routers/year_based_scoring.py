"""
Year-based scoring router - API endpoints for year-based scoring.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field

from app.services.year_based_scoring_service import year_based_scoring_service


router = APIRouter(
    prefix="/year-scores",
    tags=["Year-Based Scoring"]
)


# Response Models
class CollectionScore(BaseModel):
    """Score for a single collection."""
    collection: str
    display_name: str
    raw_value: float
    score: float
    min_value: float
    max_value: float
    lower_is_better: bool


class ProvinceScore(BaseModel):
    """Composite score for a province."""
    province_id: str
    province_name: str
    year: int
    composite_score: float
    rank: Optional[int] = None
    collections_scored: int


class ProvinceScoreDetailed(ProvinceScore):
    """Detailed province score with collection breakdown."""
    collection_scores: dict


class ScoreBreakdown(BaseModel):
    """Detailed score breakdown."""
    province_id: str
    province_name: Optional[str] = None
    year: int
    composite_score: Optional[float] = None
    rank: Optional[int] = None
    collections: List[CollectionScore]


class YearsResponse(BaseModel):
    """Available years response."""
    years: List[int]
    count: int


class ProvinceInfo(BaseModel):
    """Basic province information."""
    province_id: str
    province_name: str
    score: float


class NationalStatistics(BaseModel):
    """National statistics for a year."""
    year: int
    median_score: float
    leader: Optional[ProvinceInfo] = None
    critical: Optional[ProvinceInfo] = None
    total_population: int
    provinces_count: int


@router.get(
    "/available-years",
    response_model=YearsResponse,
    summary="Get available years"
)
async def get_available_years():
    """
    Get list of years that have data in any collection.
    
    Returns:
        List of available years sorted ascending
    """
    years = await year_based_scoring_service.get_available_years()
    return YearsResponse(years=years, count=len(years))


@router.get(
    "/{year}/statistics",
    response_model=NationalStatistics,
    summary="Get national statistics for a year"
)
async def get_national_statistics(
    year: int = Path(..., description="Year to get statistics for", ge=2000, le=2100)
):
    """
    Get national statistics including median score, leader, critical province, and population.
    
    Args:
        year: Year to calculate statistics for
        
    Returns:
        National statistics for the year
    """
    stats = await year_based_scoring_service.get_national_statistics(year)
    
    if not stats:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for year {year}"
        )
    
    return stats


@router.get("/_test/{year}")
async def test_data(year: int):
    """Test endpoint to see what data we can get"""
    result = {}
    for collection_name in year_based_scoring_service.COLLECTION_CONFIGS.keys():
        data = await year_based_scoring_service.get_collection_data_for_year(collection_name, year)
        result[collection_name] = {
            "count": len(data),
            "sample": data[:2] if data else []
        }
    return result


@router.get(
    "/debug-data/{collection}/{year}",
    summary="Debug: Get raw data from collection"
)
async def debug_collection_data(
    collection: str = Path(..., description="Collection name"),
    year: int = Path(..., description="Year", ge=2000, le=2100)
):
    """
    Debug endpoint to see raw data from a collection.
    """
    data = await year_based_scoring_service.get_collection_data_for_year(collection, year)
    return {
        "collection": collection,
        "year": year,
        "count": len(data),
        "data": data[:5] if len(data) > 5 else data  # Show first 5 items
    }


@router.get(
    "/{year}",
    response_model=List[ProvinceScoreDetailed],
    summary="Get all province scores for a year"
)
async def get_scores_for_year(
    year: int = Path(..., description="Year to get scores for", ge=2000, le=2100)
):
    """
    Get composite scores for all provinces in a specific year.
    
    Args:
        year: Year to calculate scores for
        
    Returns:
        List of province scores sorted by rank (best to worst)
    """
    scores = await year_based_scoring_service.calculate_all_scores_for_year(year)
    
    if not scores:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for year {year}"
        )
    
    return scores


@router.get(
    "/{year}/top",
    response_model=List[ProvinceScoreDetailed],
    summary="Get top performing provinces"
)
async def get_top_provinces(
    year: int = Path(..., description="Year", ge=2000, le=2100),
    count: int = Query(5, description="Number of top provinces to return", ge=1, le=50)
):
    """
    Get top performing provinces for a specific year.
    
    Args:
        year: Year
        count: Number of provinces to return
        
    Returns:
        List of top provinces sorted by score (descending)
    """
    all_scores = await year_based_scoring_service.calculate_all_scores_for_year(year)
    
    if not all_scores:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for year {year}"
        )
    
    return all_scores[:count]


@router.get(
    "/{year}/bottom",
    response_model=List[ProvinceScoreDetailed],
    summary="Get bottom performing provinces"
)
async def get_bottom_provinces(
    year: int = Path(..., description="Year", ge=2000, le=2100),
    count: int = Query(5, description="Number of bottom provinces to return", ge=1, le=50)
):
    """
    Get bottom performing provinces for a specific year.
    
    Args:
        year: Year
        count: Number of provinces to return
        
    Returns:
        List of bottom provinces sorted by score (ascending)
    """
    all_scores = await year_based_scoring_service.calculate_all_scores_for_year(year)
    
    if not all_scores:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for year {year}"
        )
    
    return all_scores[-count:][::-1]  # Reverse to show worst first


@router.get(
    "/{year}/{province_id}",
    response_model=ProvinceScoreDetailed,
    summary="Get specific province score for a year"
)
async def get_province_score(
    year: int = Path(..., description="Year", ge=2000, le=2100),
    province_id: str = Path(..., description="Province ID")
):
    """
    Get composite score for a specific province in a specific year.
    
    Args:
        year: Year
        province_id: Province ID
        
    Returns:
        Province score with collection breakdown
    """
    score = await year_based_scoring_service.calculate_composite_score(
        province_id, 
        year
    )
    
    if not score:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for province {province_id} in year {year}"
        )
    
    return score


@router.get(
    "/{year}/{province_id}/breakdown",
    response_model=ScoreBreakdown,
    summary="Get detailed score breakdown"
)
async def get_score_breakdown(
    year: int = Path(..., description="Year", ge=2000, le=2100),
    province_id: str = Path(..., description="Province ID")
):
    """
    Get detailed score breakdown showing raw values and scores for each collection.
    
    Args:
        year: Year
        province_id: Province ID
        
    Returns:
        Detailed breakdown with raw values, scores, and min/max for each collection
    """
    breakdown = await year_based_scoring_service.get_score_breakdown(
        province_id,
        year
    )
    
    if not breakdown:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for province {province_id} in year {year}"
        )
    
    return breakdown
