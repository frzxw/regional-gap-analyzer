"use client"

import { useMemo } from "react"
import { useAppStore } from "@/lib/store"
import { INDICATORS } from "@/lib/constants"
import { generateMockData, normalizeValue } from "@/lib/scoring-engine"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from "recharts"

export function NationalComparison({ id }: { id: string }) {
  const { selectedYear, normalizationOverrides } = useAppStore()
  const allData = useMemo(() => generateMockData(), [])
  const yearData = allData.filter((d) => d.year === selectedYear)
  const currentData = yearData.find((d) => d.provinceId === id)

  const chartData = useMemo(() => {
    if (!currentData) return []

    // Take top 6 indicators for radar clarity
    const selectedInds = INDICATORS.slice(0, 6)

    return selectedInds.map((ind) => {
      const normType = normalizationOverrides[ind.id] || ind.defaultNormalization
      const val = normalizeValue(currentData.metrics[ind.id], normType, currentData.population, currentData.area)

      const values = yearData.map((d) => normalizeValue(d.metrics[ind.id], normType, d.population, d.area))
      const avg = values.reduce((a, b) => a + b, 0) / values.length

      // Normalize for radar (0-100 scale)
      const max = Math.max(...values)
      return {
        subject: ind.name,
        province: (val / max) * 100,
        national: (avg / max) * 100,
      }
    })
  }, [currentData, yearData, normalizationOverrides])

  return (
    <Card className="border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden p-6">
      <CardHeader className="p-0 mb-6">
        <CardTitle className="text-sm font-black text-foreground uppercase tracking-tight">
          National Benchmark
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[300px] p-0">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
            <PolarGrid stroke="#E5E7EB" />
            <PolarAngleAxis dataKey="subject" tick={{ fontSize: 8, fontWeight: 600, fill: "#666" }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} hide />
            <Radar
              name="Province"
              dataKey="province"
              stroke="#1A1A1A"
              fill="#1A1A1A"
              fillOpacity={0.15}
              strokeWidth={2}
            />
            <Radar
              name="National Average"
              dataKey="national"
              stroke="#3b82f6"
              fill="#3b82f6"
              fillOpacity={0.3}
              strokeWidth={2}
              strokeDasharray="4 4"
            />
          </RadarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
