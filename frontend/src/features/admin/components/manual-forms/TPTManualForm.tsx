"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Info } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ProvinceYearSelector } from "./ProvinceYearSelector";

export function TPTManualForm() {
    const { toast } = useToast();
    const [loading, setLoading] = useState(false);
    const [provinceId, setProvinceId] = useState<string>("");
    const [tahun, setTahun] = useState<string>(new Date().getFullYear().toString());
    const [februari, setFebruari] = useState<string>("");
    const [agustus, setAgustus] = useState<string>("");
    const [tahunan, setTahunan] = useState<string>("");

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
                    februari: parseValue(februari),
                    agustus: parseValue(agustus),
                    tahunan: parseValue(tahunan),
                },
            };

            setLoading(true);

            try {
                const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
                const response = await fetch(`${API_BASE}/api/v1/tingkat-pengangguran-terbuka`, {
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
                    description: "Data TPT berhasil disimpan",
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
        [provinceId, tahun, februari, agustus, tahunan, toast]
    );

    const handleReset = () => {
        setProvinceId("");
        setTahun(new Date().getFullYear().toString());
        setFebruari("");
        setAgustus("");
        setTahunan("");
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg flex items-start gap-3">
                <Info className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
                <div className="text-sm">
                    <p className="font-medium text-blue-500">Input Manual TPT</p>
                    <p className="text-muted-foreground mt-1">
                        Masukkan Tingkat Pengangguran Terbuka (%) untuk periode Februari, Agustus, dan Tahunan.
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
                    <CardTitle className="text-base">Data TPT (%)</CardTitle>
                    <CardDescription>Tingkat Pengangguran Terbuka</CardDescription>
                </CardHeader>
                <CardContent className="grid md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                        <Label htmlFor="februari">Februari</Label>
                        <Input
                            id="februari"
                            type="number"
                            step="0.01"
                            min="0"
                            max="100"
                            value={februari}
                            onChange={(e) => setFebruari(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="agustus">Agustus</Label>
                        <Input
                            id="agustus"
                            type="number"
                            step="0.01"
                            min="0"
                            max="100"
                            value={agustus}
                            onChange={(e) => setAgustus(e.target.value)}
                            disabled={loading}
                            placeholder="0.00"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="tahunan">Tahunan</Label>
                        <Input
                            id="tahunan"
                            type="number"
                            step="0.01"
                            min="0"
                            max="100"
                            value={tahunan}
                            onChange={(e) => setTahunan(e.target.value)}
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
