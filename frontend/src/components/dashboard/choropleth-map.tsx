"use client"

import { useMemo, useState, useEffect } from "react"
import { ComposableMap, Geographies, Geography, ZoomableGroup } from "react-simple-maps"
import { scaleThreshold } from "d3-scale"
import { useAppStore } from "@/lib/store"
import { PROVINCES } from "@/lib/constants"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import { yearScoringApi, type ProvinceScoreDetailed } from "@/utils/yearScoringApi"

// Fallback simple map URL
const GEO_URL = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province.json"

export function ChoroplethMap() {
  const router = useRouter()
  const { selectedYear, setMapCenter, setIsTransitioning, selectedProvinceId } = useAppStore()
  const [position, setPosition] = useState<{ coordinates: [number, number]; zoom: number }>({
    coordinates: [118, -2],
    zoom: 1,
  })
  const [scores, setScores] = useState<ProvinceScoreDetailed[]>([])
  const [loading, setLoading] = useState(true)

  // Fetch year-based scores and aggregate Papua provinces
  useEffect(() => {
    const fetchScores = async () => {
      setLoading(true)
      try {
        const data = await yearScoringApi.getScoresForYear(selectedYear)
        console.log("Raw data from API:", data)
        console.log("Sample province_id:", data[0]?.province_id, "Type:", typeof data[0]?.province_id)

        // Aggregate Papua provinces for old GeoJSON compatibility
        // Old GeoJSON only has: Papua Barat (91) and Papua (94)
        // New data has 6 provinces: 91, 92, 94, 95, 96, 97
        const aggregatedScores = [...data]

        // Find Papua Barat group (91, 92)
        const papuaBaratGroup = data.filter(s => ["91", "92"].includes(s.province_id))
        if (papuaBaratGroup.length > 0) {
          const avgScore = papuaBaratGroup.reduce((sum, s) => sum + s.composite_score, 0) / papuaBaratGroup.length
          const papuaBaratIndex = aggregatedScores.findIndex(s => s.province_id === "91")
          if (papuaBaratIndex >= 0) {
            aggregatedScores[papuaBaratIndex] = {
              ...aggregatedScores[papuaBaratIndex],
              composite_score: avgScore,
              province_name: "Papua Barat"
            }
          }
        }

        // Find Papua group (94, 95, 96, 97)
        const papuaGroup = data.filter(s => ["94", "95", "96", "97"].includes(s.province_id))
        if (papuaGroup.length > 0) {
          const avgScore = papuaGroup.reduce((sum, s) => sum + s.composite_score, 0) / papuaGroup.length
          const papuaIndex = aggregatedScores.findIndex(s => s.province_id === "94")
          if (papuaIndex >= 0) {
            aggregatedScores[papuaIndex] = {
              ...aggregatedScores[papuaIndex],
              composite_score: avgScore,
              province_name: "Papua"
            }
          }
        }

        setScores(aggregatedScores)
      } catch (error) {
        console.error("Failed to fetch scores:", error)
        setScores([])
      } finally {
        setLoading(false)
      }
    }
    fetchScores()
  }, [selectedYear])

  const colorScale = scaleThreshold<number, string>()
    .domain([20, 40, 60, 80])
    .range(["#1e293b", "#475569", "#94a3b8", "#cbd5e1", "#f1f5f9"])  // Reversed: dark to light

  // Mapping from GeoJSON province names (case-insensitive) to province IDs
  // Note: Old GeoJSON only has 2 Papua regions, but we have 6 new provinces
  // We map multiple new provinces to the same old GeoJSON geometry
  const getProvinceId = (geoName: string): string | undefined => {
    const nameMap: Record<string, string> = {
      // Aceh variants
      "aceh": "11",
      "di.aceh": "11",
      "d.i. aceh": "11",
      "di. aceh": "11",
      "d.i.aceh": "11",
      // Sumatera Utara
      "sumatera utara": "12",
      "sumatra utara": "12",
      // Sumatera Barat
      "sumatera barat": "13",
      "sumatra barat": "13",
      // Riau
      "riau": "14",
      // Jambi
      "jambi": "15",
      // Sumatera Selatan
      "sumatera selatan": "16",
      "sumatra selatan": "16",
      // Bengkulu
      "bengkulu": "17",
      // Lampung
      "lampung": "18",
      // Bangka Belitung
      "kepulauan bangka belitung": "19",
      "bangka belitung": "19",
      // Kepulauan Riau
      "kepulauan riau": "21",
      // DKI Jakarta
      "dki jakarta": "31",
      "jakarta raya": "31",
      // Jawa Barat
      "jawa barat": "32",
      // Jawa Tengah
      "jawa tengah": "33",
      // DI Yogyakarta variants
      "di yogyakarta": "34",
      "daerah istimewa yogyakarta": "34",
      "d.i. yogyakarta": "34",
      "di. yogyakarta": "34",
      "d.i.yogyakarta": "34",
      "yogyakarta": "34",
      // Jawa Timur
      "jawa timur": "35",
      // Banten variants
      "banten": "36",
      "probanten": "36",
      "prop. banten": "36",
      // Bali
      "bali": "51",
      // Nusa Tenggara Barat variants
      "nusa tenggara barat": "52",
      "nusatenggara barat": "52",
      "ntb": "52",
      // Nusa Tenggara Timur
      "nusa tenggara timur": "53",
      "nusatenggara timur": "53",
      "ntt": "53",
      // Kalimantan Barat
      "kalimantan barat": "61",
      // Kalimantan Tengah
      "kalimantan tengah": "62",
      // Kalimantan Selatan
      "kalimantan selatan": "63",
      // Kalimantan Timur
      "kalimantan timur": "64",
      // Kalimantan Utara
      "kalimantan utara": "65",
      // Sulawesi Utara
      "sulawesi utara": "71",
      // Sulawesi Tengah
      "sulawesi tengah": "72",
      // Sulawesi Selatan
      "sulawesi selatan": "73",
      // Sulawesi Tenggara
      "sulawesi tenggara": "74",
      // Gorontalo
      "gorontalo": "75",
      // Sulawesi Barat
      "sulawesi barat": "76",
      // Maluku
      "maluku": "81",
      // Maluku Utara
      "maluku utara": "82",
      // Papua Barat variants (91) - Also represents Papua Barat Daya (92) in old GeoJSON
      "papua barat": "91",
      "irian jaya barat": "91",
      "irjabar": "91",
      // Papua variants (94) - Also represents Papua Selatan (95), Tengah (96), Pegunungan (97)
      "papua": "94",
      "irian jaya timur": "94",
      "irian jaya tengah": "94",  // Papua Tengah maps to Papua
      "irjatim": "94",
    }
    return nameMap[geoName.toLowerCase()]
  }

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
                  // Get province_id from GeoJSON name using case-insensitive mapping
                  const geoName = geo.properties.Propinsi
                  const provinceId = getProvinceId(geoName)
                  const province = PROVINCES.find((p) => p.id === provinceId)
                  const provinceScore = scores.find((s) => s.province_id === provinceId)
                  const isSelected = selectedProvinceId === provinceId

                  // Debug: Log unmapped provinces
                  if (!provinceId) {
                    console.log("Unmapped province:", geoName)
                  }
                  if (provinceId && !provinceScore) {
                    console.log("No score for province:", geoName, "ID:", provinceId)
                  }

                  return (
                    <Tooltip key={geo.rsmKey}>
                      <TooltipTrigger asChild>
                        <Geography
                          geography={geo}
                          onClick={() => handleProvinceClick(geo, province)}
                          style={{
                            default: {
                              fill: provinceScore ? colorScale(provinceScore.composite_score) : "hsl(var(--muted))",
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
                          <span className="font-bold">{provinceScore?.province_name || province?.name || geo.properties.Propinsi}</span>
                          <span className="text-xs">Score: {provinceScore?.composite_score.toFixed(1) || "N/A"}</span>
                          {provinceScore && (
                            <span className="text-xs text-muted-foreground">Rank: #{provinceScore.rank}</span>
                          )}
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
            Composite Score
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
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-background/50 backdrop-blur-sm">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      )}
    </motion.div>
  )
}
