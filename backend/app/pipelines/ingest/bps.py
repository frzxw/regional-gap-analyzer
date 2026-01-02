"""
BPS (Badan Pusat Statistik) data ingester.
Handles data ingestion from BPS statistical datasets.
"""

import pandas as pd
from typing import Optional, Dict, List, Any
from datetime import datetime
from pathlib import Path

from app.logging import get_logger

logger = get_logger(__name__)


class BPSIngester:
    """Ingester for BPS (Statistics Indonesia) data sources."""

    SUPPORTED_FORMATS = ["csv", "xlsx", "json"]

    def __init__(self):
        self.source_name = "BPS"
        self.source_url = "https://www.bps.go.id"

    async def ingest_from_file(
        self,
        file_path: str,
        indicator_code: str,
        year: int,
        region_column: str = "provinsi",
        value_column: str = "nilai",
    ) -> List[Dict[str, Any]]:
        """
        Ingest data from a local BPS file.

        Args:
            file_path: Path to the data file
            indicator_code: Code for the indicator being imported
            year: Year of the data
            region_column: Column name containing region names
            value_column: Column name containing values

        Returns:
            List of indicator records ready for import
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower().lstrip(".")
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {ext}")

        logger.info(f"Ingesting BPS data from {file_path}")

        # Read data based on format
        if ext == "csv":
            df = pd.read_csv(file_path)
        elif ext == "xlsx":
            df = pd.read_excel(file_path)
        elif ext == "json":
            df = pd.read_json(file_path)

        return self._process_dataframe(
            df, indicator_code, year, region_column, value_column
        )

    def _process_dataframe(
        self,
        df: pd.DataFrame,
        indicator_code: str,
        year: int,
        region_column: str,
        value_column: str,
    ) -> List[Dict[str, Any]]:
        """Process dataframe into indicator records."""
        records = []
        now = datetime.utcnow()

        # Map province names to codes
        region_mapping = self._get_region_mapping()

        for _, row in df.iterrows():
            region_name = str(row[region_column]).strip().upper()
            region_code = region_mapping.get(region_name)

            if not region_code:
                logger.warning(f"Unknown region: {region_name}")
                continue

            value = row[value_column]
            if pd.isna(value):
                continue

            records.append({
                "region_code": region_code,
                "indicator_code": indicator_code,
                "year": year,
                "value": float(value),
                "source": self.source_name,
                "source_url": self.source_url,
                "imported_at": now,
            })

        logger.info(f"Processed {len(records)} records from BPS data")
        return records

    def _get_region_mapping(self) -> Dict[str, str]:
        """Get mapping from province names to ISO codes."""
        return {
            "ACEH": "ID-AC",
            "SUMATERA UTARA": "ID-SU",
            "SUMATERA BARAT": "ID-SB",
            "RIAU": "ID-RI",
            "JAMBI": "ID-JA",
            "SUMATERA SELATAN": "ID-SS",
            "BENGKULU": "ID-BE",
            "LAMPUNG": "ID-LA",
            "KEPULAUAN BANGKA BELITUNG": "ID-BB",
            "KEPULAUAN RIAU": "ID-KR",
            "DKI JAKARTA": "ID-JK",
            "JAWA BARAT": "ID-JB",
            "JAWA TENGAH": "ID-JT",
            "DI YOGYAKARTA": "ID-YO",
            "JAWA TIMUR": "ID-JI",
            "BANTEN": "ID-BT",
            "BALI": "ID-BA",
            "NUSA TENGGARA BARAT": "ID-NB",
            "NUSA TENGGARA TIMUR": "ID-NT",
            "KALIMANTAN BARAT": "ID-KB",
            "KALIMANTAN TENGAH": "ID-KT",
            "KALIMANTAN SELATAN": "ID-KS",
            "KALIMANTAN TIMUR": "ID-KI",
            "KALIMANTAN UTARA": "ID-KU",
            "SULAWESI UTARA": "ID-SA",
            "SULAWESI TENGAH": "ID-ST",
            "SULAWESI SELATAN": "ID-SN",
            "SULAWESI TENGGARA": "ID-SG",
            "GORONTALO": "ID-GO",
            "SULAWESI BARAT": "ID-SR",
            "MALUKU": "ID-MA",
            "MALUKU UTARA": "ID-MU",
            "PAPUA BARAT": "ID-PB",
            "PAPUA": "ID-PA",
            "PAPUA SELATAN": "ID-PS",
            "PAPUA TENGAH": "ID-PT",
            "PAPUA PEGUNUNGAN": "ID-PP",
            "PAPUA BARAT DAYA": "ID-PD",
        }


# Singleton instance
bps_ingester = BPSIngester()
