"use client"

import { useMemo } from "react"
import { useAppStore } from "@/lib/store"
import { generateMockData, calculateCompositeScore } from "@/lib/scoring-engine"
import { PRESETS } from "@/lib/constants"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

export function TrendComparison({ id }: { id: string }) {
  const { activePresetId, normalizationOverrides } = useAppStore()

  const chartData = useMemo(() => {
    const allData = generateMockData()
    const activePreset = PRESETS.find((p) => p.id === activePresetId) || PRESETS[0]
    const years = [2019, 2020, 2021, 2022, 2023, 2024]

    return years.map((year) => {
      const yearData = allData.filter((d) => d.year === year)
      const provinceData = yearData.find((d) => d.provinceId === id)

      // Calculate province score
      const provinceScore = provinceData
        ? calculateCompositeScore(provinceData, activePreset.weights, normalizationOverrides, yearData)
        : 0

      // Calculate national average
      const nationalAvg =
        yearData.reduce(
          (acc, d) => acc + calculateCompositeScore(d, activePreset.weights, normalizationOverrides, yearData),
          0,
        ) / yearData.length

      return {
        year,
        province: Number(provinceScore.toFixed(1)),
        national: Number(nationalAvg.toFixed(1)),
      }
    })
  }, [id, activePresetId, normalizationOverrides])

  return (
    <Card className="border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden p-6">
      <CardHeader className="p-0 mb-6">
        <CardTitle className="text-sm font-black text-foreground uppercase tracking-tight">
          Trend Comparison (2019-2024)
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[300px] p-0">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
            <XAxis dataKey="year" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 600 }} dy={10} />
            <YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 600 }} />
            <Tooltip
              contentStyle={{ borderRadius: "12px", border: "none", boxShadow: "0 10px 30px rgba(0,0,0,0.1)" }}
              itemStyle={{ fontWeight: 700, fontSize: "12px" }}
            />
            <Legend verticalAlign="top" align="right" iconType="circle" />
            <Line
              type="monotone"
              dataKey="province"
              name="Province Score"
              stroke="#1A1A1A"
              strokeWidth={4}
              dot={{ r: 4, fill: "#1A1A1A", strokeWidth: 2, stroke: "#fff" }}
              activeDot={{ r: 6 }}
            />
            <Line
              type="monotone"
              dataKey="national"
              name="National Avg"
              stroke="#3b82f6"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
