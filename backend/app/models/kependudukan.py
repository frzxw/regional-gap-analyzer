"""
Kependudukan (Population) models for API request/response.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class PopulationData(BaseModel):
    """Population data metrics."""
    
    jumlah_penduduk_ribu: Optional[float] = Field(None, description="Population in thousands")
    laju_pertumbuhan_tahunan: Optional[float] = Field(None, description="Annual growth rate")
    persentase_penduduk: Optional[float] = Field(None, description="Population percentage")
    kepadatan_per_km2: Optional[float] = Field(None, description="Density per square km")
    rasio_jenis_kelamin: Optional[float] = Field(None, description="Sex ratio")


class KependudukanRecord(BaseModel):
    """Complete population record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: kependudukan")
    data: Optional[PopulationData] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value: Any) -> str:
        """Convert ObjectId to string."""
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)

    class Config:
        populate_by_name = True


class KependudukanResponse(BaseModel):
    """Response model for population data."""
    
    data: KependudukanRecord
    status: str = "success"


class KependudukanListResponse(BaseModel):
    """Response model for list of population records."""
    
    data: list[KependudukanRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
