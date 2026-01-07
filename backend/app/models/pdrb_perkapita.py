"""
PDRB Per Kapita (GDP Per Capita) models for API request/response.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class PdrbPerkapitaData(BaseModel):
    """PDRB per capita data."""
    
    data_ribu_rp: Optional[float] = Field(None, description="GDP per capita in thousands of Rupiah")


class PdrbPerkapitaRecord(BaseModel):
    """Complete PDRB per capita record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: pdrb_per_kapita_adhb")
    data: Optional[PdrbPerkapitaData] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value: Any) -> str:
        """Convert ObjectId to string."""
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)

    class Config:
        populate_by_name = True


class PdrbPerkapitaResponse(BaseModel):
    """Response model for PDRB per capita data."""
    
    data: PdrbPerkapitaRecord
    status: str = "success"


class PdrbPerkapitaListResponse(BaseModel):
    """Response model for list of PDRB per capita records."""
    
    data: list[PdrbPerkapitaRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
