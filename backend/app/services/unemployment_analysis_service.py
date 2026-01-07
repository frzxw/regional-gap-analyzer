"""
Service for unemployment rate analysis, scoring, and alerts.
"""

from typing import List, Optional, Tuple
import statistics
from app.db.client import get_database
from app.repositories.tingkat_pengangguran_terbuka_repo import TingkatPengangguranTerbukaRepository
from app.models.unemployment_analysis import (
    UnemploymentScore, TrendAnalysis, Alert, ProvinceAnalysis,
    RegionalGapAnalysis, ComparisonAnalysis, SeverityLevel, TrendDirection
)


class UnemploymentAnalysisService:
    """Service for analyzing unemployment data and generating insights."""

    def calculate_score(self, unemployment_rate: float) -> UnemploymentScore:
        """
        Calculate score based on unemployment rate.
        
        Scoring logic:
        - 0-3%: Excellent (90-100 points)
        - 3-5%: Good (70-89 points)
        - 5-7%: Fair (50-69 points)
        - 7-10%: Poor (30-49 points)
        - >10%: Critical (0-29 points)
        """
        if unemployment_rate <= 3:
            score = 100 - int(unemployment_rate * 3.33)
            category = "Excellent"
            severity = SeverityLevel.LOW
        elif unemployment_rate <= 5:
            score = 90 - int((unemployment_rate - 3) * 10)
            category = "Good"
            severity = SeverityLevel.LOW
        elif unemployment_rate <= 7:
            score = 70 - int((unemployment_rate - 5) * 10)
            category = "Fair"
            severity = SeverityLevel.MEDIUM
        elif unemployment_rate <= 10:
            score = 50 - int((unemployment_rate - 7) * 6.67)
            category = "Poor"
            severity = SeverityLevel.HIGH
        else:
            score = max(0, 30 - int((unemployment_rate - 10) * 3))
            category = "Critical"
            severity = SeverityLevel.CRITICAL

        return UnemploymentScore(
            rate=unemployment_rate,
            score=max(0, min(100, score)),
            category=category,
            severity=severity
        )

    def analyze_trend(self, rate_from: float, rate_to: float, year_from: int, year_to: int) -> TrendAnalysis:
        """Analyze trend between two years."""
        change_absolute = rate_to - rate_from
        change_percentage = (change_absolute / rate_from * 100) if rate_from > 0 else 0
        
        # Determine direction (negative change is good for unemployment)
        if change_absolute < -0.5:
            direction = TrendDirection.IMPROVING
        elif change_absolute > 0.5:
            direction = TrendDirection.WORSENING
        else:
            direction = TrendDirection.STABLE
        
        is_significant = abs(change_absolute) > 0.5
        
        return TrendAnalysis(
            year_from=year_from,
            year_to=year_to,
            rate_from=rate_from,
            rate_to=rate_to,
            change_absolute=round(change_absolute, 2),
            change_percentage=round(change_percentage, 2),
            direction=direction,
            is_significant=is_significant
        )

    def generate_alerts(self, province_name: str, score: UnemploymentScore, trend: Optional[TrendAnalysis]) -> List[Alert]:
        """Generate alerts based on score and trend."""
        alerts = []
        
        # Critical unemployment rate alert
        if score.severity == SeverityLevel.CRITICAL:
            alerts.append(Alert(
                type="critical_unemployment",
                severity=SeverityLevel.CRITICAL,
                message=f"{province_name} has critical unemployment rate of {score.rate}%",
                recommendation="Immediate intervention needed: job creation programs, skills training, and economic stimulus"
            ))
        
        # High unemployment alert
        elif score.severity == SeverityLevel.HIGH:
            alerts.append(Alert(
                type="high_unemployment",
                severity=SeverityLevel.HIGH,
                message=f"{province_name} has high unemployment rate of {score.rate}%",
                recommendation="Implement targeted employment programs and monitor closely"
            ))
        
        # Worsening trend alert
        if trend and trend.direction == TrendDirection.WORSENING and trend.is_significant:
            alerts.append(Alert(
                type="worsening_trend",
                severity=SeverityLevel.HIGH if abs(trend.change_absolute) > 1 else SeverityLevel.MEDIUM,
                message=f"Unemployment increased by {abs(trend.change_absolute):.1f} percentage points from {trend.year_from} to {trend.year_to}",
                recommendation="Investigate causes and implement corrective measures"
            ))
        
        # Improvement recognition
        if trend and trend.direction == TrendDirection.IMPROVING and trend.is_significant:
            alerts.append(Alert(
                type="positive_trend",
                severity=SeverityLevel.LOW,
                message=f"Unemployment decreased by {abs(trend.change_absolute):.1f} percentage points - positive progress",
                recommendation="Continue current policies and share best practices"
            ))
        
        return alerts

    async def analyze_regional_gap(self, year: int) -> RegionalGapAnalysis:
        """
        Analyze regional inequality for a specific year.
        
        Args:
            year: Year to analyze
            
        Returns:
            Complete regional gap analysis with scoring and alerts
        """
        db = await get_database()
        repo = TingkatPengangguranTerbukaRepository(db)
        
        # Get all provinces for the year
        records, _ = await repo.find_by_year(year, skip=0, limit=100)
        
        if not records:
            raise ValueError(f"No data found for year {year}")
        
        # Get previous year data for trend analysis
        prev_year_records, _ = await repo.find_by_year(year - 1, skip=0, limit=100)
        prev_year_map = {r.get("province_id"): r for r in prev_year_records}
        
        # Analyze each province
        province_analyses = []
        unemployment_rates = []
        
        for record in records:
            province_id = record.get("province_id")
            province_name = await repo.get_province_name(province_id) or province_id
            
            # Use tahunan (annual) rate, fallback to agustus
            unemployment_rate = record.get("data", {}).get("tahunan") or record.get("data", {}).get("agustus")
            
            if unemployment_rate is None:
                continue
            
            unemployment_rates.append(unemployment_rate)
            
            # Calculate score
            score = self.calculate_score(unemployment_rate)
            
            # Analyze trend if previous year data exists
            trend = None
            prev_record = prev_year_map.get(province_id)
            if prev_record:
                prev_rate = prev_record.get("data", {}).get("tahunan") or prev_record.get("data", {}).get("agustus")
                if prev_rate:
                    trend = self.analyze_trend(prev_rate, unemployment_rate, year - 1, year)
            
            # Generate alerts
            alerts = self.generate_alerts(province_name, score, trend)
            
            province_analyses.append(ProvinceAnalysis(
                province_id=province_id,
                province_name=province_name,
                year=year,
                unemployment_rate=unemployment_rate,
                score=score,
                trend=trend,
                alerts=alerts
            ))
        
        # Sort by unemployment rate (lower is better)
        province_analyses.sort(key=lambda x: x.unemployment_rate)
        
        # Add rankings and percentiles
        total = len(province_analyses)
        for idx, analysis in enumerate(province_analyses):
            analysis.rank = idx + 1
            analysis.percentile = round((idx / total) * 100, 1)
        
        # Calculate statistics
        national_average = statistics.mean(unemployment_rates)
        critical_count = sum(1 for p in province_analyses if p.score.severity == SeverityLevel.CRITICAL)
        high_risk_count = sum(1 for p in province_analyses if p.score.severity == SeverityLevel.HIGH)
        
        # Calculate gap index (coefficient of variation)
        std_dev = statistics.stdev(unemployment_rates) if len(unemployment_rates) > 1 else 0
        gap_index = round(std_dev / national_average, 3) if national_average > 0 else 0
        
        # Generate summary
        summary = self._generate_summary(
            year, national_average, critical_count, high_risk_count, 
            total, gap_index, province_analyses
        )
        
        return RegionalGapAnalysis(
            year=year,
            national_average=round(national_average, 2),
            provinces=province_analyses,
            total_provinces=total,
            critical_provinces=critical_count,
            high_risk_provinces=high_risk_count,
            gap_index=gap_index,
            summary=summary
        )

    async def compare_years(self, year_from: int, year_to: int) -> ComparisonAnalysis:
        """Compare unemployment trends between two years."""
        db = await get_database()
        repo = TingkatPengangguranTerbukaRepository(db)
        
        # Get data for both years
        records_from, _ = await repo.find_by_year(year_from, skip=0, limit=100)
        records_to, _ = await repo.find_by_year(year_to, skip=0, limit=100)
        
        # Create maps for easy lookup
        map_from = {r.get("province_id"): r for r in records_from}
        map_to = {r.get("province_id"): r for r in records_to}
        
        # Find common provinces
        common_provinces = set(map_from.keys()) & set(map_to.keys())
        
        improved = []
        worsened = []
        stable = []
        
        for province_id in common_provinces:
            rate_from = map_from[province_id].get("data", {}).get("tahunan") or map_from[province_id].get("data", {}).get("agustus")
            rate_to = map_to[province_id].get("data", {}).get("tahunan") or map_to[province_id].get("data", {}).get("agustus")
            
            if rate_from is None or rate_to is None:
                continue
            
            province_name = await repo.get_province_name(province_id) or province_id
            trend = self.analyze_trend(rate_from, rate_to, year_from, year_to)
            score = self.calculate_score(rate_to)
            alerts = self.generate_alerts(province_name, score, trend)
            
            analysis = ProvinceAnalysis(
                province_id=province_id,
                province_name=province_name,
                year=year_to,
                unemployment_rate=rate_to,
                score=score,
                trend=trend,
                alerts=alerts
            )
            
            if trend.direction == TrendDirection.IMPROVING:
                improved.append(analysis)
            elif trend.direction == TrendDirection.WORSENING:
                worsened.append(analysis)
            else:
                stable.append(analysis)
        
        # Find biggest changes
        biggest_improvement = max(improved, key=lambda x: abs(x.trend.change_absolute)) if improved else None
        biggest_decline = max(worsened, key=lambda x: abs(x.trend.change_absolute)) if worsened else None
        
        return ComparisonAnalysis(
            year_from=year_from,
            year_to=year_to,
            provinces_improved=len(improved),
            provinces_worsened=len(worsened),
            provinces_stable=len(stable),
            biggest_improvement=biggest_improvement,
            biggest_decline=biggest_decline
        )

    def _generate_summary(self, year: int, avg: float, critical: int, high_risk: int, 
                         total: int, gap_index: float, analyses: List[ProvinceAnalysis]) -> str:
        """Generate human-readable summary."""
        summary_parts = [
            f"Unemployment analysis for {year}:",
            f"National average: {avg:.2f}%",
            f"Total provinces analyzed: {total}"
        ]
        
        if critical > 0:
            summary_parts.append(f"⚠️ {critical} province(s) with CRITICAL unemployment (>10%)")
        
        if high_risk > 0:
            summary_parts.append(f"⚠️ {high_risk} province(s) with HIGH unemployment (7-10%)")
        
        if gap_index > 0.3:
            summary_parts.append(f"⚠️ High regional inequality detected (gap index: {gap_index})")
        elif gap_index > 0.2:
            summary_parts.append(f"Moderate regional inequality (gap index: {gap_index})")
        else:
            summary_parts.append(f"Low regional inequality (gap index: {gap_index})")
        
        # Best and worst performers
        if analyses:
            best = analyses[0]
            worst = analyses[-1]
            summary_parts.append(f"Best: {best.province_name} ({best.unemployment_rate}%)")
            summary_parts.append(f"Worst: {worst.province_name} ({worst.unemployment_rate}%)")
        
        return " | ".join(summary_parts)
