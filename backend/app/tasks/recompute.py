"""
Score recomputation task.

This module provides functions to recompute composite scores
based on the latest indicator data and weights.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime

from app.repositories import get_indicators_repository, get_scores_repository, get_configs_repository
from app.pipelines.transform.score import score_calculator, ScoreCalculator, IndicatorWeight
from app.pipelines.transform.normalize import min_max_normalize
from app.services import alerts_service
from app.logging import get_logger

logger = get_logger(__name__)


async def recompute_scores(
    year: int,
    generate_alerts: bool = True,
) -> Dict[str, Any]:
    """
    Recompute composite scores for a specific year.

    Steps:
    1. Fetch all indicators for the year
    2. Normalize values per indicator
    3. Calculate composite scores
    4. Update rankings
    5. Optionally generate alerts

    Args:
        year: Year to recompute scores for
        generate_alerts: Whether to generate alerts after recomputation

    Returns:
        Dict with recomputation results
    """
    start_time = datetime.utcnow()
    logger.info(f"Starting score recomputation for year {year}")

    indicators_repo = await get_indicators_repository()
    scores_repo = await get_scores_repository()
    configs_repo = await get_configs_repository()

    # Get custom weights if configured
    weights_config = await configs_repo.find_by_key("indicator_weights")
    if weights_config:
        weights = {
            code: IndicatorWeight(code=code, weight=w, invert=code in ["POVERTY_RATE", "GINI", "UNEMPLOYMENT"])
            for code, w in weights_config.get("value", {}).items()
        }
        calculator = ScoreCalculator(weights)
    else:
        calculator = score_calculator

    # Fetch indicators for the year
    indicators = await indicators_repo.find_by_year(year)
    if not indicators:
        logger.warning(f"No indicators found for year {year}")
        return {
            "success": False,
            "message": f"No indicators found for year {year}",
            "year": year,
        }

    # Group by indicator code for normalization
    by_indicator: Dict[str, List[Dict]] = {}
    for ind in indicators:
        code = ind["indicator_code"]
        if code not in by_indicator:
            by_indicator[code] = []
        by_indicator[code].append(ind)

    # Normalize each indicator
    normalized: Dict[str, Dict[str, float]] = {}  # region_code -> indicator_code -> value
    for code, records in by_indicator.items():
        values = [r["value"] for r in records]
        norm_values = min_max_normalize(values)

        for record, norm_val in zip(records, norm_values):
            region = record["region_code"]
            if region not in normalized:
                normalized[region] = {}
            normalized[region][code] = norm_val

    # Calculate composite scores
    scores = []
    for region_code, indicators_dict in normalized.items():
        composite = calculator.calculate_composite_score(indicators_dict)
        dimension_scores = calculator.calculate_dimension_scores(indicators_dict)

        scores.append({
            "region_code": region_code,
            "year": year,
            "composite_score": round(composite, 2),
            "economic_score": round(dimension_scores.get("economic", 0) or 0, 2),
            "social_score": round(dimension_scores.get("social", 0) or 0, 2),
            "infrastructure_score": round(dimension_scores.get("infrastructure", 0) or 0, 2),
            "calculated_at": datetime.utcnow(),
        })

    # Get previous year scores for delta
    prev_scores = await scores_repo.find_rankings(year - 1)
    prev_scores_list = [(s["region_code"], s["composite_score"]) for s in prev_scores]

    # Calculate rankings
    current_scores_list = [(s["region_code"], s["composite_score"]) for s in scores]
    rankings = calculator.calculate_rankings(current_scores_list, prev_scores_list)

    # Merge rankings into scores
    rankings_map = {r["region_code"]: r for r in rankings}
    for score in scores:
        ranking = rankings_map.get(score["region_code"], {})
        score["rank"] = ranking.get("rank")
        score["previous_rank"] = ranking.get("previous_rank")
        score["rank_delta"] = ranking.get("rank_delta")

    # Save scores
    saved = 0
    for score in scores:
        await scores_repo.upsert(
            {"region_code": score["region_code"], "year": year},
            score,
        )
        saved += 1

    logger.info(f"Saved {saved} scores for year {year}")

    # Generate alerts if requested
    alerts_generated = 0
    if generate_alerts:
        alert_result = await alerts_service.generate_alerts(year)
        alerts_generated = alert_result.get("created", 0)

    duration = (datetime.utcnow() - start_time).total_seconds()

    return {
        "success": True,
        "message": f"Recomputed scores for {saved} regions",
        "year": year,
        "regions_processed": saved,
        "alerts_generated": alerts_generated,
        "duration_seconds": duration,
    }


async def recompute_all_scores(
    start_year: int = 2015,
    end_year: Optional[int] = None,
    generate_alerts: bool = False,
) -> Dict[str, Any]:
    """
    Recompute scores for all years.

    Args:
        start_year: First year to recompute
        end_year: Last year to recompute (current year if None)
        generate_alerts: Whether to generate alerts (only for latest year)

    Returns:
        Dict with recomputation results
    """
    if end_year is None:
        end_year = datetime.now().year

    logger.info(f"Starting full score recomputation: {start_year}-{end_year}")

    results = []
    for year in range(start_year, end_year + 1):
        # Only generate alerts for the latest year
        gen_alerts = generate_alerts and year == end_year
        result = await recompute_scores(year, generate_alerts=gen_alerts)
        results.append(result)

    total_regions = sum(r.get("regions_processed", 0) for r in results)
    successful = sum(1 for r in results if r.get("success"))

    return {
        "success": successful == len(results),
        "message": f"Recomputed {total_regions} scores across {successful} years",
        "years_processed": successful,
        "total_regions": total_regions,
        "details": results,
    }
