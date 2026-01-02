"""
Data validation - Quality checks for data integrity.
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import statistics

from app.logging import get_logger

logger = get_logger(__name__)


@dataclass
class QualityIssue:
    """Represents a data quality issue."""
    severity: str  # "error", "warning", "info"
    category: str
    message: str
    affected_records: int = 0
    details: Optional[Dict] = None


@dataclass
class QualityReport:
    """Data quality assessment report."""
    passed: bool
    issues: List[QualityIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    checked_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")


class QualityChecker:
    """Checker for data quality issues."""

    # Valid Indonesian province codes
    VALID_REGION_CODES: Set[str] = {
        "ID-AC", "ID-SU", "ID-SB", "ID-RI", "ID-JA", "ID-SS", "ID-BE", "ID-LA",
        "ID-BB", "ID-KR", "ID-JK", "ID-JB", "ID-JT", "ID-YO", "ID-JI", "ID-BT",
        "ID-BA", "ID-NB", "ID-NT", "ID-KB", "ID-KT", "ID-KS", "ID-KI", "ID-KU",
        "ID-SA", "ID-ST", "ID-SN", "ID-SG", "ID-GO", "ID-SR", "ID-MA", "ID-MU",
        "ID-PB", "ID-PA", "ID-PS", "ID-PT", "ID-PP", "ID-PD",
    }

    def check_indicators(
        self,
        records: List[Dict[str, Any]],
        year: Optional[int] = None,
    ) -> QualityReport:
        """
        Run quality checks on indicator records.

        Args:
            records: List of indicator records
            year: Expected year (for year consistency check)

        Returns:
            QualityReport with issues and metrics
        """
        issues = []
        metrics = {
            "total_records": len(records),
            "unique_regions": 0,
            "unique_indicators": 0,
        }

        if not records:
            return QualityReport(passed=True, issues=issues, metrics=metrics)

        # Collect statistics
        region_codes = set()
        indicator_codes = set()
        years = set()
        values = []

        for record in records:
            region_codes.add(record.get("region_code"))
            indicator_codes.add(record.get("indicator_code"))
            years.add(record.get("year"))
            if record.get("value") is not None:
                values.append(record["value"])

        metrics["unique_regions"] = len(region_codes)
        metrics["unique_indicators"] = len(indicator_codes)
        metrics["years"] = sorted(years)

        # Check for invalid region codes
        invalid_regions = region_codes - self.VALID_REGION_CODES - {None}
        if invalid_regions:
            issues.append(QualityIssue(
                severity="warning",
                category="invalid_region",
                message=f"Unknown region codes found",
                affected_records=len([
                    r for r in records
                    if r.get("region_code") in invalid_regions
                ]),
                details={"invalid_codes": list(invalid_regions)},
            ))

        # Check for missing regions
        missing_regions = self.VALID_REGION_CODES - region_codes
        if missing_regions:
            issues.append(QualityIssue(
                severity="info",
                category="missing_region",
                message=f"{len(missing_regions)} regions missing from data",
                details={"missing_codes": list(missing_regions)[:10]},
            ))

        # Check year consistency
        if year and years != {year}:
            issues.append(QualityIssue(
                severity="warning",
                category="year_mismatch",
                message=f"Expected year {year}, found: {years}",
            ))

        # Check for outliers in values
        if values:
            metrics["value_min"] = min(values)
            metrics["value_max"] = max(values)
            metrics["value_mean"] = statistics.mean(values)

            if len(values) > 2:
                metrics["value_stdev"] = statistics.stdev(values)
                outliers = self._find_outliers(values)
                if outliers:
                    issues.append(QualityIssue(
                        severity="info",
                        category="outliers",
                        message=f"Found {len(outliers)} potential outlier values",
                        affected_records=len(outliers),
                    ))

        # Check for duplicates
        seen = set()
        duplicates = 0
        for record in records:
            key = (
                record.get("region_code"),
                record.get("indicator_code"),
                record.get("year"),
            )
            if key in seen:
                duplicates += 1
            seen.add(key)

        if duplicates:
            issues.append(QualityIssue(
                severity="error",
                category="duplicates",
                message=f"Found {duplicates} duplicate records",
                affected_records=duplicates,
            ))

        # Determine if passed (no errors)
        passed = not any(i.severity == "error" for i in issues)

        return QualityReport(
            passed=passed,
            issues=issues,
            metrics=metrics,
        )

    def _find_outliers(
        self,
        values: List[float],
        threshold: float = 3.0,
    ) -> List[float]:
        """Find values that are more than threshold standard deviations from mean."""
        if len(values) < 3:
            return []

        mean = statistics.mean(values)
        stdev = statistics.stdev(values)

        if stdev == 0:
            return []

        return [v for v in values if abs(v - mean) / stdev > threshold]


# Singleton instance
quality_checker = QualityChecker()
