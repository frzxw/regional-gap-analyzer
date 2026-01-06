'use client';

import React from 'react';
import Link from 'next/link';
import type { Alert } from '@/utils/api';
import { AlertBadge } from './AlertBadge';

interface AlertsTableProps {
    alerts: Alert[];
    loading?: boolean;
    onAcknowledge?: (alertId: string) => void;
    onResolve?: (alertId: string) => void;
}

export function AlertsTable({
    alerts,
    loading = false,
    onAcknowledge,
    onResolve,
}: AlertsTableProps) {
    if (loading) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
                <div className="p-4 space-y-3">
                    {Array.from({ length: 5 }).map((_, i) => (
                        <div key={i} className="h-16 bg-gray-100 dark:bg-gray-700 rounded animate-pulse" />
                    ))}
                </div>
            </div>
        );
    }

    if (alerts.length === 0) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-8 text-center">
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
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                </svg>
                <p className="text-gray-500 dark:text-gray-400">
                    Tidak ada peringatan yang sesuai dengan filter
                </p>
            </div>
        );
    }

    const getStatusBadge = (status: Alert['status']) => {
        switch (status) {
            case 'active':
                return (
                    <span className="px-2 py-1 text-xs rounded-full bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400">
                        Active
                    </span>
                );
            case 'acknowledged':
                return (
                    <span className="px-2 py-1 text-xs rounded-full bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400">
                        Acknowledged
                    </span>
                );
            case 'resolved':
                return (
                    <span className="px-2 py-1 text-xs rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400">
                        Resolved
                    </span>
                );
        }
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead className="bg-gray-50 dark:bg-gray-700/50 border-b border-gray-100 dark:border-gray-700">
                        <tr>
                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                Severity
                            </th>
                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                Wilayah
                            </th>
                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                Pesan
                            </th>
                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                Waktu
                            </th>
                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                Status
                            </th>
                            <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                Aksi
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                        {alerts.map((alert) => (
                            <tr key={alert.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/30">
                                <td className="px-4 py-4 whitespace-nowrap">
                                    <AlertBadge severity={alert.severity} />
                                </td>
                                <td className="px-4 py-4 whitespace-nowrap">
                                    <Link
                                        href={`/regions/${alert.region_code}`}
                                        className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
                                    >
                                        {alert.region_name || alert.region_code}
                                    </Link>
                                    <div className="text-xs text-gray-500 dark:text-gray-400">
                                        {alert.region_code}
                                    </div>
                                </td>
                                <td className="px-4 py-4">
                                    <p className="text-sm text-gray-700 dark:text-gray-300 max-w-md truncate">
                                        {alert.message}
                                    </p>
                                </td>
                                <td className="px-4 py-4 whitespace-nowrap">
                                    <p className="text-sm text-gray-600 dark:text-gray-400">
                                        {new Date(alert.created_at).toLocaleDateString('id-ID')}
                                    </p>
                                    <p className="text-xs text-gray-400 dark:text-gray-500">
                                        {new Date(alert.created_at).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}
                                    </p>
                                </td>
                                <td className="px-4 py-4 whitespace-nowrap">
                                    {getStatusBadge(alert.status)}
                                </td>
                                <td className="px-4 py-4 whitespace-nowrap text-right">
                                    <div className="flex items-center justify-end gap-2">
                                        {alert.status === 'active' && onAcknowledge && (
                                            <button
                                                onClick={() => onAcknowledge(alert.id)}
                                                className="px-3 py-1 text-xs bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 rounded hover:bg-yellow-200 dark:hover:bg-yellow-900/50 transition-colors"
                                            >
                                                Acknowledge
                                            </button>
                                        )}
                                        {(alert.status === 'active' || alert.status === 'acknowledged') && onResolve && (
                                            <button
                                                onClick={() => onResolve(alert.id)}
                                                className="px-3 py-1 text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded hover:bg-green-200 dark:hover:bg-green-900/50 transition-colors"
                                            >
                                                Resolve
                                            </button>
                                        )}
                                        <Link
                                            href={`/regions/${alert.region_code}`}
                                            className="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                                        >
                                            Detail
                                        </Link>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
