"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Info } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ProvinceYearSelector } from "./ProvinceYearSelector";

export function KependudukanManualForm() {
    const { toast } = useToast();
    const [loading, setLoading] = useState(false);
    const [provinceId, setProvinceId] = useState<string>("");
    const [tahun, setTahun] = useState<string>(new Date().getFullYear().toString());
    const [jumlahPenduduk, setJumlahPenduduk] = useState<string>("");
    const [lajuPertumbuhan, setLajuPertumbuhan] = useState<string>("");
    const [persentasePenduduk, setPersentasePenduduk] = useState<string>("");
    const [kepadatan, setKepadatan] = useState<string>("");
    const [rasioJenisKelamin, setRasioJenisKelamin] = useState<string>("");

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
                data: {
                    jumlah_penduduk_ribu: parseValue(jumlahPenduduk),
                    laju_pertumbuhan_tahunan: parseValue(lajuPertumbuhan),
                    persentase_penduduk: parseValue(persentasePenduduk),
                    kepadatan_per_km2: parseValue(kepadatan),
                    rasio_jenis_kelamin: parseValue(rasioJenisKelamin),
                },
            };

            setLoading(true);

            try {
                const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
                const response = await fetch(`${API_BASE}/api/v1/kependudukan`, {
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
                    description: "Data Kependudukan berhasil disimpan",
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
        [provinceId, tahun, jumlahPenduduk, lajuPertumbuhan, persentasePenduduk, kepadatan, rasioJenisKelamin, toast]
    );

    const handleReset = () => {
        setProvinceId("");
        setTahun(new Date().getFullYear().toString());
        setJumlahPenduduk("");
        setLajuPertumbuhan("");
        setPersentasePenduduk("");
        setKepadatan("");
        setRasioJenisKelamin("");
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg flex items-start gap-3">
                <Info className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
                <div className="text-sm">
                    <p className="font-medium text-blue-500">Input Manual Kependudukan</p>
                    <p className="text-muted-foreground mt-1">
                        Masukkan data kependudukan lengkap untuk provinsi dan tahun yang dipilih.
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
                    <CardTitle className="text-base">Data Kependudukan</CardTitle>
                    <CardDescription>Statistik kependudukan lengkap</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="jumlah_penduduk">Jumlah Penduduk (ribu)</Label>
                            <Input
                                id="jumlah_penduduk"
                                type="number"
                                step="0.01"
                                value={jumlahPenduduk}
                                onChange={(e) => setJumlahPenduduk(e.target.value)}
                                disabled={loading}
                                placeholder="Contoh: 45123.45"
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="laju_pertumbuhan">Laju Pertumbuhan Tahunan (%)</Label>
                            <Input
                                id="laju_pertumbuhan"
                                type="number"
                                step="0.01"
                                value={lajuPertumbuhan}
                                onChange={(e) => setLajuPertumbuhan(e.target.value)}
                                disabled={loading}
                                placeholder="Contoh: 1.23"
                            />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-3 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="persentase_penduduk">Persentase Penduduk (%)</Label>
                            <Input
                                id="persentase_penduduk"
                                type="number"
                                step="0.01"
                                value={persentasePenduduk}
                                onChange={(e) => setPersentasePenduduk(e.target.value)}
                                disabled={loading}
                                placeholder="Contoh: 15.67"
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="kepadatan">Kepadatan (per km²)</Label>
                            <Input
                                id="kepadatan"
                                type="number"
                                step="0.01"
                                value={kepadatan}
                                onChange={(e) => setKepadatan(e.target.value)}
                                disabled={loading}
                                placeholder="Contoh: 234.56"
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="rasio">Rasio Jenis Kelamin</Label>
                            <Input
                                id="rasio"
                                type="number"
                                step="0.01"
                                value={rasioJenisKelamin}
                                onChange={(e) => setRasioJenisKelamin(e.target.value)}
                                disabled={loading}
                                placeholder="Contoh: 102.34"
                            />
                        </div>
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
