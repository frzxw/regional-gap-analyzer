"use client"

import { useMemo } from "react"
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Cell, Tooltip as RechartsTooltip } from "recharts"
import { useAppStore } from "@/lib/store"
import { PRESETS } from "@/lib/constants"
import { calculateCompositeScore, generateMockData } from "@/lib/scoring-engine"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function DistributionCard() {
  const { selectedYear, activePresetId, normalizationOverrides } = useAppStore()

  const allData = useMemo(() => generateMockData(), [])
  const yearData = useMemo(() => allData.filter((d) => d.year === selectedYear), [selectedYear, allData])
  const activePreset = useMemo(() => PRESETS.find((p) => p.id === activePresetId) || PRESETS[0], [activePresetId])

  const chartData = useMemo(() => {
    const scores = yearData.map((d) =>
      calculateCompositeScore(d, activePreset.weights, normalizationOverrides, yearData),
    )

    // Create buckets of 10
    const buckets = Array(10).fill(0)
    scores.forEach((s) => {
      const idx = Math.min(Math.floor(s / 10), 9)
      buckets[idx]++
    })

    return buckets.map((count, i) => ({
      range: `${i * 10}-${(i + 1) * 10}`,
      count,
    }))
  }, [yearData, activePreset, normalizationOverrides])

  return (
    <Card className="border-none shadow-md">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold">Score Distribution</CardTitle>
      </CardHeader>
      <CardContent className="h-[120px] p-0 pb-2 pr-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <Bar dataKey="count" fill="currentColor" radius={[2, 2, 0, 0]} className="fill-primary/60">
              {chartData.map((_, index) => (
                <Cell key={`cell-${index}`} className="hover:fill-primary transition-colors" />
              ))}
            </Bar>
            <XAxis dataKey="range" hide />
            <YAxis hide />
            <RechartsTooltip
              cursor={{ fill: "transparent" }}
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="rounded-lg border bg-background p-2 text-[10px] shadow-sm">
                      <p className="font-bold">Range: {payload[0].payload.range}</p>
                      <p>Count: {payload[0].value}</p>
                    </div>
                  )
                }
                return null
              }}
            />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
