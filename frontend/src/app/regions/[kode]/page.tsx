'use client';

import React from 'react';
import Link from 'next/link';
import { useRegionDetail } from '@/features/regions/hooks/useRegionDetail';
import { RegionHeader } from '@/features/regions/components/RegionHeader';
import { RegionKPICards } from '@/features/regions/components/RegionKPICards';
import { ScoreTrendChart } from '@/features/regions/components/ScoreTrendChart';
import { IndicatorBreakdown } from '@/features/regions/components/IndicatorBreakdown';
import { RegionComparison } from '@/features/regions/components/RegionComparison';

interface PageProps {
    params: Promise<{ kode: string }>;
}

export default function RegionDetailPage({ params }: PageProps) {
    const [regionCode, setRegionCode] = React.useState<string>('');

    React.useEffect(() => {
        params.then(p => setRegionCode(p.kode.toUpperCase()));
    }, [params]);

    const { score, history, gapAnalysis, isLoading, isError, refetch } = useRegionDetail(regionCode);

    // Error state
    if (isError && !isLoading) {
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
                            Gagal Memuat Data
                        </h2>
                        <p className="text-red-600 dark:text-red-300 mb-4">
                            Terjadi kesalahan saat mengambil data untuk kode wilayah: {regionCode}
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

    // Empty state (region not found)
    if (!isLoading && !score) {
        return (
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
                <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                    <Link
                        href="/dashboard"
                        className="inline-flex items-center text-sm text-blue-600 dark:text-blue-400 hover:underline mb-6"
                    >
                        ← Kembali ke Dashboard
                    </Link>

                    <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-8 text-center">
                        <svg
                            className="w-12 h-12 mx-auto text-gray-400 mb-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                        <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-200 mb-2">
                            Wilayah Tidak Ditemukan
                        </h2>
                        <p className="text-gray-500 dark:text-gray-400 mb-4">
                            Tidak ada data untuk kode wilayah: {regionCode}
                        </p>
                        <Link
                            href="/dashboard"
                            className="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                        >
                            Lihat Semua Wilayah
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {/* Header */}
            <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-100 dark:border-gray-700">
                <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
                    <Link
                        href="/dashboard"
                        className="inline-flex items-center text-sm text-blue-600 dark:text-blue-400 hover:underline mb-4"
                    >
                        ← Kembali ke Dashboard
                    </Link>

                    <RegionHeader
                        regionCode={score?.region_code || regionCode}
                        regionName={score?.region_name || 'Memuat...'}
                        score={score?.composite_score || 0}
                        rank={score?.rank || 0}
                        year={score?.year || new Date().getFullYear()}
                        loading={isLoading}
                    />
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                {/* KPI Cards */}
                <section className="mb-8">
                    <RegionKPICards
                        compositeScore={score?.composite_score || 0}
                        rank={score?.rank || 0}
                        gapFromAverage={score?.gap_from_average || 0}
                        nationalAverage={gapAnalysis?.national_average || 55}
                        rankDelta={score?.rank_delta}
                        loading={isLoading}
                    />
                </section>

                {/* Charts Row */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Score Trend Chart */}
                    <ScoreTrendChart
                        history={history?.history || []}
                        nationalAverage={gapAnalysis?.national_average}
                        loading={isLoading}
                    />

                    {/* Indicator Breakdown */}
                    <IndicatorBreakdown
                        categoryScores={score?.category_scores || {
                            economic: 0,
                            infrastructure: 0,
                            health: 0,
                            education: 0,
                        }}
                        loading={isLoading}
                    />
                </div>

                {/* Comparison Chart */}
                <section className="mb-8">
                    <RegionComparison
                        regionName={score?.region_name || regionCode}
                        regionScores={score?.category_scores || {
                            economic: 0,
                            infrastructure: 0,
                            health: 0,
                            education: 0,
                        }}
                        nationalAverage={gapAnalysis?.national_average || 55}
                        compositeScore={score?.composite_score || 0}
                        loading={isLoading}
                    />
                </section>

                {/* Quick Links */}
                <section className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                        Tautan Cepat
                    </h3>
                    <div className="flex flex-wrap gap-3">
                        <Link
                            href="/alerts"
                            className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-sm"
                        >
                            Lihat Peringatan
                        </Link>
                        <Link
                            href="/dashboard"
                            className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-sm"
                        >
                            Dashboard Nasional
                        </Link>
                    </div>
                </section>
            </main>

            {/* Footer */}
            <footer className="bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 mt-12">
                <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
                    <p className="text-center text-sm text-gray-500 dark:text-gray-400">
                        Regional Gap Analyzer — Data Demo. Bukan untuk penggunaan resmi.
                    </p>
                </div>
            </footer>
        </div>
    );
}
