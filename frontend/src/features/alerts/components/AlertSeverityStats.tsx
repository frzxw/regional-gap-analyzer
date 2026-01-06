'use client';

import React from 'react';
import type { AlertsSummary } from '@/utils/api';

interface AlertSeverityStatsProps {
    summary: AlertsSummary | undefined;
    loading?: boolean;
}

interface StatCardProps {
    label: string;
    count: number;
    color: string;
    icon: React.ReactNode;
    loading?: boolean;
}

function StatCard({ label, count, color, icon, loading }: StatCardProps) {
    if (loading) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-4 animate-pulse">
                <div className="h-4 w-16 bg-gray-200 dark:bg-gray-700 rounded mb-2" />
                <div className="h-8 w-12 bg-gray-200 dark:bg-gray-700 rounded" />
            </div>
        );
    }

    return (
        <div className={`bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-4 ${color}`}>
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{count}</p>
                </div>
                <div className="text-2xl opacity-50">{icon}</div>
            </div>
        </div>
    );
}

export function AlertSeverityStats({
    summary,
    loading = false,
}: AlertSeverityStatsProps) {
    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
                label="Total Alerts"
                count={summary?.total || 0}
                color="border-l-4 border-l-blue-500"
                icon="📊"
                loading={loading}
            />
            <StatCard
                label="Critical"
                count={summary?.by_severity.critical || 0}
                color="border-l-4 border-l-red-500"
                icon="🔴"
                loading={loading}
            />
            <StatCard
                label="Warning"
                count={summary?.by_severity.warning || 0}
                color="border-l-4 border-l-yellow-500"
                icon="🟡"
                loading={loading}
            />
            <StatCard
                label="Info"
                count={summary?.by_severity.info || 0}
                color="border-l-4 border-l-blue-400"
                icon="🔵"
                loading={loading}
            />
        </div>
    );
}
