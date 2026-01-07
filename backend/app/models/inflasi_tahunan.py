"""
Inflasi Tahunan (Annual Inflation) models for API request/response.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class MonthlyInflationData(BaseModel):
    """Monthly inflation data."""
    
    januari: Optional[float] = Field(None, description="January inflation")
    februari: Optional[float] = Field(None, description="February inflation")
    maret: Optional[float] = Field(None, description="March inflation")
    april: Optional[float] = Field(None, description="April inflation")
    mei: Optional[float] = Field(None, description="May inflation")
    juni: Optional[float] = Field(None, description="June inflation")
    juli: Optional[float] = Field(None, description="July inflation")
    agustus: Optional[float] = Field(None, description="August inflation")
    september: Optional[float] = Field(None, description="September inflation")
    oktober: Optional[float] = Field(None, description="October inflation")
    november: Optional[float] = Field(None, description="November inflation")
    desember: Optional[float] = Field(None, description="December inflation")
    tahunan: Optional[float] = Field(None, description="Annual inflation")


class InflasiTahunanRecord(BaseModel):
    """Complete annual inflation record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: inflasi_tahunan")
    data_bulanan: Optional[MonthlyInflationData] = None

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
