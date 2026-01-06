import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

def extract_json(df, tahun):
    prov_name = str(df['Unnamed: 0']).strip()

    province_id = utils.find_province(prov_name)
    if province_id is None:
        print(f"Province not found for: {prov_name}")
        return False
    json = {
        "province_id": province_id,
        "tahun": int(tahun),
        "indikator": "angkatan_kerja",
        "data_februari": {
            "bekerja": int(df['Februari']),
            "pengangguran": int(df['Februari.1']),
            "jumlah_ak": int(df['Februari.2']),
            "persentase_bekerja_ak": float(df['Februari.3'])
        },
        "data_agustus": {
            "bekerja": int(df['Agustus']),
            "pengangguran": int(df['Agustus.1']),
            "jumlah_ak": int(df['Agustus.2']),
            "persentase_bekerja_ak": float(df['Agustus.3'])
        }
    }
    collection.insert_one(json)
    print(f"Inserted data for province: {prov_name}")
    return True

collection = utils.get_mongo_collection("angkatan_kerja")

try:    
    angkatan_kerja_df = pd.read_csv('../../../raw/angkatan-kerja/AK-2025.csv', skiprows=4)
except Exception as e:
    print(f"Error reading CSV file: {e}")

count = 0

for index, row in angkatan_kerja_df.iterrows():
    if extract_json(row, 2025):
        count += 1

print(f"Total records inserted: {count}")