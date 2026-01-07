"use client"

import { useMemo } from "react"
import { useAppStore } from "@/lib/store"
import { PRESETS } from "@/lib/constants"
import { calculateCompositeScore, generateMockData } from "@/lib/scoring-engine"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown, AlertCircle, CheckCircle2 } from "lucide-react"

export function NationalKPIs() {
  const { selectedYear, activePresetId, normalizationOverrides } = useAppStore()

  const allData = useMemo(() => generateMockData(), [])
  const yearData = useMemo(() => allData.filter((d) => d.year === selectedYear), [selectedYear, allData])
  const activePreset = useMemo(() => PRESETS.find((p) => p.id === activePresetId) || PRESETS[0], [activePresetId])

  const scores = useMemo(() => {
    return yearData
      .map((d) => ({
        name: d.provinceName,
        score: calculateCompositeScore(d, activePreset.weights, normalizationOverrides, yearData),
      }))
      .sort((a, b) => a.score - b.score)
  }, [yearData, activePreset, normalizationOverrides])

  const medianScore = scores[Math.floor(scores.length / 2)]?.score || 0
  const bestProvince = scores[0]
  const worstProvince = scores[scores.length - 1]

  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4 lg:gap-4">
      <Card className="rounded-2xl border-none bg-primary p-3 text-primary-foreground shadow-xl md:p-4">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 p-0 pb-1">
          <CardTitle className="text-[10px] font-bold uppercase tracking-wider opacity-70 md:text-xs">Median</CardTitle>
          <TrendingUp className="h-3 w-3 opacity-70 md:h-4 md:w-4" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="text-xl font-black md:text-3xl">{medianScore.toFixed(1)}</div>
          <p className="mt-0.5 text-[10px] opacity-60">+2.1% YoY</p>
        </CardContent>
      </Card>

      <Card className="rounded-2xl border-none bg-background/80 p-3 shadow-xl backdrop-blur-md md:p-4">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 p-0 pb-1">
          <CardTitle className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground md:text-xs">
            Leader
          </CardTitle>
          <CheckCircle2 className="h-3 w-3 text-emerald-500 md:h-4 md:w-4" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="truncate text-lg font-bold md:text-xl">{bestProvince?.name || "N/A"}</div>
          <p className="text-[10px] text-muted-foreground">{bestProvince?.score.toFixed(1)} Pts</p>
        </CardContent>
      </Card>

      <Card className="rounded-2xl border-none bg-background/80 p-3 shadow-xl backdrop-blur-md md:p-4">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 p-0 pb-1">
          <CardTitle className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground md:text-xs">
            Critical
          </CardTitle>
          <AlertCircle className="h-3 w-3 text-destructive md:h-4 md:w-4" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="truncate text-lg font-bold md:text-xl">{worstProvince?.name || "N/A"}</div>
          <p className="text-[10px] text-muted-foreground">{worstProvince?.score.toFixed(1)} Pts</p>
        </CardContent>
      </Card>

      <Card className="rounded-2xl border-none bg-background/80 p-3 shadow-xl backdrop-blur-md md:p-4">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 p-0 pb-1">
          <CardTitle className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground md:text-xs">
            Pop. Coverage
          </CardTitle>
          <TrendingDown className="h-3 w-3 text-muted-foreground md:h-4 md:w-4" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="text-xl font-bold md:text-2xl">278.8M</div>
          <p className="text-[10px] text-muted-foreground">Est. 2024</p>
        </CardContent>
      </Card>
    </div>
  )
}
