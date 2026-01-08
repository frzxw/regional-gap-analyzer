"use client";

import { useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { History, Trash2, Loader2, FileText } from "lucide-react";
import { ImportHistoryItem } from "@/lib/api";

interface ImportHistoryProps {
    history: ImportHistoryItem[];
    loading: boolean;
    onRefresh: () => void;
    onRollback: (sourceId: string) => void;
}

export function ImportHistory({
    history,
    loading,
    onRefresh,
    onRollback,
}: ImportHistoryProps) {
    useEffect(() => {
        onRefresh();
    }, [onRefresh]);

    const formatDate = (dateString: string): string => {
        if (!dateString) return "N/A";
        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) return "N/A";
            return date.toLocaleDateString("id-ID", {
                day: "numeric",
                month: "short",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit",
            });
        } catch {
            return "N/A";
        }
    };

    // return (
    //     // <Card className="bg-card/50 backdrop-blur-sm border-muted">
    //     //     <CardHeader className="flex flex-row items-center justify-between pb-3">
    //     //         <CardTitle className="flex items-center gap-2 text-lg">
    //     //             <History className="w-5 h-5" />
    //     //             Riwayat Import
    //     //         </CardTitle>
    //     //         <Button
    //     //             variant="ghost"
    //     //             size="sm"
    //     //             onClick={onRefresh}
    //     //             disabled={loading}
    //     //         >
    //     //             {loading ? (
    //     //                 <Loader2 className="w-4 h-4 animate-spin" />
    //     //             ) : (
    //     //                 "Refresh"
    //     //             )}
    //     //         </Button>
    //     //     </CardHeader>
    //     //     <CardContent>
    //     //         {loading && history.length === 0 ? (
    //     //             <div className="flex items-center justify-center py-8 text-muted-foreground">
    //     //                 <Loader2 className="w-5 h-5 animate-spin mr-2" />
    //     //                 Loading...
    //     //             </div>
    //     //         ) : history.length === 0 ? (
    //     //             <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
    //     //                 <FileText className="w-10 h-10 mb-2 opacity-50" />
    //     //                 <p>Belum ada riwayat import</p>
    //     //             </div>
    //     //         ) : (
    //     //             <ScrollArea className="h-[300px] pr-4">
    //     //                 <div className="space-y-3">
    //     //                     {history.map((item, index) => (
    //     //                         <div
    //     //                             key={item._id || `import-${index}`}
    //     //                             className="flex items-center justify-between p-3 bg-muted/30 rounded-lg border border-muted-foreground/10 hover:bg-muted/50 transition-colors"
    //     //                         >
    //     //                             <div className="flex-1 min-w-0">
    //     //                                 <div className="flex items-center gap-2 flex-wrap">
    //     //                                     <FileText className="w-4 h-4 text-muted-foreground" />
    //     //                                     <p className="font-medium text-sm truncate">
    //     //                                         {item.name || "Unknown"}
    //     //                                     </p>
    //     //                                     {item.indicator_code && (
    //     //                                         <Badge variant="default" className="text-xs">
    //     //                                             {item.indicator_code}
    //     //                                         </Badge>
    //     //                                     )}
    //     //                                     {item.tahun && (
    //     //                                         <Badge variant="outline" className="text-xs">
    //     //                                             {item.tahun}
    //     //                                         </Badge>
    //     //                                     )}
    //     //                                 </div>
    //     //                                 <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
    //     //                                     <span>{formatDate(item.created_at)}</span>
    //     //                                     {item.records_count !== undefined && item.records_count > 0 && (
    //     //                                         <span className="text-green-600 dark:text-green-400">
    //     //                                             ✓ {item.records_count} records
    //     //                                         </span>
    //     //                                     )}
    //     //                                     {item.source_type && (
    //     //                                         <span className="opacity-50">{item.source_type}</span>
    //     //                                     )}
    //     //                                 </div>
    //     //                             </div>
    //     //                             <Button
    //     //                                 variant="ghost"
    //     //                                 size="sm"
    //     //                                 className="text-destructive hover:text-destructive hover:bg-destructive/10"
    //     //                                 onClick={() => onRollback(item._id)}
    //     //                                 title="Delete import"
    //     //                             >
    //     //                                 <Trash2 className="w-4 h-4" />
    //     //                             </Button>
    //     //                         </div>
    //     //                     ))}
    //     //                 </div>
    //     //             </ScrollArea>
    //     //         )}
    //     //     </CardContent>
    //     // </Card>
    // );
}
