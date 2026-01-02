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


@router.post("/rollback/{source_id}")
async def rollback_import(source_id: str):
    """
    Rollback an import by deleting all indicators from a source.
    """
    result = await imports_service.rollback_import(source_id)
    return result


@router.get("/history")
async def get_import_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
):
    """
    Get history of import operations.
    """
    from app.repositories import get_sources_repository
    repo = await get_sources_repository()
    sources = await repo.find_all(skip=skip, limit=limit)

    return {
        "imports": sources,
        "total": len(sources),
    }
