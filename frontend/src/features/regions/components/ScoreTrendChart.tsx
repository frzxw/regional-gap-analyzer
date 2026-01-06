'use client';

import React from 'react';
import type { ScoreHistoryEntry } from '../types';

interface ScoreTrendChartProps {
    history: ScoreHistoryEntry[];
    nationalAverage?: number;
    loading?: boolean;
}

/**
 * Simple SVG-based line chart for score trend
 * Using native SVG to avoid adding heavy chart library dependency
 */
export function ScoreTrendChart({
    history,
    nationalAverage = 55,
    loading = false,
}: ScoreTrendChartProps) {
    if (loading) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                <div className="h-4 w-32 bg-gray-200 dark:bg-gray-700 rounded mb-4 animate-pulse" />
                <div className="h-64 bg-gray-100 dark:bg-gray-700 rounded animate-pulse" />
            </div>
        );
    }

    if (!history.length) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Tren Skor Kesenjangan
                </h3>
                <div className="h-64 flex items-center justify-center text-gray-500 dark:text-gray-400">
                    Tidak ada data historis tersedia
                </div>
            </div>
        );
    }

    // Chart dimensions
    const width = 600;
    const height = 250;
    const padding = { top: 20, right: 30, bottom: 40, left: 50 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    // Calculate scales
    const years = history.map(h => h.year);
    const scores = history.map(h => h.composite_score);
    const minYear = Math.min(...years);
    const maxYear = Math.max(...years);
    const minScore = Math.min(0, ...scores, nationalAverage - 10);
    const maxScore = Math.max(100, ...scores, nationalAverage + 10);

    const xScale = (year: number) =>
        padding.left + ((year - minYear) / (maxYear - minYear)) * chartWidth;
    const yScale = (score: number) =>
        padding.top + chartHeight - ((score - minScore) / (maxScore - minScore)) * chartHeight;

    // Generate path for score line
    const linePath = history
        .map((h, i) => `${i === 0 ? 'M' : 'L'} ${xScale(h.year)} ${yScale(h.composite_score)}`)
        .join(' ');

    // Generate national average line
    const avgY = yScale(nationalAverage);

    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Tren Skor Kesenjangan
            </h3>

            <div className="overflow-x-auto">
                <svg
                    viewBox={`0 0 ${width} ${height}`}
                    className="w-full min-w-[500px]"
                    preserveAspectRatio="xMidYMid meet"
                >
                    {/* Grid lines */}
                    <g className="text-gray-200 dark:text-gray-700">
                        {[0, 25, 50, 75, 100].map(score => (
                            <line
                                key={score}
                                x1={padding.left}
                                y1={yScale(score)}
                                x2={width - padding.right}
                                y2={yScale(score)}
                                stroke="currentColor"
                                strokeDasharray="4"
                            />
                        ))}
                    </g>

                    {/* National average line */}
                    <line
                        x1={padding.left}
                        y1={avgY}
                        x2={width - padding.right}
                        y2={avgY}
                        stroke="#f59e0b"
                        strokeWidth={2}
                        strokeDasharray="6"
                    />
                    <text
                        x={width - padding.right + 5}
                        y={avgY + 4}
                        className="text-xs fill-amber-600 dark:fill-amber-400"
                    >
                        Avg
                    </text>

                    {/* Score line */}
                    <path
                        d={linePath}
                        fill="none"
                        stroke="#3b82f6"
                        strokeWidth={3}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />

                    {/* Data points */}
                    {history.map((h, i) => (
                        <g key={i}>
                            <circle
                                cx={xScale(h.year)}
                                cy={yScale(h.composite_score)}
                                r={5}
                                fill="#3b82f6"
                                stroke="white"
                                strokeWidth={2}
                            />
                            {/* Tooltip on hover - simple version */}
                            <title>{`${h.year}: ${h.composite_score.toFixed(1)}`}</title>
                        </g>
                    ))}

                    {/* Y-axis labels */}
                    {[0, 25, 50, 75, 100].map(score => (
                        <text
                            key={score}
                            x={padding.left - 10}
                            y={yScale(score) + 4}
                            textAnchor="end"
                            className="text-xs fill-gray-500 dark:fill-gray-400"
                        >
                            {score}
                        </text>
                    ))}

                    {/* X-axis labels */}
                    {years.filter((_, i) => i % 2 === 0 || years.length <= 5).map(year => (
                        <text
                            key={year}
                            x={xScale(year)}
                            y={height - padding.bottom + 20}
                            textAnchor="middle"
                            className="text-xs fill-gray-500 dark:fill-gray-400"
                        >
                            {year}
                        </text>
                    ))}
                </svg>
            </div>

            {/* Legend */}
            <div className="flex items-center gap-6 mt-4 text-sm">
                <div className="flex items-center gap-2">
                    <span className="w-4 h-0.5 bg-blue-500 rounded" />
                    <span className="text-gray-600 dark:text-gray-400">Skor Provinsi</span>
                </div>
                <div className="flex items-center gap-2">
                    <span className="w-4 h-0.5 bg-amber-500 rounded" style={{ borderStyle: 'dashed' }} />
                    <span className="text-gray-600 dark:text-gray-400">Rata-rata Nasional</span>
                </div>
            </div>
        </div>
    );
}
