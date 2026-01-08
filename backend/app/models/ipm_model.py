"""
Pydantic models for indeks_pembangunan_manusia (IPM/HDI).
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class IndeksPembangunanManusiaModel(BaseModel):
    """
    Indeks Pembangunan Manusia (IPM) data model.
    
    Sesuai format dari ingest.py:
    - province_id: ID provinsi
    - tahun: Tahun data
    - indikator: "indeks_pembangunan_manusia"
    - data: Nilai IPM
    """
    province_id: str = Field(..., description="ID provinsi")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(default="indeks_pembangunan_manusia", description="Nama indikator")
    data: Optional[float] = Field(None, description="Nilai IPM")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "indeks_pembangunan_manusia",
                "data": 75.44
            }
        }


class IPMCreateRequest(BaseModel):
    """Request model for creating IPM data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    data: Optional[float] = None


class IPMUpdateRequest(BaseModel):
    """Request model for updating IPM data."""
    data: Optional[float] = None
    value: Optional[float] = Field(None, description="Simplified value field for single-value updates")


class IPMResponse(BaseModel):
    """Response model for IPM."""
    province_id: str
    tahun: int
    indikator: str
    data: Optional[float]
    created_at: datetime
    updated_at: datetime
