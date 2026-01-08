"""
Indeks Harga Konsumen (Consumer Price Index) models for API request/response.
"""

from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class IndeksHargaKonsumenRecord(BaseModel):
    """Complete consumer price index record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: ihk_indeks_harga_konsumen")
    data_bulanan: Dict[str, Optional[float]] = Field(default_factory=dict, description="Monthly data (januari-desember)")
    tahunan: Optional[float] = Field(None, description="Annual index")
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


class IndeksHargaKonsumenResponse(BaseModel):
    """Response model for consumer price index data."""
    
    data: IndeksHargaKonsumenRecord
    status: str = "success"


class IndeksHargaKonsumenListResponse(BaseModel):
    """Response model for list of consumer price index records."""
    
    data: list[IndeksHargaKonsumenRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
