import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, Database, FileText } from "lucide-react"
import Link from "next/link"

export function DataNotes() {
  return (
    <Card className="h-full border-none bg-white shadow-[0_4px_20px_rgba(0,0,0,0.03)] rounded-2xl p-6">
      <CardHeader className="p-0 mb-4">
        <CardTitle className="text-sm font-black text-foreground uppercase tracking-tight">Data Governance</CardTitle>
      </CardHeader>
      <CardContent className="p-0 space-y-4">
        <div className="flex items-start gap-3 p-3 rounded-xl bg-muted/30">
          <Database className="h-4 w-4 mt-0.5 text-primary" />
          <div className="space-y-1">
            <p className="text-[10px] font-bold uppercase tracking-wider">Source Status</p>
            <p className="text-[11px] text-muted-foreground leading-relaxed">
              Data derived from BPS Open Data Registry. Latest verification: Jan 2026.
            </p>
          </div>
        </div>

        <div className="flex items-start gap-3 p-3 rounded-xl bg-muted/30">
          <AlertCircle className="h-4 w-4 mt-0.5 text-orange-500" />
          <div className="space-y-1">
            <p className="text-[10px] font-bold uppercase tracking-wider">Scaling Logic</p>
            <p className="text-[11px] text-muted-foreground leading-relaxed">
              Min-Max normalization active. Directionality adjusted for inverse indicators.
            </p>
          </div>
        </div>

        <Link
          href="/methodology"
          className="flex items-center justify-center gap-2 w-full py-3 rounded-xl border border-input bg-background hover:bg-accent hover:text-accent-foreground transition-colors text-xs font-bold"
        >
          <FileText className="h-3.5 w-3.5" />
          Full Methodology
        </Link>
      </CardContent>
    </Card>
  )
}
