'use client';

import React from 'react';

interface KPICardProps {
    title: string;
    value: string | number;
    subtitle?: string;
    icon?: React.ReactNode;
    trend?: 'up' | 'down' | 'neutral';
    trendValue?: string;
    loading?: boolean;
}

function KPICard({ title, value, subtitle, icon, trend, trendValue, loading }: KPICardProps) {
    if (loading) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-5 animate-pulse">
                <div className="h-4 w-20 bg-gray-200 dark:bg-gray-700 rounded mb-3" />
                <div className="h-8 w-24 bg-gray-200 dark:bg-gray-700 rounded mb-2" />
                <div className="h-3 w-16 bg-gray-200 dark:bg-gray-700 rounded" />
            </div>
        );
    }

    const trendColors = {
        up: 'text-green-600 dark:text-green-400',
        down: 'text-red-600 dark:text-red-400',
        neutral: 'text-gray-500 dark:text-gray-400',
    };

    const trendIcons = {
        up: '↑',
        down: '↓',
        neutral: '–',
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-5 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</p>
                {icon && <span className="text-gray-400 dark:text-gray-500">{icon}</span>}
            </div>
            <div className="mt-2 flex items-baseline gap-2">
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {typeof value === 'number' ? value.toFixed(1) : value}
                </p>
                {trend && trendValue && (
                    <span className={`text-sm font-medium ${trendColors[trend]}`}>
                        {trendIcons[trend]} {trendValue}
                    </span>
                )}
            </div>
            {subtitle && (
                <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">{subtitle}</p>
            )}
        </div>
    );
}

interface RegionKPICardsProps {
    compositeScore: number;
    rank: number;
    totalRegions?: number;
    gapFromAverage: number;
    nationalAverage: number;
    rankDelta?: number | null;
    loading?: boolean;
}

export function RegionKPICards({
    compositeScore,
    rank,
    totalRegions = 38,
    gapFromAverage,
    nationalAverage,
    rankDelta,
    loading = false,
}: RegionKPICardsProps) {
    const gapTrend = gapFromAverage >= 0 ? 'up' : 'down';
    const rankTrend = rankDelta
        ? rankDelta > 0 ? 'up' : rankDelta < 0 ? 'down' : 'neutral'
        : 'neutral';

    return (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <KPICard
                title="Skor Komposit"
                value={compositeScore}
                subtitle="Skala 0-100"
                loading={loading}
                icon={
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                }
            />

            <KPICard
                title="Peringkat Nasional"
                value={`#${rank}`}
                subtitle={`dari ${totalRegions} provinsi`}
                trend={rankTrend}
                trendValue={rankDelta ? `${Math.abs(rankDelta)} posisi` : undefined}
                loading={loading}
                icon={
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                    </svg>
                }
            />

            <KPICard
                title="Gap vs Rata-rata"
                value={gapFromAverage >= 0 ? `+${gapFromAverage.toFixed(1)}` : gapFromAverage.toFixed(1)}
                subtitle={gapFromAverage >= 0 ? 'Di atas rata-rata' : 'Di bawah rata-rata'}
                trend={gapTrend}
                loading={loading}
                icon={
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                }
            />

            <KPICard
                title="Rata-rata Nasional"
                value={nationalAverage}
                subtitle="Benchmark nasional"
                loading={loading}
                icon={
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" />
                    </svg>
                }
            />
        </div>
    );
}
