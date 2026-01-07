'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRegionalGapAnalysis } from '@/features/unemployment/hooks/useUnemploymentAnalysis';
import { SeverityDistribution } from '@/features/unemployment/components/SeverityDistribution';
import { ProvinceScoreChart } from '@/features/unemployment/components/ProvinceScoreChart';
import { CriticalAlertsPanel } from '@/features/unemployment/components/CriticalAlertsPanel';
import { GapIndexCard } from '@/features/unemployment/components/GapIndexCard';

export default function AlertsPage() {
    const [selectedYear, setSelectedYear] = useState(2024);

    const { data: analysisData, isLoading, isError, refetch } = useRegionalGapAnalysis(selectedYear);

    // Available years
    const availableYears = [2020, 2021, 2022, 2023, 2024, 2025];

    // Error state
    if (isError) {
        return (
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
                <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                    <Link
                        href="/dashboard"
                        className="inline-flex items-center text-sm text-blue-600 dark:text-blue-400 hover:underline mb-6"
                    >
                        ← Kembali ke Dashboard
                    </Link>

                    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-8 text-center">
                        <svg
                            className="w-12 h-12 mx-auto text-red-500 mb-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                            />
                        </svg>
                        <h2 className="text-xl font-semibold text-red-800 dark:text-red-200 mb-2">
                            Gagal Memuat Data Analisis
                        </h2>
                        <p className="text-red-600 dark:text-red-300 mb-4">
                            Terjadi kesalahan saat mengambil data analisis ketimpangan
                        </p>
                        <button
                            onClick={() => refetch()}
                            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                        >
                            Coba Lagi
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {/* Header */}
            <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-100 dark:border-gray-700">
                <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                        <div>
                            <Link
                                href="/dashboard"
                                className="inline-flex items-center text-sm text-blue-600 dark:text-blue-400 hover:underline mb-2"
                            >
                                ← Kembali ke Dashboard
                            </Link>
                            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
                                Analisis Ketimpangan Pengangguran
                            </h1>
                            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                                Monitoring dan analisis tingkat pengangguran regional dengan scoring dan alerts
                            </p>
                        </div>

                        {/* Year Selector */}
                        <div className="flex items-center gap-3">
                            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                Tahun:
                            </label>
                            <select
                                value={selectedYear}
                                onChange={(e) => setSelectedYear(Number(e.target.value))}
                                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                {availableYears.map(year => (
                                    <option key={year} value={year}>{year}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                {isLoading ? (
                    <div className="flex items-center justify-center h-96">
                        <div className="text-center">
                            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                            <p className="text-gray-600 dark:text-gray-400">Memuat data analisis...</p>
                        </div>
                    </div>
                ) : analysisData ? (
                    <div className="space-y-8">
                        {/* Summary Cards */}
                        <section>
                            <GapIndexCard
                                gapIndex={analysisData.gap_index}
                                nationalAverage={analysisData.national_average}
                                criticalProvinces={analysisData.critical_provinces}
                                highRiskProvinces={analysisData.high_risk_provinces}
                            />
                        </section>

                        {/* Summary Text */}
                        <section className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4">
                            <p className="text-sm text-blue-900 dark:text-blue-100">
                                📊 {analysisData.summary}
                            </p>
                        </section>

                        {/* Charts Row */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            {/* Severity Distribution */}
                            <section className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                                <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                    Distribusi Tingkat Keparahan
                                </h2>
                                <SeverityDistribution provinces={analysisData.provinces} />
                            </section>

                            {/* Province Rankings */}
                            <section className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                                <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                    Peringkat Provinsi (Top 15)
                                </h2>
                                <ProvinceScoreChart provinces={analysisData.provinces} maxProvinces={15} />
                            </section>
                        </div>

                        {/* Critical Alerts */}
                        <section className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                Peringatan Kritis & Prioritas Tinggi
                            </h2>
                            <CriticalAlertsPanel provinces={analysisData.provinces} />
                        </section>

                        {/* Detailed Province Table */}
                        <section className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
                            <div className="p-6 border-b border-gray-100 dark:border-gray-700">
                                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                                    Detail Semua Provinsi
                                </h2>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead className="bg-gray-50 dark:bg-gray-700">
                                        <tr>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                Peringkat
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                Provinsi
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                Tingkat Pengangguran
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                Score
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                Kategori
                                            </th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                                Trend
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                                        {analysisData.provinces.map((province) => (
                                            <tr key={province.province_id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                                    #{province.rank}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                                    {province.province_name}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                                    {province.unemployment_rate}%
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                                    {province.score.score}/100
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${province.score.severity === 'critical' ? 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400' :
                                                            province.score.severity === 'high' ? 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400' :
                                                                province.score.severity === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400' :
                                                                    'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
                                                        }`}>
                                                        {province.score.category}
                                                    </span>
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                                    {province.trend ? (
                                                        <span className={`flex items-center gap-1 ${province.trend.direction === 'improving' ? 'text-green-600 dark:text-green-400' :
                                                                province.trend.direction === 'worsening' ? 'text-red-600 dark:text-red-400' :
                                                                    'text-gray-600 dark:text-gray-400'
                                                            }`}>
                                                            {province.trend.direction === 'improving' ? '↓' :
                                                                province.trend.direction === 'worsening' ? '↑' : '→'}
                                                            {Math.abs(province.trend.change_absolute).toFixed(1)}%
                                                        </span>
                                                    ) : (
                                                        <span className="text-gray-400">-</span>
                                                    )}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </section>
                    </div>
                ) : null}
            </main>

            {/* Footer */}
            <footer className="bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 mt-12">
                <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
                    <p className="text-center text-sm text-gray-500 dark:text-gray-400">
                        Regional Gap Analyzer — Analisis Ketimpangan Regional Indonesia
                    </p>
                </div>
            </footer>
        </div>
    );
}
