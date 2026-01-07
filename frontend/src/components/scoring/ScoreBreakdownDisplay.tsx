"use client";

import { useEffect, useState } from "react";
import { yearScoringApi, type ScoreBreakdown } from "@/utils/yearScoringApi";

interface ScoreBreakdownDisplayProps {
    provinceId: string;
    year: number;
}

export function ScoreBreakdownDisplay({
    provinceId,
    year,
}: ScoreBreakdownDisplayProps) {
    const [breakdown, setBreakdown] = useState<ScoreBreakdown | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchBreakdown = async () => {
            setLoading(true);
            setError(null);

            try {
                const data = await yearScoringApi.getScoreBreakdown(year, provinceId);
                setBreakdown(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : "Failed to fetch breakdown");
            } finally {
                setLoading(false);
            }
        };

        fetchBreakdown();
    }, [provinceId, year]);

    if (loading) {
        return (
            <div className="flex items-center justify-center p-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-800 text-sm">{error}</p>
            </div>
        );
    }

    if (!breakdown) {
        return (
            <div className="text-center py-8 text-gray-500">
                Tidak ada data breakdown
            </div>
        );
    }

    const getScoreColor = (score: number) => {
        if (score >= 80) return "bg-green-500";
        if (score >= 60) return "bg-blue-500";
        if (score >= 40) return "bg-yellow-500";
        return "bg-red-500";
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    {breakdown.province_name}
                </h2>
                <div className="flex items-center gap-6">
                    <div>
                        <p className="text-sm text-gray-500">Tahun</p>
                        <p className="text-lg font-semibold text-gray-900">{breakdown.year}</p>
                    </div>
                    {breakdown.composite_score && (
                        <div>
                            <p className="text-sm text-gray-500">Skor Komposit</p>
                            <p className="text-3xl font-bold text-blue-600">
                                {breakdown.composite_score.toFixed(1)}
                            </p>
                        </div>
                    )}
                    {breakdown.rank && (
                        <div>
                            <p className="text-sm text-gray-500">Peringkat</p>
                            <p className="text-lg font-semibold text-gray-900">#{breakdown.rank}</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Collection Breakdown */}
            <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Breakdown per Indikator
                </h3>
                <div className="space-y-4">
                    {breakdown.collections
                        .sort((a, b) => b.score - a.score)
                        .map((collection) => (
                            <div
                                key={collection.collection}
                                className="border border-gray-200 rounded-lg p-4"
                            >
                                <div className="flex items-start justify-between mb-3">
                                    <div className="flex-1">
                                        <h4 className="font-semibold text-gray-900">
                                            {collection.display_name}
                                        </h4>
                                        <p className="text-xs text-gray-500 mt-1">
                                            {collection.lower_is_better
                                                ? "Lebih rendah lebih baik"
                                                : "Lebih tinggi lebih baik"}
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-2xl font-bold text-gray-900">
                                            {collection.score.toFixed(1)}
                                        </div>
                                        <p className="text-xs text-gray-500">Skor</p>
                                    </div>
                                </div>

                                {/* Progress Bar */}
                                <div className="mb-3">
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className={`h-2 rounded-full ${getScoreColor(collection.score)}`}
                                            style={{ width: `${collection.score}%` }}
                                        ></div>
                                    </div>
                                </div>

                                {/* Raw Value and Range */}
                                <div className="grid grid-cols-3 gap-4 text-sm">
                                    <div>
                                        <p className="text-gray-500">Nilai</p>
                                        <p className="font-semibold text-gray-900">
                                            {collection.raw_value.toLocaleString("id-ID", {
                                                maximumFractionDigits: 2,
                                            })}
                                        </p>
                                    </div>
                                    <div>
                                        <p className="text-gray-500">Min</p>
                                        <p className="font-semibold text-gray-900">
                                            {collection.min_value.toLocaleString("id-ID", {
                                                maximumFractionDigits: 2,
                                            })}
                                        </p>
                                    </div>
                                    <div>
                                        <p className="text-gray-500">Max</p>
                                        <p className="font-semibold text-gray-900">
                                            {collection.max_value.toLocaleString("id-ID", {
                                                maximumFractionDigits: 2,
                                            })}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                </div>
            </div>
        </div>
    );
}
