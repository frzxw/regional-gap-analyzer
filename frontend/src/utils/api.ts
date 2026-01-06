/**
 * API Client for Regional Gap Analyzer
 * Centralized API utilities with typed functions
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

/**
 * Base fetch wrapper with error handling
 */
async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options?.headers,
        },
    });

    if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
}

// ============================================================================
// Health API
// ============================================================================

export interface HealthResponse {
    status: string;
}

export interface HealthDetailedResponse {
    status: string;
    database: string;
}

export const healthApi = {
    check: () => fetchApi<HealthResponse>('/health'),
    checkDetailed: () => fetchApi<HealthDetailedResponse>('/health/detailed'),
};

// ============================================================================
// Regions API
// ============================================================================

export interface Region {
    id: string;
    code: string;
    name: string;
    province: string;
}

export interface RegionsListResponse {
    regions: Region[];
    total: number;
}

export const regionsApi = {
    list: (page = 1, pageSize = 20) =>
        fetchApi<RegionsListResponse>(`/api/v1/regions?page=${page}&page_size=${pageSize}`),

    get: (regionId: string) =>
        fetchApi<Region>(`/api/v1/regions/${regionId}`),
};

// ============================================================================
// Scores API
// ============================================================================

export interface CategoryScore {
    economic: number;
    infrastructure: number;
    health: number;
    education: number;
}

export interface RegionScore {
    region_code: string;
    region_name: string;
    year: number;
    composite_score: number;
    category_scores: CategoryScore;
    rank: number;
    rank_delta?: number | null;
    gap_from_average: number;
}

export interface ScoreHistoryEntry {
    year: number;
    composite_score: number;
    category_scores?: CategoryScore;
    rank?: number;
}

export interface ScoreHistoryResponse {
    region_code: string;
    start_year: number;
    end_year: number;
    history: ScoreHistoryEntry[];
}

export interface RankingEntry {
    region_code: string;
    region_name: string;
    score: number;
    rank: number;
    rank_delta?: number | null;
}

export interface RankingsResponse {
    year: number;
    rankings: RankingEntry[];
}

export interface TopBottomResponse {
    year: number;
    top_performers: RankingEntry[];
    bottom_performers: RankingEntry[];
}

export interface GapAnalysis {
    year: number;
    national_average: number;
    std_deviation: number;
    coefficient_of_variation: number;
    max_score: number;
    min_score: number;
    gap_range: number;
}

export const scoresApi = {
    list: (year?: number, skip = 0, limit = 50) => {
        const params = new URLSearchParams();
        if (year) params.set('year', year.toString());
        params.set('skip', skip.toString());
        params.set('limit', limit.toString());
        return fetchApi<{ scores: RegionScore[] }>(`/api/v1/scores?${params}`);
    },

    rankings: (year?: number, limit = 38) => {
        const params = new URLSearchParams();
        if (year) params.set('year', year.toString());
        params.set('limit', limit.toString());
        return fetchApi<RankingsResponse>(`/api/v1/scores/rankings?${params}`);
    },

    topBottom: (year?: number, count = 5) => {
        const params = new URLSearchParams();
        if (year) params.set('year', year.toString());
        params.set('count', count.toString());
        return fetchApi<TopBottomResponse>(`/api/v1/scores/top-bottom?${params}`);
    },

    getRegionScore: (regionCode: string, year?: number) => {
        const params = year ? `?year=${year}` : '';
        return fetchApi<RegionScore>(`/api/v1/scores/region/${regionCode}${params}`);
    },

    getRegionHistory: (regionCode: string, startYear = 2015, endYear = 2024) =>
        fetchApi<ScoreHistoryResponse>(
            `/api/v1/scores/region/${regionCode}/history?start_year=${startYear}&end_year=${endYear}`
        ),

    gapAnalysis: (year?: number) => {
        const params = year ? `?year=${year}` : '';
        return fetchApi<GapAnalysis>(`/api/v1/scores/gap-analysis${params}`);
    },

    getAvailableYears: () =>
        fetchApi<{ years: number[] }>('/api/v1/scores/years'),

    recalculate: (year?: number, force = false) => {
        const params = new URLSearchParams();
        if (year) params.set('year', year.toString());
        params.set('force', force.toString());
        return fetchApi<{ message: string }>(`/api/v1/scores/recalculate?${params}`, {
            method: 'POST',
        });
    },
};

// ============================================================================
// Alerts API
// ============================================================================

export type AlertSeverity = 'critical' | 'warning' | 'info';
export type AlertStatus = 'active' | 'acknowledged' | 'resolved';

export interface Alert {
    id: string;
    region_code: string;
    region_name?: string;
    severity: AlertSeverity;
    message: string;
    created_at: string;
    status: AlertStatus;
    acknowledged_at?: string;
    acknowledged_by?: string;
    resolved_at?: string;
    resolved_by?: string;
    resolution_notes?: string;
}

export interface AlertsListResponse {
    items: Alert[];
    total: number;
    skip: number;
    limit: number;
}

export interface ActiveAlertsResponse {
    alerts: Alert[];
    count: number;
}

export interface AlertsSummary {
    total: number;
    by_severity: {
        critical: number;
        warning: number;
        info: number;
    };
    by_status: {
        active: number;
        acknowledged: number;
        resolved: number;
    };
    by_region: Array<{
        region_code: string;
        region_name: string;
        count: number;
    }>;
}

export interface AlertFilters {
    region_code?: string;
    severity?: AlertSeverity;
    status?: AlertStatus;
}

export const alertsApi = {
    list: (filters: AlertFilters = {}, skip = 0, limit = 50) => {
        const params = new URLSearchParams();
        if (filters.region_code) params.set('region_code', filters.region_code);
        if (filters.severity) params.set('severity', filters.severity);
        if (filters.status) params.set('status', filters.status);
        params.set('skip', skip.toString());
        params.set('limit', limit.toString());
        return fetchApi<AlertsListResponse>(`/api/v1/alerts?${params}`);
    },

    active: (regionCode?: string, limit = 20) => {
        const params = new URLSearchParams();
        if (regionCode) params.set('region_code', regionCode);
        params.set('limit', limit.toString());
        return fetchApi<ActiveAlertsResponse>(`/api/v1/alerts/active?${params}`);
    },

    summary: () => fetchApi<AlertsSummary>('/api/v1/alerts/summary'),

    get: (alertId: string) => fetchApi<Alert>(`/api/v1/alerts/${alertId}`),

    acknowledge: (alertId: string, acknowledgedBy: string, notes?: string) =>
        fetchApi<Alert>(`/api/v1/alerts/${alertId}/acknowledge`, {
            method: 'POST',
            body: JSON.stringify({ acknowledged_by: acknowledgedBy, notes }),
        }),

    resolve: (alertId: string, resolvedBy: string, resolutionNotes?: string) =>
        fetchApi<Alert>(`/api/v1/alerts/${alertId}/resolve`, {
            method: 'POST',
            body: JSON.stringify({ resolved_by: resolvedBy, resolution_notes: resolutionNotes }),
        }),

    generate: (year?: number) => {
        const params = year ? `?year=${year}` : '';
        return fetchApi<{ generated: number; updated: number; message: string }>(
            `/api/v1/alerts/generate${params}`,
            { method: 'POST' }
        );
    },
};

// ============================================================================
// Legacy API object (for backward compatibility)
// ============================================================================

export const api = {
    getRegions: async () => {
        try {
            const response = await regionsApi.list();
            return response.regions;
        } catch {
            return [];
        }
    },
};
