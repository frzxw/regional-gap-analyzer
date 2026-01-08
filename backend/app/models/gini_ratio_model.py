"""
Pydantic models for gini_ratio.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DataSemester(BaseModel):
    """Data gini ratio per semester."""
    perkotaan: Optional[float] = Field(None, description="Gini ratio perkotaan")
    perdesaan: Optional[float] = Field(None, description="Gini ratio perdesaan")
    total: Optional[float] = Field(None, description="Gini ratio total")


class GiniRatioModel(BaseModel):
    """
    Gini Ratio data model.
    
    Sesuai format dari ingest.py:
    - province_id: ID provinsi
    - tahun: Tahun data
    - indikator: "gini_ratio"
    - data_semester_1: Data semester 1 (Maret)
    - data_semester_2: Data semester 2 (September)
    - data_tahunan: Data tahunan
    """
    province_id: str = Field(..., description="ID provinsi")
    tahun: int = Field(..., ge=1900, le=2100, description="Tahun data")
    indikator: str = Field(default="gini_ratio", description="Nama indikator")
    data_semester_1: DataSemester = Field(..., description="Data semester 1 (Maret)")
    data_semester_2: DataSemester = Field(..., description="Data semester 2 (September)")
    data_tahunan: DataSemester = Field(..., description="Data tahunan")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "province_id": "507f1f77bcf86cd799439011",
                "tahun": 2025,
                "indikator": "gini_ratio",
                "data_semester_1": {"perkotaan": 0.385, "perdesaan": 0.312, "total": 0.365},
                "data_semester_2": {"perkotaan": 0.390, "perdesaan": 0.315, "total": 0.368},
                "data_tahunan": {"perkotaan": 0.388, "perdesaan": 0.314, "total": 0.367}
            }
        }


class GiniRatioCreateRequest(BaseModel):
    """Request model for creating gini_ratio data."""
    province_id: str
    tahun: int = Field(..., ge=1900, le=2100)
    data_semester_1: DataSemester
    data_semester_2: DataSemester
    data_tahunan: DataSemester


class GiniRatioUpdateRequest(BaseModel):
    """Request model for updating gini_ratio data."""
    data_semester_1: Optional[DataSemester] = None
    data_semester_2: Optional[DataSemester] = None
    data_tahunan: Optional[DataSemester] = None
    value: Optional[float] = Field(None, description="Simplified value field for single-value updates")


class GiniRatioResponse(BaseModel):
    """Response model for gini_ratio - flexible to handle both old and new format."""
    province_id: str
    tahun: int
    indikator: Optional[str] = None
    indicator_code: Optional[str] = None
    value: Optional[float] = None  # For imported data
    data_semester_1: Optional[DataSemester] = None  # For old format
    data_semester_2: Optional[DataSemester] = None
    data_tahunan: Optional[DataSemester] = None
    source: Optional[str] = None
    source_name: Optional[str] = None
    province_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    imported_at: Optional[datetime] = None

    class Config:
        extra = "ignore"  # Ignore extra fields

