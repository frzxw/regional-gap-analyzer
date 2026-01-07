/**
 * Critical Alerts Panel Component
 */

'use client';

import React from 'react';
import type { ProvinceAnalysis } from '@/utils/unemploymentApi';

interface CriticalAlertsPanelProps {
    provinces: ProvinceAnalysis[];
}

const SEVERITY_ICONS = {
    critical: '🔴',
    high: '🟠',
    medium: '🟡',
    low: '🟢',
};

export function CriticalAlertsPanel({ provinces }: CriticalAlertsPanelProps) {
    // Filter provinces with high or critical alerts
    const criticalProvinces = provinces.filter(p =>
        p.alerts.some(alert => alert.severity === 'critical' || alert.severity === 'high')
    );

    if (criticalProvinces.length === 0) {
        return (
            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-xl p-6">
                <div className="flex items-center gap-3">
                    <span className="text-3xl">✅</span>
                    <div>
                        <h3 className="font-semibold text-green-900 dark:text-green-100">
                            Tidak Ada Peringatan Kritis
                        </h3>
                        <p className="text-sm text-green-700 dark:text-green-300">
                            Semua provinsi dalam kondisi baik
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-3">
            {criticalProvinces.map((province) => {
                const criticalAlerts = province.alerts.filter(
                    alert => alert.severity === 'critical' || alert.severity === 'high'
                );

                return (
                    <div
                        key={province.province_id}
                        className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                        <div className="flex items-start gap-3">
                            <span className="text-2xl flex-shrink-0">
                                {SEVERITY_ICONS[province.score.severity]}
                            </span>
                            <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between gap-2 mb-2">
                                    <h4 className="font-semibold text-gray-900 dark:text-white truncate">
                                        {province.province_name}
                                    </h4>
                                    <span className="text-sm text-gray-500 dark:text-gray-400 flex-shrink-0">
                                        #{province.rank}
                                    </span>
                                </div>

                                <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mb-3">
                                    <span>Tingkat: {province.unemployment_rate}%</span>
                                    <span>Score: {province.score.score}/100</span>
                                    <span className={`font-medium ${province.score.severity === 'critical' ? 'text-red-600 dark:text-red-400' :
                                            province.score.severity === 'high' ? 'text-orange-600 dark:text-orange-400' :
                                                'text-yellow-600 dark:text-yellow-400'
                                        }`}>
                                        {province.score.category}
                                    </span>
                                </div>

                                <div className="space-y-2">
                                    {criticalAlerts.map((alert, idx) => (
                                        <div key={idx} className="text-sm">
                                            <p className="text-gray-700 dark:text-gray-300 font-medium">
                                                {alert.message}
                                            </p>
                                            {alert.recommendation && (
                                                <p className="text-gray-600 dark:text-gray-400 mt-1 pl-4 border-l-2 border-blue-500">
                                                    💡 {alert.recommendation}
                                                </p>
                                            )}
                                        </div>
                                    ))}
                                </div>

                                {province.trend && province.trend.direction === 'worsening' && (
                                    <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                                        <p className="text-sm text-red-600 dark:text-red-400">
                                            📈 Meningkat {Math.abs(province.trend.change_absolute).toFixed(1)} poin dari tahun {province.trend.year_from}
                                        </p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
