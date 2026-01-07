"""
Pydantic models for indeks_harga_konsumen (IHK).
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class IndeksHargaKonsumenModel(BaseModel):
    """
    Indeks Harga Konsumen (IHK) data model.
    
    Sesuai format dari ingest.py:
    - province_id: ID provinsi
    - tahun: Tahun data
    - indikator: "ihk_indeks_harga_konsumen"
    - data_bulanan: Dictionary dengan key bulan (januari, februari, dst)
    - tahunan: Data tahunan
    """
    province_id: str = Field(..., description="ID provinsi")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(default="ihk_indeks_harga_konsumen", description="Nama indikator")
    data_bulanan: Dict[str, Optional[float]] = Field(..., description="Data bulanan (januari-desember)")
    tahunan: Optional[float] = Field(None, description="Data tahunan")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "ihk_indeks_harga_konsumen",
                "data_bulanan": {
                    "januari": 105.23, "februari": 105.67, "maret": 106.12,
                    "april": 106.45, "mei": 106.89, "juni": 107.34,
                    "juli": 107.78, "agustus": 108.23, "september": 108.67,
                    "oktober": 109.12, "november": 109.56, "desember": 110.00
                },
                "tahunan": 107.25
            }
        }


class IHKCreateRequest(BaseModel):
    """Request model for creating IHK data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    data_bulanan: Dict[str, Optional[float]]
    tahunan: Optional[float] = None


class IHKUpdateRequest(BaseModel):
    """Request model for updating IHK data."""
    data_bulanan: Optional[Dict[str, Optional[float]]] = None
    tahunan: Optional[float] = None


class IHKResponse(BaseModel):
    """Response model for IHK."""
    province_id: str
    tahun: int
    indikator: str
    data_bulanan: Dict[str, Optional[float]]
    tahunan: Optional[float]
    created_at: datetime
    updated_at: datetime
