"""
Pydantic models for persentase_penduduk_miskin.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DataSemesterKemiskinan(BaseModel):
    """Data persentase penduduk miskin per semester."""
    perkotaan: Optional[float] = Field(None, description="Persentase perkotaan")
    perdesaan: Optional[float] = Field(None, description="Persentase perdesaan")
    total: Optional[float] = Field(None, description="Persentase total")


class PersentasePendudukMiskinModel(BaseModel):
    """
    Persentase Penduduk Miskin data model.
    
    Sesuai format dari ingest.py:
    - province_id: ID provinsi
    - tahun: Tahun data
    - indikator: "persentase_penduduk_miskin"
    - data_semester_1: Data semester 1 (Maret)
    - data_semester_2: Data semester 2 (September)
    - data_tahunan: Data tahunan
    """
    province_id: str = Field(..., description="ID provinsi")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(default="persentase_penduduk_miskin", description="Nama indikator")
    data_semester_1: DataSemesterKemiskinan = Field(..., description="Data semester 1 (Maret)")
    data_semester_2: DataSemesterKemiskinan = Field(..., description="Data semester 2 (September)")
    data_tahunan: DataSemesterKemiskinan = Field(..., description="Data tahunan")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "persentase_penduduk_miskin",
                "data_semester_1": {"perkotaan": 7.53, "perdesaan": 12.63, "total": 9.54},
                "data_semester_2": {"perkotaan": 7.72, "perdesaan": 12.82, "total": 9.73},
                "data_tahunan": {"perkotaan": 7.63, "perdesaan": 12.73, "total": 9.64}
            }
        }


class PersentasePendudukMiskinCreateRequest(BaseModel):
    """Request model for creating persentase_penduduk_miskin data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    data_semester_1: DataSemesterKemiskinan
    data_semester_2: DataSemesterKemiskinan
    data_tahunan: DataSemesterKemiskinan


class PersentasePendudukMiskinUpdateRequest(BaseModel):
    """Request model for updating persentase_penduduk_miskin data."""
    data_semester_1: Optional[DataSemesterKemiskinan] = None
    data_semester_2: Optional[DataSemesterKemiskinan] = None
    data_tahunan: Optional[DataSemesterKemiskinan] = None


class PersentasePendudukMiskinResponse(BaseModel):
    """Response model for persentase_penduduk_miskin."""
    province_id: str
    tahun: int
    indikator: str
    data_semester_1: DataSemesterKemiskinan
    data_semester_2: DataSemesterKemiskinan
    data_tahunan: DataSemesterKemiskinan
    created_at: datetime
    updated_at: datetime
