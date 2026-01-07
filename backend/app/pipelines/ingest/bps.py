"""
BPS (Badan Pusat Statistik) data ingester.
Handles data ingestion from BPS statistical datasets with various formats.
"""

import pandas as pd
import re
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
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Ingest data from a local BPS file.
        Automatically detects and handles various BPS CSV formats.

        Args:
            file_path: Path to the data file
            indicator_code: Code for the indicator being imported
            year: Year of the data

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

        # Read raw CSV to detect format
        if ext == "csv":
            return await self._parse_bps_csv(file_path, indicator_code, year)
        elif ext == "xlsx":
            df = pd.read_excel(file_path)
            return self._simple_process(df, indicator_code, year)
        elif ext == "json":
            df = pd.read_json(file_path)
            return self._simple_process(df, indicator_code, year)

    async def _parse_bps_csv(
        self,
        file_path: str,
        indicator_code: str,
        year: int,
    ) -> List[Dict[str, Any]]:
        """Parse BPS-style CSV files with multi-row headers."""
        
        # Read all lines first
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Detect header format - find the row with province data
        data_start_row = 0
        for i, line in enumerate(lines):
            # Province data starts with province name (ACEH, SUMATERA, etc)
            first_cell = line.split(',')[0].strip().upper()
            # Clean prefix like "PROV "
            first_cell_clean = re.sub(r'^PROV\.?\s*', '', first_cell)
            if first_cell_clean in self._get_region_mapping():
                data_start_row = i
                break
            # Also check for standard province names with different cases
            if first_cell_clean in ['ACEH', 'SUMATERA UTARA', 'DKI JAKARTA', 'JAWA BARAT']:
                data_start_row = i
                break
        
        logger.info(f"Detected data starting at row {data_start_row}")
        
        # Read the CSV skipping header rows
        df = pd.read_csv(file_path, skiprows=data_start_row, header=None)
        
        return self._process_bps_dataframe(df, indicator_code, year)

    def _process_bps_dataframe(
        self,
        df: pd.DataFrame,
        indicator_code: str,
        year: int,
    ) -> List[Dict[str, Any]]:
        """Process BPS dataframe into indicator records."""
        records = []
        now = datetime.utcnow()
        region_mapping = self._get_region_mapping()
        
        for _, row in df.iterrows():
            if pd.isna(row.iloc[0]):
                continue
                
            # Get province name from first column
            province_raw = str(row.iloc[0]).strip().upper()
            
            # Clean common prefixes
            province_clean = re.sub(r'^PROV\.?\s*', '', province_raw)
            province_clean = re.sub(r'^KEP\.?\s*', 'KEPULAUAN ', province_clean)
            province_clean = re.sub(r'^DI\.?\s*', 'DI ', province_clean)
            province_clean = province_clean.strip()
            
            # Skip aggregate rows
            if province_clean in ['INDONESIA', '38 PROVINSI', 'TOTAL', '']:
                continue
            
            region_code = region_mapping.get(province_clean)
            if not region_code:
                # Try partial match
                for name, code in region_mapping.items():
                    if name in province_clean or province_clean in name:
                        region_code = code
                        break
            
            if not region_code:
                logger.warning(f"Unknown region: {province_clean}")
                continue
            
            # Extract value - prioritize specific columns based on indicator type
            value = None
            
            # Try different column positions for value
            # Column 1 is often the first data column
            for col_idx in [1, 6, 7]:  # Common value positions
                if col_idx < len(row):
                    val = row.iloc[col_idx]
                    if not pd.isna(val) and val != '-' and val != '...' and val != '':
                        try:
                            value = float(val)
                            break
                        except (ValueError, TypeError):
                            continue
            
            if value is None:
                logger.debug(f"No valid value found for {province_clean}")
                continue
            
            records.append({
                "province_id": region_code,
                "indicator_code": indicator_code,
                "tahun": year,
                "value": value,
                "source": self.source_name,
                "imported_at": now,
            })
        
        logger.info(f"Processed {len(records)} records from BPS CSV")
        return records

    def _simple_process(
        self,
        df: pd.DataFrame,
        indicator_code: str,
        year: int,
    ) -> List[Dict[str, Any]]:
        """Simple processing for standard format files."""
        records = []
        now = datetime.utcnow()
        region_mapping = self._get_region_mapping()
        
        # Try to find province column
        province_col = None
        for col in df.columns:
            col_lower = str(col).lower()
            if 'provinsi' in col_lower or 'province' in col_lower:
                province_col = col
                break
        
        if province_col is None and len(df.columns) > 0:
            province_col = df.columns[0]
        
        for _, row in df.iterrows():
            province_raw = str(row[province_col]).strip().upper()
            province_clean = re.sub(r'^PROV\.?\s*', '', province_raw)
            
            if province_clean in ['INDONESIA', 'TOTAL', '']:
                continue
            
            region_code = region_mapping.get(province_clean)
            if not region_code:
                continue
            
            # Find value column
            value = None
            for col in df.columns[1:]:
                val = row[col]
                if not pd.isna(val) and val != '-':
                    try:
                        value = float(val)
                        break
                    except (ValueError, TypeError):
                        continue
            
            if value is None:
                continue
            
            records.append({
                "province_id": region_code,
                "indicator_code": indicator_code,
                "tahun": year,
                "value": value,
                "source": self.source_name,
                "imported_at": now,
            })
        
        return records

    def _get_region_mapping(self) -> Dict[str, str]:
        """Get mapping from province names to internal IDs."""
        return {
            "ACEH": "11",
            "SUMATERA UTARA": "12",
            "SUMATERA BARAT": "13",
            "RIAU": "14",
            "JAMBI": "15",
            "SUMATERA SELATAN": "16",
            "BENGKULU": "17",
            "LAMPUNG": "18",
            "KEPULAUAN BANGKA BELITUNG": "19",
            "KEP. BANGKA BELITUNG": "19",
            "KEPULAUAN RIAU": "21",
            "KEP. RIAU": "21",
            "DKI JAKARTA": "31",
            "JAWA BARAT": "32",
            "JAWA TENGAH": "33",
            "DI YOGYAKARTA": "34",
            "JAWA TIMUR": "35",
            "BANTEN": "36",
            "BALI": "51",
            "NUSA TENGGARA BARAT": "52",
            "NUSA TENGGARA TIMUR": "53",
            "KALIMANTAN BARAT": "61",
            "KALIMANTAN TENGAH": "62",
            "KALIMANTAN SELATAN": "63",
            "KALIMANTAN TIMUR": "64",
            "KALIMANTAN UTARA": "65",
            "SULAWESI UTARA": "71",
            "SULAWESI TENGAH": "72",
            "SULAWESI SELATAN": "73",
            "SULAWESI TENGGARA": "74",
            "GORONTALO": "75",
            "SULAWESI BARAT": "76",
            "MALUKU": "81",
            "MALUKU UTARA": "82",
            "PAPUA BARAT": "91",
            "PAPUA": "94",
            "PAPUA SELATAN": "92",
            "PAPUA TENGAH": "93",
            "PAPUA PEGUNUNGAN": "95",
            "PAPUA BARAT DAYA": "96",
        }


# Singleton instance
bps_ingester = BPSIngester()
