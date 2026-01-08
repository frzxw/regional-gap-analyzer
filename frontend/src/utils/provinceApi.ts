/**
 * Province API Client
 * API utilities for province-specific data and scoring
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
// Type Definitions
// ============================================================================

export interface CollectionScore {
    collection: string;
    display_name: string;
    raw_value: number;
    score: number;
    min_value: number;
    max_value: number;
    lower_is_better: boolean;
}

export interface ProvinceScore {
    province_id: string;
    province_name: string;
    year: number;
    composite_score: number;
    rank: number | null;
    collections_scored: number;
}

export interface ProvinceScoreDetailed extends ProvinceScore {
    collection_scores: Record<string, CollectionScore>;
}

export interface ScoreBreakdown {
    province_id: string;
    province_name: string | null;
    year: number;
    composite_score: number | null;
    rank: number | null;
    collections: CollectionScore[];
}

// ============================================================================
// Province API
// ============================================================================

export const provinceApi = {
    /**
     * Get province score with collection breakdown for a specific year
     */
    getProvinceScore: (provinceId: string, year: number) =>
        fetchApi<ProvinceScoreDetailed>(`/api/v1/year-scores/${year}/${provinceId}`),

    /**
     * Get detailed score breakdown with raw values
     */
    getScoreBreakdown: (provinceId: string, year: number) =>
        fetchApi<ScoreBreakdown>(`/api/v1/year-scores/${year}/${provinceId}/breakdown`),

    /**
     * Get all province scores for a specific year
     */
    getScoresForYear: (year: number) =>
        fetchApi<ProvinceScoreDetailed[]>(`/api/v1/year-scores/${year}`),

    /**
     * Get top performing provinces for a year
     */
    getTopProvinces: (year: number, count = 5) =>
        fetchApi<ProvinceScoreDetailed[]>(`/api/v1/year-scores/${year}/top?count=${count}`),

    /**
     * Get bottom performing provinces for a year
     */
    getBottomProvinces: (year: number, count = 5) =>
        fetchApi<ProvinceScoreDetailed[]>(`/api/v1/year-scores/${year}/bottom?count=${count}`),
};

