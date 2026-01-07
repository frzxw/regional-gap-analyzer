"""Routers module initialization."""

from app.routers.health import router as health_router
from app.routers.regions import router as regions_router

# CRUD routers (new)
from app.routers.angkatan_kerja_crud import router as angkatan_kerja_crud_router
from app.routers.gini_ratio_crud import router as gini_ratio_crud_router
from app.routers.ipm_crud import router as ipm_crud_router
from app.routers.persentase_penduduk_miskin_crud import router as persentase_penduduk_miskin_crud_router
from app.routers.ihk_crud import router as ihk_crud_router
from app.routers.inflasi_tahunan_crud import router as inflasi_tahunan_crud_router
from app.routers.kependudukan_crud import router as kependudukan_crud_router
from app.routers.pdrb_per_kapita_crud import router as pdrb_per_kapita_crud_router
from app.routers.rata_rata_upah_bersih_crud import router as rata_rata_upah_bersih_crud_router
from app.routers.tpt_crud import router as tpt_crud_router

# Old routers (existing analytics/read-only)
from app.routers.angkatan_kerja import router as angkatan_kerja_router
from app.routers.gini_ratio import router as gini_ratio_router
from app.routers.indeks_harga_konsumen import router as indeks_harga_konsumen_router
from app.routers.indeks_pembangunan_manusia import router as indeks_pembangunan_manusia_router
from app.routers.inflasi_tahunan import router as inflasi_tahunan_router
from app.routers.kependudukan import router as kependudukan_router
from app.routers.pdrb_perkapita import router as pdrb_perkapita_router
from app.routers.persentase_penduduk_miskin import router as persentase_penduduk_miskin_router
from app.routers.rata_rata_upah import router as rata_rata_upah_router
from app.routers.tingkat_pengangguran_terbuka import router as tingkat_pengangguran_terbuka_router
from app.routers.unemployment_analysis import router as unemployment_analysis_router
from app.routers.year_based_scoring import router as year_based_scoring_router

__all__ = [
    "health_router", 
    "regions_router",
    # CRUD routers
    "angkatan_kerja_crud_router",
    "gini_ratio_crud_router",
    "ipm_crud_router",
    "persentase_penduduk_miskin_crud_router",
    "ihk_crud_router",
    "inflasi_tahunan_crud_router",
    "kependudukan_crud_router",
    "pdrb_per_kapita_crud_router",
    "rata_rata_upah_bersih_crud_router",
    "tpt_crud_router",
    # Old routers
    "angkatan_kerja_router", 
    "gini_ratio_router", 
    "indeks_harga_konsumen_router", 
    "indeks_pembangunan_manusia_router", 
    "inflasi_tahunan_router", 
    "kependudukan_router", 
    "pdrb_perkapita_router", 
    "persentase_penduduk_miskin_router", 
    "rata_rata_upah_router", 
    "tingkat_pengangguran_terbuka_router",
    "unemployment_analysis_router",
    "year_based_scoring_router"
]
