"""
Tingkat Pengangguran Terbuka (Open Unemployment Rate) models for API request/response.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class UnemploymentData(BaseModel):
    """Unemployment rate data for different periods."""
    
    februari: Optional[float] = Field(None, description="February unemployment rate")
    agustus: Optional[float] = Field(None, description="August unemployment rate")
    tahunan: Optional[float] = Field(None, description="Annual unemployment rate")


class TingkatPengangguranTerbukaRecord(BaseModel):
    """Complete unemployment rate record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: tingkat_pengangguran_terbuka")
    data: Optional[UnemploymentData] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value: Any) -> str:
        """Convert ObjectId to string."""
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)

    class Config:
        populate_by_name = True


class TingkatPengangguranTerbukaResponse(BaseModel):
    """Response model for unemployment rate data."""
    
    data: TingkatPengangguranTerbukaRecord
    status: str = "success"


class TingkatPengangguranTerbukaListResponse(BaseModel):
    """Response model for list of unemployment rate records."""
    
    data: list[TingkatPengangguranTerbukaRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
