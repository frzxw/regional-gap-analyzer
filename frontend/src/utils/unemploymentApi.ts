/**
 * API Client for Unemployment Analysis
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

// ============================================================================
// Types
// ============================================================================

export type SeverityLevel = 'low' | 'medium' | 'high' | 'critical';
export type TrendDirection = 'improving' | 'stable' | 'worsening';

export interface UnemploymentScore {
    rate: number;
    score: number;
    category: string;
    severity: SeverityLevel;
}

export interface TrendAnalysis {
    year_from: number;
    year_to: number;
    rate_from: number;
    rate_to: number;
    change_absolute: number;
    change_percentage: number;
    direction: TrendDirection;
    is_significant: boolean;
}

export interface Alert {
    type: string;
    severity: SeverityLevel;
    message: string;
    recommendation?: string;
}

export interface ProvinceAnalysis {
    province_id: string;
    province_name: string;
    year: number;
    unemployment_rate: number;
    score: UnemploymentScore;
    trend?: TrendAnalysis;
    alerts: Alert[];
    rank?: number;
    percentile?: number;
}

export interface RegionalGapAnalysis {
    year: number;
    national_average: number;
    provinces: ProvinceAnalysis[];
    total_provinces: number;
    critical_provinces: number;
    high_risk_provinces: number;
    gap_index: number;
    summary: string;
    status: string;
}

export interface ComparisonAnalysis {
    year_from: number;
    year_to: number;
    provinces_improved: number;
    provinces_worsened: number;
    provinces_stable: number;
    biggest_improvement?: ProvinceAnalysis;
    biggest_decline?: ProvinceAnalysis;
    status: string;
}

export interface CriticalAlertsResponse {
    year: number;
    total_critical: number;
    provinces: Array<{
        province_id: string;
        province_name: string;
        unemployment_rate: number;
        score: number;
        severity: SeverityLevel;
        alerts: Alert[];
        rank: number;
    }>;
    status: string;
}

// ============================================================================
// API Functions
// ============================================================================

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

export const unemploymentAnalysisApi = {
    /**
     * Get regional gap analysis for a specific year
     */
    getRegionalGap: (year: number) =>
        fetchApi<RegionalGapAnalysis>(`/api/v1/analysis/unemployment/regional-gap/${year}`),

    /**
     * Compare unemployment trends between two years
     */
    compareYears: (yearFrom: number, yearTo: number) =>
        fetchApi<ComparisonAnalysis>(`/api/v1/analysis/unemployment/compare?year_from=${yearFrom}&year_to=${yearTo}`),

    /**
     * Get critical alerts for a specific year
     */
    getCriticalAlerts: (year: number) =>
        fetchApi<CriticalAlertsResponse>(`/api/v1/analysis/unemployment/alerts/${year}`),
};
