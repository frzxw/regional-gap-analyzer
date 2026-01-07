"""
API routes for unemployment analysis, scoring, and regional gap detection.
"""

from fastapi import APIRouter, HTTPException, Query, Path
from app.services.unemployment_analysis_service import UnemploymentAnalysisService
from app.models.unemployment_analysis import RegionalGapAnalysis, ComparisonAnalysis

router = APIRouter(
    prefix="/analysis/unemployment",
    tags=["Unemployment Analysis"],
)


@router.get(
    "/regional-gap/{year}",
    response_model=RegionalGapAnalysis,
    summary="Analyze regional unemployment inequality",
    description="""
    Comprehensive regional gap analysis for unemployment rates.
    
    Features:
    - Scoring system (0-100 points)
    - Severity classification (Low/Medium/High/Critical)
    - Trend analysis (year-over-year comparison)
    - Automated alerts for problematic regions
    - Regional inequality gap index
    - Province rankings and percentiles
    
    Perfect for creating visualizations and identifying areas needing intervention.
    """
)
async def analyze_regional_gap(
    year: int = Path(..., description="Year to analyze", ge=2020, le=2030)
):
    """
    Analyze regional unemployment inequality for a specific year.
    
    Returns comprehensive analysis including:
    - Individual province scores and rankings
    - Trend analysis compared to previous year
    - Alerts for critical regions
    - National statistics and gap index
    """
    try:
        service = UnemploymentAnalysisService()
        analysis = await service.analyze_regional_gap(year)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get(
    "/compare",
    response_model=ComparisonAnalysis,
    summary="Compare unemployment trends between years",
    description="""
    Year-over-year comparison analysis.
    
    Shows:
    - Number of provinces that improved/worsened/stayed stable
    - Biggest improvement and decline
    - Detailed trend analysis for each province
    """
)
async def compare_years(
    year_from: int = Query(..., description="Starting year", ge=2020, le=2030),
    year_to: int = Query(..., description="Ending year", ge=2020, le=2030)
):
    """
    Compare unemployment trends between two years.
    
    Identifies provinces with improving or worsening conditions.
    """
    if year_from >= year_to:
        raise HTTPException(status_code=400, detail="year_from must be less than year_to")
    
    try:
        service = UnemploymentAnalysisService()
        comparison = await service.compare_years(year_from, year_to)
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@router.get(
    "/alerts/{year}",
    summary="Get critical alerts for a year",
    description="Get only provinces with critical or high severity alerts"
)
async def get_critical_alerts(
    year: int = Path(..., description="Year to check", ge=2020, le=2030)
):
    """Get provinces that need immediate attention."""
    try:
        service = UnemploymentAnalysisService()
        analysis = await service.analyze_regional_gap(year)
        
        # Filter provinces with alerts
        critical_provinces = [
            {
                "province_id": p.province_id,
                "province_name": p.province_name,
                "unemployment_rate": p.unemployment_rate,
                "score": p.score.score,
                "severity": p.score.severity,
                "alerts": p.alerts,
                "rank": p.rank
            }
            for p in analysis.provinces
            if p.alerts and any(a.severity in ["high", "critical"] for a in p.alerts)
        ]
        
        return {
            "year": year,
            "total_critical": len(critical_provinces),
            "provinces": critical_provinces,
            "status": "success"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get alerts: {str(e)}")
