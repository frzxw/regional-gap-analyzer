import { DashboardHeader } from "@/components/dashboard/dashboard-header"
import { ChoroplethMap } from "@/components/dashboard/choropleth-map"
import { NationalKPIs } from "@/components/dashboard/kpi-cards"
import { YearScoreDisplay } from "@/components/scoring/YearScoreDisplay"

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

          <div className="mt-auto flex justify-end">
            <div className="pointer-events-auto w-full max-w-md shrink-0">
              <div className="rounded-lg bg-white/95 backdrop-blur-sm shadow-lg p-4 max-h-[500px] overflow-y-auto">
                <h2 className="text-lg font-semibold mb-3">Provincial Scores</h2>
                <YearScoreDisplay showTopBottom={true} topBottomCount={10} />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
