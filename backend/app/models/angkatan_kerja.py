"""
Pydantic models for angkatan_kerja (Labor Force).
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DataPeriode(BaseModel):
    """Data untuk periode tertentu (Februari/Agustus)."""
    bekerja: int = Field(..., description="Jumlah penduduk bekerja")
    pengangguran: int = Field(..., description="Jumlah pengangguran")
    jumlah_ak: int = Field(..., description="Jumlah angkatan kerja")
    persentase_bekerja_ak: float = Field(..., description="Persentase bekerja dari angkatan kerja")


class AngkatanKerjaModel(BaseModel):
    """
    Angkatan Kerja data model.
    
    Sesuai format dari ingest_ak.py:
    - province_id: ID provinsi (dari MongoDB provinces)
    - tahun: Tahun data
    - indikator: "angkatan_kerja"
    - data_februari: Data periode Februari
    - data_agustus: Data periode Agustus
    """
    province_id: str = Field(..., description="ID provinsi (ObjectId dari collection provinces)")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(default="angkatan_kerja", description="Nama indikator")
    data_februari: DataPeriode = Field(..., description="Data periode Februari")
    data_agustus: DataPeriode = Field(..., description="Data periode Agustus")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "angkatan_kerja",
                "data_februari": {
                    "bekerja": 15000000,
                    "pengangguran": 500000,
                    "jumlah_ak": 15500000,
                    "persentase_bekerja_ak": 96.77
                },
                "data_agustus": {
                    "bekerja": 15200000,
                    "pengangguran": 480000,
                    "jumlah_ak": 15680000,
                    "persentase_bekerja_ak": 96.94
                }
            }
        }


class AngkatanKerjaCreateRequest(BaseModel):
    """Request model for creating angkatan kerja data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    data_februari: DataPeriode
    data_agustus: DataPeriode


class AngkatanKerjaUpdateRequest(BaseModel):
    """Request model for updating angkatan kerja data."""
    data_februari: Optional[DataPeriode] = None
    data_agustus: Optional[DataPeriode] = None
    value: Optional[float] = Field(None, description="Simplified value field for single-value updates")


class AngkatanKerjaResponse(BaseModel):
    """Response model for angkatan kerja."""
    province_id: str
    tahun: int
    indikator: str
    data_februari: DataPeriode
    data_agustus: DataPeriode
    created_at: datetime
    updated_at: datetime
