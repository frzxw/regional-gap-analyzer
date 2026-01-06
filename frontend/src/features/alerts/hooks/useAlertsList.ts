'use client';

import { useQuery } from '@tanstack/react-query';
import type { Alert, AlertFilters, AlertsListResponse, AlertsSummary } from '@/utils/api';

const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

/**
 * Mock data for development
 */
const MOCK_ALERTS: Alert[] = [
    {
        id: '1',
        region_code: 'ID-PA',
        region_name: 'Papua',
        severity: 'critical',
        message: 'Skor kesenjangan wilayah sangat rendah (28.3). Diperlukan intervensi kebijakan segera.',
        created_at: new Date().toISOString(),
        status: 'active',
    },
    {
        id: '2',
        region_code: 'ID-PB',
        region_name: 'Papua Barat',
        severity: 'critical',
        message: 'Indikator infrastruktur turun 15% dari tahun sebelumnya.',
        created_at: new Date(Date.now() - 86400000).toISOString(),
        status: 'active',
    },
    {
        id: '3',
        region_code: 'ID-NT',
        region_name: 'Nusa Tenggara Timur',
        severity: 'warning',
        message: 'Skor pendidikan berada di bawah ambang batas minimum (35.2).',
        created_at: new Date(Date.now() - 172800000).toISOString(),
        status: 'active',
    },
    {
        id: '4',
        region_code: 'ID-MA',
        region_name: 'Maluku',
        severity: 'warning',
        message: 'Gap kesenjangan dengan rata-rata nasional meningkat 5 poin.',
        created_at: new Date(Date.now() - 259200000).toISOString(),
        status: 'acknowledged',
        acknowledged_at: new Date(Date.now() - 172800000).toISOString(),
        acknowledged_by: 'Admin',
    },
    {
        id: '5',
        region_code: 'ID-SS',
        region_name: 'Sumatera Selatan',
        severity: 'info',
        message: 'Skor ekonomi meningkat namun masih di bawah target SDG.',
        created_at: new Date(Date.now() - 345600000).toISOString(),
        status: 'resolved',
        resolved_at: new Date(Date.now() - 259200000).toISOString(),
        resolved_by: 'Analyst',
        resolution_notes: 'Target telah direvisi sesuai kondisi lokal.',
    },
];

const MOCK_SUMMARY: AlertsSummary = {
    total: 12,
    by_severity: {
        critical: 3,
        warning: 5,
        info: 4,
    },
    by_status: {
        active: 6,
        acknowledged: 3,
        resolved: 3,
    },
    by_region: [
        { region_code: 'ID-PA', region_name: 'Papua', count: 3 },
        { region_code: 'ID-PB', region_name: 'Papua Barat', count: 2 },
        { region_code: 'ID-NT', region_name: 'Nusa Tenggara Timur', count: 2 },
    ],
};

/**
 * Fetch alerts with filters
 */
async function fetchAlerts(
    filters: AlertFilters = {},
    skip = 0,
    limit = 20
): Promise<AlertsListResponse> {
    try {
        const params = new URLSearchParams();
        if (filters.region_code) params.set('region_code', filters.region_code);
        if (filters.severity) params.set('severity', filters.severity);
        if (filters.status) params.set('status', filters.status);
        params.set('skip', skip.toString());
        params.set('limit', limit.toString());

        const response = await fetch(`${API_BASE}/api/v1/alerts?${params}`);
        if (!response.ok) throw new Error('API not available');
        return await response.json();
    } catch {
        // Return filtered mock data
        let filteredAlerts = [...MOCK_ALERTS];
        if (filters.severity) {
            filteredAlerts = filteredAlerts.filter(a => a.severity === filters.severity);
        }
        if (filters.status) {
            filteredAlerts = filteredAlerts.filter(a => a.status === filters.status);
        }
        if (filters.region_code) {
            filteredAlerts = filteredAlerts.filter(a => a.region_code === filters.region_code);
        }
        return {
            items: filteredAlerts.slice(skip, skip + limit),
            total: filteredAlerts.length,
            skip,
            limit,
        };
    }
}

/**
 * Fetch alerts summary
 */
async function fetchAlertsSummary(): Promise<AlertsSummary> {
    try {
        const response = await fetch(`${API_BASE}/api/v1/alerts/summary`);
        if (!response.ok) throw new Error('API not available');
        return await response.json();
    } catch {
        return MOCK_SUMMARY;
    }
}

/**
 * Hook to fetch paginated alerts with filters
 */
export function useAlertsList(
    filters: AlertFilters = {},
    page = 1,
    pageSize = 20
) {
    const skip = (page - 1) * pageSize;

    return useQuery({
        queryKey: ['alerts-list', filters, page, pageSize],
        queryFn: () => fetchAlerts(filters, skip, pageSize),
        staleTime: 30000,
    });
}

/**
 * Hook to fetch alerts summary statistics
 */
export function useAlertsSummary() {
    return useQuery({
        queryKey: ['alerts-summary'],
        queryFn: fetchAlertsSummary,
        staleTime: 60000,
    });
}
