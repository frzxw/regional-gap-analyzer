'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import type { AlertSeverity, AlertStatus, AlertFilters } from '@/utils/api';
import { useAlertsList } from '@/features/alerts/hooks/useAlertsList';
import { useAlertsSummary } from '@/features/alerts/hooks/useAlerts';
import { AlertsTable } from '@/features/alerts/components/AlertsTable';
import { AlertsFilter } from '@/features/alerts/components/AlertsFilter';
import { AlertSeverityStats } from '@/features/alerts/components/AlertSeverityStats';

export default function AlertsPage() {
    const [severity, setSeverity] = useState<AlertSeverity | ''>('');
    const [status, setStatus] = useState<AlertStatus | ''>('');
    const [page, setPage] = useState(1);
    const pageSize = 20;

    const filters: AlertFilters = {};
    if (severity) filters.severity = severity;
    if (status) filters.status = status;

    const { data: alertsData, isLoading: alertsLoading, isError: alertsError, refetch } = useAlertsList(filters, page, pageSize);
    const { data: summaryData, isLoading: summaryLoading } = useAlertsSummary();

    const handleClearFilters = () => {
        setSeverity('');
        setStatus('');
        setPage(1);
    };

    const totalPages = alertsData ? Math.ceil(alertsData.total / pageSize) : 1;

    // Error state
    if (alertsError) {
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
                            Gagal Memuat Peringatan
                        </h2>
                        <p className="text-red-600 dark:text-red-300 mb-4">
                            Terjadi kesalahan saat mengambil data peringatan
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
                                Monitoring Peringatan
                            </h1>
                            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                                Pantau peringatan kesenjangan wilayah dan ambil tindakan yang diperlukan
                            </p>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                {/* Summary Stats */}
                <section className="mb-8">
                    <AlertSeverityStats
                        summary={summaryData}
                        loading={summaryLoading}
                    />
                </section>

                {/* Filters */}
                <section className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-4 mb-6">
                    <AlertsFilter
                        severity={severity}
                        status={status}
                        onSeverityChange={(val) => { setSeverity(val); setPage(1); }}
                        onStatusChange={(val) => { setStatus(val); setPage(1); }}
                        onClear={handleClearFilters}
                    />
                </section>

                {/* Alerts Table */}
                <section className="mb-6">
                    <AlertsTable
                        alerts={alertsData?.items || []}
                        loading={alertsLoading}
                        onAcknowledge={(alertId) => {
                            console.log('Acknowledge:', alertId);
                            // TODO: Implement acknowledge mutation
                        }}
                        onResolve={(alertId) => {
                            console.log('Resolve:', alertId);
                            // TODO: Implement resolve mutation
                        }}
                    />
                </section>

                {/* Pagination */}
                {totalPages > 1 && (
                    <section className="flex items-center justify-between bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-4">
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                            Menampilkan {((page - 1) * pageSize) + 1} - {Math.min(page * pageSize, alertsData?.total || 0)} dari {alertsData?.total || 0} peringatan
                        </p>
                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => setPage(p => Math.max(1, p - 1))}
                                disabled={page === 1}
                                className="px-3 py-1.5 text-sm rounded-lg border border-gray-200 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                            >
                                ← Sebelumnya
                            </button>
                            <span className="text-sm text-gray-600 dark:text-gray-400">
                                Halaman {page} dari {totalPages}
                            </span>
                            <button
                                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                                disabled={page === totalPages}
                                className="px-3 py-1.5 text-sm rounded-lg border border-gray-200 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                            >
                                Selanjutnya →
                            </button>
                        </div>
                    </section>
                )}

                {/* Quick Links */}
                <section className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6 mt-8">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                        Tautan Cepat
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                        Klik pada nama wilayah di tabel untuk melihat detail analisis provinsi tersebut.
                    </p>
                    <div className="flex flex-wrap gap-3">
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
