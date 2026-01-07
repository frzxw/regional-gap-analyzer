"use client"

import { useMemo, useState } from "react"
import { ComposableMap, Geographies, Geography, ZoomableGroup } from "react-simple-maps"
import { scaleThreshold } from "d3-scale"
import { useAppStore } from "@/lib/store"
import { PROVINCES, PRESETS } from "@/lib/constants"
import { calculateCompositeScore, generateMockData } from "@/lib/scoring-engine"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"

// Fallback simple map URL
const GEO_URL = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province.json"

export function ChoroplethMap() {
  const router = useRouter()
  const { selectedYear, activePresetId, normalizationOverrides, setMapCenter, setIsTransitioning, selectedProvinceId } =
    useAppStore()
  const [position, setPosition] = useState<{ coordinates: [number, number]; zoom: number }>({
    coordinates: [118, -2],
    zoom: 1,
  })

  const allData = useMemo(() => generateMockData(), [])
  const yearData = useMemo(() => allData.filter((d) => d.year === selectedYear), [selectedYear, allData])
  const activePreset = useMemo(() => PRESETS.find((p) => p.id === activePresetId) || PRESETS[0], [activePresetId])

  const scores = useMemo(() => {
    return yearData.map((d) => ({
      id: d.provinceId,
      score: calculateCompositeScore(d, activePreset.weights, normalizationOverrides, yearData),
    }))
  }, [yearData, activePreset, normalizationOverrides])

  const colorScale = scaleThreshold<number, string>()
    .domain([20, 40, 60, 80])
    .range(["#f1f5f9", "#cbd5e1", "#94a3b8", "#475569", "#1e293b"])

  const handleProvinceClick = (geo: any, province: any) => {
    if (!province) return

    setIsTransitioning(true)

    // Calculate centroid from geometry
    const bounds = geo.geometry.coordinates[0][0] || geo.geometry.coordinates[0]
    let sumLng = 0
    let sumLat = 0
    let count = 0

    bounds.forEach((coord: [number, number]) => {
      sumLng += coord[0]
      sumLat += coord[1]
      count++
    })

    const centroid: [number, number] = [sumLng / count, sumLat / count]
    setMapCenter(centroid)

    // Animate zoom to province
    setPosition({
      coordinates: centroid,
      zoom: 3,
    })

    // Navigate after animation
    setTimeout(() => {
      setIsTransitioning(false)
      router.push(`/province/${province.id}`)
    }, 600)
  }

  return (
    <motion.div
      className="h-full w-full bg-muted/20"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <TooltipProvider>
        <ComposableMap
          projection="geoMercator"
          projectionConfig={{
            scale: 1400,
            center: [118, -2],
          }}
          className="h-full w-full outline-none"
        >
          <ZoomableGroup
            maxZoom={5}
            minZoom={0.8}
            center={position.coordinates}
            zoom={position.zoom}
            onMoveEnd={setPosition}
          >
            <Geographies geography={GEO_URL}>
              {({ geographies }) =>
                geographies.map((geo) => {
                  // Match by name or ID (fallback logic for mock mapping)
                  const province = PROVINCES.find((p) => p.name.toLowerCase() === geo.properties.Propinsi.toLowerCase())
                  const provinceScore = scores.find((s) => s.id === province?.id)
                  const isSelected = selectedProvinceId === province?.id

                  return (
                    <Tooltip key={geo.rsmKey}>
                      <TooltipTrigger asChild>
                        <Geography
                          geography={geo}
                          onClick={() => handleProvinceClick(geo, province)}
                          style={{
                            default: {
                              fill: provinceScore ? colorScale(provinceScore.score) : "hsl(var(--muted))",
                              outline: "none",
                              stroke: "hsl(var(--background))",
                              strokeWidth: 0.5,
                              opacity: isSelected ? 1 : 0.85,
                            },
                            hover: {
                              fill: "hsl(var(--primary))",
                              fillOpacity: 0.8,
                              outline: "none",
                              cursor: "pointer",
                            },
                            pressed: {
                              fill: "hsl(var(--primary))",
                              outline: "none",
                            },
                          }}
                        />
                      </TooltipTrigger>
                      <TooltipContent side="top">
                        <div className="flex flex-col gap-1">
                          <span className="font-bold">{province?.name || geo.properties.Propinsi}</span>
                          <span className="text-xs">Score: {provinceScore?.score.toFixed(1) || "N/A"}</span>
                        </div>
                      </TooltipContent>
                    </Tooltip>
                  )
                })
              }
            </Geographies>
          </ZoomableGroup>
        </ComposableMap>
      </TooltipProvider>
      <div className="absolute bottom-6 right-6 z-20 rounded-lg border bg-background/80 p-3 backdrop-blur-md">
        <div className="flex flex-col gap-2">
          <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
            Inequality Score
          </span>
          <div className="flex items-center gap-1.5">
            {[20, 40, 60, 80].map((val, i) => (
              <div key={val} className="flex flex-col gap-1">
                <div className="h-2 w-8 rounded-sm" style={{ backgroundColor: colorScale(val) }} />
              </div>
            ))}
          </div>
          <div className="flex justify-between text-[10px] text-muted-foreground">
            <span>Low</span>
            <span>High</span>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
