"""
Scoring service - Business logic for regional inequality scoring.
Implements normalization and composite score calculation.
"""

import numpy as np
from typing import Optional


class ScoringService:
    """
    Service for calculating regional inequality scores.

    TODO: Implement full scoring logic with:
    - Min-max normalization
    - Z-score normalization
    - Weighted composite scoring
    - Gap analysis between regions
    """

    @staticmethod
    def normalize_min_max(
        values: list[float], inverse: bool = False
    ) -> list[float]:
        """
        Min-max normalization to 0-100 scale.

        Args:
            values: List of raw values
            inverse: If True, higher raw values get lower scores

        Returns:
            Normalized values (0-100)
        """
        if not values:
            return []

        arr = np.array(values, dtype=float)
        min_val = np.nanmin(arr)
        max_val = np.nanmax(arr)

        if max_val == min_val:
            return [50.0] * len(values)

        normalized = (arr - min_val) / (max_val - min_val) * 100

        if inverse:
            normalized = 100 - normalized

        return normalized.tolist()

    @staticmethod
    def calculate_composite_score(
        scores: dict[str, Optional[float]],
        weights: Optional[dict[str, float]] = None,
    ) -> float:
        """
        Calculate weighted composite score from individual indicator scores.

        Args:
            scores: Dictionary of indicator name -> score (0-100)
            weights: Optional weights for each indicator (default: equal weights)

        Returns:
            Composite score (0-100)
        """
        valid_scores = {k: v for k, v in scores.items() if v is not None}

        if not valid_scores:
            return 0.0

        if weights is None:
            # Equal weights
            return sum(valid_scores.values()) / len(valid_scores)

        weighted_sum = 0.0
        weight_sum = 0.0

        for indicator, score in valid_scores.items():
            weight = weights.get(indicator, 1.0)
            weighted_sum += score * weight
            weight_sum += weight

        return weighted_sum / weight_sum if weight_sum > 0 else 0.0


# Singleton instance
scoring_service = ScoringService()
