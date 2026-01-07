"use client"

import { useMemo } from "react"
import { useAppStore } from "@/lib/store"
import { INDICATORS, PRESETS } from "@/lib/constants"
import { generateMockData, normalizeValue } from "@/lib/scoring-engine"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts"

export function ScoreBreakdown({ id }: { id: string }) {
  const { selectedYear, activePresetId, normalizationOverrides } = useAppStore()
  const allData = useMemo(() => generateMockData(), [])
  const yearData = allData.filter((d) => d.year === selectedYear)
  const currentData = yearData.find((d) => d.provinceId === id)
  const activePreset = PRESETS.find((p) => p.id === activePresetId) || PRESETS[0]

  const chartData = useMemo(() => {
    if (!currentData) return []

    return INDICATORS.map((ind) => {
      const normType = normalizationOverrides[ind.id] || ind.defaultNormalization
      const val = normalizeValue(currentData.metrics[ind.id], normType, currentData.population, currentData.area)

      // Get scaling
      const values = yearData.map((d) => normalizeValue(d.metrics[ind.id], normType, d.population, d.area))
      const min = Math.min(...values)
      const max = Math.max(...values)
      let scaled = (val - min) / (max - min || 1)
      if (ind.direction === "higher_is_better") scaled = 1 - scaled

      const weight = activePreset.weights[ind.id] || 0
      const contribution = scaled * weight

      return {
        name: ind.name,
        contribution: Number(contribution.toFixed(1)),
      }
    })
      .filter((d) => d.contribution > 0)
      .sort((a, b) => b.contribution - a.contribution)
  }, [currentData, activePreset, yearData, normalizationOverrides])

  return (
    <Card className="border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden p-6">
      <CardHeader className="p-0 mb-6">
        <CardTitle className="text-sm font-black text-foreground uppercase tracking-tight">
          Contribution to Score
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[350px] p-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} layout="vertical" margin={{ left: -20, right: 10 }}>
            <XAxis type="number" hide />
            <YAxis
              dataKey="name"
              type="category"
              width={140}
              tick={{ fontSize: 9, fontWeight: 600, fill: "#666" }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              cursor={{ fill: "transparent" }}
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="rounded-xl border-none bg-[#1A1A1A] text-white p-3 text-[10px] shadow-xl">
                      <p className="font-black uppercase tracking-widest mb-1">{payload[0].payload.name}</p>
                      <p className="font-bold opacity-60">Contribution: {payload[0].value}</p>
                    </div>
                  )
                }
                return null
              }}
            />
            <Bar dataKey="contribution" fill="#1A1A1A" radius={[0, 6, 6, 0]} barSize={20} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
