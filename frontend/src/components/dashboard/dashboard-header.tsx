"use client"

import { Search, FileDown, Settings2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { useAppStore } from "@/lib/store"
import { YEARS, PRESETS } from "@/lib/constants"
import { Badge } from "@/components/ui/badge"

export function DashboardHeader() {
  const { selectedYear, setYear, activePresetId, setPreset } = useAppStore()

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/60 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between gap-4 px-4 md:px-6">
        <div className="flex items-center gap-4">
          <div className="flex flex-col">
            <h1 className="text-lg font-bold tracking-tight">Indonesia Inequality</h1>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="h-5 px-1.5 text-[10px] font-medium text-muted-foreground">
                LIVE DATA
              </Badge>
              <span className="text-[10px] text-muted-foreground">Last updated: Jan 2026</span>
            </div>
          </div>
        </div>

        <div className="hidden flex-1 items-center justify-center px-4 md:flex">
          <div className="relative w-full max-w-sm">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input type="search" placeholder="Search province..." className="w-full bg-muted/50 pl-8 md:w-[300px]" />
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Select value={selectedYear.toString()} onValueChange={(v) => setYear(Number.parseInt(v))}>
            <SelectTrigger className="h-9 w-[80px]">
              <SelectValue placeholder="Year" />
            </SelectTrigger>
            <SelectContent>
              {YEARS.map((y) => (
                <SelectItem key={y} value={y.toString()}>
                  {y}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Select value={activePresetId} onValueChange={setPreset}>
            <SelectTrigger className="h-9 w-[140px] hidden sm:flex">
              <SelectValue placeholder="Preset" />
            </SelectTrigger>
            <SelectContent>
              {PRESETS.map((p) => (
                <SelectItem key={p.id} value={p.id}>
                  {p.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Button variant="outline" size="icon" className="h-9 w-9 bg-transparent">
            <FileDown className="h-4 w-4" />
          </Button>

          <Button variant="outline" size="icon" className="h-9 w-9 md:hidden bg-transparent">
            <Settings2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </header>
  )
}
