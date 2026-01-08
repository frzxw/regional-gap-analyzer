"""
Pydantic models for pdrb_per_kapita.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PDRBPerKapitaModel(BaseModel):
    """
    PDRB Per Kapita data model.
    
    Sesuai format dari ingest.py - bisa ADHB atau ADHK:
    - province_id: ID provinsi
    - tahun: Tahun data
    - indikator: "pdrb_per_kapita_adhb" atau "pdrb_per_kapita_adhk_2010"
    - data_ribu_rp: PDRB per kapita dalam ribu rupiah
    """
    province_id: str = Field(..., description="ID provinsi")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(..., description="Jenis PDRB: pdrb_per_kapita_adhb atau pdrb_per_kapita_adhk_2010")
    data_ribu_rp: Optional[float] = Field(None, description="PDRB per kapita dalam ribu rupiah")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "pdrb_per_kapita_adhb",
                "data_ribu_rp": 75432.56
            }
        }


class PDRBPerKapitaCreateRequest(BaseModel):
    """Request model for creating PDRB per kapita data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    indikator: str = Field(..., description="pdrb_per_kapita_adhb atau pdrb_per_kapita_adhk_2010")
    data_ribu_rp: Optional[float] = None


class PDRBPerKapitaUpdateRequest(BaseModel):
    """Request model for updating PDRB per kapita data."""
    data_ribu_rp: Optional[float] = None
    value: Optional[float] = Field(None, description="Simplified value field for single-value updates")


class PDRBPerKapitaResponse(BaseModel):
    """Response model for PDRB per kapita."""
    province_id: str
    tahun: int
    indikator: str
    data_ribu_rp: Optional[float]
    created_at: datetime
    updated_at: datetime
