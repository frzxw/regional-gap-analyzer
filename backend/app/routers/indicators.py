from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Dict, Optional, Any
from app.db import get_database
from datetime import datetime

router = APIRouter()

COLLECTION_MAPPING = {
    "gini_ratio": "gini_ratio",
    "ipm": "indeks_pembangunan_manusia",
    "tpt": "tingkat_pengangguran_terbuka",
    "kependudukan": "kependudukan",
    "pdrb_per_kapita": "pdrb_per_kapita",
    "ihk": "indeks_harga_konsumen",
    "inflasi_tahunan": "inflasi_tahunan",
    "persentase_penduduk_miskin": "persentase_penduduk_miskin",
    "angkatan_kerja": "angkatan_kerja",
    "rata_rata_upah_bersih": "rata_rata_upah_bersih",
}

from app.common.provinces import PROVINCE_NAMES

@router.get("/{indicator_code}")
async def list_indicator_data(
    indicator_code: str,
    tahun: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    Generic list endpoint for any indicator.
    """
    collection_name = COLLECTION_MAPPING.get(indicator_code)
    if not collection_name:
        raise HTTPException(status_code=404, detail=f"Indicator '{indicator_code}' not found")

    db = await get_database()
    collection = db[collection_name]

    query = {}
    if tahun:
        query["tahun"] = tahun

    cursor = collection.find(query).skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    total = await collection.count_documents(query)

    # Convert ObjectId to string and enrich with province name
    data = []
    for item in items:
        item["_id"] = str(item["_id"])
        
        # Enrich province name if missing
        if "province_name" not in item:
             pid = str(item.get("province_id", ""))
             item["province_name"] = PROVINCE_NAMES.get(pid, f"Unknown ({pid})")
             
        data.append(item)

    return {
        "data": data,
        "total": total,
        "page": (skip // limit) + 1,
        "page_size": limit,
    }

@router.put("/{indicator_code}/{province_id}/{tahun}")
async def update_indicator_data(
    indicator_code: str,
    province_id: str,
    tahun: int,
    payload: Dict[str, Any] = Body(...),
):
    """
    Generic update endpoint.
    """
    collection_name = COLLECTION_MAPPING.get(indicator_code)
    if not collection_name:
        raise HTTPException(status_code=404, detail=f"Indicator '{indicator_code}' not found")

    db = await get_database()
    collection = db[collection_name]

    # Only allow updating value for now, or other specific fields
    update_fields = {}
    if "value" in payload:
        update_fields["value"] = payload["value"]
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    update_fields["updated_at"] = datetime.utcnow()

    result = await collection.update_one(
        {"province_id": province_id, "tahun": tahun},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Data not found")

    return {"message": "Data updated successfully", "success": True}

@router.delete("/{indicator_code}/{province_id}/{tahun}")
async def delete_indicator_data(
    indicator_code: str,
    province_id: str,
    tahun: int,
):
    """
    Generic delete endpoint.
    """
    collection_name = COLLECTION_MAPPING.get(indicator_code)
    if not collection_name:
        raise HTTPException(status_code=404, detail=f"Indicator '{indicator_code}' not found")

    db = await get_database()
    collection = db[collection_name]

    result = await collection.delete_one({"province_id": province_id, "tahun": tahun})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Data not found")

    return {"message": "Data deleted successfully", "success": True}
