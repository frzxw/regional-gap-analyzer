"use client";

import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

// Daftar provinsi sesuai dengan data BPS
export const PROVINCES = [
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

interface ProvinceYearSelectorProps {
    provinceId: string;
    tahun: string;
    onProvinceChange: (value: string) => void;
    onTahunChange: (value: string) => void;
    disabled?: boolean;
}

export function ProvinceYearSelector({
    provinceId,
    tahun,
    onProvinceChange,
    onTahunChange,
    disabled = false,
}: ProvinceYearSelectorProps) {
    return (
        <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
                <Label htmlFor="province">Provinsi *</Label>
                <Select value={provinceId} onValueChange={onProvinceChange} disabled={disabled}>
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
                    onChange={(e) => onTahunChange(e.target.value)}
                    disabled={disabled}
                    placeholder="Contoh: 2024"
                />
            </div>
        </div>
    );
}
