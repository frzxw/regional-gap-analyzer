"""
Labor Force (Angkatan Kerja) models for API request/response.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class MonthlyLaborData(BaseModel):
    """Monthly labor data for a specific month."""
    
    bekerja: int = Field(..., description="Number of employed")
    pengangguran: int = Field(..., description="Number of unemployed")
    jumlah_ak: int = Field(..., description="Total labor force")
    persentase_bekerja_ak: float = Field(..., description="Percentage of employed in labor force")


class LaborForceRecord(BaseModel):
    """Complete labor force record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: angkatan_kerja")
    data_januari: Optional[MonthlyLaborData] = None
    data_februari: Optional[MonthlyLaborData] = None
    data_maret: Optional[MonthlyLaborData] = None
    data_april: Optional[MonthlyLaborData] = None
    data_mei: Optional[MonthlyLaborData] = None
    data_juni: Optional[MonthlyLaborData] = None
    data_juli: Optional[MonthlyLaborData] = None
    data_agustus: Optional[MonthlyLaborData] = None
    data_september: Optional[MonthlyLaborData] = None
    data_oktober: Optional[MonthlyLaborData] = None
    data_november: Optional[MonthlyLaborData] = None
    data_desember: Optional[MonthlyLaborData] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value: Any) -> str:
        """Convert ObjectId to string."""
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)

    class Config:
        populate_by_name = True


class LaborForceResponse(BaseModel):
    """Response model for labor force data."""
    
    data: LaborForceRecord
    status: str = "success"


class LaborForceListResponse(BaseModel):
    """Response model for list of labor force records."""
    
    data: list[LaborForceRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
