"""
Unit tests for the scoring service.
"""

import pytest
from app.services.scoring_service import ScoringService


class TestScoringService:
    """Test cases for ScoringService."""

    def test_normalize_min_max_basic(self):
        """Test basic min-max normalization."""
        values = [0, 50, 100]
        result = ScoringService.normalize_min_max(values)
        assert result == [0.0, 50.0, 100.0]

    def test_normalize_min_max_inverse(self):
        """Test inverse normalization (lower is better)."""
        values = [0, 50, 100]
        result = ScoringService.normalize_min_max(values, inverse=True)
        assert result == [100.0, 50.0, 0.0]

    def test_normalize_min_max_empty(self):
        """Test empty list returns empty."""
        result = ScoringService.normalize_min_max([])
        assert result == []

    def test_normalize_min_max_single_value(self):
        """Test single value returns 50 (midpoint)."""
        result = ScoringService.normalize_min_max([42])
        assert result == [50.0]

    def test_calculate_composite_score_equal_weights(self):
        """Test composite score with equal weights."""
        scores = {
            "economic": 80.0,
            "health": 60.0,
            "education": 70.0,
            "infrastructure": 90.0,
        }
        result = ScoringService.calculate_composite_score(scores)
        assert result == 75.0

    def test_calculate_composite_score_with_weights(self):
        """Test composite score with custom weights."""
        scores = {
            "economic": 100.0,
            "health": 0.0,
        }
        weights = {
            "economic": 0.8,
            "health": 0.2,
        }
        result = ScoringService.calculate_composite_score(scores, weights)
        assert result == 80.0

    def test_calculate_composite_score_with_none_values(self):
        """Test composite score ignores None values."""
        scores = {
            "economic": 80.0,
            "health": None,
            "education": 60.0,
        }
        result = ScoringService.calculate_composite_score(scores)
        assert result == 70.0
