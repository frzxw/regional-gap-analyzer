"use client";

import { useState, useEffect } from "react";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface EditDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    data: any;
    onSave: (data: any) => Promise<void>;
}

export function EditDialog({ open, onOpenChange, data, onSave }: EditDialogProps) {
    const [formData, setFormData] = useState<any>({});
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (data) {
            setFormData({ ...data });
        }
    }, [data]);

    const handleSave = async () => {
        if (!data) return;

        setLoading(true);
        try {
            await onSave(formData);
            onOpenChange(false);
        } catch (error) {
            console.error("Failed to save:", error);
            alert(error instanceof Error ? error.message : "Gagal menyimpan data");
        } finally {
            setLoading(false);
        }
    };

    const updateNestedValue = (path: string, value: string) => {
        const numValue = value === "" ? null : parseFloat(value);
        const keys = path.split(".");

        setFormData((prev: any) => {
            const updated = { ...prev };
            let current = updated;

            for (let i = 0; i < keys.length - 1; i++) {
                if (!current[keys[i]]) {
                    current[keys[i]] = {};
                }
                current[keys[i]] = { ...current[keys[i]] };
                current = current[keys[i]];
            }

            current[keys[keys.length - 1]] = isNaN(numValue as number) ? null : numValue;
            return updated;
        });
    };

    const getNestedValue = (obj: any, path: string): string => {
        const keys = path.split(".");
        let current = obj;
        for (const key of keys) {
            if (current == null) return "";
            current = current[key];
        }
        return current?.toString() || "";
    };

    const indicatorCode = data?.indicator_code || data?.indikator || "gini_ratio";

    // Render form fields based on indicator type
    const renderFields = () => {
        // GINI RATIO & PERSENTASE PENDUDUK MISKIN - Semester data
        if (indicatorCode === "gini_ratio" || indicatorCode === "persentase_penduduk_miskin") {
            return (
                <Tabs defaultValue="semester1" className="w-full">
                    <TabsList className="grid w-full grid-cols-3">
                        <TabsTrigger value="semester1">Semester 1</TabsTrigger>
                        <TabsTrigger value="semester2">Semester 2</TabsTrigger>
                        <TabsTrigger value="tahunan">Tahunan</TabsTrigger>
                    </TabsList>

                    {["semester1", "semester2", "tahunan"].map((period) => (
                        <TabsContent key={period} value={period} className="space-y-3">
                            {["perkotaan", "perdesaan", "total"].map((field) => {
                                const path = period === "tahunan"
                                    ? `data_tahunan.${field}`
                                    : `data_${period.replace("semester", "semester_")}.${field}`;
                                return (
                                    <div key={field} className="grid grid-cols-4 items-center gap-4">
                                        <Label className="text-right capitalize">{field}</Label>
                                        <Input
                                            type="number"
                                            step="0.001"
                                            value={getNestedValue(formData, path)}
                                            onChange={(e) => updateNestedValue(path, e.target.value)}
                                            className="col-span-3"
                                            placeholder={`Masukkan ${field}...`}
                                        />
                                    </div>
                                );
                            })}
                        </TabsContent>
                    ))}
                </Tabs>
            );
        }

        // TPT - Februari/Agustus/Tahunan
        if (indicatorCode === "tpt") {
            return (
                <div className="space-y-3">
                    {[
                        { key: "data.februari", label: "Februari (%)" },
                        { key: "data.agustus", label: "Agustus (%)" },
                        { key: "data.tahunan", label: "Tahunan (%)" },
                    ].map(({ key, label }) => (
                        <div key={key} className="grid grid-cols-4 items-center gap-4">
                            <Label className="text-right">{label}</Label>
                            <Input
                                type="number"
                                step="0.01"
                                value={getNestedValue(formData, key)}
                                onChange={(e) => updateNestedValue(key, e.target.value)}
                                className="col-span-3"
                            />
                        </div>
                    ))}
                </div>
            );
        }

        // ANGKATAN KERJA - Februari/Agustus periods
        if (indicatorCode === "angkatan_kerja") {
            return (
                <Tabs defaultValue="februari" className="w-full">
                    <TabsList className="grid w-full grid-cols-2">
                        <TabsTrigger value="februari">Februari</TabsTrigger>
                        <TabsTrigger value="agustus">Agustus</TabsTrigger>
                    </TabsList>

                    {["februari", "agustus"].map((period) => (
                        <TabsContent key={period} value={period} className="space-y-3">
                            {[
                                { key: "bekerja", label: "Bekerja" },
                                { key: "pengangguran", label: "Pengangguran" },
                                { key: "jumlah_ak", label: "Jumlah AK" },
                                { key: "persentase_bekerja_ak", label: "% Bekerja AK" },
                            ].map(({ key, label }) => (
                                <div key={key} className="grid grid-cols-4 items-center gap-4">
                                    <Label className="text-right text-sm">{label}</Label>
                                    <Input
                                        type="number"
                                        step="0.01"
                                        value={getNestedValue(formData, `data_${period}.${key}`)}
                                        onChange={(e) => updateNestedValue(`data_${period}.${key}`, e.target.value)}
                                        className="col-span-3"
                                    />
                                </div>
                            ))}
                        </TabsContent>
                    ))}
                </Tabs>
            );
        }

        // KEPENDUDUKAN - Multiple fields
        if (indicatorCode === "kependudukan") {
            return (
                <div className="space-y-3">
                    {[
                        { key: "data.jumlah_penduduk_ribu", label: "Penduduk (ribu)" },
                        { key: "data.laju_pertumbuhan_tahunan", label: "Pertumbuhan (%)" },
                        { key: "data.persentase_penduduk", label: "Persentase (%)" },
                        { key: "data.kepadatan_per_km2", label: "Kepadatan/km²" },
                        { key: "data.rasio_jenis_kelamin", label: "Rasio JK" },
                    ].map(({ key, label }) => (
                        <div key={key} className="grid grid-cols-4 items-center gap-4">
                            <Label className="text-right text-sm">{label}</Label>
                            <Input
                                type="number"
                                step="0.01"
                                value={getNestedValue(formData, key)}
                                onChange={(e) => updateNestedValue(key, e.target.value)}
                                className="col-span-3"
                            />
                        </div>
                    ))}
                </div>
            );
        }

        // IPM - Simple value
        if (indicatorCode === "ipm") {
            return (
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label className="text-right">IPM</Label>
                    <Input
                        type="number"
                        step="0.01"
                        value={getNestedValue(formData, "data") || formData.value || ""}
                        onChange={(e) => {
                            const val = e.target.value === "" ? null : parseFloat(e.target.value);
                            setFormData((prev: any) => ({ ...prev, data: val, value: val }));
                        }}
                        className="col-span-3"
                    />
                </div>
            );
        }

        // DEFAULT - Simple value field
        return (
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="value" className="text-right">Nilai</Label>
                <Input
                    id="value"
                    type="number"
                    step="0.001"
                    value={formData.value ?? ""}
                    onChange={(e) => {
                        const val = e.target.value === "" ? null : parseFloat(e.target.value);
                        setFormData((prev: any) => ({ ...prev, value: val }));
                    }}
                    className="col-span-3"
                />
            </div>
        );
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[500px] max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>
                        Edit Data - {indicatorCode.replace(/_/g, " ").toUpperCase()}
                    </DialogTitle>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label className="text-right">Provinsi</Label>
                        <Input
                            value={data?.province_name || data?.province_id || ""}
                            disabled
                            className="col-span-3"
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label className="text-right">Tahun</Label>
                        <Input
                            value={data?.tahun || ""}
                            disabled
                            className="col-span-3"
                        />
                    </div>

                    <div className="border-t pt-4">
                        {renderFields()}
                    </div>
                </div>
                <DialogFooter>
                    <Button
                        variant="outline"
                        onClick={() => onOpenChange(false)}
                        disabled={loading}
                    >
                        Batal
                    </Button>
                    <Button onClick={handleSave} disabled={loading}>
                        {loading ? "Menyimpan..." : "Simpan"}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
