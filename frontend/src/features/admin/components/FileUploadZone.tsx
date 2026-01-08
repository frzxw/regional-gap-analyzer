"use client";

import { useCallback, useState } from "react";
import { Upload, FileText, X } from "lucide-react";

interface FileUploadZoneProps {
    onFileSelect: (file: File) => void;
    disabled?: boolean;
    acceptedTypes?: string[];
}

export function FileUploadZone({
    onFileSelect,
    disabled = false,
    acceptedTypes = [".csv"], // Only CSV for indicator-specific imports
}: FileUploadZoneProps) {
    const [isDragging, setIsDragging] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (!disabled) {
            setIsDragging(true);
        }
    }, [disabled]);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback(
        (e: React.DragEvent) => {
            e.preventDefault();
            e.stopPropagation();
            setIsDragging(false);

            if (disabled) return;

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const file = files[0];
                setSelectedFile(file);
                onFileSelect(file);
            }
        },
        [disabled, onFileSelect]
    );

    const handleFileInput = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            const files = e.target.files;
            if (files && files.length > 0) {
                const file = files[0];
                setSelectedFile(file);
                onFileSelect(file);
            }
        },
        [onFileSelect]
    );

    const clearFile = useCallback(() => {
        setSelectedFile(null);
    }, []);

    const formatFileSize = (bytes: number): string => {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    };

    return (
        <div className="space-y-3">
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`
          relative border-2 border-dashed rounded-xl p-8
          transition-all duration-200 ease-in-out
          ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer hover:border-primary/60"}
          ${isDragging
                        ? "border-primary bg-primary/5 scale-[1.02]"
                        : "border-muted-foreground/25 bg-muted/30"
                    }
        `}
            >
                <input
                    type="file"
                    accept={acceptedTypes.join(",")}
                    onChange={handleFileInput}
                    disabled={disabled}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
                />
                <div className="flex flex-col items-center justify-center text-center space-y-3">
                    <div
                        className={`
              p-4 rounded-full transition-colors
              ${isDragging ? "bg-primary/20 text-primary" : "bg-muted text-muted-foreground"}
            `}
                    >
                        <Upload className="w-8 h-8" />
                    </div>
                    <div>
                        <p className="font-medium text-foreground">
                            {isDragging ? "Drop file here..." : "Drag & drop file or click to browse"}
                        </p>
                        <p className="text-sm text-muted-foreground mt-1">
                            Supported: CSV
                        </p>
                    </div>
                </div>
            </div>

            {selectedFile && (
                <div className="flex items-center gap-3 p-3 bg-muted/50 rounded-lg border border-muted-foreground/10">
                    <FileText className="w-5 h-5 text-primary" />
                    <div className="flex-1 min-w-0">
                        <p className="font-medium text-sm truncate">{selectedFile.name}</p>
                        <p className="text-xs text-muted-foreground">
                            {formatFileSize(selectedFile.size)}
                        </p>
                    </div>
                    <button
                        type="button"
                        onClick={clearFile}
                        className="p-1.5 hover:bg-destructive/10 rounded-md transition-colors"
                    >
                        <X className="w-4 h-4 text-destructive" />
                    </button>
                </div>
            )}
        </div>
    );
}
