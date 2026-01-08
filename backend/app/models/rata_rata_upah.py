"""
Rata-rata Upah Bersih (Average Net Wage) models for API request/response.
"""

from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class SectorWageData(BaseModel):
    """Wage data for a sector (februari, agustus, tahunan)."""
    
    februari: Optional[float] = Field(None, description="February wage")
    agustus: Optional[float] = Field(None, description="August wage")
    tahunan: Optional[float] = Field(None, description="Annual wage")


class RataRataUpahBersihRecord(BaseModel):
    """Complete average net wage record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: rata_rata_upah_bersih")
    sektor: Dict[str, SectorWageData] = Field(default_factory=dict, description="Wage data by sector")
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


class RataRataUpahBersihResponse(BaseModel):
    """Response model for average net wage data."""
    
    data: RataRataUpahBersihRecord
    status: str = "success"


class RataRataUpahBersihListResponse(BaseModel):
    """Response model for list of average net wage records."""
    
    data: list[RataRataUpahBersihRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
