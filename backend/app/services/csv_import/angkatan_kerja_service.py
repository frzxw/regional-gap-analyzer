"""
CSV Import Service for Angkatan Kerja data.
"""

import pandas as pd
from io import BytesIO
from datetime import datetime

from app.db import get_database
from app.models.csv_import import ImportResult, CSVImportResponse
from .base_service import BaseCSVImportService


class AngkatanKerjaImportService(BaseCSVImportService):
    """Service for importing Angkatan Kerja CSV files."""

    @staticmethod
    async def import_csv(file_content: bytes, tahun: int) -> CSVImportResponse:
        """
        Import Angkatan Kerja CSV.
        Columns: Province | Februari (Bekerja, Pengangguran, Jumlah AK, %Bekerja/AK) | 
                 Agustus (Bekerja, Pengangguran, Jumlah AK, %Bekerja/AK)
        """
        df = pd.read_csv(BytesIO(file_content), skiprows=4)
        db = await get_database()
        collection = db["angkatan_kerja"]
        
        success_count = 0
        failed_rows = []
        
        for index, row in df.iterrows():
            prov_name = str(row['Unnamed: 0']).strip()
            province_id = await AngkatanKerjaImportService.find_province(prov_name)
            
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
                    "indikator": "angkatan_kerja",
                    "data_februari": {
                        "bekerja": AngkatanKerjaImportService.safe_int(row['Februari']),
                        "pengangguran": AngkatanKerjaImportService.safe_int(row['Februari.1']),
                        "jumlah_ak": AngkatanKerjaImportService.safe_int(row['Februari.2']),
                        "persentase_bekerja_ak": AngkatanKerjaImportService.clean_val(row['Februari.3'])
                    },
                    "data_agustus": {
                        "bekerja": AngkatanKerjaImportService.safe_int(row['Agustus']),
                        "pengangguran": AngkatanKerjaImportService.safe_int(row['Agustus.1']),
                        "jumlah_ak": AngkatanKerjaImportService.safe_int(row['Agustus.2']),
                        "persentase_bekerja_ak": AngkatanKerjaImportService.clean_val(row['Agustus.3'])
                    },
                    "imported_at": datetime.utcnow()
                }
                
                await collection.update_one(
                    {"province_id": province_id, "tahun": tahun, "indikator": "angkatan_kerja"},
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
            indikator="angkatan_kerja",
            tahun=tahun,
            total_rows=len(df),
            success_count=success_count,
            failed_count=len(failed_rows),
            failed_rows=failed_rows,
            message=f"Successfully imported {success_count}/{len(df)} records"
        )
