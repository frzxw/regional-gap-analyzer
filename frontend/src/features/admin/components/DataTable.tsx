"use client";

import React, { useState, useEffect, useCallback } from "react";
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

/**
 * Map indicator code (underscore) to API endpoint path (kebab-case)
 */
function getIndicatorEndpoint(indicatorCode: string): string {
    const mapping: Record<string, string> = {
        gini_ratio: "gini-ratio",
        ipm: "indeks-pembangunan-manusia",
        tpt: "tingkat-pengangguran-terbuka",
        kependudukan: "kependudukan",
        pdrb_per_kapita: "pdrb-perkapita",
        ihk: "indeks-harga-konsumen",
        inflasi_tahunan: "inflasi-tahunan",
        persentase_penduduk_miskin: "persentase-penduduk-miskin",
        angkatan_kerja: "angkatan-kerja",
        rata_rata_upah_bersih: "rata-rata-upah",
    };
    return mapping[indicatorCode] || indicatorCode;
}

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
    indikator?: string;
    source?: string;
    
    // Gini Ratio structure
    data_semester_1?: {
        perkotaan?: number;
        perdesaan?: number;
        total?: number;
    };
    data_semester_2?: {
        perkotaan?: number;
        perdesaan?: number;
        total?: number;
    };
    data_tahunan?: {
        perkotaan?: number;
        perdesaan?: number;
        total?: number;
    };
    
    // TPT structure
    data?: {
        februari?: number;
        agustus?: number;
        tahunan?: number;
        // Kependudukan fields
        jumlah_penduduk_ribu?: number;
        laju_pertumbuhan_tahunan?: number;
        persentase_penduduk?: number;
        kepadatan_per_km2?: number;
        rasio_jenis_kelamin?: number;
    } | number; // IPM uses simple number
    
    // Angkatan Kerja structure
    data_februari?: {
        bekerja?: number;
        pengangguran?: number;
        jumlah_ak?: number;
        persentase_bekerja_ak?: number;
    };
    data_agustus?: {
        bekerja?: number;
        pengangguran?: number;
        jumlah_ak?: number;
        persentase_bekerja_ak?: number;
    };
    
    // IHK structure
    data_bulanan?: {
        [key: string]: number | null;
    };
    tahunan?: number;
    
    // PDRB structure
    data_ribu_rp?: number;
    
    // Rata-rata Upah Bersih structure
    sektor?: {
        [key: string]: {
            februari?: number;
            agustus?: number;
            tahunan?: number;
        };
    };
    
    [key: string]: any; // For other dynamic properties
}

interface DataTableProps {
    onEdit?: (item: DataItem) => void;
    onDelete?: (item: DataItem) => void;
}

/**
 * Render value based on indicator type
 */
