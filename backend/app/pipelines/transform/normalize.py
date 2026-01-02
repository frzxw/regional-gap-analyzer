"""
Data transformation - Normalization functions.
"""

import numpy as np
from typing import List, Optional


def min_max_normalize(
    values: List[float],
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    scale: float = 100,
) -> List[float]:
    """
    Apply min-max normalization to a list of values.

    Args:
        values: List of values to normalize
        min_val: Minimum value (uses actual min if None)
        max_val: Maximum value (uses actual max if None)
        scale: Scale factor (default 0-100)

    Returns:
        Normalized values
    """
    if not values:
        return []

    arr = np.array(values, dtype=float)
    min_v = min_val if min_val is not None else np.nanmin(arr)
    max_v = max_val if max_val is not None else np.nanmax(arr)

    if max_v == min_v:
        return [scale / 2] * len(values)

    normalized = (arr - min_v) / (max_v - min_v) * scale
    return normalized.tolist()


def z_score_normalize(values: List[float]) -> List[float]:
    """
    Apply z-score normalization to a list of values.

    Args:
        values: List of values to normalize

    Returns:
        Z-score normalized values
    """
    if not values:
        return []

    arr = np.array(values, dtype=float)
    mean = np.nanmean(arr)
    std = np.nanstd(arr)

    if std == 0:
        return [0.0] * len(values)

    normalized = (arr - mean) / std
    return normalized.tolist()


def percentile_rank(values: List[float]) -> List[float]:
    """
    Convert values to percentile ranks (0-100).

    Args:
        values: List of values

    Returns:
        Percentile ranks
    """
    if not values:
        return []

    from scipy import stats
    arr = np.array(values, dtype=float)
    ranks = stats.rankdata(arr, method="average")
    percentiles = (ranks - 1) / (len(ranks) - 1) * 100
    return percentiles.tolist()


def invert_scale(
    values: List[float],
    max_value: float = 100,
) -> List[float]:
    """
    Invert values (for indicators where lower is better).

    Args:
        values: List of values (0 to max_value)
        max_value: Maximum value of the scale

    Returns:
        Inverted values
    """
    return [max_value - v for v in values]


def apply_log_transform(
    values: List[float],
    base: float = np.e,
    shift: float = 1,
) -> List[float]:
    """
    Apply log transformation to values.

    Args:
        values: List of values
        base: Log base (e for natural log, 10 for log10)
        shift: Value to add before log (handles zeros)

    Returns:
        Log-transformed values
    """
    arr = np.array(values, dtype=float) + shift

    if base == np.e:
        transformed = np.log(arr)
    elif base == 10:
        transformed = np.log10(arr)
    else:
        transformed = np.log(arr) / np.log(base)

    return transformed.tolist()
