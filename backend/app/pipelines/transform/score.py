"""
Data transformation - Score calculation functions.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from app.logging import get_logger

logger = get_logger(__name__)


@dataclass
class IndicatorWeight:
    """Weight configuration for an indicator."""
    code: str
    weight: float
    invert: bool = False  # True if lower values are better


class ScoreCalculator:
    """Calculator for composite inequality scores."""

    # Default weights for indicators
    DEFAULT_WEIGHTS: Dict[str, IndicatorWeight] = {
        "HDI": IndicatorWeight("HDI", 0.25, invert=False),
        "POVERTY_RATE": IndicatorWeight("POVERTY_RATE", 0.20, invert=True),
        "GRDP_CAPITA": IndicatorWeight("GRDP_CAPITA", 0.20, invert=False),
        "GINI": IndicatorWeight("GINI", 0.15, invert=True),
        "UNEMPLOYMENT": IndicatorWeight("UNEMPLOYMENT", 0.10, invert=True),
        "LITERACY": IndicatorWeight("LITERACY", 0.10, invert=False),
    }

    def __init__(self, weights: Optional[Dict[str, IndicatorWeight]] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS

    def calculate_composite_score(
        self,
        indicators: Dict[str, float],
    ) -> float:
        """
        Calculate composite score from normalized indicators.

        Args:
            indicators: Dict of indicator_code -> normalized_value (0-100)

        Returns:
            Composite score (0-100)
        """
        weighted_sum = 0.0
        total_weight = 0.0

        for code, value in indicators.items():
            if code not in self.weights:
                logger.warning(f"Unknown indicator: {code}")
                continue

            weight_config = self.weights[code]
            weight = weight_config.weight

            # Invert if lower is better
            if weight_config.invert:
                value = 100 - value

            weighted_sum += value * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0

        return weighted_sum / total_weight

    def calculate_dimension_scores(
        self,
        indicators: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Calculate dimension-level scores (economic, social, infrastructure).

        Args:
            indicators: Dict of indicator_code -> normalized_value

        Returns:
            Dict of dimension -> score
        """
        # Define dimension mappings
        dimensions = {
            "economic": ["GRDP_CAPITA", "UNEMPLOYMENT", "GINI"],
            "social": ["HDI", "POVERTY_RATE", "LITERACY"],
            "infrastructure": ["ELECTRIFICATION", "CLEAN_WATER", "INTERNET"],
        }

        dimension_scores = {}

        for dim_name, dim_indicators in dimensions.items():
            dim_values = []
            dim_weights = []

            for code in dim_indicators:
                if code in indicators and code in self.weights:
                    value = indicators[code]
                    weight_config = self.weights[code]

                    if weight_config.invert:
                        value = 100 - value

                    dim_values.append(value)
                    dim_weights.append(weight_config.weight)

            if dim_values:
                # Normalize weights within dimension
                total = sum(dim_weights)
                dim_weights = [w / total for w in dim_weights]
                dimension_scores[dim_name] = sum(
                    v * w for v, w in zip(dim_values, dim_weights)
                )
            else:
                dimension_scores[dim_name] = None

        return dimension_scores

    def calculate_rankings(
        self,
        scores: List[Tuple[str, float]],
        previous_scores: Optional[List[Tuple[str, float]]] = None,
    ) -> List[Dict]:
        """
        Calculate rankings with optional delta from previous period.

        Args:
            scores: List of (region_code, score) tuples
            previous_scores: Previous period scores for delta calculation

        Returns:
            List of ranking dicts with rank, score, delta
        """
        # Sort by score descending (higher is better)
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        # Get previous ranks if available
        prev_ranks = {}
        if previous_scores:
            prev_sorted = sorted(previous_scores, key=lambda x: x[1], reverse=True)
            prev_ranks = {code: i + 1 for i, (code, _) in enumerate(prev_sorted)}

        rankings = []
        for i, (region_code, score) in enumerate(sorted_scores):
            rank = i + 1
            prev_rank = prev_ranks.get(region_code)

            rankings.append({
                "region_code": region_code,
                "score": round(score, 2),
                "rank": rank,
                "previous_rank": prev_rank,
                "rank_delta": prev_rank - rank if prev_rank else None,
            })

        return rankings


# Singleton instance
score_calculator = ScoreCalculator()
