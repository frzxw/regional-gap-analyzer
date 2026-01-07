"""
Imports router - API endpoints for data import operations.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
import tempfile
import os

from app.services import imports_service
from app.pipelines import run_full_pipeline, run_validation

router = APIRouter(prefix="/imports", tags=["Data Import"])


@router.post("/file")
async def import_from_file(
    file: UploadFile = File(...),
    indicator_code: str = Form(...),
    year: int = Form(...),
    source_name: Optional[str] = Form(None),
    source_type: str = Form("file"),
):
    """
    Import indicator data from an uploaded file.

    Supports CSV, Excel, and JSON formats.
    """
    # Validate file type
    allowed_extensions = {".csv", ".xlsx", ".xls", ".json"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {allowed_extensions}",
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Run the import pipeline
        result = await run_full_pipeline(
            file_path=tmp_path,
            indicator_code=indicator_code,
            year=year,
            source_type=source_type,
            source_name=source_name or file.filename,
            save_to_db=True,
        )

        if not result.success:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result.message,
                    "errors": result.errors,
                    "warnings": result.warnings,
                },
            )

        return {
            "success": True,
            "message": result.message,
            "records_processed": result.records_processed,
            "records_imported": result.records_imported,
            "duration_seconds": result.duration_seconds,
        }

    finally:
        # Clean up temp file
        os.unlink(tmp_path)


@router.post("/validate")
async def validate_import_file(
    file: UploadFile = File(...),
):
    """
    Validate an import file without actually importing.

    Returns validation errors and a preview of the data.
    """
    # Validate file type
    allowed_extensions = {".csv", ".xlsx", ".xls", ".json"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}",
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        from app.pipelines.ingest.file import file_ingester
        validation = await file_ingester.validate_file(tmp_path)
        return validation

    finally:
        os.unlink(tmp_path)


@router.post("/batch")
async def import_batch(
    indicators: List[dict],
    source_name: str,
    source_id: Optional[str] = None,
    upsert: bool = True,
):
    """
    Import a batch of indicator records.

    Expected format for each indicator:
    {
        "region_code": "ID-JK",
        "indicator_code": "HDI",
        "year": 2023,
        "value": 80.5
    }
    """
    result = await imports_service.import_indicators(
        indicators=indicators,
        source_name=source_name,
        source_id=source_id,
        upsert=upsert,
    )
    return result


@router.post("/rollback/{log_id}")
async def rollback_import(log_id: str):
    """
    Delete an import log entry. Also optionally deletes imported data.
    """
    from app.db import get_database
    from bson import ObjectId
    
    try:
        db = await get_database()
        
        # Get the import log first
        import_log = await db["import_logs"].find_one({"_id": ObjectId(log_id)})
        
        if not import_log:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Import log not found")
        
        # Delete the log entry
        await db["import_logs"].delete_one({"_id": ObjectId(log_id)})
        
        return {
            "status": "deleted",
            "log_id": log_id,
            "message": f"Import log deleted successfully",
        }
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history")
async def get_import_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
):
    """
    Get history of import operations from import_logs collection.
    """
    from app.db import get_database
    from datetime import datetime
    
    db = await get_database()
    collection = db["import_logs"]
    
    # Get imports sorted by created_at descending
    cursor = collection.find().sort("created_at", -1).skip(skip).limit(limit)
    imports = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string for JSON serialization
    result = []
    for imp in imports:
        result.append({
            "_id": str(imp.get("_id", "")),
            "name": imp.get("name", imp.get("source_name", "Unknown")),
            "indicator_code": imp.get("indicator_code", ""),
            "tahun": imp.get("tahun", imp.get("year", 0)),
            "records_count": imp.get("records_count", 0),
            "source_type": imp.get("source_type", "file"),
            "created_at": imp.get("created_at", datetime.utcnow()).isoformat() if imp.get("created_at") else None,
        })
    
    total = await collection.count_documents({})
    
    return {
        "imports": result,
        "total": total,
    }

