"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Info } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ProvinceYearSelector } from "./ProvinceYearSelector";

export function PersentasePendudukMiskinManualForm() {
    const { toast } = useToast();
    const [loading, setLoading] = useState(false);
    const [provinceId, setProvinceId] = useState<string>("");
    const [tahun, setTahun] = useState<string>(new Date().getFullYear().toString());
    
    const [sem1Perkotaan, setSem1Perkotaan] = useState<string>("");
    const [sem1Perdesaan, setSem1Perdesaan] = useState<string>("");
    const [sem1Total, setSem1Total] = useState<string>("");
    
    const [sem2Perkotaan, setSem2Perkotaan] = useState<string>("");
    const [sem2Perdesaan, setSem2Perdesaan] = useState<string>("");
    const [sem2Total, setSem2Total] = useState<string>("");
    
    const [tahunanPerkotaan, setTahunanPerkotaan] = useState<string>("");
    const [tahunanPerdesaan, setTahunanPerdesaan] = useState<string>("");
    const [tahunanTotal, setTahunanTotal] = useState<string>("");

    const parseValue = (value: string): number | null => {
        if (!value || value.trim() === "") return null;
        const parsed = parseFloat(value);
        return isNaN(parsed) ? null : parsed;
    };

    const handleSubmit = useCallback(
        async (e: React.FormEvent) => {
            e.preventDefault();
            
            if (!provinceId || !tahun) {
                toast({
                    title: "Form tidak lengkap",
                    description: "Mohon pilih provinsi dan tahun terlebih dahulu",
                    variant: "destructive",
                });
                return;
            }

            const payload = {
                province_id: provinceId,
                tahun: parseInt(tahun, 10),
                data_semester_1: {
                    perkotaan: parseValue(sem1Perkotaan),
                    perdesaan: parseValue(sem1Perdesaan),
                    total: parseValue(sem1Total),
                },
                data_semester_2: {
                    perkotaan: parseValue(sem2Perkotaan),
                    perdesaan: parseValue(sem2Perdesaan),
                    total: parseValue(sem2Total),
                },
                data_tahunan: {
                    perkotaan: parseValue(tahunanPerkotaan),
                    perdesaan: parseValue(tahunanPerdesaan),
                    total: parseValue(tahunanTotal),
                },
            };

            setLoading(true);

            try {
                const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
                const response = await fetch(`${API_BASE}/api/v1/persentase-penduduk-miskin`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || "Gagal menyimpan data");
                }

                toast({
                    title: "Berhasil!",
                    description: "Data Persentase Penduduk Miskin berhasil disimpan",
                });

                handleReset();
            } catch (error: any) {
                toast({
                    title: "Error",
                    description: error.message || "Terjadi kesalahan saat menyimpan data",
                    variant: "destructive",
                });
            } finally {
                setLoading(false);
            }
        },
        [provinceId, tahun, sem1Perkotaan, sem1Perdesaan, sem1Total, sem2Perkotaan, sem2Perdesaan, sem2Total, tahunanPerkotaan, tahunanPerdesaan, tahunanTotal, toast]
    );

    const handleReset = () => {
        setProvinceId("");
        setTahun(new Date().getFullYear().toString());
        setSem1Perkotaan("");
        setSem1Perdesaan("");
        setSem1Total("");
        setSem2Perkotaan("");
        setSem2Perdesaan("");
        setSem2Total("");
        setTahunanPerkotaan("");
        setTahunanPerdesaan("");
        setTahunanTotal("");
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg flex items-start gap-3">
                <Info className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
                <div className="text-sm">
                    <p className="font-medium text-blue-500">Input Manual Persentase Penduduk Miskin</p>
                    <p className="text-muted-foreground mt-1">
                        Masukkan data persentase penduduk miskin (%) per semester dan tahunan.
                    </p>
                </div>
            </div>

            <ProvinceYearSelector
                provinceId={provinceId}
                tahun={tahun}
                onProvinceChange={setProvinceId}
                onTahunChange={setTahun}
                disabled={loading}
            />

            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Semester 1 (Maret)</CardTitle>
                    <CardDescription>Persentase penduduk miskin (%)</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                        <Label>Perkotaan</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={sem1Perkotaan}
                            onChange={(e) => setSem1Perkotaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Perdesaan</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={sem1Perdesaan}
                            onChange={(e) => setSem1Perdesaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Total</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={sem1Total}
                            onChange={(e) => setSem1Total(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Semester 2 (September)</CardTitle>
                    <CardDescription>Persentase penduduk miskin (%)</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                        <Label>Perkotaan</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={sem2Perkotaan}
                            onChange={(e) => setSem2Perkotaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Perdesaan</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={sem2Perdesaan}
                            onChange={(e) => setSem2Perdesaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Total</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={sem2Total}
                            onChange={(e) => setSem2Total(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Data Tahunan</CardTitle>
                    <CardDescription>Persentase penduduk miskin tahunan (%)</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                        <Label>Perkotaan</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={tahunanPerkotaan}
                            onChange={(e) => setTahunanPerkotaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Perdesaan</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={tahunanPerdesaan}
                            onChange={(e) => setTahunanPerdesaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Total</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={tahunanTotal}
                            onChange={(e) => setTahunanTotal(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                </CardContent>
            </Card>

            <div className="flex gap-3">
                <Button type="submit" disabled={!provinceId || !tahun || loading} className="flex-1">
                    {loading ? (
                        <>
                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                            Menyimpan...
                        </>
                    ) : (
                        "Simpan Data"
                    )}
                </Button>
                <Button type="button" variant="outline" onClick={handleReset} disabled={loading}>
                    Reset
                </Button>
            </div>
        </form>
    );
}
