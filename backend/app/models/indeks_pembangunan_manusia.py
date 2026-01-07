"""
Indeks Pembangunan Manusia (Human Development Index) models for API request/response.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class IndeksPembangunanManusiaRecord(BaseModel):
    """Complete human development index record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: indeks_pembangunan_manusia")
    data: Optional[float] = Field(None, description="Index value")

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value: Any) -> str:
        """Convert ObjectId to string."""
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)

    class Config:
        populate_by_name = True


class IndeksPembangunanManusiaResponse(BaseModel):
    """Response model for human development index data."""
    
    data: IndeksPembangunanManusiaRecord
    status: str = "success"


class IndeksPembangunanManusiaListResponse(BaseModel):
    """Response model for list of human development index records."""
    
    data: list[IndeksPembangunanManusiaRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
