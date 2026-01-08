"use client";

import { useState, useCallback } from "react";
import { importsApi, ImportResult, ImportHistoryItem, CSVImportResponse } from "@/lib/api";

export type UploadStatus = "idle" | "uploading" | "success" | "error";

interface UseImportReturn {
    // State
    status: UploadStatus;
    error: string | null;
    result: ImportResult | null;
    history: ImportHistoryItem[];
    historyLoading: boolean;

    // Actions
    uploadFile: (file: File, indicatorCode: string, year: number) => Promise<void>;
    fetchHistory: () => Promise<void>;
    rollbackImport: (sourceId: string) => Promise<void>;
    reset: () => void;
}

/**
 * Convert CSVImportResponse to ImportResult for UI compatibility
 */
function convertToImportResult(csvResponse: CSVImportResponse): ImportResult {
    return {
        success: csvResponse.success_count > 0,
        message: csvResponse.message,
        records_processed: csvResponse.total_rows,
        records_imported: csvResponse.success_count,
        duration_seconds: 0, // Not available from CSV import endpoint
    };
}

export function useImport(): UseImportReturn {
    const [status, setStatus] = useState<UploadStatus>("idle");
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<ImportResult | null>(null);
    const [history, setHistory] = useState<ImportHistoryItem[]>([]);
    const [historyLoading, setHistoryLoading] = useState(false);

    const uploadFile = useCallback(
        async (file: File, indicatorCode: string, year: number) => {
            setStatus("uploading");
            setError(null);
            setResult(null);

            try {
                const response = await importsApi.uploadFile(file, indicatorCode, year);
                const convertedResult = convertToImportResult(response);
                setResult(convertedResult);
                setStatus("success");
            } catch (err) {
                setError(err instanceof Error ? err.message : "Upload failed");
                setStatus("error");
            }
        },
        []
    );

    const fetchHistory = useCallback(async () => {
        setHistoryLoading(true);
        try {
            const response = await importsApi.getHistory();
            setHistory(response.imports || []);
        } catch (err) {
            console.error("Failed to fetch history:", err);
        } finally {
            setHistoryLoading(false);
        }
    }, []);

    const rollbackImport = useCallback(async (sourceId: string) => {
        try {
            await importsApi.rollback(sourceId);
            // Refresh history after rollback
            const response = await importsApi.getHistory();
            setHistory(response.imports || []);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Rollback failed");
        }
    }, []);

    const reset = useCallback(() => {
        setStatus("idle");
        setError(null);
        setResult(null);
    }, []);

    return {
        status,
        error,
        result,
        history,
        historyLoading,
        uploadFile,
        fetchHistory,
        rollbackImport,
        reset,
    };
}
