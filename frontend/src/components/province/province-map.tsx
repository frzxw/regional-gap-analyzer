"use client"

import { useMemo, useEffect, useState } from "react"
import { ComposableMap, Geographies, Geography, ZoomableGroup } from "react-simple-maps"
import { scaleThreshold } from "d3-scale"
import { useAppStore } from "@/lib/store"
import { PROVINCES, PRESETS } from "@/lib/constants"
import { calculateCompositeScore, generateMockData } from "@/lib/scoring-engine"
import { Button } from "@/components/ui/button"
import { ZoomIn, ZoomOut, Home } from "lucide-react"
import { motion } from "framer-motion"

const GEO_URL = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province.json"

interface ProvinceMapProps {
  id: string
}

export function ProvinceMap({ id }: ProvinceMapProps) {
  const { selectedYear, activePresetId, normalizationOverrides, mapCenter, setProvince } = useAppStore()
  const [position, setPosition] = useState<{ coordinates: [number, number]; zoom: number }>({
    coordinates: mapCenter,
    zoom: 3,
  })
  const [geographies, setGeographies] = useState<any[]>([])

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

  // Set selected province in store
  useEffect(() => {
    setProvince(id)
    return () => setProvince(null)
  }, [id, setProvince])

  // Focus on selected province on mount
  useEffect(() => {
    if (geographies.length > 0) {
      const geo = geographies.find((g) => {
        const province = PROVINCES.find((p) => p.id === id)
        return province && g.properties.Propinsi.toLowerCase() === province.name.toLowerCase()
      })

      if (geo) {
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
        setPosition({ coordinates: centroid, zoom: 3 })
      }
    }
  }, [geographies, id])

  const handleZoomIn = () => {
    setPosition((prev) => ({ ...prev, zoom: Math.min(prev.zoom + 0.5, 8) }))
  }

  const handleZoomOut = () => {
    setPosition((prev) => ({ ...prev, zoom: Math.max(prev.zoom - 0.5, 0.8) }))
  }

  const handleReset = () => {
    setPosition({ coordinates: [118, -2], zoom: 1 })
  }

  const handleFitProvince = () => {
    const geo = geographies.find((g) => {
      const province = PROVINCES.find((p) => p.id === id)
      return province && g.properties.Propinsi.toLowerCase() === province.name.toLowerCase()
    })

    if (geo) {
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
      setPosition({ coordinates: centroid, zoom: 4 })
    }
  }

  return (
    <motion.div
      className="relative h-full w-full bg-muted/10"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <ComposableMap
        projection="geoMercator"
        projectionConfig={{
          scale: 1400,
          center: [118, -2],
        }}
        className="h-full w-full outline-none"
      >
        <ZoomableGroup
          maxZoom={8}
          minZoom={0.8}
          center={position.coordinates}
          zoom={position.zoom}
          onMoveEnd={setPosition}
        >
          <Geographies geography={GEO_URL}>
            {({ geographies: geos }) => {
              if (geographies.length === 0) setGeographies(geos)
              return geos.map((geo) => {
                const province = PROVINCES.find((p) => p.name.toLowerCase() === geo.properties.Propinsi.toLowerCase())
                const provinceScore = scores.find((s) => s.id === province?.id)
                const isSelected = province?.id === id

                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    style={{
                      default: {
                        fill: isSelected ? "#1A1A1A" : provinceScore ? colorScale(provinceScore.score) : "#E5E7EB",
                        outline: "none",
                        stroke: "#FFFFFF",
                        strokeWidth: isSelected ? 2 : 0.5,
                        opacity: isSelected ? 1 : 0.4,
                      },
                      hover: {
                        fill: isSelected ? "#1A1A1A" : provinceScore ? colorScale(provinceScore.score) : "#E5E7EB",
                        outline: "none",
                        opacity: 0.8,
                      },
                      pressed: {
                        fill: isSelected ? "#1A1A1A" : provinceScore ? colorScale(provinceScore.score) : "#E5E7EB",
                        outline: "none",
                      },
                    }}
                  />
                )
              })
            }}
          </Geographies>
        </ZoomableGroup>
      </ComposableMap>

      {/* Map Controls */}
      <div className="absolute top-4 right-4 z-10 flex flex-col gap-2">
        <Button size="icon" variant="secondary" onClick={handleZoomIn} className="h-9 w-9 shadow-lg">
          <ZoomIn className="h-4 w-4" />
        </Button>
        <Button size="icon" variant="secondary" onClick={handleZoomOut} className="h-9 w-9 shadow-lg">
          <ZoomOut className="h-4 w-4" />
        </Button>
        <Button size="icon" variant="secondary" onClick={handleReset} className="h-9 w-9 shadow-lg">
          <Home className="h-4 w-4" />
        </Button>
      </div>

      {/* Fit Province Button */}
      <div className="absolute bottom-4 left-4 z-10">
        <Button onClick={handleFitProvince} variant="default" className="shadow-lg">
          Fit Selected Province
        </Button>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 z-10 rounded-lg border bg-background/90 p-3 backdrop-blur-md shadow-lg">
        <div className="flex flex-col gap-2">
          <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
            Inequality Score
          </span>
          <div className="flex items-center gap-1.5">
            {[20, 40, 60, 80].map((val) => (
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
