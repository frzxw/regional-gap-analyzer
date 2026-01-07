"""
CSV Import Service for Indeks Pembangunan Manusia (IPM) data.
"""

import pandas as pd
from io import BytesIO
from datetime import datetime

from app.db import get_database
from app.models.csv_import import ImportResult, CSVImportResponse
from .base_service import BaseCSVImportService


class IPMImportService(BaseCSVImportService):
    """Service for importing Indeks Pembangunan Manusia CSV files."""

    @staticmethod
    async def import_csv(file_content: bytes, tahun: int) -> CSVImportResponse:
        """
        Import Indeks Pembangunan Manusia CSV.
        Columns: Province | [Year columns]
        """
        df = pd.read_csv(BytesIO(file_content), skiprows=2)
        db = await get_database()
        collection = db["indeks_pembangunan_manusia"]
        
        success_count = 0
        failed_rows = []
        
        for index, row in df.iterrows():
            prov_name = str(row['Unnamed: 0']).strip()
            province_id = await IPMImportService.find_province(prov_name)
            
            if province_id is None:
                failed_rows.append(ImportResult(
                    province_name=prov_name,
                    success=False,
                    message="Province not found"
                ))
                continue
            
            try:
                doc = {
                    "province_id": province_id,
                    "tahun": int(tahun),
                    "indikator": "indeks_pembangunan_manusia",
                    "data": IPMImportService.clean_val(row[str(tahun)]),
                    "imported_at": datetime.utcnow()
                }
                
                await collection.update_one(
                    {"province_id": province_id, "tahun": tahun},
                    {"$set": doc},
                    upsert=True
                )
                success_count += 1
            except Exception as e:
                failed_rows.append(ImportResult(
                    province_name=prov_name,
                    success=False,
                    message=str(e)
                ))
        
        return CSVImportResponse(
            indikator="indeks_pembangunan_manusia",
            tahun=tahun,
            total_rows=len(df),
            success_count=success_count,
            failed_count=len(failed_rows),
            failed_rows=failed_rows,
            message=f"Successfully imported {success_count}/{len(df)} records"
        )
