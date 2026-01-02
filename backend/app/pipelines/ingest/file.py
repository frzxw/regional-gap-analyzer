"""
Generic file ingester for various data formats.
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

from app.logging import get_logger

logger = get_logger(__name__)


class FileIngester:
    """Generic file ingester for CSV, Excel, and JSON files."""

    def __init__(self):
        self.supported_formats = ["csv", "xlsx", "xls", "json"]

    async def ingest(
        self,
        file_path: str,
        mapping: Dict[str, str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Ingest data from a file with custom column mapping.

        Args:
            file_path: Path to the data file
            mapping: Dict mapping output fields to input columns
                     e.g., {"region_code": "province_id", "value": "amount"}
            metadata: Additional metadata to add to all records

        Returns:
            List of records
        """
        path = Path(file_path)
        ext = path.suffix.lower().lstrip(".")

        if ext not in self.supported_formats:
            raise ValueError(
                f"Unsupported format: {ext}. "
                f"Supported: {self.supported_formats}"
            )

        logger.info(f"Ingesting data from {file_path}")

        df = self._read_file(path, ext)
        records = self._process_with_mapping(df, mapping, metadata or {})

        logger.info(f"Ingested {len(records)} records from {path.name}")
        return records

    def _read_file(self, path: Path, ext: str) -> pd.DataFrame:
        """Read file into dataframe."""
        if ext == "csv":
            return pd.read_csv(path)
        elif ext in ("xlsx", "xls"):
            return pd.read_excel(path)
        elif ext == "json":
            return pd.read_json(path)
        raise ValueError(f"Unknown format: {ext}")

    def _process_with_mapping(
        self,
        df: pd.DataFrame,
        mapping: Dict[str, str],
        metadata: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Process dataframe with column mapping."""
        records = []
        now = datetime.utcnow()

        for _, row in df.iterrows():
            record = {"imported_at": now, **metadata}

            for output_field, input_column in mapping.items():
                if input_column in df.columns:
                    value = row[input_column]
                    if pd.notna(value):
                        record[output_field] = value

            records.append(record)

        return records

    async def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a file and return metadata about it.

        Returns:
            Dict with file metadata (rows, columns, sample, etc.)
        """
        path = Path(file_path)
        ext = path.suffix.lower().lstrip(".")

        if not path.exists():
            return {"valid": False, "error": "File not found"}

        if ext not in self.supported_formats:
            return {"valid": False, "error": f"Unsupported format: {ext}"}

        try:
            df = self._read_file(path, ext)
            return {
                "valid": True,
                "rows": len(df),
                "columns": list(df.columns),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "sample": df.head(5).to_dict(orient="records"),
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}


# Singleton instance
file_ingester = FileIngester()
