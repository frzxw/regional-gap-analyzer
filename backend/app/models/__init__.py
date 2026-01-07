"""Models module initialization."""

from app.models.region import RegionModel, RegionScoreModel, GeoFeatureModel, GeometryModel
from app.models.indicator import (
    IndicatorBase,
    IndicatorCreate,
    IndicatorUpdate,
    IndicatorResponse,
    IndicatorFilter,
)
from app.models.score import (
    ScoreBase,
    ScoreCreate,
    ScoreResponse,
    ScoreSummary,
    ScoreRanking,
    ScoreTrend,
    RecomputeRequest,
    RecomputeResponse,
)
from app.models.alert import (
    AlertBase,
    AlertCreate,
    AlertUpdate,
    AlertResponse,
    AlertSummary,
    AlertFilter,
)
from app.models.source import (
    SourceBase,
    SourceCreate,
    SourceUpdate,
    SourceResponse,
)
from app.models.config import (
    ScoringConfig,
    ConfigItem,
    ConfigResponse,
    ConfigUpdate,
)
from app.models.labor_force import (
    MonthlyLaborData,
    LaborForceRecord,
    LaborForceResponse,
    LaborForceListResponse,
)
from app.models.gini_ratio import (
    SemesterData,
    GiniRatioRecord,
    GiniRatioResponse,
    GiniRatioListResponse,
)
from app.models.indeks_harga_konsumen import (
    MonthlyIndexData,
    IndeksHargaKonsumenRecord,
    IndeksHargaKonsumenResponse,
    IndeksHargaKonsumenListResponse,
)
from app.models.indeks_pembangunan_manusia import (
    IndeksPembangunanManusiaRecord,
    IndeksPembangunanManusiaResponse,
    IndeksPembangunanManusiaListResponse,
)
from app.models.inflasi_tahunan import (
    MonthlyInflationData,
    InflasiTahunanRecord,
    InflasiTahunanResponse,
    InflasiTahunanListResponse,
)
from app.models.kependudukan import (
    PopulationData,
    KependudukanRecord,
    KependudukanResponse,
    KependudukanListResponse,
)
from app.models.pdrb_perkapita import (
    PdrbPerkapitaData,
    PdrbPerkapitaRecord,
    PdrbPerkapitaResponse,
    PdrbPerkapitaListResponse,
)
from app.models.persentase_penduduk_miskin import (
    SemesterPovertyData,
    PersentasePendudukMiskinRecord,
    PersentasePendudukMiskinResponse,
    PersentasePendudukMiskinListResponse,
)
from app.models.rata_rata_upah import (
    SectorWageData,
    WageSektor,
    RataRataUpahBersihRecord,
    RataRataUpahBersihResponse,
    RataRataUpahBersihListResponse,
)

__all__ = [
    # Region
    "RegionModel",
    "RegionScoreModel",
    "GeoFeatureModel",
    # Indicator
    "IndicatorBase",
    "IndicatorCreate",
    "IndicatorUpdate",
    "IndicatorResponse",
    "IndicatorFilter",
    # Score
    "ScoreBase",
    "ScoreCreate",
    "ScoreResponse",
    "ScoreSummary",
    "ScoreRanking",
    "ScoreTrend",
    "RecomputeRequest",
    "RecomputeResponse",
    # Alert
    "AlertBase",
    "AlertCreate",
    "AlertUpdate",
    "AlertResponse",
    "AlertSummary",
    "AlertFilter",
    # Source
    "SourceBase",
    "SourceCreate",
    "SourceUpdate",
    "SourceResponse",
    # Config
    "ScoringConfig",
    "ConfigItem",
    "ConfigResponse",
    "ConfigUpdate",
    # Labor Force
    "MonthlyLaborData",
    "LaborForceRecord",
    "LaborForceResponse",
    "LaborForceListResponse",
    # Gini Ratio
    "SemesterData",
    "GiniRatioRecord",
    "GiniRatioResponse",
    "GiniRatioListResponse",
    # Indeks Harga Konsumen
    "MonthlyIndexData",
    "IndeksHargaKonsumenRecord",
    "IndeksHargaKonsumenResponse",
    "IndeksHargaKonsumenListResponse",
    # Indeks Pembangunan Manusia
    "IndeksPembangunanManusiaRecord",
    "IndeksPembangunanManusiaResponse",
    "IndeksPembangunanManusiaListResponse",
    # Inflasi Tahunan
    "MonthlyInflationData",
    "InflasiTahunanRecord",
    "InflasiTahunanResponse",
    "InflasiTahunanListResponse",
    # Kependudukan
    "PopulationData",
    "KependudukanRecord",
    "KependudukanResponse",
    "KependudukanListResponse",
    # PDRB Per Kapita
    "PdrbPerkapitaData",
    "PdrbPerkapitaRecord",
    "PdrbPerkapitaResponse",
    "PdrbPerkapitaListResponse",
    # Persentase Penduduk Miskin
    "SemesterPovertyData",
    "PersentasePendudukMiskinRecord",
    "PersentasePendudukMiskinResponse",
    "PersentasePendudukMiskinListResponse",
    # Rata-rata Upah Bersih
    "SectorWageData",
    "WageSektor",
    "RataRataUpahBersihRecord",
    "RataRataUpahBersihResponse",
    "RataRataUpahBersihListResponse",
]
