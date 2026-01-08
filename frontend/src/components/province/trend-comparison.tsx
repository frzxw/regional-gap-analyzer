"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"
import { provinceApi, type ProvinceScoreDetailed } from "@/utils/provinceApi"

export function TrendComparison({ id }: { id: string }) {
  const [chartData, setChartData] = useState<Array<{ year: number; province: number; national: number }>>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError(null)
      try {
        const years = [2019, 2020, 2021, 2022, 2023, 2024]

        // Fetch data for all years in parallel
        const yearDataPromises = years.map(async (year) => {
          try {
            const [provinceScore, allScores] = await Promise.all([
              provinceApi.getProvinceScore(id, year),
              provinceApi.getScoresForYear(year)
            ])

            // Calculate national average
            const nationalAvg = allScores.length > 0
              ? allScores.reduce((sum, p) => sum + p.composite_score, 0) / allScores.length
              : 0

            return {
              year,
              province: Number(provinceScore.composite_score.toFixed(1)),
              national: Number(nationalAvg.toFixed(1)),
            }
          } catch (err) {
            console.warn(`No data for year ${year}:`, err)
            return null
          }
        })

        const results = await Promise.all(yearDataPromises)
        const validData = results.filter((d): d is NonNullable<typeof d> => d !== null)

        setChartData(validData)
      } catch (err) {
        console.error("Failed to fetch trend data:", err)
        setError(err instanceof Error ? err.message : "Failed to load data")
        setChartData([])
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [id])

  return (
    <Card className="border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden p-6">
      <CardHeader className="p-0 mb-6">
        <CardTitle className="text-sm font-black text-foreground uppercase tracking-tight">
          Trend Comparison (2019-2024)
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[300px] p-0">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : error || chartData.length === 0 ? (
          <div className="flex items-center justify-center h-full text-sm text-muted-foreground">
            {error ? "Failed to load data" : "No historical data available"}
          </div>
        ) : (
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
        )}
      </CardContent>
    </Card>
  )
}

