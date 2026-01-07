import { DashboardHeader } from "@/components/dashboard/dashboard-header"
import { ProvinceMap } from "@/components/province/province-map"
import { ProvinceHeader } from "@/components/province/province-header"
import { IndicatorGrid } from "@/components/province/indicator-grid"
import { ScoreBreakdown } from "@/components/province/score-breakdown"
import { NationalComparison } from "@/components/province/national-comparison"
import { TrendComparison } from "@/components/province/trend-comparison"
import { DataNotes } from "@/components/province/data-notes"

export default async function ProvincePage(props: { params: Promise<{ id: string }> }) {
  const params = await props.params
  return (
    <div className="flex min-h-screen flex-col bg-[#F8F9FA]">
      <DashboardHeader />
      <main className="flex-1 overflow-x-hidden overflow-y-auto">
        <div className="min-h-[calc(100vh-4rem)] p-6">
          <div className="mx-auto max-w-[1800px] space-y-6">
            {/* Province Header */}
            <ProvinceHeader id={params.id} />

            <div className="grid gap-6 lg:grid-cols-12">
              {/* HERO MAP CARD - Focus of the Bento */}
              <div className="lg:col-span-8 lg:h-[600px] rounded-2xl overflow-hidden border bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)]">
                <ProvinceMap id={params.id} />
              </div>

              {/* Right Sidebar Analytics */}
              <div className="lg:col-span-4 flex flex-col gap-6">
                <ScoreBreakdown id={params.id} />
                <NationalComparison id={params.id} />
              </div>

              {/* Bottom Bento Row */}
              <div className="lg:col-span-8">
                <TrendComparison id={params.id} />
              </div>
              <div className="lg:col-span-4">
                <DataNotes />
              </div>
            </div>

            {/* Indicator Grid */}
            <div className="pt-6 border-t">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-xl font-bold tracking-tight text-foreground">Core Indicators</h3>
                <span className="text-[10px] text-muted-foreground uppercase tracking-[0.2em] font-bold">
                  Live Data - 2026
                </span>
              </div>
              <IndicatorGrid id={params.id} />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
