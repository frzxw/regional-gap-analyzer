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

    SEKTOR_LIST = [
        "pertanian_kehutanan_perikanan", "pertambangan_penggalian", "industri_pengolahan", "listrik_gas", 
        "air_sampah_limbah_daurulang", "konstruksi", "perdagangan", "transportasi_pergudangan", "akomodasi_makan_minum",
        "informasi_komunikasi", "jasa_keuangan", "real_estate", "jasa_perusahaan",
        "admin_pemerintahan", "jasa_pendidikan", "jasa_kesehatan", "jasa_lainnya", "total"
    ]

    current_col = 0
    sektor_data = {}
    for sektor in SEKTOR_LIST:
        suffix = "" if current_col == 0 else f".{current_col}"
        sektor_data[sektor] = {
            "februari": utils.clean_val(df["Februari" + suffix]),
            "agustus": utils.clean_val(df["Agustus" + suffix]),
            "tahunan": utils.clean_val(df["Tahunan" + suffix])
        }
        current_col += 1

    json = {   
        "province_id": province_id,
        "tahun": int(tahun),
        "indikator": "rata_rata_upah_bersih",
        "sektor": sektor_data
    }
    collection.insert_one(json)
    print(f"Inserted data for province: {prov_name}")
    return True

def extract_tahun(tahun):
    for year in tahun:
        try:
            print(f"Processing year: {year}")
            rata_rata_upah_df = pd.read_csv(f'../../../raw/rata-rata-upah/{year}.csv', skiprows=4)
            count = 0

            for index, row in rata_rata_upah_df.iterrows():
                if extract_json(row, year):
                    count += 1
                    
            print(f"Total records inserted for year {year}: {count}")
        except Exception as e:
            print(f"Error reading CSV file for year {year}: {e}")
        print(f"Finished processing year: {year}\n")

tahun = [
    '2024',
    '2025'
]

collection = utils.get_mongo_collection("rata_rata_upah_bersih")
extract_tahun(tahun)