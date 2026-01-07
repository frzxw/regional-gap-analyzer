export type NormalizationType = "raw" | "per_100k" | "per_km2" | "density_adjusted"

export interface Indicator {
  id: string
  name: string
  unit: string
  direction: "higher_is_worse" | "higher_is_better"
  defaultNormalization: NormalizationType
}

export interface ProvinceData {
  provinceId: string
  provinceName: string
  year: number
  metrics: Record<string, number> // indicatorId -> value
  population: number
  area: number // km2
}

export interface WeightPreset {
  id: string
  name: string
  weights: Record<string, number> // indicatorId -> percentage (0-100)
}

export interface AppState {
  selectedYear: number
  selectedProvinceId: string | null
  activePresetId: string
  customWeights: Record<string, number> | null
  normalizationOverrides: Record<string, NormalizationType>
  mapState: {
    center: [number, number]
    zoom: number
    transitioning: boolean
  }
  mapZoom: number
  mapCenter: [number, number]
  isTransitioning: boolean
}
