"use client"

import { useMemo } from "react"
import { useAppStore } from "@/lib/store"
import { PRESETS } from "@/lib/constants"
import { calculateCompositeScore, generateMockData } from "@/lib/scoring-engine"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import Link from "next/link"

export function RankingCard() {
  const { selectedYear, activePresetId, normalizationOverrides } = useAppStore()

  const allData = useMemo(() => generateMockData(), [])
  const yearData = useMemo(() => allData.filter((d) => d.year === selectedYear), [selectedYear, allData])
  const activePreset = useMemo(() => PRESETS.find((p) => p.id === activePresetId) || PRESETS[0], [activePresetId])

  const sortedProvinces = useMemo(() => {
    return yearData
      .map((d) => ({
        id: d.provinceId,
        name: d.provinceName,
        score: calculateCompositeScore(d, activePreset.weights, normalizationOverrides, yearData),
      }))
      .sort((a, b) => a.score - b.score)
  }, [yearData, activePreset, normalizationOverrides])

  return (
    <Card className="h-full border-none shadow-md">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold">Province Ranking</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[250px] px-4">
          <div className="space-y-2 pb-4">
            {sortedProvinces.map((prov, i) => (
              <Link
                key={prov.id}
                href={`/province/${prov.id}`}
                className="flex items-center justify-between rounded-lg p-2 text-xs transition-colors hover:bg-muted"
              >
                <div className="flex items-center gap-3">
                  <span className="w-4 font-mono text-muted-foreground">{i + 1}</span>
                  <span className="font-medium">{prov.name}</span>
                </div>
                <span className="font-mono font-bold">{prov.score.toFixed(1)}</span>
              </Link>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
