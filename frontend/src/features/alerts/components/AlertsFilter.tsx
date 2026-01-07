'use client';

import React from 'react';
import type { AlertSeverity, AlertStatus } from '@/utils/api';

interface AlertsFilterProps {
    severity: AlertSeverity | '';
    status: AlertStatus | '';
    onSeverityChange: (severity: AlertSeverity | '') => void;
    onStatusChange: (status: AlertStatus | '') => void;
    onClear: () => void;
}

export function AlertsFilter({
    severity,
    status,
    onSeverityChange,
    onStatusChange,
    onClear,
}: AlertsFilterProps) {
    const hasFilters = severity !== '' || status !== '';

    return (
        <div className="flex flex-wrap items-center gap-4">
            {/* Severity filter */}
            <div className="flex items-center gap-2">
                <label htmlFor="severity" className="text-sm text-gray-600 dark:text-gray-400">
                    Severity:
                </label>
                <select
                    id="severity"
                    value={severity}
                    onChange={(e) => onSeverityChange(e.target.value as AlertSeverity | '')}
                    className="px-3 py-1.5 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                    <option value="">Semua</option>
                    <option value="critical">🔴 Critical</option>
                    <option value="warning">🟡 Warning</option>
                    <option value="info">🔵 Info</option>
                </select>
            </div>

            {/* Status filter */}
            <div className="flex items-center gap-2">
                <label htmlFor="status" className="text-sm text-gray-600 dark:text-gray-400">
                    Status:
                </label>
                <select
                    id="status"
                    value={status}
                    onChange={(e) => onStatusChange(e.target.value as AlertStatus | '')}
                    className="px-3 py-1.5 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                    <option value="">Semua</option>
                    <option value="active">Active</option>
                    <option value="acknowledged">Acknowledged</option>
                    <option value="resolved">Resolved</option>
                </select>
            </div>

            {/* Clear button */}
            {hasFilters && (
                <button
                    onClick={onClear}
                    className="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
                >
                    ✕ Hapus filter
                </button>
            )}
        </div>
    );
}
