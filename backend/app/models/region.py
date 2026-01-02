"""
Pydantic models for regions.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RegionModel(BaseModel):
    """
    Region data model representing a province/region.
    """

    code: str = Field(..., description="Unique region code (e.g., 'ID-JK' for Jakarta)")
    name: str = Field(..., description="Region name")
    province: str = Field(..., description="Province name")
    population: Optional[int] = Field(None, description="Population count")
    area_km2: Optional[float] = Field(None, description="Area in square kilometers")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "code": "ID-JK",
                "name": "DKI Jakarta",
                "province": "DKI Jakarta",
                "population": 10562088,
                "area_km2": 664.01,
            }
        }


class RegionScoreModel(BaseModel):
    """
    Scoring data for a region.
    Contains normalized indicators for inequality analysis.
    """

    region_code: str = Field(..., description="Reference to region code")
    year: int = Field(..., description="Year of the data")

    # Economic indicators (normalized 0-100)
    gdp_per_capita_score: Optional[float] = Field(None, ge=0, le=100)
    unemployment_score: Optional[float] = Field(None, ge=0, le=100)
    poverty_rate_score: Optional[float] = Field(None, ge=0, le=100)

    # Infrastructure indicators
    road_density_score: Optional[float] = Field(None, ge=0, le=100)
    electricity_access_score: Optional[float] = Field(None, ge=0, le=100)
    internet_access_score: Optional[float] = Field(None, ge=0, le=100)

    # Health indicators
    hospital_beds_score: Optional[float] = Field(None, ge=0, le=100)
    life_expectancy_score: Optional[float] = Field(None, ge=0, le=100)

    # Education indicators
    literacy_rate_score: Optional[float] = Field(None, ge=0, le=100)
    school_enrollment_score: Optional[float] = Field(None, ge=0, le=100)

    # Composite score
    composite_score: Optional[float] = Field(None, ge=0, le=100)

    created_at: datetime = Field(default_factory=datetime.utcnow)


class GeoFeatureModel(BaseModel):
    """
    GeoJSON feature for a region.
    Used for map visualization.
    """

    region_code: str
    geometry_type: str = "MultiPolygon"
    # Note: Actual geometry stored separately or in MongoDB as GeoJSON
    centroid_lat: Optional[float] = None
    centroid_lng: Optional[float] = None
