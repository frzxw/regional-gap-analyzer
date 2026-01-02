"""
Time utilities for consistent datetime handling.
"""

from datetime import datetime, timezone
from typing import Optional


def utc_now() -> datetime:
    """
    Get current UTC datetime.

    Returns:
        Timezone-aware datetime in UTC
    """
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%dT%H:%M:%SZ") -> str:
    """
    Format datetime to ISO string.

    Args:
        dt: Datetime to format
        fmt: Format string (default: ISO 8601)

    Returns:
        Formatted datetime string
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime(fmt)


def parse_datetime(value: str) -> Optional[datetime]:
    """
    Parse datetime string to datetime object.

    Args:
        value: Datetime string (ISO 8601 format)

    Returns:
        Parsed datetime or None if invalid
    """
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    return None


def start_of_year(year: int) -> datetime:
    """Get start of a given year in UTC."""
    return datetime(year, 1, 1, tzinfo=timezone.utc)


def end_of_year(year: int) -> datetime:
    """Get end of a given year in UTC."""
    return datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
