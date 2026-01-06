'use client';

import React from 'react';
import { getScoreBgColor, getScoreLabel } from '../types';

interface RegionHeaderProps {
    regionCode: string;
    regionName: string;
    score: number;
    rank: number;
    year: number;
    loading?: boolean;
}

export function RegionHeader({
    regionCode,
    regionName,
    score,
    rank,
    year,
    loading = false,
}: RegionHeaderProps) {
    if (loading) {
        return (
            <div className="animate-pulse">
                <div className="h-8 w-64 bg-gray-200 dark:bg-gray-700 rounded mb-2" />
                <div className="h-4 w-32 bg-gray-200 dark:bg-gray-700 rounded" />
            </div>
        );
    }

    return (
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
                    {regionName}
                </h1>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    Kode: <span className="font-mono">{regionCode}</span> • Data tahun {year}
                </p>
            </div>

            <div className="flex items-center gap-4">
                {/* Score Badge */}
                <div className={`px-4 py-2 rounded-lg text-white ${getScoreBgColor(score)}`}>
                    <div className="text-2xl font-bold">{score.toFixed(1)}</div>
                    <div className="text-xs opacity-90">{getScoreLabel(score)}</div>
                </div>

                {/* Rank Badge */}
                <div className="px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-800">
                    <div className="text-2xl font-bold text-gray-900 dark:text-white">
                        #{rank}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Peringkat</div>
                </div>
            </div>
        </div>
    );
}
