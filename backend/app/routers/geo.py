"""
Geo router - API endpoints for geographic data.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.services import geo_service

router = APIRouter(prefix="/geo", tags=["Geographic Data"])


@router.get("/provinces")
async def get_provinces_geojson():
    """
    Get base GeoJSON for all Indonesian provinces.
    """
    geojson = await geo_service.get_geojson()
    return JSONResponse(content=geojson)


@router.get("/choropleth")
async def get_choropleth_data(
    year: Optional[int] = Query(None, description="Year (latest if not specified)"),
    metric: str = Query("composite_score", description="Metric to display"),
):
    """
    Get GeoJSON with score data for choropleth map visualization.
    """
    choropleth = await geo_service.get_choropleth_data(year=year, metric=metric)
    return JSONResponse(content=choropleth)


@router.get("/province/{region_code}")
async def get_province_boundary(region_code: str):
    """
    Get GeoJSON feature for a specific province.
    """
    feature = await geo_service.get_region_boundary(region_code)
    if not feature:
        raise HTTPException(
            status_code=404,
            detail=f"Province {region_code} not found",
        )
    return JSONResponse(content=feature)


@router.get("/color-scale")
async def get_color_scale(
    min_value: float = Query(0, description="Minimum value"),
    max_value: float = Query(100, description="Maximum value"),
    palette: str = Query("RdYlGn", description="Color palette"),
):
    """
    Get color scale configuration for map legend.
    """
    scale = geo_service.get_color_scale(min_value, max_value, palette)
    return {
        "palette": palette,
        "min": min_value,
        "max": max_value,
        "stops": scale,
    }
