/**
 * Province Score Bar Chart Component
 */

'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { ProvinceAnalysis } from '@/utils/unemploymentApi';

interface ProvinceScoreChartProps {
    provinces: ProvinceAnalysis[];
    maxProvinces?: number;
}

const SEVERITY_COLORS = {
    low: '#10b981',      // green
    medium: '#f59e0b',   // orange  
    high: '#ef4444',     // red
    critical: '#991b1b', // dark red
};

export function ProvinceScoreChart({ provinces, maxProvinces = 15 }: ProvinceScoreChartProps) {
    // Sort by rank (best first) and limit
    const topProvinces = [...provinces]
        .sort((a, b) => (a.rank || 999) - (b.rank || 999))
        .slice(0, maxProvinces);

    const chartData = topProvinces.map(province => ({
        name: province.province_name,
        score: province.score.score,
        rate: province.unemployment_rate,
        severity: province.score.severity,
        rank: province.rank,
    }));

    if (chartData.length === 0) {
        return (
            <div className="flex items-center justify-center h-96 text-gray-400">
                Tidak ada data
            </div>
        );
    }

    return (
        <div className="w-full h-96">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart
                    data={chartData}
                    layout="vertical"
                    margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" domain={[0, 100]} />
                    <YAxis
                        dataKey="name"
                        type="category"
                        width={90}
                        tick={{ fontSize: 12 }}
                    />
                    <Tooltip
                        content={({ active, payload }) => {
                            if (active && payload && payload.length) {
                                const data = payload[0].payload;
                                return (
                                    <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
                                        <p className="font-semibold text-gray-900 dark:text-white">
                                            {data.name}
                                        </p>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">
                                            Peringkat: #{data.rank}
                                        </p>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">
                                            Score: {data.score}/100
                                        </p>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">
                                            Tingkat Pengangguran: {data.rate}%
                                        </p>
                                    </div>
                                );
                            }
                            return null;
                        }}
                    />
                    <Bar dataKey="score" radius={[0, 4, 4, 0]}>
                        {chartData.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={SEVERITY_COLORS[entry.severity as keyof typeof SEVERITY_COLORS]}
                            />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
