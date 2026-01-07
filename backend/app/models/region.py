"""
Pydantic models for regions.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime


class GeometryModel(BaseModel):
    """
    GeoJSON geometry model.
    """
    type: str = Field(..., description="Geometry type (Polygon, MultiPolygon, etc.)")
    coordinates: List[Any] = Field(..., description="Geometry coordinates array")


class RegionModel(BaseModel):
    """
    Region data model representing a province (SESUAI FORMAT indonesia-38.json).
    
    Structure follows GeoJSON Feature from indonesia-38.json:
    - id: Unique identifier
    - KODE_PROV: BPS province code (e.g., "31", "72")
    - PROVINSI: Province name (e.g., "DKI Jakarta")
    - geometry: GeoJSON geometry object
    
    Note: NO population or area_km2 fields - these are NOT in the official source data.
    """

    id: str = Field(..., description="ID unik region")
    KODE_PROV: str = Field(..., description="Kode provinsi BPS")
    PROVINSI: str = Field(..., description="Nama provinsi")
    geometry: Optional[GeometryModel] = Field(None, description="GeoJSON geometry object")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "31",
                "KODE_PROV": "31",
                "PROVINSI": "DKI Jakarta",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[106.7, -6.1], [106.9, -6.1], [106.9, -6.3], [106.7, -6.3], [106.7, -6.1]]]
                }
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
