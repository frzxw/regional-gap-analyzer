"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Info } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ProvinceYearSelector } from "./ProvinceYearSelector";

export function AngkatanKerjaManualForm() {
    const { toast } = useToast();
    const [loading, setLoading] = useState(false);
    const [provinceId, setProvinceId] = useState<string>("");
    const [tahun, setTahun] = useState<string>(new Date().getFullYear().toString());
    
    // Februari
    const [febBekerja, setFebBekerja] = useState<string>("");
    const [febPengangguran, setFebPengangguran] = useState<string>("");
    const [febJumlahAk, setFebJumlahAk] = useState<string>("");
    const [febPersentase, setFebPersentase] = useState<string>("");
    
    // Agustus
    const [agustBekerja, setAgustBekerja] = useState<string>("");
    const [agustPengangguran, setAgustPengangguran] = useState<string>("");
    const [agustJumlahAk, setAgustJumlahAk] = useState<string>("");
    const [agustPersentase, setAgustPersentase] = useState<string>("");

    const parseIntValue = (value: string): number | null => {
        if (!value || value.trim() === "") return null;
        const parsed = parseInt(value, 10);
        return isNaN(parsed) ? null : parsed;
    };

    const parseFloatValue = (value: string): number | null => {
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
                data_februari: {
                    bekerja: parseIntValue(febBekerja) || 0,
                    pengangguran: parseIntValue(febPengangguran) || 0,
                    jumlah_ak: parseIntValue(febJumlahAk) || 0,
                    persentase_bekerja_ak: parseFloatValue(febPersentase) || 0,
                },
                data_agustus: {
                    bekerja: parseIntValue(agustBekerja) || 0,
                    pengangguran: parseIntValue(agustPengangguran) || 0,
                    jumlah_ak: parseIntValue(agustJumlahAk) || 0,
                    persentase_bekerja_ak: parseFloatValue(agustPersentase) || 0,
                },
            };

            setLoading(true);

            try {
                const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
                const response = await fetch(`${API_BASE}/api/v1/angkatan-kerja`, {
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
                    description: "Data Angkatan Kerja berhasil disimpan",
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
        [provinceId, tahun, febBekerja, febPengangguran, febJumlahAk, febPersentase, agustBekerja, agustPengangguran, agustJumlahAk, agustPersentase, toast]
    );

    const handleReset = () => {
        setProvinceId("");
        setTahun(new Date().getFullYear().toString());
        setFebBekerja("");
        setFebPengangguran("");
        setFebJumlahAk("");
        setFebPersentase("");
        setAgustBekerja("");
        setAgustPengangguran("");
        setAgustJumlahAk("");
        setAgustPersentase("");
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg flex items-start gap-3">
                <Info className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
                <div className="text-sm">
                    <p className="font-medium text-blue-500">Input Manual Angkatan Kerja</p>
                    <p className="text-muted-foreground mt-1">
                        Masukkan data angkatan kerja untuk periode Februari dan Agustus (dalam jumlah orang).
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
                    <CardTitle className="text-base">Data Februari</CardTitle>
                    <CardDescription>Angkatan kerja periode Februari</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label>Bekerja (orang)</Label>
                        <Input
                            type="number"
                            value={febBekerja}
                            onChange={(e) => setFebBekerja(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 15000000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Pengangguran (orang)</Label>
                        <Input
                            type="number"
                            value={febPengangguran}
                            onChange={(e) => setFebPengangguran(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 500000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Jumlah Angkatan Kerja (orang)</Label>
                        <Input
                            type="number"
                            value={febJumlahAk}
                            onChange={(e) => setFebJumlahAk(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 15500000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Persentase Bekerja (%)</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={febPersentase}
                            onChange={(e) => setFebPersentase(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 96.77"
                        />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Data Agustus</CardTitle>
                    <CardDescription>Angkatan kerja periode Agustus</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label>Bekerja (orang)</Label>
                        <Input
                            type="number"
                            value={agustBekerja}
                            onChange={(e) => setAgustBekerja(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 15200000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Pengangguran (orang)</Label>
                        <Input
                            type="number"
                            value={agustPengangguran}
                            onChange={(e) => setAgustPengangguran(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 480000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Jumlah Angkatan Kerja (orang)</Label>
                        <Input
                            type="number"
                            value={agustJumlahAk}
                            onChange={(e) => setAgustJumlahAk(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 15680000"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Persentase Bekerja (%)</Label>
                        <Input
                            type="number"
                            step="0.01"
                            value={agustPersentase}
                            onChange={(e) => setAgustPersentase(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 96.94"
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