function renderIndicatorValue(item: DataItem, indicatorCode: string): React.ReactNode {
    // 1. GINI RATIO & PERSENTASE PENDUDUK MISKIN - Semester breakdown
    if (indicatorCode === "gini_ratio" || indicatorCode === "persentase_penduduk_miskin") {
        const hasData = item.data_semester_1 || item.data_semester_2 || item.data_tahunan;
        if (!hasData) return <span className="text-muted-foreground">-</span>;
        
        return (
            <div className="text-xs space-y-1">
                {item.data_semester_1?.total !== null && item.data_semester_1?.total !== undefined && (
                    <div className="flex justify-between gap-3">
                        <span className="text-muted-foreground">S1:</span>
                        <span className="font-mono">{item.data_semester_1.total.toFixed(3)}</span>
                    </div>
                )}
                {item.data_semester_2?.total !== null && item.data_semester_2?.total !== undefined && (
                    <div className="flex justify-between gap-3">
                        <span className="text-muted-foreground">S2:</span>
                        <span className="font-mono">{item.data_semester_2.total.toFixed(3)}</span>
                    </div>
                )}
                {item.data_tahunan?.total !== null && item.data_tahunan?.total !== undefined && (
                    <div className="flex justify-between gap-3 pt-1 border-t">
                        <span className="font-semibold">Tahunan:</span>
                        <span className="font-mono font-bold text-primary">{item.data_tahunan.total.toFixed(3)}</span>
                    </div>
                )}
            </div>
        );
    }
    
    // 2. TPT - Februari/Agustus/Tahunan
    if (indicatorCode === "tpt") {
        if (!item.data) return <span className="text-muted-foreground">-</span>;
        
        return (
            <div className="text-xs space-y-1">
                {item.data.februari !== null && item.data.februari !== undefined && (
                    <div className="flex justify-between gap-3">
                        <span className="text-muted-foreground">Feb:</span>
                        <span className="font-mono">{item.data.februari.toFixed(2)}%</span>
                    </div>
                )}
                {item.data.agustus !== null && item.data.agustus !== undefined && (
                    <div className="flex justify-between gap-3">
                        <span className="text-muted-foreground">Agt:</span>
                        <span className="font-mono">{item.data.agustus.toFixed(2)}%</span>
                    </div>
                )}
                {item.data.tahunan !== null && item.data.tahunan !== undefined && (
                    <div className="flex justify-between gap-3 pt-1 border-t">
                        <span className="font-semibold">Tahunan:</span>
                        <span className="font-mono font-bold text-primary">{item.data.tahunan.toFixed(2)}%</span>
                    </div>
                )}
            </div>
        );
    }
    
    // 3. ANGKATAN KERJA - Februari/Agustus complex data
    if (indicatorCode === "angkatan_kerja") {
        const hasFeb = item.data_februari?.jumlah_ak;
        const hasAgt = item.data_agustus?.jumlah_ak;
        
        if (!hasFeb && !hasAgt) return <span className="text-muted-foreground">-</span>;
        
        return (
            <div className="text-xs space-y-1">
                {hasFeb && (
                    <div className="space-y-0.5">
                        <div className="font-medium text-muted-foreground">Februari:</div>
                        <div className="flex justify-between gap-2 pl-2">
                            <span>Jumlah AK:</span>
                            <span className="font-mono">{item.data_februari.jumlah_ak?.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between gap-2 pl-2">
                            <span>% Bekerja:</span>
                            <span className="font-mono text-primary">{item.data_februari.persentase_bekerja_ak?.toFixed(2)}%</span>
                        </div>
                    </div>
                )}
                {hasAgt && (
                    <div className="space-y-0.5 pt-1 border-t">
                        <div className="font-medium text-muted-foreground">Agustus:</div>
                        <div className="flex justify-between gap-2 pl-2">
                            <span>Jumlah AK:</span>
                            <span className="font-mono">{item.data_agustus.jumlah_ak?.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between gap-2 pl-2">
                            <span>% Bekerja:</span>
                            <span className="font-mono text-primary">{item.data_agustus.persentase_bekerja_ak?.toFixed(2)}%</span>
                        </div>
                    </div>
                )}
            </div>
        );
    }
    
    // 4. KEPENDUDUKAN - Multiple fields
    if (indicatorCode === "kependudukan") {
        if (!item.data) return <span className="text-muted-foreground">-</span>;
        
        return (
            <div className="text-xs space-y-0.5">
                {item.data.jumlah_penduduk_ribu && (
                    <div className="flex justify-between gap-2">
                        <span className="text-muted-foreground">Penduduk:</span>
                        <span className="font-mono">{item.data.jumlah_penduduk_ribu.toLocaleString()} rb</span>
                    </div>
                )}
                {item.data.kepadatan_per_km2 && (
                    <div className="flex justify-between gap-2">
                        <span className="text-muted-foreground">Kepadatan:</span>
                        <span className="font-mono">{item.data.kepadatan_per_km2.toFixed(0)}/km²</span>
                    </div>
                )}
                {item.data.laju_pertumbuhan_tahunan !== null && item.data.laju_pertumbuhan_tahunan !== undefined && (
                    <div className="flex justify-between gap-2">
                        <span className="text-muted-foreground">Pertumbuhan:</span>
                        <span className="font-mono text-primary">{item.data.laju_pertumbuhan_tahunan.toFixed(2)}%</span>
                    </div>
                )}
            </div>
        );
    }
    
    // 5. IHK - Monthly data with all months
    if (indicatorCode === "ihk") {
        const hasTahunan = item.tahunan !== null && item.tahunan !== undefined;
        const hasBulanan = item.data_bulanan && Object.keys(item.data_bulanan).length > 0;
        
        if (!hasTahunan && !hasBulanan) return <span className="text-muted-foreground">-</span>;
        
        const monthOrder = ['januari', 'februari', 'maret', 'april', 'mei', 'juni', 
                           'juli', 'agustus', 'september', 'oktober', 'november', 'desember'];
        const months = hasBulanan ? 
            monthOrder.map(m => [m, item.data_bulanan[m]]).filter(([_, val]) => val !== null) : [];
        
        return (
            <div className="text-xs space-y-1.5 max-w-[300px]">
                {hasTahunan ? (
                    <div className="flex justify-between gap-3 pb-1.5 border-b">
                        <span className="font-semibold">Tahunan:</span>
                        <span className="font-mono font-bold text-primary">{item.tahunan?.toFixed(2)}</span>
                    </div>
                ) : (
                    <div className="text-[10px] text-muted-foreground/60 pb-1.5 border-b">Tahunan: null</div>
                )}
                
                {hasBulanan && months.length > 0 && (
                    <div className="grid grid-cols-2 gap-x-3 gap-y-0.5">
                        {months.map(([month, value]) => (
                            <div key={month} className="flex justify-between gap-2 text-[11px]">
                                <span className="text-muted-foreground capitalize">{month.substring(0, 3)}:</span>
                                <span className="font-mono">{value?.toFixed(2)}</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        );
    }
    
    // 6. IPM - Simple value
    if (indicatorCode === "ipm") {
        const val = typeof item.data === 'number' ? item.data : item.value;
        if (val === null || val === undefined) return <span className="text-muted-foreground">-</span>;
        
        return <span className="font-mono font-medium text-primary">{val.toFixed(2)}</span>;
    }
    
    // 7. PDRB - ADHB/ADHK with currency format
    if (indicatorCode === "pdrb_per_kapita") {
        if (!item.data_ribu_rp) return <span className="text-muted-foreground">-</span>;
        
        const type = item.indikator?.includes('adhb') ? 'ADHB' : 
                     item.indikator?.includes('adhk') ? 'ADHK 2010' : 'PDRB';
        
        return (
            <div className="text-xs">
                <div className="flex items-center gap-2 mb-1">
                    <Badge variant="outline" className="text-[10px] px-1.5 py-0">{type}</Badge>
                </div>
                <div className="font-mono font-semibold text-primary">
                    Rp {item.data_ribu_rp.toLocaleString()}
                </div>
                <div className="text-[10px] text-muted-foreground/60 mt-0.5">ribu rupiah</div>
            </div>
        );
    }
    
    // 8. INFLASI TAHUNAN - Monthly inflation data (same as IHK)
    if (indicatorCode === "inflasi_tahunan") {
        const hasTahunan = item.tahunan !== null && item.tahunan !== undefined;
        const hasBulanan = item.data_bulanan && Object.keys(item.data_bulanan).length > 0;
        
        if (!hasTahunan && !hasBulanan) return <span className="text-muted-foreground">-</span>;
        
        const monthOrder = ['januari', 'februari', 'maret', 'april', 'mei', 'juni', 
                           'juli', 'agustus', 'september', 'oktober', 'november', 'desember'];
        const months = hasBulanan ? 
            monthOrder.map(m => [m, item.data_bulanan[m]]).filter(([_, val]) => val !== null) : [];
        
        return (
            <div className="text-xs space-y-1.5 max-w-[300px]">
                {hasTahunan ? (
                    <div className="flex justify-between gap-3 pb-1.5 border-b">
                        <span className="font-semibold">Tahunan:</span>
                        <span className="font-mono font-bold text-primary">{item.tahunan?.toFixed(2)}%</span>
                    </div>
                ) : (
                    <div className="text-[10px] text-muted-foreground/60 pb-1.5 border-b">Tahunan: null</div>
                )}
                
                {hasBulanan && months.length > 0 && (
                    <div className="grid grid-cols-2 gap-x-3 gap-y-0.5">
                        {months.map(([month, value]) => (
                            <div key={month} className="flex justify-between gap-2 text-[11px]">
                                <span className="text-muted-foreground capitalize">{month.substring(0, 3)}:</span>
                                <span className="font-mono">{value?.toFixed(2)}%</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        );
    }
    
    // 9. RATA-RATA UPAH BERSIH - Sector-based wage data
    if (indicatorCode === "rata_rata_upah_bersih") {
        if (!item.sektor || Object.keys(item.sektor).length === 0) {
            return <span className="text-muted-foreground">-</span>;
        }
        
        const sectorNames: Record<string, string> = {
            pertanian_kehutanan_perikanan: "Pertanian",
            pertambangan_penggalian: "Pertambangan",
            industri_pengolahan: "Industri",
            listrik_gas: "Listrik & Gas",
            air_sampah_limbah_daurlulang: "Air & Limbah",
            konstruksi: "Konstruksi",
            perdagangan: "Perdagangan",
            transportasi_pergudangan: "Transportasi",
            akomodasi_makan_minum: "Akomodasi",
            informasi_komunikasi: "Informasi",
            jasa_keuangan: "Keuangan",
            real_estate: "Real Estate",
            jasa_perusahaan: "Jasa Perusahaan",
            admin_pemerintahan: "Pemerintahan",
            jasa_pendidikan: "Pendidikan",
            jasa_kesehatan: "Kesehatan",
            jasa_lainnya: "Jasa Lainnya",
            total: "TOTAL"
        };
        
        return (
            <div className="text-xs space-y-0.5 max-w-[280px]">
                {Object.entries(item.sektor).map(([sectorKey, sectorData]) => {
                    if (!sectorData) return null;
                    
                    const hasData = sectorData.februari || sectorData.agustus || sectorData.tahunan;
                    if (!hasData) return null;
                    
                    const isTotal = sectorKey === 'total';
                    
                    return (
                        <div key={sectorKey} className={`flex items-start gap-2 text-[10px] ${isTotal ? "pt-1 mt-0.5 border-t font-semibold" : ""}`}>
                            <div className={`min-w-[85px] text-right ${isTotal ? "font-bold" : "text-muted-foreground"}`}>
                                {sectorNames[sectorKey] || sectorKey}:
                            </div>
                            <div className="flex gap-2 font-mono">
                                {sectorData.februari && (
                                    <span className={isTotal ? "text-primary" : ""}>
                                        {(sectorData.februari / 1000).toFixed(0)}K
                                    </span>
                                )}
                                {sectorData.agustus && (
                                    <span className={isTotal ? "text-primary" : ""}>
                                        {(sectorData.agustus / 1000).toFixed(0)}K
                                    </span>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>
        );
    }
    
    // DEFAULT: Simple value for other indicators
    return (
        <span className="font-mono">
            {item.value ? item.value.toFixed(3) : "-"}
        </span>
    );
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
            const endpoint = getIndicatorEndpoint(indicator);
            let url = `${API_BASE}/api/v1/${endpoint}`;
            
            if (tahun) {
                url += `/year/${tahun}`;
            } else {
                // Add trailing slash and pagination params for root endpoint
                url += `/?skip=0&limit=100`;
            }

            const response = await fetch(url);
            if (response.ok) {
                const result = await response.json();
                console.log('API Response:', result); // Debug
                console.log('First item:', result.data?.[0]); // Debug
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
            const endpoint = getIndicatorEndpoint(indicator);
            const response = await fetch(
                `${API_BASE}/api/v1/${endpoint}/${item.province_id}/${item.tahun}`,
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
                                    <TableHead className="text-right">
                                        {indicator === "gini_ratio" && "Data (S1/S2/Tahunan)"}
                                        {indicator === "persentase_penduduk_miskin" && "Kemiskinan (%)"}
                                        {indicator === "tpt" && "TPT (%)"}
                                        {indicator === "angkatan_kerja" && "Angkatan Kerja"}
                                        {indicator === "kependudukan" && "Kependudukan"}
                                        {indicator === "ihk" && "IHK"}
                                        {indicator === "ipm" && "IPM"}
                                        {indicator === "pdrb_per_kapita" && "PDRB Per Kapita"}
                                        {indicator === "inflasi_tahunan" && "Inflasi (%)"}
                                        {indicator === "rata_rata_upah_bersih" && "Upah Bersih"}
                                        {!["gini_ratio", "persentase_penduduk_miskin", "tpt", "angkatan_kerja", "kependudukan", "ihk", "ipm", "pdrb_per_kapita", "inflasi_tahunan", "rata_rata_upah_bersih"].includes(indicator) && "Value"}
                                    </TableHead>
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
                                        <TableCell className="text-right">
                                            {renderIndicatorValue(item, indicator)}
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
                                                    onClick={() => onEdit?.({ ...item, indicator_code: indicator })}
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
