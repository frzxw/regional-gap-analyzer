import os, sys
import pandas as pd
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
        "indikator": "bukan_angkatan_kerja",
        "data": {
            "februari": int(df['Februari']),
            "agustus": int(df['Agustus'])
        }
    }
    collection.insert_one(json)
    print(f"Inserted data for province: {prov_name}")
    return True

collection = utils.get_mongo_collection("angkatan_kerja")

try:
    bak_df = pd.read_csv('../../../raw/angkatan-kerja/BAK-2025.csv', skiprows=3)
except Exception as e:
    print(f"Error reading CSV file: {e}")

count = 0

for index, row in bak_df.iterrows():
    if extract_json(row, 2025):
        count += 1
        
print(f"Total records inserted: {count}")