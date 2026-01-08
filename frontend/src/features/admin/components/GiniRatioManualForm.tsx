"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, CheckCircle2, AlertCircle, Info } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

// Daftar provinsi sesuai dengan data BPS
const PROVINCES = [
    { id: "11", name: "Aceh" },
    { id: "12", name: "Sumatera Utara" },
    { id: "13", name: "Sumatera Barat" },
    { id: "14", name: "Riau" },
    { id: "15", name: "Jambi" },
    { id: "16", name: "Sumatera Selatan" },
    { id: "17", name: "Bengkulu" },
    { id: "18", name: "Lampung" },
    { id: "19", name: "Kepulauan Bangka Belitung" },
    { id: "21", name: "Kepulauan Riau" },
    { id: "31", name: "DKI Jakarta" },
    { id: "32", name: "Jawa Barat" },
    { id: "33", name: "Jawa Tengah" },
    { id: "34", name: "DI Yogyakarta" },
    { id: "35", name: "Jawa Timur" },
    { id: "36", name: "Banten" },
    { id: "51", name: "Bali" },
    { id: "52", name: "Nusa Tenggara Barat" },
    { id: "53", name: "Nusa Tenggara Timur" },
    { id: "61", name: "Kalimantan Barat" },
    { id: "62", name: "Kalimantan Tengah" },
    { id: "63", name: "Kalimantan Selatan" },
    { id: "64", name: "Kalimantan Timur" },
    { id: "65", name: "Kalimantan Utara" },
    { id: "71", name: "Sulawesi Utara" },
    { id: "72", name: "Sulawesi Tengah" },
    { id: "73", name: "Sulawesi Selatan" },
    { id: "74", name: "Sulawesi Tenggara" },
    { id: "75", name: "Gorontalo" },
    { id: "76", name: "Sulawesi Barat" },
    { id: "81", name: "Maluku" },
    { id: "82", name: "Maluku Utara" },
    { id: "91", name: "Papua Barat" },
    { id: "94", name: "Papua" },
];

interface DataSemester {
    perkotaan: number | null;
    perdesaan: number | null;
    total: number | null;
}

interface GiniRatioData {
    province_id: string;
    tahun: number;
    data_semester_1: DataSemester;
    data_semester_2: DataSemester;
    data_tahunan: DataSemester;
}

