"use client";

import { useState } from "react";
import { useImport, ImportForm, ImportHistory, DataTable, EditDialog } from "@/features/admin";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Upload, Database, FileText } from "lucide-react";
import Link from "next/link";
import { useToast } from "@/hooks/use-toast";

export default function AdminImportPage() {
    const {
        status,
        error,
        result,
        history,
        historyLoading,
        uploadFile,
        fetchHistory,
        rollbackImport,
        reset,
    } = useImport();

    const [editOpen, setEditOpen] = useState(false);
    const [editData, setEditData] = useState<any>(null);
    const [refreshKey, setRefreshKey] = useState(0);

    const handleEdit = (item: any) => {
        setEditData(item);
        setEditOpen(true);
    };

    const handleSave = async (data: any) => {
        try {
            const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

            // Map indicator code to endpoint
            const indicatorCode = data.indicator_code || data.indikator || "gini_ratio";
            const mapping: Record<string, string> = {
                gini_ratio: "gini-ratio",
                ipm: "indeks-pembangunan-manusia",
                tpt: "tingkat-pengangguran-terbuka",
                kependudukan: "kependudukan",
                pdrb_per_kapita: "pdrb-per-kapita",
                ihk: "indeks-harga-konsumen",
                inflasi_tahunan: "inflasi-tahunan",
                persentase_penduduk_miskin: "persentase-penduduk-miskin",
                angkatan_kerja: "angkatan-kerja",
                rata_rata_upah_bersih: "rata-rata-upah",
            };
            const endpoint = mapping[indicatorCode] || indicatorCode;

            const response = await fetch(
                `${API_BASE}/api/v1/${endpoint}/${data.province_id}/${data.tahun}`,
                {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ value: data.value }),
                }
            );

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || "Failed to update");
            }

            setRefreshKey((prev) => prev + 1); // Trigger table refresh
        } catch (error) {
            console.error("Update failed:", error);
            throw error;
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/30">
            {/* Header */}
            <header className="sticky top-0 z-50 backdrop-blur-xl bg-background/80 border-b border-border/50">
                <div className="container mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-primary/10 rounded-lg">
                                <Database className="w-6 h-6 text-primary" />
                            </div>
                            <div>
                                <h1 className="text-xl font-bold">Admin Panel</h1>
                                <p className="text-sm text-muted-foreground">
                                    Manage regional indicator data
                                </p>
                            </div>
                        </div>
                        <Link
                            href="/"
                            className="text-sm text-muted-foreground hover:text-primary transition-colors"
                        >
                            ← Kembali ke Laman Utama
                        </Link>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-8">
                <Tabs defaultValue="import" className="max-w-6xl mx-auto">
                    <TabsList className="grid w-full grid-cols-2 mb-8">
                        <TabsTrigger value="import" className="flex items-center gap-2">
                            <Upload className="w-4 h-4" />
                            Import Data (CSV/Excel)
                        </TabsTrigger>
                        <TabsTrigger value="data" className="flex items-center gap-2">
                            <Database className="w-4 h-4" />
                            Manage Data (CRUD)
                        </TabsTrigger>
                    </TabsList>

                    <TabsContent value="import" className="space-y-8">
                        <div className="grid lg:grid-cols-2 gap-8">
                            {/* Import Form */}
                            <Card className="bg-card/50 backdrop-blur-sm border-muted shadow-xl">
                                <CardHeader>
                                    <CardTitle>Import Data Baru</CardTitle>
                                    <CardDescription>
                                        Upload file CSV/Excel untuk import data ke database.
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <ImportForm
                                        onSubmit={uploadFile}
                                        status={status}
                                        error={error || null}
                                        result={result || null}
                                        onReset={reset}
                                    />
                                </CardContent>
                            </Card>

                            {/* Import History */}
                            <ImportHistory
                                history={history}
                                loading={historyLoading}
                                onRefresh={fetchHistory}
                                onRollback={rollbackImport}
                            />
                        </div>

                        {/* Instructions */}
                        <Card className="bg-muted/30 border-muted-foreground/10">
                            <CardHeader>
                                <CardTitle className="text-base flex items-center gap-2">
                                    <FileText className="w-4 h-4" />
                                    Panduan Format File
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="text-sm text-muted-foreground space-y-3">
                                <p><strong>Format CSV yang didukung:</strong></p>
                                <ul className="list-disc list-inside space-y-1 ml-2">
                                    <li>Hanya file CSV (format BPS standard)</li>
                                    <li>Setiap indikator memiliki struktur kolom spesifik</li>
                                    <li>Header rows akan diproses otomatis sesuai indikator</li>
                                    <li>Nilai "-" atau "..." dianggap null</li>
                                    <li>Nama provinsi dengan prefix (PROV., KEP., DI.) didukung</li>
                                </ul>
                                <p className="text-xs text-muted-foreground/70 mt-2">
                                    💡 Import menggunakan endpoint spesifik per indikator untuk akurasi maksimal
                                </p>
                            </CardContent>
                        </Card>
                    </TabsContent>

                    <TabsContent value="data">
                        <DataTable
                            key={refreshKey}
                            onEdit={handleEdit}
                            onDelete={() => setRefreshKey(prev => prev + 1)}
                        />
                    </TabsContent>
                </Tabs>
            </main>

            <EditDialog
                open={editOpen}
                onOpenChange={setEditOpen}
                data={editData}
                onSave={handleSave}
            />
        </div>
    );
}
