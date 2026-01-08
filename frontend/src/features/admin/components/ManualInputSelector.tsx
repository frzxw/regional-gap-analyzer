"use client";

import { useState } from "react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { GiniRatioManualForm } from "./GiniRatioManualForm";
import { IPMManualForm } from "./manual-forms/IPMManualForm";
import { TPTManualForm } from "./manual-forms/TPTManualForm";
import { KependudukanManualForm } from "./manual-forms/KependudukanManualForm";
import { PersentasePendudukMiskinManualForm } from "./manual-forms/PersentasePendudukMiskinManualForm";
import { PDRBPerKapitaManualForm } from "./manual-forms/PDRBPerKapitaManualForm";
import { AngkatanKerjaManualForm } from "./manual-forms/AngkatanKerjaManualForm";
import { IHKManualForm } from "./manual-forms/IHKManualForm";
import { InflasiTahunanManualForm } from "./manual-forms/InflasiTahunanManualForm";

const INDICATORS = [
    { code: "gini_ratio", label: "Gini Ratio" },
    { code: "ipm", label: "Indeks Pembangunan Manusia (IPM)" },
    { code: "tpt", label: "Tingkat Pengangguran Terbuka (TPT)" },
    { code: "kependudukan", label: "Kependudukan" },
    { code: "persentase_penduduk_miskin", label: "Persentase Penduduk Miskin" },
    { code: "pdrb_per_kapita", label: "PDRB Per Kapita" },
    { code: "angkatan_kerja", label: "Angkatan Kerja" },
    { code: "ihk", label: "Indeks Harga Konsumen (IHK)" },
    { code: "inflasi_tahunan", label: "Inflasi Tahunan" },
];

export function ManualInputSelector() {
    const [selectedIndicator, setSelectedIndicator] = useState<string>("");

    const renderForm = () => {
        switch (selectedIndicator) {
            case "gini_ratio":
                return <GiniRatioManualForm />;
            case "ipm":
                return <IPMManualForm />;
            case "tpt":
                return <TPTManualForm />;
            case "kependudukan":
                return <KependudukanManualForm />;
            case "persentase_penduduk_miskin":
                return <PersentasePendudukMiskinManualForm />;
            case "pdrb_per_kapita":
                return <PDRBPerKapitaManualForm />;
            case "angkatan_kerja":
                return <AngkatanKerjaManualForm />;
            case "ihk":
                return <IHKManualForm />;
            case "inflasi_tahunan":
                return <InflasiTahunanManualForm />;
            default:
                return (
                    <div className="text-center py-12 text-muted-foreground">
                        Pilih indikator untuk mulai input manual data
                    </div>
                );
        }
    };

    return (
        <div className="space-y-6">
            <div className="space-y-2">
                <Label htmlFor="indicator-selector">Pilih Indikator</Label>
                <Select value={selectedIndicator} onValueChange={setSelectedIndicator}>
                    <SelectTrigger id="indicator-selector">
                        <SelectValue placeholder="Pilih indikator yang akan diinput..." />
                    </SelectTrigger>
                    <SelectContent>
                        {INDICATORS.map((indicator) => (
                            <SelectItem key={indicator.code} value={indicator.code}>
                                {indicator.label}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            <div className="mt-6">
                {renderForm()}
            </div>
        </div>
    );
}
