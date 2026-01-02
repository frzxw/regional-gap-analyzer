"""Models module initialization."""

from app.models.region import RegionModel, RegionScoreModel, GeoFeatureModel
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
]
