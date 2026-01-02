"""
Geo service - Business logic for geographic data operations.
"""

import json
from typing import Optional, List, Dict, Any
from pathlib import Path

from app.repositories import get_scores_repository, get_region_repository
from app.logging import get_logger

logger = get_logger(__name__)


class GeoService:
    """Service layer for geographic data operations."""

    def __init__(self, geojson_path: Optional[str] = None):
        self.geojson_path = geojson_path or "data/geo/indonesia_provinces.geojson"
        self._geojson_cache: Optional[Dict] = None

    async def get_geojson(self) -> Dict:
        """
        Get the base GeoJSON for Indonesia provinces.

        Returns:
            GeoJSON FeatureCollection
        """
        if self._geojson_cache is None:
            self._geojson_cache = self._load_geojson()
        return self._geojson_cache

    async def get_choropleth_data(
        self,
        year: Optional[int] = None,
        metric: str = "composite_score",
    ) -> Dict:
        """
        Get GeoJSON with score data joined for choropleth visualization.

        Args:
            year: Year to get scores for (latest if None)
            metric: Score metric to include (composite_score, economic_score, etc.)

        Returns:
            GeoJSON FeatureCollection with score properties
        """
        geojson = await self.get_geojson()
        scores_repo = await get_scores_repository()

        # Get year if not specified
        if year is None:
            year = await scores_repo.get_latest_year()

        if year is None:
            # No scores available, return base geojson
            return geojson

        # Get scores for the year
        rankings = await scores_repo.find_rankings(year)
        scores_by_code = {s["region_code"]: s for s in rankings}

        # Join scores to features
        features = []
        for feature in geojson.get("features", []):
            code = feature["properties"].get("code")
            score_data = scores_by_code.get(code, {})

            # Add score properties
            feature["properties"]["year"] = year
            feature["properties"]["composite_score"] = score_data.get("composite_score")
            feature["properties"]["rank"] = score_data.get("rank")
            feature["properties"]["rank_delta"] = score_data.get("rank_delta")
            feature["properties"][metric] = score_data.get(metric)

            features.append(feature)

        return {
            "type": "FeatureCollection",
            "metadata": {
                "year": year,
                "metric": metric,
                "total_regions": len(features),
            },
            "features": features,
        }

    async def get_region_boundary(self, region_code: str) -> Optional[Dict]:
        """
        Get GeoJSON feature for a single region.

        Args:
            region_code: Province code (e.g., "ID-JK")

        Returns:
            GeoJSON Feature or None
        """
        geojson = await self.get_geojson()

        for feature in geojson.get("features", []):
            if feature["properties"].get("code") == region_code:
                return feature

        return None

    def get_color_scale(
        self,
        min_value: float = 0,
        max_value: float = 100,
        palette: str = "RdYlGn",
    ) -> List[Dict]:
        """
        Get color scale configuration for choropleth.

        Args:
            min_value: Minimum score value
            max_value: Maximum score value
            palette: Color palette name

        Returns:
            List of color stops
        """
        # Red-Yellow-Green palette
        colors = [
            {"value": 0, "color": "#d73027"},    # Red (lowest)
            {"value": 20, "color": "#fc8d59"},   # Orange
            {"value": 40, "color": "#fee08b"},   # Yellow
            {"value": 60, "color": "#d9ef8b"},   # Light green
            {"value": 80, "color": "#91cf60"},   # Green
            {"value": 100, "color": "#1a9850"}, # Dark green (highest)
        ]
        return colors

    def _load_geojson(self) -> Dict:
        """Load GeoJSON from file."""
        path = Path(self.geojson_path)
        if not path.exists():
            logger.warning(f"GeoJSON file not found: {path}")
            return {"type": "FeatureCollection", "features": []}

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


# Singleton instance
geo_service = GeoService()
