"""Services module initialization."""

from app.services.region_service import region_service, RegionService
from app.services.scoring_service import scoring_service, ScoringService
from app.services.indicators_service import indicators_service, IndicatorsService
from app.services.alerts_service import alerts_service, AlertsService
from app.services.imports_service import imports_service, ImportsService
from app.services.geo_service import geo_service, GeoService

__all__ = [
    "region_service",
    "RegionService",
    "scoring_service",
    "ScoringService",
    "indicators_service",
    "IndicatorsService",
    "alerts_service",
    "AlertsService",
    "imports_service",
    "ImportsService",
    "geo_service",
    "GeoService",
]
