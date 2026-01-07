'use client';

import React from 'react';
import { CATEGORY_CONFIG, type CategoryScore, type CategoryKey } from '../types';

interface IndicatorBreakdownProps {
    categoryScores: CategoryScore;
    loading?: boolean;
}

/**
 * Category breakdown component showing score bars for each indicator category
 */
export function IndicatorBreakdown({
    categoryScores,
    loading = false,
}: IndicatorBreakdownProps) {
    if (loading) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                <div className="h-5 w-40 bg-gray-200 dark:bg-gray-700 rounded mb-6 animate-pulse" />
                <div className="space-y-6">
                    {[1, 2, 3, 4].map(i => (
                        <div key={i} className="animate-pulse">
                            <div className="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded mb-2" />
                            <div className="h-3 w-full bg-gray-100 dark:bg-gray-700 rounded" />
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    const categories = Object.entries(CATEGORY_CONFIG) as [CategoryKey, typeof CATEGORY_CONFIG[CategoryKey]][];

    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                Breakdown per Kategori
            </h3>

            <div className="space-y-5">
                {categories.map(([key, config]) => {
                    const score = categoryScores[key];
                    const weightPercent = config.weight * 100;

                    return (
                        <div key={key}>
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <span
                                        className="w-3 h-3 rounded-full"
                                        style={{ backgroundColor: config.color }}
                                    />
                                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                        {config.label}
                                    </span>
                                    <span className="text-xs text-gray-400 dark:text-gray-500">
                                        (bobot {weightPercent}%)
                                    </span>
                                </div>
                                <span className="text-sm font-bold text-gray-900 dark:text-white">
                                    {score.toFixed(1)}
                                </span>
                            </div>

                            {/* Progress bar */}
                            <div className="relative h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                                <div
                                    className="absolute inset-y-0 left-0 rounded-full transition-all duration-500"
                                    style={{
                                        width: `${Math.min(score, 100)}%`,
                                        backgroundColor: config.color,
                                    }}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Category legend */}
            <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-700">
                <p className="text-xs text-gray-500 dark:text-gray-400">
                    Skor dihitung berdasarkan metodologi normalisasi min-max (0-100).
                    Semakin tinggi skor, semakin baik kondisi wilayah pada kategori tersebut.
                </p>
            </div>
        </div>
    );
}
