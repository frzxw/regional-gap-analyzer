"""
CSV Import Service for Inflasi Tahunan data.
"""

import pandas as pd
from io import BytesIO
from datetime import datetime

from app.db import get_database
from app.models.csv_import import ImportResult, CSVImportResponse
from .base_service import BaseCSVImportService


class InflasiTahunanImportService(BaseCSVImportService):
    """Service for importing Inflasi Tahunan CSV files."""

    @staticmethod
    async def import_csv(file_content: bytes, tahun: int) -> CSVImportResponse:
        """
        Import Inflasi Tahunan CSV.
        Columns: Province | Januari | Februari | ... | Desember | Tahunan
        """
        df = pd.read_csv(BytesIO(file_content), skiprows=3)
        db = await get_database()
        collection = db["inflasi_tahunan"]
        
        success_count = 0
        failed_rows = []
        bulan_list = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                      'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
        
        for index, row in df.iterrows():
            prov_name = str(row['Unnamed: 0']).strip()
            province_id = await InflasiTahunanImportService.find_province(prov_name)
            
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
                    "indikator": "inflasi_tahunan",
                    "data_bulanan": {
                        bulan.lower(): InflasiTahunanImportService.clean_val(row[bulan]) 
                        for bulan in bulan_list
                    },
                    "tahunan": InflasiTahunanImportService.clean_val(row['Tahunan']),
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
            indikator="inflasi_tahunan",
            tahun=tahun,
            total_rows=len(df),
            success_count=success_count,
            failed_count=len(failed_rows),
            failed_rows=failed_rows,
            message=f"Successfully imported {success_count}/{len(df)} records"
        )
