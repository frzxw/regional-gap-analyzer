import { DashboardHeader } from "@/components/dashboard/dashboard-header"
import { ChoroplethMap } from "@/components/dashboard/choropleth-map"
import { NationalKPIs } from "@/components/dashboard/kpi-cards"
import { RankingCard } from "@/components/dashboard/ranking-card"
import { DistributionCard } from "@/components/dashboard/distribution-card"

export default function Home() {
  return (
    <div className="flex h-screen flex-col overflow-hidden bg-background">
      <DashboardHeader />
      <main className="relative flex-1 overflow-hidden">
        <div className="absolute inset-0 z-0">
          <ChoroplethMap />
        </div>

        <div className="pointer-events-none relative z-10 flex h-full flex-col p-4 md:p-6 lg:p-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
            <div className="pointer-events-auto w-full md:max-w-xl lg:max-w-2xl">
              <NationalKPIs />
            </div>
          </div>

          <div className="mt-auto flex flex-col items-end gap-6 md:flex-row md:justify-between">
            <div className="pointer-events-auto w-full max-w-sm shrink-0">
              <RankingCard />
            </div>
            <div className="pointer-events-auto hidden w-full max-w-sm shrink-0 md:block">
              <DistributionCard />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
