"use client"

import { useMemo } from "react"
import { useAppStore } from "@/lib/store"
import { INDICATORS } from "@/lib/constants"
import { generateMockData, normalizeValue } from "@/lib/scoring-engine"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { LineChart, Line, ResponsiveContainer } from "recharts"

export function IndicatorGrid({ id }: { id: string }) {
  const { selectedYear, normalizationOverrides } = useAppStore()
  const allData = useMemo(() => generateMockData(), [])
  const provinceHistory = useMemo(() => allData.filter((d) => d.provinceId === id), [allData, id])
  const currentData = provinceHistory.find((d) => d.year === selectedYear)

  if (!currentData) return null

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {INDICATORS.map((ind) => {
        const normType = normalizationOverrides[ind.id] || ind.defaultNormalization
        const val = normalizeValue(currentData.metrics[ind.id], normType, currentData.population, currentData.area)

        const sparklineData = provinceHistory.map((d) => ({
          value: normalizeValue(d.metrics[ind.id], normType, d.population, d.area),
        }))

        return (
          <Card
            key={ind.id}
            className="border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden group hover:shadow-[0_8px_30px_rgba(0,0,0,0.06)] transition-all duration-300"
          >
            <CardHeader className="p-6 pb-2">
              <CardTitle className="text-[10px] font-black text-muted-foreground uppercase tracking-[0.15em]">
                {ind.name}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6 pt-0">
              <div className="flex items-center justify-between gap-4">
                <div className="flex flex-col gap-1">
                  <span className="text-3xl font-black tracking-tighter text-foreground">
                    {val > 1000 ? val.toLocaleString(undefined, { maximumFractionDigits: 0 }) : val.toFixed(2)}
                  </span>
                  <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
                    {ind.unit}
                  </span>
                </div>
                <div className="h-12 w-24">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={sparklineData}>
                      <Line
                        type="monotone"
                        dataKey="value"
                        stroke="#000"
                        strokeWidth={2.5}
                        dot={false}
                        className="transition-all duration-300 group-hover:stroke-primary"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