export function GiniRatioManualForm() {
    const { toast } = useToast();
    const [loading, setLoading] = useState(false);
    const [provinceId, setProvinceId] = useState<string>("");
    const [tahun, setTahun] = useState<string>(new Date().getFullYear().toString());

    // Semester 1 (Maret)
    const [sem1Perkotaan, setSem1Perkotaan] = useState<string>("");
    const [sem1Perdesaan, setSem1Perdesaan] = useState<string>("");
    const [sem1Total, setSem1Total] = useState<string>("");

    // Semester 2 (September)
    const [sem2Perkotaan, setSem2Perkotaan] = useState<string>("");
    const [sem2Perdesaan, setSem2Perdesaan] = useState<string>("");
    const [sem2Total, setSem2Total] = useState<string>("");

    // Tahunan
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

            const data: GiniRatioData = {
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
                const response = await fetch(`${API_BASE}/api/v1/gini-ratio`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || "Gagal menyimpan data");
                }

                toast({
                    title: "Berhasil!",
                    description: "Data Gini Ratio berhasil disimpan",
                });

                // Reset form
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
        [
            provinceId,
            tahun,
            sem1Perkotaan,
            sem1Perdesaan,
            sem1Total,
            sem2Perkotaan,
            sem2Perdesaan,
            sem2Total,
            tahunanPerkotaan,
            tahunanPerdesaan,
            tahunanTotal,
            toast,
        ]
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
            {/* Info Banner */}
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg flex items-start gap-3">
                <Info className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
                <div className="text-sm">
                    <p className="font-medium text-blue-500">Input Manual Gini Ratio</p>
                    <p className="text-muted-foreground mt-1">
                        Masukkan data Gini Ratio per provinsi dan tahun. Field yang kosong akan disimpan sebagai null.
                        Nilai Gini Ratio berkisar antara 0 (pemerataan sempurna) hingga 1 (ketimpangan maksimal).
                    </p>
                </div>
            </div>

            {/* Province & Year Selection */}
            <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                    <Label htmlFor="province">Provinsi *</Label>
                    <Select value={provinceId} onValueChange={setProvinceId} disabled={loading}>
                        <SelectTrigger id="province">
                            <SelectValue placeholder="Pilih provinsi..." />
                        </SelectTrigger>
                        <SelectContent>
                            {PROVINCES.map((prov) => (
                                <SelectItem key={prov.id} value={prov.id}>
                                    {prov.name}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>

                <div className="space-y-2">
                    <Label htmlFor="tahun">Tahun *</Label>
                    <Input
                        id="tahun"
                        type="number"
                        min="2000"
                        max="2100"
                        value={tahun}
                        onChange={(e) => setTahun(e.target.value)}
                        disabled={loading}
                        placeholder="Contoh: 2024"
                    />
                </div>
            </div>

            {/* Semester 1 (Maret) */}
            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Semester 1 (Maret)</CardTitle>
                    <CardDescription>Data Gini Ratio periode Maret</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                        <Label htmlFor="sem1_perkotaan">Perkotaan</Label>
                        <Input
                            id="sem1_perkotaan"
                            type="number"
                            step="0.001"
                            min="0"
                            max="1"
                            value={sem1Perkotaan}
                            onChange={(e) => setSem1Perkotaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="sem1_perdesaan">Perdesaan</Label>
                        <Input
                            id="sem1_perdesaan"
                            type="number"
                            step="0.001"
                            min="0"
                            max="1"
                            value={sem1Perdesaan}
                            onChange={(e) => setSem1Perdesaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="sem1_total">Total</Label>
                        <Input
                            id="sem1_total"
                            type="number"
                            step="0.001"
                            min="0"
                            max="1"
                            value={sem1Total}
                            onChange={(e) => setSem1Total(e.target.value)}
                            disabled={loading}
                            placeholder="0.000"
                        />
                    </div>
                </CardContent>
            </Card>

            {/* Semester 2 (September) */}
            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Semester 2 (September)</CardTitle>
                    <CardDescription>Data Gini Ratio periode September</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                        <Label htmlFor="sem2_perkotaan">Perkotaan</Label>
                        <Input
                            id="sem2_perkotaan"
                            type="number"
                            step="0.001"
                            min="0"
                            max="1"
                            value={sem2Perkotaan}
                            onChange={(e) => setSem2Perkotaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="sem2_perdesaan">Perdesaan</Label>
                        <Input
                            id="sem2_perdesaan"
                            type="number"
                            step="0.001"
                            min="0"
                            max="1"
                            value={sem2Perdesaan}
                            onChange={(e) => setSem2Perdesaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="sem2_total">Total</Label>
                        <Input
                            id="sem2_total"
                            type="number"
                            step="0.001"
                            min="0"
                            max="1"
                            value={sem2Total}
                            onChange={(e) => setSem2Total(e.target.value)}
                            disabled={loading}
                            placeholder="0.000"
                        />
                    </div>
                </CardContent>
            </Card>

            {/* Tahunan */}
            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Data Tahunan</CardTitle>
                    <CardDescription>Data Gini Ratio agregat tahunan</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                        <Label htmlFor="tahunan_perkotaan">Perkotaan</Label>
                        <Input
                            id="tahunan_perkotaan"
                            type="number"
                            step="0.001"
                            min="0"
                            max="1"
                            value={tahunanPerkotaan}
                            onChange={(e) => setTahunanPerkotaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="tahunan_perdesaan">Perdesaan</Label>
                        <Input
                            id="tahunan_perdesaan"
                            type="number"
                            step="0.001"
                            min="0"
                            max="1"
                            value={tahunanPerdesaan}
                            onChange={(e) => setTahunanPerdesaan(e.target.value)}
                            disabled={loading}
                            placeholder="0.000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="tahunan_total">Total</Label>
                        <Input
                            id="tahunan_total"
                            type="number"
                            step="0.001"
                            min="0"
                            max="1"
                            value={tahunanTotal}
                            onChange={(e) => setTahunanTotal(e.target.value)}
                            disabled={loading}
                            placeholder="0.000"
                        />
                    </div>
                </CardContent>
            </Card>

            {/* Action Buttons */}
            <div className="flex gap-3">
                <Button
                    type="submit"
                    disabled={!provinceId || !tahun || loading}
                    className="flex-1"
                >
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
