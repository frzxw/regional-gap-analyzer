"""
CSV Import Service for Persentase Penduduk Miskin data.
"""

import pandas as pd
from io import BytesIO
from datetime import datetime

from app.db import get_database
from app.models.csv_import import ImportResult, CSVImportResponse
from .base_service import BaseCSVImportService


class PersentasePendudukMiskinImportService(BaseCSVImportService):
    """Service for importing Persentase Penduduk Miskin CSV files."""

    @staticmethod
    async def import_csv(file_content: bytes, tahun: int) -> CSVImportResponse:
        """
        Import Persentase Penduduk Miskin CSV.
        Columns: Province | Semester 1 (Perkotaan, Perdesaan, Total) | 
                 Semester 2 (Perkotaan, Perdesaan, Total) | Tahunan (Perkotaan, Perdesaan, Total)
        """
        df = pd.read_csv(BytesIO(file_content), skiprows=4)
        db = await get_database()
        collection = db["persentase_penduduk_miskin"]
        
        success_count = 0
        failed_rows = []
        
        for index, row in df.iterrows():
            prov_name = str(row['Unnamed: 0']).strip()
            province_id = await PersentasePendudukMiskinImportService.find_province(prov_name)
            
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
                    "indikator": "persentase_penduduk_miskin",
                    "data_semester_1": {
                        "perkotaan": PersentasePendudukMiskinImportService.clean_val(row['Semester 1 (Maret)']),
                        "perdesaan": PersentasePendudukMiskinImportService.clean_val(row['Semester 1 (Maret).1']),
                        "total": PersentasePendudukMiskinImportService.clean_val(row['Semester 1 (Maret).2'])
                    },
                    "data_semester_2": {
                        "perkotaan": PersentasePendudukMiskinImportService.clean_val(row['Semester 2 (September)']),
                        "perdesaan": PersentasePendudukMiskinImportService.clean_val(row['Semester 2 (September).1']),
                        "total": PersentasePendudukMiskinImportService.clean_val(row['Semester 2 (September).2'])
                    },
                    "data_tahunan": {
                        "perkotaan": PersentasePendudukMiskinImportService.clean_val(row['Tahunan']),
                        "perdesaan": PersentasePendudukMiskinImportService.clean_val(row['Tahunan.1']),
                        "total": PersentasePendudukMiskinImportService.clean_val(row['Tahunan.2'])
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
            indikator="persentase_penduduk_miskin",
            tahun=tahun,
            total_rows=len(df),
            success_count=success_count,
            failed_count=len(failed_rows),
            failed_rows=failed_rows,
            message=f"Successfully imported {success_count}/{len(df)} records"
        )
