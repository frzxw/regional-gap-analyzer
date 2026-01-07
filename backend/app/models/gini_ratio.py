"""
Gini Ratio models for API request/response.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class SemesterData(BaseModel):
    """Semester data with urban, rural, and total values."""
    
    perkotaan: Optional[float] = Field(None, description="Urban/City value")
    perdesaan: Optional[float] = Field(None, description="Rural value")
    total: Optional[float] = Field(None, description="Total value")


class GiniRatioRecord(BaseModel):
    """Complete gini ratio record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: gini_ratio")
    data_semester_1: Optional[SemesterData] = None
    data_semester_2: Optional[SemesterData] = None
    data_tahunan: Optional[SemesterData] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value: Any) -> str:
        """Convert ObjectId to string."""
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)

    class Config:
        populate_by_name = True


class GiniRatioResponse(BaseModel):
    """Response model for gini ratio data."""
    
    data: GiniRatioRecord
    status: str = "success"


class GiniRatioListResponse(BaseModel):
    """Response model for list of gini ratio records."""
    
    data: list[GiniRatioRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
