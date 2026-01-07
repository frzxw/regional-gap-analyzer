"""
CSV Import Service for Kependudukan data.
"""

import pandas as pd
from io import BytesIO
from datetime import datetime

from app.db import get_database
from app.models.csv_import import ImportResult, CSVImportResponse
from .base_service import BaseCSVImportService


class KependudukanImportService(BaseCSVImportService):
    """Service for importing Kependudukan CSV files."""

    @staticmethod
    async def import_csv(file_content: bytes, tahun: int) -> CSVImportResponse:
        """
        Import Kependudukan CSV.
        Columns: Provinsi | Jumlah Penduduk (Ribu) | Laju Pertumbuhan | 
                 Persentase Penduduk | Kepadatan per km2 | Rasio Jenis Kelamin
        """
        df = pd.read_csv(BytesIO(file_content))
        db = await get_database()
        collection = db["kependudukan"]
        
        success_count = 0
        failed_rows = []
        
        for index, row in df.iterrows():
            prov_name = str(row['Provinsi']).strip()
            province_id = await KependudukanImportService.find_province(prov_name)
            
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
                    "indikator": "kependudukan",
                    "data": {
                        "jumlah_penduduk_ribu": KependudukanImportService.clean_val(row['Jumlah Penduduk (Ribu)']),
                        "laju_pertumbuhan_tahunan": KependudukanImportService.clean_val(row['Laju Pertumbuhan Penduduk per Tahun']),
                        "persentase_penduduk": KependudukanImportService.clean_val(row['Persentase Penduduk']),
                        "kepadatan_per_km2": KependudukanImportService.clean_val(row['Kepadatan Penduduk per km persegi (Km2)']),
                        "rasio_jenis_kelamin": KependudukanImportService.clean_val(row['Rasio Jenis Kelamin Penduduk'])
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
            indikator="kependudukan",
            tahun=tahun,
            total_rows=len(df),
            success_count=success_count,
            failed_count=len(failed_rows),
            failed_rows=failed_rows,
            message=f"Successfully imported {success_count}/{len(df)} records"
        )
