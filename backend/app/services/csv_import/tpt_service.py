"""
CSV Import Service for Tingkat Pengangguran Terbuka (TPT) data.
"""

import pandas as pd
from io import BytesIO
from datetime import datetime

from app.db import get_database
from app.models.csv_import import ImportResult, CSVImportResponse
from .base_service import BaseCSVImportService


class TPTImportService(BaseCSVImportService):
    """Service for importing Tingkat Pengangguran Terbuka CSV files."""

    @staticmethod
    async def import_csv(file_content: bytes, tahun: int) -> CSVImportResponse:
        """
        Import Tingkat Pengangguran Terbuka CSV.
        Columns: Province | Februari | Agustus | Tahunan
        """
        df = pd.read_csv(BytesIO(file_content), skiprows=3)
        db = await get_database()
        collection = db["tingkat_pengangguran_terbuka"]
        
        success_count = 0
        failed_rows = []
        
        for index, row in df.iterrows():
            prov_name = str(row['Unnamed: 0']).strip()
            province_id = await TPTImportService.find_province(prov_name)
            
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
                    "indikator": "tingkat_pengangguran_terbuka",
                    "data": {
                        "februari": TPTImportService.clean_val(row['Februari']),
                        "agustus": TPTImportService.clean_val(row['Agustus']),
                        "tahunan": TPTImportService.clean_val(row['Tahunan'])
                    },
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
            indikator="tingkat_pengangguran_terbuka",
            tahun=tahun,
            total_rows=len(df),
            success_count=success_count,
            failed_count=len(failed_rows),
            failed_rows=failed_rows,
            message=f"Successfully imported {success_count}/{len(df)} records"
        )
