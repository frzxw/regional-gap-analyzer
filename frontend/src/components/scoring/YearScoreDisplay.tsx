"use client";

import { useEffect, useState } from "react";
import { yearScoringApi, type ProvinceScoreDetailed } from "@/utils/yearScoringApi";
import { useAppStore } from "@/lib/store";

interface YearScoreDisplayProps {
    provinceId?: string;
    showTopBottom?: boolean;
    topBottomCount?: number;
}

export function YearScoreDisplay({
    provinceId,
    showTopBottom = false,
    topBottomCount = 5,
}: YearScoreDisplayProps) {
    const [scores, setScores] = useState<ProvinceScoreDetailed[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Use selectedYear from app store to sync with map
    const { selectedYear } = useAppStore();

    // Fetch scores
    useEffect(() => {
        const fetchScores = async () => {
            setLoading(true);
            setError(null);

            try {
                if (provinceId) {
                    // Fetch single province score
                    const data = await yearScoringApi.getProvinceScore(selectedYear, provinceId);
                    setScores([data]);
                } else if (showTopBottom) {
                    // Fetch top and bottom performers
                    const [topData, bottomData] = await Promise.all([
                        yearScoringApi.getTopProvinces(selectedYear, topBottomCount),
                        yearScoringApi.getBottomProvinces(selectedYear, topBottomCount),
                    ]);
                    setScores([...topData, ...bottomData]);
                } else {
                    // Fetch all scores
                    const data = await yearScoringApi.getScoresForYear(selectedYear);
                    setScores(data);
                }
            } catch (err) {
                setError(err instanceof Error ? err.message : "Failed to fetch scores");
            } finally {
                setLoading(false);
            }
        };

        if (selectedYear) {
            fetchScores();
        }
    }, [selectedYear, provinceId, showTopBottom, topBottomCount]);

    const getScoreColor = (score: number) => {
        if (score >= 80) return "text-green-600 bg-green-50";
        if (score >= 60) return "text-blue-600 bg-blue-50";
        if (score >= 40) return "text-yellow-600 bg-yellow-50";
        return "text-red-600 bg-red-50";
    };

    const getRankBadgeColor = (rank: number) => {
        if (rank === 1) return "bg-yellow-500 text-white";
        if (rank === 2) return "bg-gray-400 text-white";
        if (rank === 3) return "bg-orange-600 text-white";
        return "bg-gray-200 text-gray-700";
    };

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


    return (
        <div className="space-y-4">
            {/* Scores Display */}
            {scores.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                    Tidak ada data untuk tahun {selectedYear}
                </div>
            ) : (
                <div className="space-y-3">
                    {scores.map((score) => (
                        <div
                            key={score.province_id}
                            className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow"
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    {/* Rank Badge */}
                                    {score.rank && (
                                        <div
                                            className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${getRankBadgeColor(
                                                score.rank
                                            )}`}
                                        >
                                            {score.rank}
                                        </div>
                                    )}

                                    {/* Province Info */}
                                    <div>
                                        <h3 className="font-semibold text-gray-900">
                                            {score.province_name}
                                        </h3>
                                        <p className="text-xs text-gray-500">
                                            {score.collections_scored} indikator di-score
                                        </p>
                                    </div>
                                </div>

                                {/* Composite Score */}
                                <div className="text-right">
                                    <div
                                        className={`text-2xl font-bold px-3 py-1 rounded-lg ${getScoreColor(
                                            score.composite_score
                                        )}`}
                                    >
                                        {score.composite_score.toFixed(1)}
                                    </div>
                                    <p className="text-xs text-gray-500 mt-1">Skor Komposit</p>
                                </div>
                            </div>

                            {/* Collection Scores */}
                            {score.collection_scores && (
                                <div className="mt-4 pt-4 border-t border-gray-100">
                                    <p className="text-xs font-medium text-gray-600 mb-2">
                                        Breakdown per Indikator:
                                    </p>
                                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                                        {Object.entries(score.collection_scores).map(([name, value]) => (
                                            <div
                                                key={name}
                                                className="bg-gray-50 rounded px-2 py-1 text-xs"
                                            >
                                                <span className="text-gray-600">{name}:</span>{" "}
                                                <span className="font-semibold text-gray-900">
                                                    {value.toFixed(1)}
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
