"use client"

import { useEffect, useState } from "react"
import { ChevronLeft, Share2, Info } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { PROVINCES } from "@/lib/constants"
import { useAppStore } from "@/lib/store"
import { Badge } from "@/components/ui/badge"
import { provinceApi, type ProvinceScoreDetailed } from "@/utils/provinceApi"

export function ProvinceHeader({ id }: { id: string }) {
  const { selectedYear } = useAppStore()
  const province = PROVINCES.find((p) => p.id === id)
  const [data, setData] = useState<ProvinceScoreDetailed | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError(null)
      try {
        const result = await provinceApi.getProvinceScore(id, selectedYear)
        setData(result)
      } catch (err) {
        console.error("Failed to fetch province score:", err)
        setError(err instanceof Error ? err.message : "Failed to load data")
        setData(null)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [id, selectedYear])

  if (!province) return null

  return (
    <div className="relative overflow-hidden rounded-[2rem] bg-[#1A1A1A] p-8 text-white shadow-2xl md:p-12">
      <div className="relative z-10 flex flex-col gap-8 md:flex-row md:items-center md:justify-between">
        <div className="flex flex-col gap-6">
          <Link
            href="/"
            className="group flex w-fit items-center gap-2 text-[10px] font-bold uppercase tracking-[0.2em] text-white/50 transition-colors hover:text-white"
          >
            <ChevronLeft className="h-3 w-3 transition-transform group-hover:-translate-x-1" />
            Back to Overview
          </Link>
          <div className="space-y-4">
            <h2 className="text-5xl font-black tracking-tighter md:text-7xl">
              {data?.province_name || province.name}
            </h2>
            <div className="flex items-center gap-3">
              {loading ? (
                <div className="animate-pulse h-6 w-24 bg-white/20 rounded-full"></div>
              ) : error ? (
                <Badge
                  variant="secondary"
                  className="bg-red-500/20 text-xs text-white hover:bg-red-500/30 border-none px-3 py-1 font-bold rounded-full"
                >
                  ERROR
                </Badge>
              ) : data?.rank ? (
                <>
                  <Badge
                    variant="secondary"
                    className="bg-[#333] text-xs text-white hover:bg-[#444] border-none px-3 py-1 font-bold rounded-full"
                  >
                    RANK #{data.rank}
                  </Badge>
                  <span className="text-xs font-bold text-white/40 uppercase tracking-wider">
                    Nationwide Comparison
                  </span>
                </>
              ) : null}
            </div>
          </div>
        </div>

        <div className="flex flex-col items-end gap-2 text-right">
          <div className="flex items-center gap-4">
            <div className="flex flex-col items-end">
              <span className="text-[10px] font-black uppercase tracking-[0.2em] text-white/40">
                Inequality Score
              </span>
              {loading ? (
                <div className="animate-pulse h-20 w-32 bg-white/20 rounded"></div>
              ) : error ? (
                <div className="text-2xl font-bold text-red-400">N/A</div>
              ) : (
                <div className="flex items-baseline gap-1">
                  <span className="text-7xl font-black md:text-8xl">
                    {data?.composite_score.toFixed(1) || "0.0"}
                  </span>
                  <span className="text-2xl font-bold text-white/30">/100</span>
                </div>
              )}
            </div>
            <div className="flex flex-col gap-2 ml-4">
              <Button
                variant="outline"
                size="icon"
                className="h-10 w-10 rounded-full border-white/10 bg-white/5 hover:bg-white/10 text-white"
              >
                <Share2 className="h-4 w-4" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                className="h-10 w-10 rounded-full border-white/10 bg-white/5 hover:bg-white/10 text-white"
              >
                <Info className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

