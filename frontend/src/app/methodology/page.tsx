import { DashboardHeader } from "@/components/dashboard/dashboard-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { INDICATORS } from "@/lib/constants"
import { Badge } from "@/components/ui/badge"

export default function MethodologyPage() {
  return (
    <div className="flex min-h-screen flex-col bg-muted/30">
      <DashboardHeader />
      <main className="container flex-1 space-y-8 p-4 md:p-8">
        <div className="max-w-3xl space-y-4">
          <h2 className="text-3xl font-bold tracking-tight">Methodology</h2>
          <p className="text-muted-foreground">
            The Indonesia Inequality Score (IIS) is a composite index designed to measure socio-economic disparities
            across provinces. It combines labor market data, poverty metrics, and economic development indicators into a
            single, comparable metric.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Card className="border-none shadow-md">
            <CardHeader>
              <CardTitle>1. Data Normalization</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-sm leading-relaxed">
              <p>
                To ensure comparability between provinces of vastly different sizes (e.g., DKI Jakarta vs. Papua
                Pegunungan), raw count data is normalized using one of four methods:
              </p>
              <ul className="list-disc pl-5 space-y-2">
                <li>
                  <strong>Raw:</strong> Used for ratios and indexes (e.g., Gini Ratio, IPM).
                </li>
                <li>
                  <strong>Per 100k Population:</strong> Standardizes count data by the total provincial population.
                </li>
                <li>
                  <strong>Per km² (Area):</strong> Standardizes count data by geographical size.
                </li>
                <li>
                  <strong>Density Adjusted:</strong> Weighting metrics based on population density.
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card className="border-none shadow-md">
            <CardHeader>
              <CardTitle>2. Scoring & Scaling</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-sm leading-relaxed">
              <p>
                Indicators are scaled from 0 to 100 using <strong>Min-Max Normalization</strong> based on the values of
                all 38 provinces for that specific year.
              </p>
              <p>
                <strong>Directionality:</strong> We invert scores where "higher is better" (like IPM or PDRB) so that in
                the final index, <strong>0 always represents the best performance (lowest inequality)</strong> and{" "}
                <strong>100 represents the worst performance</strong>.
              </p>
            </CardContent>
          </Card>
        </div>

        <Card className="border-none shadow-md">
          <CardHeader>
            <CardTitle>Indicator Reference</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="relative overflow-x-auto rounded-lg border">
              <table className="w-full text-left text-sm">
                <thead className="bg-muted/50 text-xs uppercase text-muted-foreground">
                  <tr>
                    <th className="px-4 py-3">Indicator</th>
                    <th className="px-4 py-3">Unit</th>
                    <th className="px-4 py-3">Direction</th>
                    <th className="px-4 py-3">Default Normalization</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {INDICATORS.map((ind) => (
                    <tr key={ind.id}>
                      <td className="px-4 py-3 font-medium">{ind.name}</td>
                      <td className="px-4 py-3 text-muted-foreground">{ind.unit}</td>
                      <td className="px-4 py-3">
                        <Badge variant={ind.direction === "higher_is_worse" ? "destructive" : "secondary"}>
                          {ind.direction === "higher_is_worse" ? "H. is Worse" : "H. is Better"}
                        </Badge>
                      </td>
                      <td className="px-4 py-3 font-mono text-xs">{ind.defaultNormalization}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
