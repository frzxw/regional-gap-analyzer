"use client"

import { useEffect, useState } from "react"
import { useAppStore } from "@/lib/store"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from "recharts"
import { provinceApi, type ScoreBreakdown, type ProvinceScoreDetailed } from "@/utils/provinceApi"

export function NationalComparison({ id }: { id: string }) {
  const { selectedYear } = useAppStore()
  const [provinceData, setProvinceData] = useState<ScoreBreakdown | null>(null)
  const [allProvinces, setAllProvinces] = useState<ProvinceScoreDetailed[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError(null)
      try {
        const [breakdown, allScores] = await Promise.all([
          provinceApi.getScoreBreakdown(id, selectedYear),
          provinceApi.getScoresForYear(selectedYear)
        ])
        setProvinceData(breakdown)
        setAllProvinces(allScores)
      } catch (err) {
        console.error("Failed to fetch comparison data:", err)
        setError(err instanceof Error ? err.message : "Failed to load data")
        setProvinceData(null)
        setAllProvinces([])
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [id, selectedYear])

  const chartData = provinceData?.collections
    .slice(0, 6) // Take top 6 for radar clarity
    .map((collection) => {
      // Calculate national average for this collection
      const allScores = allProvinces
        .map(p => p.collection_scores[collection.collection]?.score || 0)
        .filter(s => s > 0)

      const nationalAvg = allScores.length > 0
        ? allScores.reduce((a, b) => a + b, 0) / allScores.length
        : 0

      return {
        subject: collection.display_name,
        province: collection.score,
        national: nationalAvg,
      }
    }) || []

  return (
    <Card className="border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden p-6">
      <CardHeader className="p-0 mb-6">
        <CardTitle className="text-sm font-black text-foreground uppercase tracking-tight">
          National Benchmark
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[300px] p-0">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : error || chartData.length === 0 ? (
          <div className="flex items-center justify-center h-full text-sm text-muted-foreground">
            {error ? "Failed to load data" : "No data available"}
          </div>
        ) : (
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
        )}
      </CardContent>
    </Card>
  )
}

