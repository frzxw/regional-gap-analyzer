/**
 * Severity Distribution Pie Chart Component
 */

'use client';

import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import type { ProvinceAnalysis } from '@/utils/unemploymentApi';

interface SeverityDistributionProps {
    provinces: ProvinceAnalysis[];
}

const SEVERITY_COLORS = {
    low: '#10b981',      // green
    medium: '#f59e0b',   // orange
    high: '#ef4444',     // red
    critical: '#991b1b', // dark red
};

const SEVERITY_LABELS = {
    low: 'Rendah',
    medium: 'Sedang',
    high: 'Tinggi',
    critical: 'Kritis',
};

export function SeverityDistribution({ provinces }: SeverityDistributionProps) {
    // Count provinces by severity
    const severityCounts = provinces.reduce((acc, province) => {
        const severity = province.score.severity;
        acc[severity] = (acc[severity] || 0) + 1;
        return acc;
    }, {} as Record<string, number>);

    // Convert to chart data format
    const chartData = Object.entries(severityCounts).map(([severity, count]) => ({
        name: SEVERITY_LABELS[severity as keyof typeof SEVERITY_LABELS] || severity,
        value: count,
        severity: severity,
    }));

    if (chartData.length === 0) {
        return (
            <div className="flex items-center justify-center h-64 text-gray-400">
                Tidak ada data
            </div>
        );
    }

    return (
        <div className="w-full h-64">
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, value, percent }) =>
                            `${name}: ${value} (${((percent ?? 0) * 100).toFixed(0)}%)`
                        }
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                    >
                        {chartData.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={SEVERITY_COLORS[entry.severity as keyof typeof SEVERITY_COLORS]}
                            />
                        ))}
                    </Pie>
                    <Tooltip
                        formatter={(value) => [`${value} provinsi`, 'Jumlah']}
                    />
                    <Legend />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}
