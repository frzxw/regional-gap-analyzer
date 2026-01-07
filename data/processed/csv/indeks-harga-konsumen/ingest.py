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

    bulan_list = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ]

    json = {
        "province_id": province_id,
        "tahun": int(tahun),
        "indikator": "ihk_indeks_harga_konsumen",
        "data_bulanan": {
            bulan.lower(): utils.clean_val(df[bulan]) for bulan in bulan_list
        },
        "tahunan": utils.clean_val(df['Tahunan'])
    }
    collection.insert_one(json)
    print(f"Inserted data for province: {prov_name}")
    return True

def extract_tahun(tahun):
    for year in tahun:
        try:
            print(f"Processing year: {year}")
            bak_df = pd.read_csv(f'../../../raw/indeks-harga-konsumen/{year}.csv', skiprows=3)
            count = 0

            for index, row in bak_df.iterrows():
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

collection = utils.get_mongo_collection("indeks_harga_konsumen")
extract_tahun(tahun)