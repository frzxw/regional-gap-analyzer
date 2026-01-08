"""
Pydantic models for rata_rata_upah_bersih.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class DataPeriodeUpah(BaseModel):
    """Data upah untuk satu periode (Februari, Agustus, Tahunan)."""
    februari: Optional[float] = None
    agustus: Optional[float] = None
    tahunan: Optional[float] = None


class RataRataUpahBersihModel(BaseModel):
    """
    Rata-Rata Upah Bersih data model.
    
    Sesuai format dari ingest.py:
    - province_id: ID provinsi
    - tahun: Tahun data
    - indikator: "rata_rata_upah_bersih"
    - sektor: Dictionary dengan key nama sektor, value object {februari, agustus, tahunan}
    """
    province_id: str = Field(..., description="ID provinsi")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(default="rata_rata_upah_bersih", description="Nama indikator")
    sektor: Dict[str, DataPeriodeUpah] = Field(..., description="Data per sektor industri")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "rata_rata_upah_bersih",
                "sektor": {
                    "pertanian_kehutanan_perikanan": {"februari": 2500.0, "agustus": 2550.0, "tahunan": 2525.0},
                    "industri_pengolahan": {"februari": 3200.0, "agustus": 3250.0, "tahunan": 3225.0},
                    "total": {"februari": 2950.0, "agustus": 3000.0, "tahunan": 2975.0}
                }
            }
        }


class RataRataUpahBersihCreateRequest(BaseModel):
    """Request model for creating rata_rata_upah_bersih data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    sektor: Dict[str, DataPeriodeUpah]


class RataRataUpahBersihUpdateRequest(BaseModel):
    """Request model for updating rata_rata_upah_bersih data."""
    sektor: Optional[Dict[str, DataPeriodeUpah]] = None
    value: Optional[float] = Field(None, description="Simplified value field for single-value updates")


class RataRataUpahBersihResponse(BaseModel):
    """Response model for rata_rata_upah_bersih."""
    province_id: str
    tahun: int
    indikator: str
    sektor: Dict[str, DataPeriodeUpah]
    created_at: datetime
    updated_at: datetime
