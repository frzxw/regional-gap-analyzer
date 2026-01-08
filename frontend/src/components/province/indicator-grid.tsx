"use client"

import { useEffect, useState } from "react"
import { useAppStore } from "@/lib/store"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { provinceApi, type ScoreBreakdown } from "@/utils/provinceApi"

export function IndicatorGrid({ id }: { id: string }) {
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
        console.error("Failed to fetch indicator data:", err)
        setError(err instanceof Error ? err.message : "Failed to load data")
        setData(null)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [id, selectedYear])

  if (loading) {
    return (
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {[...Array(6)].map((_, i) => (
          <Card key={i} className="border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden">
            <CardHeader className="p-6 pb-2">
              <div className="animate-pulse h-3 w-24 bg-gray-200 rounded"></div>
            </CardHeader>
            <CardContent className="p-6 pt-0">
              <div className="animate-pulse h-10 w-20 bg-gray-200 rounded"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="flex items-center justify-center p-8 text-sm text-muted-foreground">
        Failed to load indicator data
      </div>
    )
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {data.collections.map((collection) => {
        const val = collection.raw_value
        const formattedValue = val > 1000
          ? val.toLocaleString(undefined, { maximumFractionDigits: 0 })
          : val.toFixed(2)

        return (
          <Card
            key={collection.collection}
            className="border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden group hover:shadow-[0_8px_30px_rgba(0,0,0,0.06)] transition-all duration-300"
          >
            <CardHeader className="p-6 pb-2">
              <CardTitle className="text-[10px] font-black text-muted-foreground uppercase tracking-[0.15em]">
                {collection.display_name}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6 pt-0">
              <div className="flex items-center justify-between gap-4">
                <div className="flex flex-col gap-1">
                  <span className="text-3xl font-black tracking-tighter text-foreground">
                    {formattedValue}
                  </span>
                  <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
                    Score: {collection.score.toFixed(1)}
                  </span>
                </div>
                <div className="flex flex-col gap-1 text-right">
                  <span className="text-[9px] font-bold text-muted-foreground uppercase">
                    {collection.lower_is_better ? "Lower Better" : "Higher Better"}
                  </span>
                  <span className="text-[9px] text-muted-foreground">
                    Range: {collection.min_value.toFixed(1)} - {collection.max_value.toFixed(1)}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}

