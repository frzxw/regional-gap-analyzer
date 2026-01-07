"""
Persentase Penduduk Miskin (Poverty Rate) models for API request/response.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class SemesterPovertyData(BaseModel):
    """Semester poverty data with urban, rural, and total breakdown."""
    
    perkotaan: Optional[float] = Field(None, description="Urban poverty rate")
    perdesaan: Optional[float] = Field(None, description="Rural poverty rate")
    total: Optional[float] = Field(None, description="Total poverty rate")


class PersentasePendudukMiskinRecord(BaseModel):
    """Complete poverty rate record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: persentase_penduduk_miskin")
    data_semester_1: Optional[SemesterPovertyData] = None
    data_semester_2: Optional[SemesterPovertyData] = None
    data_tahunan: Optional[SemesterPovertyData] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value: Any) -> str:
        """Convert ObjectId to string."""
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)

    class Config:
        populate_by_name = True


class PersentasePendudukMiskinResponse(BaseModel):
    """Response model for poverty rate data."""
    
    data: PersentasePendudukMiskinRecord
    status: str = "success"


class PersentasePendudukMiskinListResponse(BaseModel):
    """Response model for list of poverty rate records."""
    
    data: list[PersentasePendudukMiskinRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
