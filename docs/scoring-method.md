# Scoring Methodology

## Overview

The Regional Gap Analyzer uses a multi-dimensional scoring system to quantify regional inequality across Indonesian provinces. This document describes the methodology for calculating scores.

## Scoring Framework

### 1. Indicator Categories

We measure inequality across four main dimensions:

| Category | Weight | Indicators |
|----------|--------|------------|
| **Economic** | 30% | GDP per capita, Unemployment, Poverty rate |
| **Infrastructure** | 25% | Road density, Electricity access, Internet access |
| **Health** | 25% | Hospital beds, Life expectancy, Infant mortality |
| **Education** | 20% | Literacy rate, School enrollment, Years of schooling |

### 2. Normalization Method

All raw indicators are normalized to a 0-100 scale using **Min-Max Normalization**:

$$
\text{Score} = \frac{X - X_{\min}}{X_{\max} - X_{\min}} \times 100
$$

Where:
- $X$ = Raw value for the region
- $X_{\min}$ = Minimum value across all regions
- $X_{\max}$ = Maximum value across all regions

### 3. Inverse Indicators

Some indicators are "bad" (higher raw value = worse outcome). These are inverted:

$$
\text{Score}_{\text{inverse}} = 100 - \text{Score}
$$

**Inverse indicators:**
- Unemployment rate
- Poverty rate
- Infant mortality rate

### 4. Composite Score Calculation

The composite score is a weighted average:

$$
\text{Composite} = \sum_{i=1}^{n} w_i \times \text{Score}_i
$$

Where:
- $w_i$ = Weight for indicator $i$
- $\sum w_i = 1$

## Gap Analysis

### Regional Gap Index

The gap between a region and the national average:

$$
\text{Gap}_r = \text{Score}_r - \text{Score}_{\text{national avg}}
$$

- Positive = Above average (better)
- Negative = Below average (worse)

### Inequality Coefficient

Variation across all regions (Coefficient of Variation):

$$
\text{CV} = \frac{\sigma}{\mu} \times 100
$$

Where:
- $\sigma$ = Standard deviation of scores
- $\mu$ = Mean score

## Implementation

### Python Implementation

```python
import numpy as np

def normalize_min_max(values: list[float], inverse: bool = False) -> list[float]:
    """Normalize values to 0-100 scale."""
    arr = np.array(values)
    min_val = arr.min()
    max_val = arr.max()

    if max_val == min_val:
        return [50.0] * len(values)

    normalized = (arr - min_val) / (max_val - min_val) * 100

    if inverse:
        normalized = 100 - normalized

    return normalized.tolist()

def calculate_composite(scores: dict[str, float], weights: dict[str, float]) -> float:
    """Calculate weighted composite score."""
    weighted_sum = sum(scores[k] * weights[k] for k in scores)
    weight_sum = sum(weights.values())
    return weighted_sum / weight_sum
```

## Score Interpretation

| Score Range | Interpretation | Color Code |
|-------------|----------------|------------|
| 80-100 | Very High Development | Dark Green |
| 60-79 | High Development | Light Green |
| 40-59 | Medium Development | Yellow |
| 20-39 | Low Development | Orange |
| 0-19 | Very Low Development | Red |

## Limitations

1. **Data Quality**: Scores are only as good as input data
2. **Weighting Subjectivity**: Category weights are policy choices
3. **Temporal Lag**: Data may be 1-2 years old
4. **Missing Data**: Some regions may lack certain indicators

## TODO

- [ ] Implement sensitivity analysis for weights
- [ ] Add confidence intervals for scores
- [ ] Create year-over-year comparison
- [ ] Add sub-provincial (district) scoring
