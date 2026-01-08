"use client"

import { useMemo, useState, useEffect } from "react"
import { useAppStore } from "@/lib/store"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, AlertCircle, CheckCircle2 } from "lucide-react"
import { yearScoringApi, type NationalStatistics } from "@/utils/yearScoringApi"

export function NationalKPIs() {
  const { selectedYear } = useAppStore()
  const [statistics, setStatistics] = useState<NationalStatistics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStatistics = async () => {
      setLoading(true)
      setError(null)
      try {
        const data = await yearScoringApi.getStatistics(selectedYear)
        setStatistics(data)
      } catch (err) {
        console.error("Failed to fetch statistics:", err)
        setError("Failed to load statistics")
        setStatistics(null)
      } finally {
        setLoading(false)
      }
    }
    fetchStatistics()
  }, [selectedYear])

  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-3 lg:gap-4">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="rounded-2xl border-none bg-background/80 p-3 shadow-xl backdrop-blur-md md:p-4">
            <div className="animate-pulse">
              <div className="h-4 bg-muted rounded w-16 mb-2"></div>
              <div className="h-8 bg-muted rounded w-20"></div>
            </div>
          </Card>
        ))}
      </div>
    )
  }

  if (error || !statistics) {
    return (
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-3 lg:gap-4">
        <Card className="col-span-1 lg:col-span-3 rounded-2xl border-none bg-destructive/10 p-4 text-destructive">
          <p className="text-sm">{error || "No data available"}</p>
        </Card>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-3 lg:grid-cols-3 lg:gap-4">
      <Card className="rounded-2xl border-none bg-primary p-3 text-primary-foreground shadow-xl md:p-4">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 p-0 pb-1">
          <CardTitle className="text-[10px] font-bold uppercase tracking-wider opacity-70 md:text-xs">Median</CardTitle>
          <TrendingUp className="h-3 w-3 opacity-70 md:h-4 md:w-4" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="text-xl font-black md:text-3xl">{statistics.median_score.toFixed(1)}</div>
          <p className="mt-0.5 text-[10px] opacity-60">Year {statistics.year}</p>
        </CardContent>
      </Card>

      <Card className="rounded-2xl border-none bg-background/80 p-3 shadow-xl backdrop-blur-md md:p-4">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 p-0 pb-1">
          <CardTitle className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground md:text-xs">
            Leader
          </CardTitle>
          <CheckCircle2 className="h-3 w-3 text-emerald-500 md:h-4 md:w-4" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="truncate text-lg font-bold md:text-xl">{statistics.leader?.province_name || "N/A"}</div>
          <p className="text-[10px] text-muted-foreground">{statistics.leader?.score.toFixed(1)} Pts</p>
        </CardContent>
      </Card>

      <Card className="rounded-2xl border-none bg-background/80 p-3 shadow-xl backdrop-blur-md md:p-4">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 p-0 pb-1">
          <CardTitle className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground md:text-xs">
            Critical
          </CardTitle>
          <AlertCircle className="h-3 w-3 text-destructive md:h-4 md:w-4" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="truncate text-lg font-bold md:text-xl">{statistics.critical?.province_name || "N/A"}</div>
          <p className="text-[10px] text-muted-foreground">{statistics.critical?.score.toFixed(1)} Pts</p>
        </CardContent>
      </Card>
    </div>
  )
}
