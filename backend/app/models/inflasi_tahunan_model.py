"""
Pydantic models for inflasi_tahunan.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class InflasiTahunanModel(BaseModel):
    """
    Inflasi Tahunan data model.
    
    Sesuai format dari ingest.py:
    - province_id: ID provinsi
    - tahun: Tahun data
    - indikator: "inflasi_tahunan"
    - data_bulanan: Dictionary dengan key bulan (januari, februari, dst)
    - tahunan: Data tahunan
    """
    province_id: str = Field(..., description="ID provinsi")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(default="inflasi_tahunan", description="Nama indikator")
    data_bulanan: Dict[str, Optional[float]] = Field(..., description="Data bulanan (januari-desember)")
    tahunan: Optional[float] = Field(None, description="Data tahunan")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "inflasi_tahunan",
                "data_bulanan": {
                    "januari": 2.23, "februari": 2.45, "maret": 2.67,
                    "april": 2.89, "mei": 3.12, "juni": 3.34,
                    "juli": 3.56, "agustus": 3.78, "september": 4.01,
                    "oktober": 4.23, "november": 4.45, "desember": 4.67
                },
                "tahunan": 3.42
            }
        }


class InflasiTahunanCreateRequest(BaseModel):
    """Request model for creating inflasi_tahunan data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    data_bulanan: Dict[str, Optional[float]]
    tahunan: Optional[float] = None


class InflasiTahunanUpdateRequest(BaseModel):
    """Request model for updating inflasi_tahunan data."""
    data_bulanan: Optional[Dict[str, Optional[float]]] = None
    tahunan: Optional[float] = None


class InflasiTahunanResponse(BaseModel):
    """Response model for inflasi_tahunan."""
    province_id: str
    tahun: int
    indikator: str
    data_bulanan: Dict[str, Optional[float]]
    tahunan: Optional[float]
    created_at: datetime
    updated_at: datetime
