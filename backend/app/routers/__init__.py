"""Routers module initialization."""

from app.routers.health import router as health_router
from app.routers.regions import router as regions_router
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

__all__ = ["health_router", "regions_router", "angkatan_kerja_router", "gini_ratio_router", "indeks_harga_konsumen_router", "indeks_pembangunan_manusia_router", "inflasi_tahunan_router", "kependudukan_router", "pdrb_perkapita_router", "persentase_penduduk_miskin_router", "rata_rata_upah_router", "tingkat_pengangguran_terbuka_router"]
