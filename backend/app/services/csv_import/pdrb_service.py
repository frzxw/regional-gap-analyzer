"""
CSV Import Service for PDRB Per Kapita data (ADHB & ADHK).
"""

import pandas as pd
from io import BytesIO
from datetime import datetime

from app.db import get_database
from app.models.csv_import import ImportResult, CSVImportResponse
from .base_service import BaseCSVImportService


class PDRBImportService(BaseCSVImportService):
    """Service for importing PDRB Per Kapita CSV files."""

    @staticmethod
    async def import_adhb(file_content: bytes, tahun: int) -> CSVImportResponse:
        """
        Import PDRB Per Kapita ADHB (Atas Dasar Harga Berlaku) CSV.
        Columns: Provinsi | PDRB per Kapita ADHB (Ribu Rp)
        """
        df = pd.read_csv(BytesIO(file_content))
        db = await get_database()
        collection = db["pdrb_per_kapita"]
        
        success_count = 0
        failed_rows = []
        
        for index, row in df.iterrows():
            prov_name = str(row['Provinsi']).strip()
            province_id = await PDRBImportService.find_province(prov_name)
            
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
                    "indikator": "pdrb_per_kapita_adhb",
                    "data_ribu_rp": PDRBImportService.clean_val(row["Produk Domestik Regional Bruto per Kapita Atas Dasar Harga Berlaku (Ribu Rp)"]),
                    "imported_at": datetime.utcnow()
                }
                
                await collection.update_one(
                    {"province_id": province_id, "tahun": tahun, "indikator": "pdrb_per_kapita_adhb"},
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
            indikator="pdrb_per_kapita_adhb",
            tahun=tahun,
            total_rows=len(df),
            success_count=success_count,
            failed_count=len(failed_rows),
            failed_rows=failed_rows,
            message=f"Successfully imported {success_count}/{len(df)} records"
        )

    @staticmethod
    async def import_adhk(file_content: bytes, tahun: int) -> CSVImportResponse:
        """
        Import PDRB Per Kapita ADHK (Atas Dasar Harga Konstan 2010) CSV.
        Columns: Provinsi | PDRB per Kapita HK (Ribu Rp)
        """
        df = pd.read_csv(BytesIO(file_content))
        db = await get_database()
        collection = db["pdrb_per_kapita"]
        
        success_count = 0
        failed_rows = []
        
        for index, row in df.iterrows():
            prov_name = str(row['Provinsi']).strip()
            province_id = await PDRBImportService.find_province(prov_name)
            
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
                    "indikator": "pdrb_per_kapita_adhk_2010",
                    "data_ribu_rp": PDRBImportService.clean_val(row["Produk Domestik Regional Bruto per Kapita HK (Ribu Rp)"]),
                    "imported_at": datetime.utcnow()
                }
                
                await collection.update_one(
                    {"province_id": province_id, "tahun": tahun, "indikator": "pdrb_per_kapita_adhk_2010"},
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
            indikator="pdrb_per_kapita_adhk_2010",
            tahun=tahun,
            total_rows=len(df),
            success_count=success_count,
            failed_count=len(failed_rows),
            failed_rows=failed_rows,
            message=f"Successfully imported {success_count}/{len(df)} records"
        )
