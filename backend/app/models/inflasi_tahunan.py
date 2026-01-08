"""
Inflasi Tahunan (Annual Inflation) models for API request/response.
"""

from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class InflasiTahunanRecord(BaseModel):
    """Complete annual inflation record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: inflasi_tahunan")
    data_bulanan: Dict[str, Optional[float]] = Field(default_factory=dict, description="Monthly inflation data (januari-desember)")
    tahunan: Optional[float] = Field(None, description="Annual inflation")
    source: Optional[str] = Field(None, description="Data source")

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value: Any) -> str:
        """Convert ObjectId to string."""
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)

    class Config:
        populate_by_name = True


class InflasiTahunanResponse(BaseModel):
    """Response model for annual inflation data."""
    
    data: InflasiTahunanRecord
    status: str = "success"


class InflasiTahunanListResponse(BaseModel):
    """Response model for list of annual inflation records."""
    
    data: list[InflasiTahunanRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
