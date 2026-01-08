"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Info } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ProvinceYearSelector } from "./ProvinceYearSelector";

const MONTHS = [
    "januari", "februari", "maret", "april", "mei", "juni",
    "juli", "agustus", "september", "oktober", "november", "desember"
];

export function IHKManualForm() {
    const { toast } = useToast();
    const [loading, setLoading] = useState(false);
    const [provinceId, setProvinceId] = useState<string>("");
    const [tahun, setTahun] = useState<string>(new Date().getFullYear().toString());
    const [tahunan, setTahunan] = useState<string>("");
    
    const [monthlyData, setMonthlyData] = useState<Record<string, string>>({
        januari: "", februari: "", maret: "", april: "", mei: "", juni: "",
        juli: "", agustus: "", september: "", oktober: "", november: "", desember: ""
    });

    const parseValue = (value: string): number | null => {
        if (!value || value.trim() === "") return null;
        const parsed = parseFloat(value);
        return isNaN(parsed) ? null : parsed;
    };

    const handleMonthChange = (month: string, value: string) => {
        setMonthlyData(prev => ({ ...prev, [month]: value }));
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

            const data_bulanan: Record<string, number | null> = {};
            MONTHS.forEach(month => {
                data_bulanan[month] = parseValue(monthlyData[month]);
            });

            const payload = {
                province_id: provinceId,
                tahun: parseInt(tahun, 10),
                data_bulanan,
                tahunan: parseValue(tahunan),
            };

            setLoading(true);

            try {
                const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
                const response = await fetch(`${API_BASE}/api/v1/indeks-harga-konsumen`, {
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
                    description: "Data IHK berhasil disimpan",
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
        [provinceId, tahun, monthlyData, tahunan, toast]
    );

    const handleReset = () => {
        setProvinceId("");
        setTahun(new Date().getFullYear().toString());
        setTahunan("");
        setMonthlyData({
            januari: "", februari: "", maret: "", april: "", mei: "", juni: "",
            juli: "", agustus: "", september: "", oktober: "", november: "", desember: ""
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg flex items-start gap-3">
                <Info className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
                <div className="text-sm">
                    <p className="font-medium text-blue-500">Input Manual IHK</p>
                    <p className="text-muted-foreground mt-1">
                        Masukkan nilai Indeks Harga Konsumen (IHK) per bulan dan nilai tahunan.
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
                    <CardTitle className="text-base">Data Bulanan IHK</CardTitle>
                    <CardDescription>Indeks Harga Konsumen per bulan</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-3 gap-4">
                    {MONTHS.map((month) => (
                        <div key={month} className="space-y-2">
                            <Label className="capitalize">{month}</Label>
                            <Input
                                type="number"
                                step="0.01"
                                value={monthlyData[month]}
                                onChange={(e) => handleMonthChange(month, e.target.value)}
                                disabled={loading}
                                placeholder="0.00"
                            />
                        </div>
                    ))}
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Data Tahunan</CardTitle>
                    <CardDescription>Nilai IHK tahunan</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-2">
                        <Label htmlFor="tahunan">Nilai Tahunan</Label>
                        <Input
                            id="tahunan"
                            type="number"
                            step="0.01"
                            value={tahunan}
                            onChange={(e) => setTahunan(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 107.25"
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
