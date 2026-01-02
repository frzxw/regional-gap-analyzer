"""Repositories module initialization."""

from app.repositories.region_repository import (
    RegionRepository,
    get_region_repository,
)
from app.repositories.indicators_repo import (
    IndicatorsRepository,
    get_indicators_repository,
)
from app.repositories.scores_repo import (
    ScoresRepository,
    get_scores_repository,
)
from app.repositories.alerts_repo import (
    AlertsRepository,
    get_alerts_repository,
)
from app.repositories.sources_repo import (
    SourcesRepository,
    get_sources_repository,
)
from app.repositories.configs_repo import (
    ConfigsRepository,
    get_configs_repository,
)

__all__ = [
    "RegionRepository",
    "get_region_repository",
    "IndicatorsRepository",
    "get_indicators_repository",
    "ScoresRepository",
    "get_scores_repository",
    "AlertsRepository",
    "get_alerts_repository",
    "SourcesRepository",
    "get_sources_repository",
    "ConfigsRepository",
    "get_configs_repository",
]
