"use client"

import { useEffect, useState } from "react"
import { useAppStore } from "@/lib/store"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts"
import { provinceApi, type ScoreBreakdown } from "@/utils/provinceApi"

export function ScoreBreakdown({ id }: { id: string }) {
  const { selectedYear } = useAppStore()
  const [data, setData] = useState<ScoreBreakdown | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError(null)
      try {
        const result = await provinceApi.getScoreBreakdown(id, selectedYear)
        setData(result)
      } catch (err) {
        console.error("Failed to fetch score breakdown:", err)
        setError(err instanceof Error ? err.message : "Failed to load data")
        setData(null)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [id, selectedYear])

  const chartData = data?.collections
    .map((col) => ({
      name: col.display_name,
      contribution: Number(col.score.toFixed(1)),
    }))
    .filter((d) => d.contribution > 0)
    .sort((a, b) => b.contribution - a.contribution) || []

  return (
    <Card className="border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden p-6">
      <CardHeader className="p-0 mb-6">
        <CardTitle className="text-sm font-black text-foreground uppercase tracking-tight">
          Contribution to Score
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[350px] p-0">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : error ? (
          <div className="flex items-center justify-center h-full text-sm text-muted-foreground">
            Failed to load data
          </div>
        ) : chartData.length === 0 ? (
          <div className="flex items-center justify-center h-full text-sm text-muted-foreground">
            No data available
          </div>
        ) : (
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
        )}
      </CardContent>
    </Card>
  )
}

