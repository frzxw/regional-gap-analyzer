"""
Rata-rata Upah Bersih (Average Net Wage) models for API request/response.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class SectorWageData(BaseModel):
    """Monthly wage data for a sector."""
    
    januari: Optional[float] = Field(None, description="January wage")
    februari: Optional[float] = Field(None, description="February wage")
    maret: Optional[float] = Field(None, description="March wage")
    april: Optional[float] = Field(None, description="April wage")
    mei: Optional[float] = Field(None, description="May wage")
    juni: Optional[float] = Field(None, description="June wage")
    juli: Optional[float] = Field(None, description="July wage")
    agustus: Optional[float] = Field(None, description="August wage")
    september: Optional[float] = Field(None, description="September wage")
    oktober: Optional[float] = Field(None, description="October wage")
    november: Optional[float] = Field(None, description="November wage")
    desember: Optional[float] = Field(None, description="December wage")
    tahunan: Optional[float] = Field(None, description="Annual wage")


class WageSektor(BaseModel):
    """All sectors wage data."""
    
    pertanian_kehutanan_perikanan: Optional[SectorWageData] = None
    pertambangan_penggalian: Optional[SectorWageData] = None
    industri_pengolahan: Optional[SectorWageData] = None
    listrik_gas: Optional[SectorWageData] = None
    air_sampah_limbah_daurlulang: Optional[SectorWageData] = None
    konstruksi: Optional[SectorWageData] = None
    perdagangan: Optional[SectorWageData] = None
    transportasi_pergudangan: Optional[SectorWageData] = None
    akomodasi_makan_minum: Optional[SectorWageData] = None
    informasi_komunikasi: Optional[SectorWageData] = None
    jasa_keuangan: Optional[SectorWageData] = None
    real_estate: Optional[SectorWageData] = None
    jasa_perusahaan: Optional[SectorWageData] = None
    admin_pemerintahan: Optional[SectorWageData] = None
    jasa_pendidikan: Optional[SectorWageData] = None
    jasa_kesehatan: Optional[SectorWageData] = None
    jasa_lainnya: Optional[SectorWageData] = None
    total: Optional[SectorWageData] = None


class RataRataUpahBersihRecord(BaseModel):
    """Complete average net wage record for a year and province."""
    
    id: str = Field(..., alias="_id", description="Document ID")
    province_id: str = Field(..., description="Province code")
    province_name: Optional[str] = Field(None, description="Province name")
    tahun: int = Field(..., description="Year of data")
    indikator: str = Field(..., description="Indicator type: rata_rata_upah_bersih")
    sektor: Optional[WageSektor] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value: Any) -> str:
        """Convert ObjectId to string."""
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)

    class Config:
        populate_by_name = True


class RataRataUpahBersihResponse(BaseModel):
    """Response model for average net wage data."""
    
    data: RataRataUpahBersihRecord
    status: str = "success"


class RataRataUpahBersihListResponse(BaseModel):
    """Response model for list of average net wage records."""
    
    data: list[RataRataUpahBersihRecord]
    total: int
    skip: int
    limit: int
    status: str = "success"
