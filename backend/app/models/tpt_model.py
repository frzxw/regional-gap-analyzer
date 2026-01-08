"""
Pydantic models for tingkat_pengangguran_terbuka (TPT).
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DataTPT(BaseModel):
    """Data Tingkat Pengangguran Terbuka."""
    februari: Optional[float] = Field(None, description="Data Februari")
    agustus: Optional[float] = Field(None, description="Data Agustus")
    tahunan: Optional[float] = Field(None, description="Data tahunan")


class TingkatPengangguranTerbukaModel(BaseModel):
    """
    Tingkat Pengangguran Terbuka (TPT) data model.
    
    Sesuai format dari ingest.py:
    - province_id: ID provinsi
    - tahun: Tahun data
    - indikator: "tingkat_pengangguran_terbuka"
    - data: Object {februari, agustus, tahunan}
    """
    province_id: str = Field(..., description="ID provinsi")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(default="tingkat_pengangguran_terbuka", description="Nama indikator")
    data: DataTPT = Field(..., description="Data TPT")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "tingkat_pengangguran_terbuka",
                "data": {
                    "februari": 5.67,
                    "agustus": 5.42,
                    "tahunan": 5.54
                }
            }
        }


class TPTCreateRequest(BaseModel):
    """Request model for creating TPT data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    data: DataTPT


class TPTUpdateRequest(BaseModel):
    """Request model for updating TPT data."""
    data: Optional[DataTPT] = None
    value: Optional[float] = Field(None, description="Simplified value field for single-value updates")


class TPTResponse(BaseModel):
    """Response model for TPT."""
    province_id: str
    tahun: int
    indikator: str
    data: DataTPT
    created_at: datetime
    updated_at: datetime
