"""
Data validation - Schema validation for imported data.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from app.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ValidationError:
    """Represents a validation error."""
    field: str
    message: str
    value: Any = None
    row_index: Optional[int] = None


@dataclass
class ValidationResult:
    """Result of a validation run."""
    valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    records_checked: int = 0
    records_valid: int = 0

    @property
    def records_invalid(self) -> int:
        return self.records_checked - self.records_valid


class SchemaValidator:
    """Validator for data schemas."""

    # Schema definitions for different record types
    SCHEMAS = {
        "indicator": {
            "required": ["region_code", "indicator_code", "year", "value"],
            "types": {
                "region_code": str,
                "indicator_code": str,
                "year": int,
                "value": (int, float),
            },
            "constraints": {
                "year": lambda x: 1990 <= x <= datetime.now().year + 1,
                "value": lambda x: x is not None,
            },
        },
        "region": {
            "required": ["code", "name"],
            "types": {
                "code": str,
                "name": str,
                "population": (int, type(None)),
                "area_km2": (float, int, type(None)),
            },
            "constraints": {
                "code": lambda x: len(x) >= 2,
            },
        },
        "score": {
            "required": ["region_code", "year", "composite_score"],
            "types": {
                "region_code": str,
                "year": int,
                "composite_score": (int, float),
            },
            "constraints": {
                "composite_score": lambda x: 0 <= x <= 100,
            },
        },
    }

    def validate_record(
        self,
        record: Dict[str, Any],
        schema_name: str,
    ) -> List[ValidationError]:
        """
        Validate a single record against a schema.

        Args:
            record: Record to validate
            schema_name: Name of schema to validate against

        Returns:
            List of validation errors (empty if valid)
        """
        if schema_name not in self.SCHEMAS:
            return [ValidationError("_schema", f"Unknown schema: {schema_name}")]

        schema = self.SCHEMAS[schema_name]
        errors = []

        # Check required fields
        for field in schema.get("required", []):
            if field not in record or record[field] is None:
                errors.append(ValidationError(
                    field=field,
                    message=f"Required field missing: {field}",
                ))

        # Check types
        for field, expected_type in schema.get("types", {}).items():
            if field in record and record[field] is not None:
                if not isinstance(record[field], expected_type):
                    errors.append(ValidationError(
                        field=field,
                        message=f"Invalid type for {field}: expected {expected_type}",
                        value=record[field],
                    ))

        # Check constraints
        for field, constraint in schema.get("constraints", {}).items():
            if field in record and record[field] is not None:
                try:
                    if not constraint(record[field]):
                        errors.append(ValidationError(
                            field=field,
                            message=f"Constraint failed for {field}",
                            value=record[field],
                        ))
                except Exception as e:
                    errors.append(ValidationError(
                        field=field,
                        message=f"Constraint error for {field}: {e}",
                        value=record[field],
                    ))

        return errors

    def validate_batch(
        self,
        records: List[Dict[str, Any]],
        schema_name: str,
        fail_fast: bool = False,
    ) -> ValidationResult:
        """
        Validate a batch of records.

        Args:
            records: List of records to validate
            schema_name: Name of schema to validate against
            fail_fast: Stop on first error if True

        Returns:
            ValidationResult with all errors
        """
        result = ValidationResult(valid=True, records_checked=len(records))
        valid_count = 0

        for i, record in enumerate(records):
            errors = self.validate_record(record, schema_name)

            if errors:
                for error in errors:
                    error.row_index = i
                    result.errors.append(error)

                if fail_fast:
                    result.valid = False
                    return result
            else:
                valid_count += 1

        result.records_valid = valid_count
        result.valid = len(result.errors) == 0
        return result


# Singleton instance
schema_validator = SchemaValidator()
