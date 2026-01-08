"""
Base CSV Import Service - Common utilities for all CSV import services.
"""

import pandas as pd
import re
from typing import Optional

from app.db import get_database


class BaseCSVImportService:
    """Base service with shared utilities for CSV import operations."""

    @staticmethod
    async def find_province(province_name: str) -> Optional[str]:
        """
        Find province ID by name with fuzzy matching.
        Handles common prefixes like PROV., KEP., DI.
        """
        clean_name = re.sub(r'^PROV\.?\s+', '', str(province_name), flags=re.IGNORECASE).strip()
        clean_name = re.sub(r'^KEP\.?\s+', 'KEPULAUAN ', clean_name, flags=re.IGNORECASE)
        clean_name = re.sub(r'DI\.?\s+', 'DAERAH ISTIMEWA ', clean_name, flags=re.IGNORECASE)

        db = await get_database()
        collection = db["provinces"]
        
        result = await collection.find_one({
            "properties.PROVINSI": {
                "$regex": f"^{re.escape(clean_name)}$",
                "$options": "i"
            }
        })
        
        if result:
            return result.get('properties', {}).get('id')
        return None

    @staticmethod
    def clean_val(val):
        """
        Clean and convert value to float or None.
        Handles '-', NaN, and '...' as missing values.
        """
        if val == '-' or pd.isna(val) or val == '...':
            return None
        try:
            return float(val)
        except:
            return None

    @staticmethod
    def safe_int(val):
        """Safely convert to int or None."""
        cleaned = BaseCSVImportService.clean_val(val)
        return int(cleaned) if cleaned is not None else None

    @staticmethod
    async def log_import(
        indicator_code: str,
        year: int,
        source_name: str,
        success_count: int,
        total_rows: int,
        source_type: str = "csv"
    ):
        """Record import operation to import_logs collection."""
        from datetime import datetime
        db = await get_database()
        log_collection = db["import_logs"]
        
        await log_collection.insert_one({
            "indicator_code": indicator_code,
            "name": f"Import {indicator_code} {year}",
            "source_name": source_name,
            "tahun": year,
            "source_type": source_type,
            "records_count": success_count,
            "total_rows": total_rows,
            "created_at": datetime.utcnow()
        })
