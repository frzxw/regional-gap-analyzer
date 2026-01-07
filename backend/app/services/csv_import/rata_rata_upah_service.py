"""
CSV Import Service for Rata-Rata Upah Bersih data.
"""

import pandas as pd
from io import BytesIO
from datetime import datetime

from app.db import get_database
from app.models.csv_import import ImportResult, CSVImportResponse
from .base_service import BaseCSVImportService


class RataRataUpahImportService(BaseCSVImportService):
    """Service for importing Rata-Rata Upah Bersih CSV files."""

    @staticmethod
    async def import_csv(file_content: bytes, tahun: int) -> CSVImportResponse:
        """
        Import Rata-Rata Upah Bersih CSV.
        Columns: Province | Februari (18 sectors) | Agustus (18 sectors) | Tahunan (18 sectors)
        """
        df = pd.read_csv(BytesIO(file_content), skiprows=4)
        db = await get_database()
        collection = db["rata_rata_upah_bersih"]
        
        success_count = 0
        failed_rows = []
        
        SEKTOR_LIST = [
            "pertanian_kehutanan_perikanan", "pertambangan_penggalian", "industri_pengolahan", 
            "listrik_gas", "air_sampah_limbah_daurulang", "konstruksi", "perdagangan", 
            "transportasi_pergudangan", "akomodasi_makan_minum", "informasi_komunikasi", 
            "jasa_keuangan", "real_estate", "jasa_perusahaan", "admin_pemerintahan", 
            "jasa_pendidikan", "jasa_kesehatan", "jasa_lainnya", "total"
        ]
        
        for index, row in df.iterrows():
            prov_name = str(row['Unnamed: 0']).strip()
            province_id = await RataRataUpahImportService.find_province(prov_name)
            
            if province_id is None:
                failed_rows.append(ImportResult(
                    province_name=prov_name,
                    success=False,
                    message="Province not found"
                ))
                continue
            
            try:
                current_col = 0
                sektor_data = {}
                for sektor in SEKTOR_LIST:
                    suffix = "" if current_col == 0 else f".{current_col}"
                    sektor_data[sektor] = {
                        "februari": RataRataUpahImportService.clean_val(row["Februari" + suffix]),
                        "agustus": RataRataUpahImportService.clean_val(row["Agustus" + suffix]),
                        "tahunan": RataRataUpahImportService.clean_val(row["Tahunan" + suffix])
                    }
                    current_col += 1
                
                doc = {
                    "province_id": province_id,
                    "tahun": int(tahun),
                    "indikator": "rata_rata_upah_bersih",
                    "sektor": sektor_data,
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
            indikator="rata_rata_upah_bersih",
            tahun=tahun,
            total_rows=len(df),
            success_count=success_count,
            failed_count=len(failed_rows),
            failed_rows=failed_rows,
            message=f"Successfully imported {success_count}/{len(df)} records"
        )
