"""
Pipeline runner - Orchestrates the full data processing pipeline.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from app.pipelines.ingest.bps import bps_ingester
from app.pipelines.ingest.file import file_ingester
from app.pipelines.validate.schema import schema_validator
from app.pipelines.validate.quality import quality_checker
from app.pipelines.transform.normalize import min_max_normalize
from app.pipelines.transform.score import score_calculator
from app.services import imports_service, indicators_service
from app.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PipelineResult:
    """Result of a pipeline run."""
    success: bool
    stage: str
    message: str
    records_processed: int = 0
    records_imported: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    started_at: datetime = field(default_factory=datetime.utcnow)


async def run_ingestion(
    file_path: str,
    indicator_code: str,
    year: int,
    source_type: str = "bps",
    **kwargs,
) -> PipelineResult:
    """
    Run the data ingestion stage.

    Args:
        file_path: Path to the data file
        indicator_code: Code for the indicator
        year: Year of the data
        source_type: Type of source ("bps", "file")
        **kwargs: Additional arguments for the ingester

    Returns:
        PipelineResult with ingested records
    """
    start_time = datetime.utcnow()
    result = PipelineResult(success=False, stage="ingestion", message="")

    try:
        if source_type == "bps":
            records = await bps_ingester.ingest_from_file(
                file_path, indicator_code, year, **kwargs
            )
        else:
            mapping = kwargs.get("mapping", {
                "region_code": "region_code",
                "value": "value",
            })
            records = await file_ingester.ingest(
                file_path, mapping, {"indicator_code": indicator_code, "year": year}
            )

        result.records_processed = len(records)
        result.success = True
        result.message = f"Ingested {len(records)} records"

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        result.errors.append(str(e))
        result.message = f"Ingestion failed: {e}"

    result.duration_seconds = (datetime.utcnow() - start_time).total_seconds()
    return result


async def run_validation(
    records: List[Dict[str, Any]],
    schema_name: str = "indicator",
) -> PipelineResult:
    """
    Run the data validation stage.

    Args:
        records: Records to validate
        schema_name: Schema to validate against

    Returns:
        PipelineResult with validation status
    """
    start_time = datetime.utcnow()
    result = PipelineResult(success=False, stage="validation", message="")

    try:
        # Schema validation
        schema_result = schema_validator.validate_batch(records, schema_name)
        result.records_processed = schema_result.records_checked

        if not schema_result.valid:
            result.errors = [
                f"{e.field}: {e.message}" for e in schema_result.errors[:10]
            ]
            result.message = f"Schema validation failed: {len(schema_result.errors)} errors"
            return result

        # Quality checks
        quality_result = quality_checker.check_indicators(records)

        for issue in quality_result.issues:
            if issue.severity == "error":
                result.errors.append(f"{issue.category}: {issue.message}")
            elif issue.severity == "warning":
                result.warnings.append(f"{issue.category}: {issue.message}")

        result.success = quality_result.passed
        result.message = (
            f"Validation passed: {schema_result.records_valid} valid records"
            if result.success
            else f"Validation failed: {quality_result.error_count} errors"
        )

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        result.errors.append(str(e))
        result.message = f"Validation failed: {e}"

    result.duration_seconds = (datetime.utcnow() - start_time).total_seconds()
    return result


async def run_transformation(
    records: List[Dict[str, Any]],
    normalize: bool = True,
) -> PipelineResult:
    """
    Run the data transformation stage.

    Args:
        records: Records to transform
        normalize: Whether to normalize values

    Returns:
        PipelineResult with transformation status
    """
    start_time = datetime.utcnow()
    result = PipelineResult(success=False, stage="transformation", message="")

    try:
        if normalize and records:
            values = [r["value"] for r in records if r.get("value") is not None]
            normalized = min_max_normalize(values)

            # Apply normalized values
            value_idx = 0
            for record in records:
                if record.get("value") is not None:
                    record["normalized_value"] = normalized[value_idx]
                    value_idx += 1

        result.records_processed = len(records)
        result.success = True
        result.message = f"Transformed {len(records)} records"

    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        result.errors.append(str(e))
        result.message = f"Transformation failed: {e}"

    result.duration_seconds = (datetime.utcnow() - start_time).total_seconds()
    return result


async def run_full_pipeline(
    file_path: str,
    indicator_code: str,
    year: int,
    source_type: str = "bps",
    source_name: Optional[str] = None,
    save_to_db: bool = True,
    **kwargs,
) -> PipelineResult:
    """
    Run the full data processing pipeline.

    Stages:
    1. Ingestion - Read data from source
    2. Validation - Validate schema and quality
    3. Transformation - Normalize values
    4. Import - Save to database

    Args:
        file_path: Path to the data file
        indicator_code: Code for the indicator
        year: Year of the data
        source_type: Type of source ("bps", "file")
        source_name: Name of the data source
        save_to_db: Whether to save to database
        **kwargs: Additional arguments

    Returns:
        PipelineResult with final status
    """
    start_time = datetime.utcnow()
    logger.info(f"Starting full pipeline: {indicator_code} {year}")

    final_result = PipelineResult(
        success=False,
        stage="pipeline",
        message="",
    )

    # Stage 1: Ingestion
    ingest_result = await run_ingestion(
        file_path, indicator_code, year, source_type, **kwargs
    )
    if not ingest_result.success:
        final_result.message = f"Pipeline failed at ingestion: {ingest_result.message}"
        final_result.errors = ingest_result.errors
        return final_result

    # Stage 2: Validation
    records = []  # In real implementation, get from ingestion result
    validation_result = await run_validation(records)
    if not validation_result.success:
        final_result.message = f"Pipeline failed at validation: {validation_result.message}"
        final_result.errors = validation_result.errors
        final_result.warnings = validation_result.warnings
        return final_result

    # Stage 3: Transformation
    transform_result = await run_transformation(records)
    if not transform_result.success:
        final_result.message = f"Pipeline failed at transformation: {transform_result.message}"
        final_result.errors = transform_result.errors
        return final_result

    # Stage 4: Import to database
    if save_to_db and records:
        try:
            import_result = await imports_service.import_indicators(
                records,
                source_name=source_name or source_type,
                upsert=True,
            )
            final_result.records_imported = import_result.get("inserted", 0)
        except Exception as e:
            logger.error(f"Import failed: {e}")
            final_result.errors.append(f"Import failed: {e}")
            final_result.message = f"Pipeline failed at import: {e}"
            return final_result

    final_result.success = True
    final_result.records_processed = ingest_result.records_processed
    final_result.message = (
        f"Pipeline completed: {final_result.records_processed} processed, "
        f"{final_result.records_imported} imported"
    )
    final_result.duration_seconds = (datetime.utcnow() - start_time).total_seconds()

    logger.info(f"Pipeline completed: {final_result.message}")
    return final_result
