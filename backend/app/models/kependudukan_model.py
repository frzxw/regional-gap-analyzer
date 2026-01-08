"""
Pydantic models for kependudukan.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DataKependudukan(BaseModel):
    """Data kependudukan lengkap."""
    jumlah_penduduk_ribu: Optional[float] = Field(None, description="Jumlah penduduk dalam ribuan")
    laju_pertumbuhan_tahunan: Optional[float] = Field(None, description="Laju pertumbuhan penduduk per tahun")
    persentase_penduduk: Optional[float] = Field(None, description="Persentase penduduk")
    kepadatan_per_km2: Optional[float] = Field(None, description="Kepadatan penduduk per km2")
    rasio_jenis_kelamin: Optional[float] = Field(None, description="Rasio jenis kelamin penduduk")


class KependudukanModel(BaseModel):
    """
    Kependudukan data model.
    
    Sesuai format dari ingest.py:
    - province_id: ID provinsi
    - tahun: Tahun data
    - indikator: "kependudukan"
    - data: Object berisi semua field kependudukan
    """
    province_id: str = Field(..., description="ID provinsi")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(default="kependudukan", description="Nama indikator")
    data: DataKependudukan = Field(..., description="Data kependudukan")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "kependudukan",
                "data": {
                    "jumlah_penduduk_ribu": 45123.45,
                    "laju_pertumbuhan_tahunan": 1.23,
                    "persentase_penduduk": 15.67,
                    "kepadatan_per_km2": 234.56,
                    "rasio_jenis_kelamin": 102.34
                }
            }
        }


class KependudukanCreateRequest(BaseModel):
    """Request model for creating kependudukan data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    data: DataKependudukan


class KependudukanUpdateRequest(BaseModel):
    """Request model for updating kependudukan data."""
    data: Optional[DataKependudukan] = None
    value: Optional[float] = Field(None, description="Simplified value field for single-value updates")


class KependudukanResponse(BaseModel):
    """Response model for kependudukan."""
    province_id: str
    tahun: int
    indikator: str
    data: DataKependudukan
    created_at: datetime
    updated_at: datetime
