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
import { Loader2, Info } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ProvinceYearSelector } from "./ProvinceYearSelector";

export function PDRBPerKapitaManualForm() {
    const { toast } = useToast();
    const [loading, setLoading] = useState(false);
    const [provinceId, setProvinceId] = useState<string>("");
    const [tahun, setTahun] = useState<string>(new Date().getFullYear().toString());
    const [indikator, setIndikator] = useState<string>("pdrb_per_kapita_adhb");
    const [dataRibuRp, setDataRibuRp] = useState<string>("");

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
                indikator: indikator,
                data_ribu_rp: parseValue(dataRibuRp),
            };

            setLoading(true);

            try {
                const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
                const response = await fetch(`${API_BASE}/api/v1/pdrb-per-kapita`, {
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
                    description: "Data PDRB Per Kapita berhasil disimpan",
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
        [provinceId, tahun, indikator, dataRibuRp, toast]
    );

    const handleReset = () => {
        setProvinceId("");
        setTahun(new Date().getFullYear().toString());
        setIndikator("pdrb_per_kapita_adhb");
        setDataRibuRp("");
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg flex items-start gap-3">
                <Info className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
                <div className="text-sm">
                    <p className="font-medium text-blue-500">Input Manual PDRB Per Kapita</p>
                    <p className="text-muted-foreground mt-1">
                        Masukkan nilai PDRB Per Kapita dalam ribuan rupiah (ADHB atau ADHK 2010).
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
                    <CardTitle className="text-base">Data PDRB Per Kapita</CardTitle>
                    <CardDescription>Produk Domestik Regional Bruto Per Kapita</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="indikator">Jenis PDRB *</Label>
                        <Select value={indikator} onValueChange={setIndikator} disabled={loading}>
                            <SelectTrigger id="indikator">
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="pdrb_per_kapita_adhb">ADHB (Atas Dasar Harga Berlaku)</SelectItem>
                                <SelectItem value="pdrb_per_kapita_adhk_2010">ADHK 2010 (Atas Dasar Harga Konstan)</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="data_ribu_rp">Nilai PDRB Per Kapita (ribu rupiah)</Label>
                        <Input
                            id="data_ribu_rp"
                            type="number"
                            step="0.01"
                            value={dataRibuRp}
                            onChange={(e) => setDataRibuRp(e.target.value)}
                            disabled={loading}
                            placeholder="Contoh: 75432.56"
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
