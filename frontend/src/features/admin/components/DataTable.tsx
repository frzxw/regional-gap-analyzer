"use client";

import { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Loader2, RefreshCw, Pencil, Trash2, Database } from "lucide-react";

const INDICATOR_OPTIONS = [
    { value: "gini_ratio", label: "Gini Ratio" },
    { value: "ipm", label: "IPM" },
    { value: "tpt", label: "TPT" },
    { value: "kependudukan", label: "Kependudukan" },
    { value: "pdrb_per_kapita", label: "PDRB Per Kapita" },
    { value: "ihk", label: "IHK" },
    { value: "inflasi_tahunan", label: "Inflasi Tahunan" },
    { value: "persentase_penduduk_miskin", label: "Persentase Penduduk Miskin" },
    { value: "angkatan_kerja", label: "Angkatan Kerja" },
    { value: "rata_rata_upah_bersih", label: "Rata-rata Upah Bersih" },
];

interface DataItem {
    province_id: string;
    tahun: number;
    value?: number;
    province_name?: string;
    indicator_code?: string;
    source?: string;
}

interface DataTableProps {
    onEdit?: (item: DataItem) => void;
    onDelete?: (item: DataItem) => void;
}

export function DataTable({ onEdit, onDelete }: DataTableProps) {
    const [indicator, setIndicator] = useState("gini_ratio");
    const [tahun, setTahun] = useState("");
    const [data, setData] = useState<DataItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [total, setTotal] = useState(0);

    const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            let url = `${API_BASE}/api/v1/${indicator}`;
            if (tahun) {
                url += `?tahun=${tahun}`;
            }

            const response = await fetch(url);
            if (response.ok) {
                const result = await response.json();
                setData(result.data || []);
                setTotal(result.total || 0);
            } else {
                setData([]);
                setTotal(0);
            }
        } catch (error) {
            console.error("Error fetching data:", error);
            setData([]);
        } finally {
            setLoading(false);
        }
    }, [API_BASE, indicator, tahun]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const handleDelete = async (item: DataItem) => {
        if (!confirm(`Hapus data ${item.province_id} tahun ${item.tahun}?`)) {
            return;
        }

        try {
            const response = await fetch(
                `${API_BASE}/api/v1/${indicator}/${item.province_id}/${item.tahun}`,
                { method: "DELETE" }
            );

            if (response.ok) {
                fetchData(); // Refresh
                onDelete?.(item);
            } else {
                alert("Gagal menghapus data");
            }
        } catch (error) {
            console.error("Error deleting:", error);
            alert("Error menghapus data");
        }
    };

    return (
        <Card className="bg-card/50 backdrop-blur-sm border-muted">
            <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-lg">
                    <Database className="w-5 h-5" />
                    Data Management
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {/* Filters */}
                <div className="flex flex-wrap gap-3">
                    <Select value={indicator} onValueChange={setIndicator}>
                        <SelectTrigger className="w-[200px]">
                            <SelectValue placeholder="Pilih Indikator" />
                        </SelectTrigger>
                        <SelectContent>
                            {INDICATOR_OPTIONS.map((opt) => (
                                <SelectItem key={opt.value} value={opt.value}>
                                    {opt.label}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>

                    <Select
                        value={tahun}
                        onValueChange={(value: string) => setTahun(value === "all" ? "" : value)}
                    >
                        <SelectTrigger className="w-[140px]">
                            <SelectValue placeholder="Semua Tahun" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">Semua Tahun</SelectItem>
                            {Array.from({ length: 6 }, (_, i) => 2020 + i).map((year) => (
                                <SelectItem key={year} value={year.toString()}>
                                    {year}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>

                    <Button
                        variant="outline"
                        size="sm"
                        onClick={fetchData}
                        disabled={loading}
                    >
                        {loading ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                            <RefreshCw className="w-4 h-4" />
                        )}
                        <span className="ml-1">Refresh</span>
                    </Button>

                    <Badge variant="secondary" className="ml-auto">
                        {total} records
                    </Badge>
                </div>

                {/* Table */}
                {loading ? (
                    <div className="flex items-center justify-center py-12 text-muted-foreground">
                        <Loader2 className="w-6 h-6 animate-spin mr-2" />
                        Loading...
                    </div>
                ) : data.length === 0 ? (
                    <div className="text-center py-12 text-muted-foreground">
                        <Database className="w-10 h-10 mx-auto mb-2 opacity-50" />
                        <p>Tidak ada data untuk indikator ini</p>
                    </div>
                ) : (
                    <div className="rounded-md border overflow-hidden">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Province ID</TableHead>
                                    <TableHead>Province Name</TableHead>
                                    <TableHead>Tahun</TableHead>
                                    <TableHead className="text-right">Value</TableHead>
                                    <TableHead>Source</TableHead>
                                    <TableHead className="w-[100px]">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {data.slice(0, 20).map((item, idx) => (
                                    <TableRow key={`${item.province_id}-${item.tahun}-${idx}`}>
                                        <TableCell className="font-medium">
                                            {item.province_id}
                                        </TableCell>
                                        <TableCell>
                                            {item.province_name || "-"}
                                        </TableCell>
                                        <TableCell>{item.tahun}</TableCell>
                                        <TableCell className="text-right font-mono">
                                            {item.value?.toFixed(3) || "-"}
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline" className="text-xs">
                                                {item.source || "BPS"}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex gap-1">
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => onEdit?.(item)}
                                                    title="Edit"
                                                >
                                                    <Pencil className="w-4 h-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    className="text-destructive hover:text-destructive"
                                                    onClick={() => handleDelete(item)}
                                                    title="Delete"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </Button>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                        {data.length > 20 && (
                            <div className="p-3 text-center text-sm text-muted-foreground border-t">
                                Menampilkan 20 dari {data.length} records
                            </div>
                        )}
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
