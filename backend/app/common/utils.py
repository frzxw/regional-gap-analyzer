"""
General utility functions.
"""

from typing import Any, Dict, List, Optional
import re


def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.

    Args:
        text: Input text

    Returns:
        Lowercase slug with hyphens
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text


def deep_merge(base: Dict, override: Dict) -> Dict:
    """
    Deep merge two dictionaries.

    Args:
        base: Base dictionary
        override: Dictionary to merge on top

    Returns:
        Merged dictionary
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks.

    Args:
        items: List to split
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def safe_get(data: Dict, *keys: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary value.

    Args:
        data: Dictionary to search
        *keys: Nested keys
        default: Default value if not found

    Returns:
        Value or default
    """
    result = data
    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return default
    return result


def remove_none_values(data: Dict) -> Dict:
    """
    Remove None values from dictionary.

    Args:
        data: Input dictionary

    Returns:
        Dictionary with None values removed
    """
    return {k: v for k, v in data.items() if v is not None}


def format_number(value: float, decimals: int = 2) -> str:
    """
    Format number with thousand separators.

    Args:
        value: Number to format
        decimals: Decimal places

    Returns:
        Formatted string
    """
    return f"{value:,.{decimals}f}"


def percentage_change(old_value: float, new_value: float) -> Optional[float]:
    """
    Calculate percentage change between two values.

    Args:
        old_value: Previous value
        new_value: Current value

    Returns:
        Percentage change or None if old_value is 0
    """
    if old_value == 0:
        return None
    return ((new_value - old_value) / abs(old_value)) * 100
