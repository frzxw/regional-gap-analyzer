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

interface DataItem {
    province_id: string;
    tahun: number;
    value?: number;
    province_name?: string;
    indicator_code?: string;
    source?: string;
}

interface EditDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    data: DataItem | null;
    onSave: (data: DataItem) => Promise<void>;
}

export function EditDialog({ open, onOpenChange, data, onSave }: EditDialogProps) {
    const [value, setValue] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (data) {
            setValue(data.value?.toString() || "");
        }
    }, [data]);

    const handleSave = async () => {
        if (!data) return;

        const numValue = parseFloat(value);
        if (value.trim() === "" || isNaN(numValue)) {
            alert("Nilai harus berupa angka yang valid");
            return;
        }

        setLoading(true);
        try {
            await onSave({
                ...data,
                value: numValue,
            });
            onOpenChange(false);
        } catch (error) {
            console.error("Failed to save:", error);
            alert(error instanceof Error ? error.message : "Gagal menyimpan data");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Edit Data</DialogTitle>
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
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="value" className="text-right">
                            Nilai
                        </Label>
                        <Input
                            id="value"
                            type="number"
                            value={value}
                            onChange={(e) => setValue(e.target.value)}
                            className="col-span-3"
                        />
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
