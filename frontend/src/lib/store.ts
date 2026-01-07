import { create } from "zustand"
import type { AppState, NormalizationType } from "./types"

interface StoreActions {
  setYear: (year: number) => void
  setProvince: (id: string | null) => void
  setPreset: (id: string) => void
  setNormalization: (indId: string, type: NormalizationType) => void
  setMapZoom: (zoom: number) => void
  setMapCenter: (center: [number, number]) => void
  setIsTransitioning: (transitioning: boolean) => void
}

export const useAppStore = create<AppState & StoreActions>((set) => ({
  selectedYear: 2024,
  selectedProvinceId: null,
  activePresetId: "balanced",
  customWeights: null,
  normalizationOverrides: {},
  mapZoom: 1,
  mapCenter: [118, -2],
  isTransitioning: false,
  mapState: {
    center: [118, -2],
    zoom: 1,
    transitioning: false,
  },

  setYear: (year) => set({ selectedYear: year }),
  setProvince: (id) => set({ selectedProvinceId: id }),
  setPreset: (id) => set({ activePresetId: id }),
  setNormalization: (indId, type) =>
    set((state) => ({
      normalizationOverrides: { ...state.normalizationOverrides, [indId]: type },
    })),
  setMapZoom: (zoom) => set({ mapZoom: zoom }),
  setMapCenter: (center) => set({ mapCenter: center }),
  setIsTransitioning: (transitioning) => set({ isTransitioning: transitioning }),
}))
