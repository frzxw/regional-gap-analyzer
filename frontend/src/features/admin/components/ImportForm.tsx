"use client";

import { useState, useCallback } from "react";
import { FileUploadZone } from "./FileUploadZone";
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
import { Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { UploadStatus } from "../hooks/useImport";
import { ImportResult } from "@/lib/api";

const INDICATOR_OPTIONS = [
    { code: "gini_ratio", label: "Gini Ratio" },
    { code: "ipm", label: "Indeks Pembangunan Manusia (IPM)" },
    { code: "tpt", label: "Tingkat Pengangguran Terbuka (TPT)" },
    { code: "kependudukan", label: "Kependudukan" },
    { code: "pdrb_per_kapita", label: "PDRB Per Kapita" },
    { code: "ihk", label: "Indeks Harga Konsumen (IHK)" },
    { code: "inflasi_tahunan", label: "Inflasi Tahunan" },
    { code: "persentase_penduduk_miskin", label: "Persentase Penduduk Miskin" },
    { code: "angkatan_kerja", label: "Angkatan Kerja" },
    { code: "rata_rata_upah_bersih", label: "Rata-rata Upah Bersih" },
];

interface ImportFormProps {
    onSubmit: (file: File, indicatorCode: string, year: number) => Promise<void>;
    status: UploadStatus;
    error: string | null;
    result: ImportResult | null;
    onReset: () => void;
}

export function ImportForm({
    onSubmit,
    status,
    error,
    result,
    onReset,
}: ImportFormProps) {
    const [file, setFile] = useState<File | null>(null);
    const [indicatorCode, setIndicatorCode] = useState<string>("");
    const [year, setYear] = useState<string>(new Date().getFullYear().toString());

    const handleFileSelect = useCallback((selectedFile: File) => {
        setFile(selectedFile);
    }, []);

    const handleSubmit = useCallback(
        async (e: React.FormEvent) => {
            e.preventDefault();
            if (!file || !indicatorCode || !year) return;

            await onSubmit(file, indicatorCode, parseInt(year, 10));
        },
        [file, indicatorCode, year, onSubmit]
    );

    const handleReset = useCallback(() => {
        setFile(null);
        setIndicatorCode("");
        setYear(new Date().getFullYear().toString());
        onReset();
    }, [onReset]);

    const isFormValid = file && indicatorCode && year;
    const isLoading = status === "uploading";

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            {/* Indicator Selection */}
            <div className="space-y-2">
                <Label htmlFor="indicator">Tipe Indikator</Label>
                <Select value={indicatorCode} onValueChange={setIndicatorCode} disabled={isLoading}>
                    <SelectTrigger id="indicator" className="w-full">
                        <SelectValue placeholder="Pilih tipe indikator..." />
                    </SelectTrigger>
                    <SelectContent>
                        {INDICATOR_OPTIONS.map((option) => (
                            <SelectItem key={option.code} value={option.code}>
                                {option.label}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            {/* Year Input */}
            <div className="space-y-2">
                <Label htmlFor="year">Tahun Data</Label>
                <Input
                    id="year"
                    type="number"
                    min="2000"
                    max="2100"
                    value={year}
                    onChange={(e) => setYear(e.target.value)}
                    disabled={isLoading}
                    placeholder="Contoh: 2024"
                />
            </div>

            {/* File Upload Zone */}
            <div className="space-y-2">
                <Label>File Data</Label>
                <FileUploadZone onFileSelect={handleFileSelect} disabled={isLoading} />
            </div>

            {/* Status Messages */}
            {status === "success" && result && (
                <div className="p-4 bg-green-500/10 border border-green-500/30 rounded-lg flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5" />
                    <div>
                        <p className="font-medium text-green-500">Import Berhasil!</p>
                        <p className="text-sm text-muted-foreground mt-1">
                            {result.records_imported} dari {result.records_processed} record berhasil diimport.
                        </p>
                    </div>
                </div>
            )}

            {status === "error" && error && (
                <div className="p-4 bg-destructive/10 border border-destructive/30 rounded-lg flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 text-destructive mt-0.5" />
                    <div>
                        <p className="font-medium text-destructive">Import Gagal</p>
                        <p className="text-sm text-muted-foreground mt-1">{error}</p>
                    </div>
                </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3">
                <Button
                    type="submit"
                    disabled={!isFormValid || isLoading}
                    className="flex-1"
                >
                    {isLoading ? (
                        <>
                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                            Mengupload...
                        </>
                    ) : (
                        "Import Data"
                    )}
                </Button>
                {(status === "success" || status === "error") && (
                    <Button type="button" variant="outline" onClick={handleReset}>
                        Reset
                    </Button>
                )}
            </div>
        </form>
    );
}
