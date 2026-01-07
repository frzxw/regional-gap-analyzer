'use client';

import React from 'react';
import { CATEGORY_CONFIG, type CategoryScore, type CategoryKey } from '../types';

interface RegionComparisonProps {
    regionName: string;
    regionScores: CategoryScore;
    nationalAverage: number;
    compositeScore: number;
    loading?: boolean;
}

/**
 * Comparison component showing region vs national average across categories
 */
export function RegionComparison({
    regionName,
    regionScores,
    nationalAverage,
    compositeScore,
    loading = false,
}: RegionComparisonProps) {
    if (loading) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                <div className="h-5 w-48 bg-gray-200 dark:bg-gray-700 rounded mb-6 animate-pulse" />
                <div className="h-48 bg-gray-100 dark:bg-gray-700 rounded animate-pulse" />
            </div>
        );
    }

    // Estimate national category averages (in real app, these would come from API)
    const nationalCategoryAverages: CategoryScore = {
        economic: nationalAverage * 0.95,
        infrastructure: nationalAverage * 0.98,
        health: nationalAverage * 1.02,
        education: nationalAverage * 1.05,
    };

    const categories = Object.entries(CATEGORY_CONFIG) as [CategoryKey, typeof CATEGORY_CONFIG[CategoryKey]][];

    // Calculate bar chart dimensions
    const maxScore = 100;
    const barWidth = 40;
    const gap = 60;
    const chartWidth = categories.length * (barWidth * 2 + gap) + gap;
    const chartHeight = 200;
    const padding = { top: 20, bottom: 40, left: 10, right: 10 };

    const getBarHeight = (score: number) =>
        (score / maxScore) * (chartHeight - padding.top - padding.bottom);

    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Perbandingan dengan Rata-rata Nasional
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
                {regionName} (Skor: {compositeScore.toFixed(1)}) vs Rata-rata Nasional ({nationalAverage.toFixed(1)})
            </p>

            <div className="overflow-x-auto">
                <svg
                    viewBox={`0 0 ${chartWidth} ${chartHeight}`}
                    className="w-full min-w-[400px]"
                    preserveAspectRatio="xMidYMid meet"
                >
                    {/* Grid lines */}
                    {[0, 25, 50, 75, 100].map(val => (
                        <line
                            key={val}
                            x1={padding.left}
                            y1={chartHeight - padding.bottom - getBarHeight(val)}
                            x2={chartWidth - padding.right}
                            y2={chartHeight - padding.bottom - getBarHeight(val)}
                            stroke="currentColor"
                            className="text-gray-100 dark:text-gray-700"
                            strokeDasharray="4"
                        />
                    ))}

                    {/* Bars for each category */}
                    {categories.map(([key, config], i) => {
                        const regionScore = regionScores[key];
                        const nationalScore = nationalCategoryAverages[key];
                        const x = gap + i * (barWidth * 2 + gap);

                        return (
                            <g key={key}>
                                {/* Region bar */}
                                <rect
                                    x={x}
                                    y={chartHeight - padding.bottom - getBarHeight(regionScore)}
                                    width={barWidth}
                                    height={getBarHeight(regionScore)}
                                    fill={config.color}
                                    rx={4}
                                />

                                {/* National bar */}
                                <rect
                                    x={x + barWidth + 4}
                                    y={chartHeight - padding.bottom - getBarHeight(nationalScore)}
                                    width={barWidth}
                                    height={getBarHeight(nationalScore)}
                                    fill="#9ca3af"
                                    rx={4}
                                />

                                {/* Category label */}
                                <text
                                    x={x + barWidth + 2}
                                    y={chartHeight - 10}
                                    textAnchor="middle"
                                    className="text-xs fill-gray-600 dark:fill-gray-400"
                                >
                                    {config.label.slice(0, 4)}
                                </text>

                                {/* Score labels */}
                                <text
                                    x={x + barWidth / 2}
                                    y={chartHeight - padding.bottom - getBarHeight(regionScore) - 5}
                                    textAnchor="middle"
                                    className="text-xs fill-gray-700 dark:fill-gray-300 font-medium"
                                >
                                    {regionScore.toFixed(0)}
                                </text>
                            </g>
                        );
                    })}
                </svg>
            </div>

            {/* Legend */}
            <div className="flex items-center justify-center gap-6 mt-4 text-sm">
                <div className="flex items-center gap-2">
                    <span className="w-4 h-3 bg-blue-500 rounded" />
                    <span className="text-gray-600 dark:text-gray-400">{regionName}</span>
                </div>
                <div className="flex items-center gap-2">
                    <span className="w-4 h-3 bg-gray-400 rounded" />
                    <span className="text-gray-600 dark:text-gray-400">Rata-rata Nasional</span>
                </div>
            </div>
        </div>
    );
}
