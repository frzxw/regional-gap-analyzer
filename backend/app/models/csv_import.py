"""
Models for CSV import operations.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ImportResult(BaseModel):
    """Result for a single row import."""
    province_name: str
    success: bool
    message: Optional[str] = None


class CSVImportResponse(BaseModel):
    """Response model for CSV import."""
    indikator: str
    tahun: int
    total_rows: int
    success_count: int
    failed_count: int
    failed_rows: List[ImportResult] = []
    imported_at: datetime = Field(default_factory=datetime.utcnow)
    message: str
