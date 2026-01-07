import { INDICATORS, PROVINCES, YEARS } from "./constants"
import type { NormalizationType, ProvinceData } from "./types"

// Simple mock data generator
export const generateMockData = (): ProvinceData[] => {
  const data: ProvinceData[] = []

  PROVINCES.forEach((prov) => {
    YEARS.forEach((year) => {
      // Base values that evolve slightly over years
      const population = 1000000 + Math.random() * 10000000
      const area = 5000 + Math.random() * 50000

      const metrics: Record<string, number> = {}
      INDICATORS.forEach((ind) => {
        let base = 0
        if (ind.id === "gini") base = 0.3 + Math.random() * 0.15
        else if (ind.id === "p0") base = 5 + Math.random() * 15
        else if (ind.id === "ipm") base = 65 + Math.random() * 15
        else if (ind.id === "tpt") base = 3 + Math.random() * 7
        else if (ind.id === "pdrb_kapita") base = 30000000 + Math.random() * 100000000
        else base = Math.random() * 1000

        // Add trend
        const trend = (year - 2019) * (Math.random() > 0.5 ? 1 : -1) * 0.05 * base
        metrics[ind.id] = base + trend
      })

      data.push({
        provinceId: prov.id,
        provinceName: prov.name,
        year,
        population,
        area,
        metrics,
      })
    })
  })

  return data
}

export const normalizeValue = (value: number, type: NormalizationType, pop: number, area: number) => {
  const density = pop / area
  switch (type) {
    case "per_100k":
      return (value / pop) * 100000
    case "per_km2":
      return value / area
    case "density_adjusted":
      return value / density
    default:
      return value
  }
}

export const calculateCompositeScore = (
  provinceData: ProvinceData,
  weights: Record<string, number>,
  normalizationOverrides: Record<string, NormalizationType>,
  allYearData: ProvinceData[], // For min-max scaling across all provinces in that year
) => {
  const normalizedMetrics: Record<string, number> = {}

  // 1. Apply Normalization
  INDICATORS.forEach((ind) => {
    const normType = normalizationOverrides[ind.id] || ind.defaultNormalization
    normalizedMetrics[ind.id] = normalizeValue(
      provinceData.metrics[ind.id],
      normType,
      provinceData.population,
      provinceData.area,
    )
  })

  // 2. Min-Max Scaling per Indicator (across all provinces for that year)
  const scores: Record<string, number> = {}
  INDICATORS.forEach((ind) => {
    const values = allYearData.map((d) => {
      const normType = normalizationOverrides[ind.id] || ind.defaultNormalization
      return normalizeValue(d.metrics[ind.id], normType, d.population, d.area)
    })
    const min = Math.min(...values)
    const max = Math.max(...values)

    let scaled = (normalizedMetrics[ind.id] - min) / (max - min || 1)

    // Invert if higher is better (so 0 is always best, 1 is always worst for inequality calculation)
    if (ind.direction === "higher_is_better") {
      scaled = 1 - scaled
    }

    scores[ind.id] = scaled * 100
  })

  // 3. Weighted Sum
  let totalScore = 0
  let totalWeight = 0
  INDICATORS.forEach((ind) => {
    const weight = weights[ind.id] || 0
    totalScore += scores[ind.id] * weight
    totalWeight += weight
  })

  return totalScore / (totalWeight || 1)
}
