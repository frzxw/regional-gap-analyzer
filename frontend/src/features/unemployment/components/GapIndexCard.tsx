/**
 * Gap Index Card Component
 */

'use client';

import React from 'react';

interface GapIndexCardProps {
    gapIndex: number;
    nationalAverage: number;
    criticalProvinces: number;
    highRiskProvinces: number;
}

export function GapIndexCard({
    gapIndex,
    nationalAverage,
    criticalProvinces,
    highRiskProvinces
}: GapIndexCardProps) {
    // Determine gap level
    const getGapLevel = (index: number) => {
        if (index > 0.3) return { label: 'Tinggi', color: 'text-red-600 dark:text-red-400', bg: 'bg-red-100 dark:bg-red-900/20' };
        if (index > 0.2) return { label: 'Sedang', color: 'text-orange-600 dark:text-orange-400', bg: 'bg-orange-100 dark:bg-orange-900/20' };
        return { label: 'Rendah', color: 'text-green-600 dark:text-green-400', bg: 'bg-green-100 dark:bg-green-900/20' };
    };

    const gapLevel = getGapLevel(gapIndex);
    const gapPercentage = Math.min(gapIndex * 100, 100);

    return (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Gap Index */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                        Indeks Kesenjangan
                    </h3>
                    <span className={`text-xs px-2 py-1 rounded-full ${gapLevel.bg} ${gapLevel.color} font-medium`}>
                        {gapLevel.label}
                    </span>
                </div>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                    {gapIndex.toFixed(3)}
                </p>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                        className={`h-2 rounded-full transition-all ${gapIndex > 0.3 ? 'bg-red-500' :
                                gapIndex > 0.2 ? 'bg-orange-500' :
                                    'bg-green-500'
                            }`}
                        style={{ width: `${gapPercentage}%` }}
                    />
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                    0 = tidak ada kesenjangan
                </p>
            </div>

            {/* National Average */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                    Rata-rata Nasional
                </h3>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                    {nationalAverage.toFixed(2)}%
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                    Tingkat pengangguran
                </p>
            </div>

            {/* Critical Provinces */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                    Provinsi Kritis
                </h3>
                <p className="text-3xl font-bold text-red-600 dark:text-red-400 mb-2">
                    {criticalProvinces}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                    Pengangguran {'>'} 10%
                </p>
            </div>

            {/* High Risk Provinces */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                    Provinsi Risiko Tinggi
                </h3>
                <p className="text-3xl font-bold text-orange-600 dark:text-orange-400 mb-2">
                    {highRiskProvinces}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                    Pengangguran 7-10%
                </p>
            </div>
        </div>
    );
}
