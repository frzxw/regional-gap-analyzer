'use client';

import { useQuery } from '@tanstack/react-query';
import type { RegionScore, ScoreHistoryResponse, GapAnalysis } from '../types';

const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

/**
 * Mock data for development (when backend is not available)
 */
const MOCK_REGION_SCORE: RegionScore = {
    region_code: 'ID-JK',
    region_name: 'DKI Jakarta',
    year: 2024,
    composite_score: 78.5,
    category_scores: {
        economic: 85.2,
        infrastructure: 82.1,
        health: 75.3,
        education: 68.9,
    },
    rank: 1,
    rank_delta: 0,
    gap_from_average: 23.5,
};

const MOCK_SCORE_HISTORY: ScoreHistoryResponse = {
    region_code: 'ID-JK',
    start_year: 2015,
    end_year: 2024,
    history: [
        { year: 2015, composite_score: 65.2, rank: 2 },
        { year: 2016, composite_score: 67.8, rank: 2 },
        { year: 2017, composite_score: 69.5, rank: 1 },
        { year: 2018, composite_score: 71.2, rank: 1 },
        { year: 2019, composite_score: 73.4, rank: 1 },
        { year: 2020, composite_score: 72.1, rank: 1 },
        { year: 2021, composite_score: 74.8, rank: 1 },
        { year: 2022, composite_score: 76.2, rank: 1 },
        { year: 2023, composite_score: 77.5, rank: 1 },
        { year: 2024, composite_score: 78.5, rank: 1 },
    ],
};

const MOCK_GAP_ANALYSIS: GapAnalysis = {
    year: 2024,
    national_average: 55.0,
    std_deviation: 15.2,
    coefficient_of_variation: 27.6,
    max_score: 78.5,
    min_score: 28.3,
    gap_range: 50.2,
};

/**
 * Fetch region score from API with fallback to mock data
 */
async function fetchRegionScore(regionCode: string, year?: number): Promise<RegionScore> {
    try {
        const params = year ? `?year=${year}` : '';
        const response = await fetch(`${API_BASE}/api/v1/scores/region/${regionCode}${params}`);
        if (!response.ok) throw new Error('API not available');
        return await response.json();
    } catch {
        // Return mock data with adjusted region code
        return { ...MOCK_REGION_SCORE, region_code: regionCode };
    }
}

/**
 * Fetch score history from API with fallback to mock data
 */
async function fetchScoreHistory(
    regionCode: string,
    startYear = 2015,
    endYear = 2024
): Promise<ScoreHistoryResponse> {
    try {
        const response = await fetch(
            `${API_BASE}/api/v1/scores/region/${regionCode}/history?start_year=${startYear}&end_year=${endYear}`
        );
        if (!response.ok) throw new Error('API not available');
        return await response.json();
    } catch {
        return { ...MOCK_SCORE_HISTORY, region_code: regionCode };
    }
}

/**
 * Fetch gap analysis from API with fallback to mock data
 */
async function fetchGapAnalysis(year?: number): Promise<GapAnalysis> {
    try {
        const params = year ? `?year=${year}` : '';
        const response = await fetch(`${API_BASE}/api/v1/scores/gap-analysis${params}`);
        if (!response.ok) throw new Error('API not available');
        return await response.json();
    } catch {
        return MOCK_GAP_ANALYSIS;
    }
}

/**
 * Hook to fetch region score details
 */
export function useRegionScore(regionCode: string, year?: number) {
    return useQuery({
        queryKey: ['region-score', regionCode, year],
        queryFn: () => fetchRegionScore(regionCode, year),
        staleTime: 60000, // 1 minute
        enabled: !!regionCode,
    });
}

/**
 * Hook to fetch region score history for trend chart
 */
export function useRegionScoreHistory(regionCode: string, startYear = 2015, endYear = 2024) {
    return useQuery({
        queryKey: ['region-history', regionCode, startYear, endYear],
        queryFn: () => fetchScoreHistory(regionCode, startYear, endYear),
        staleTime: 120000, // 2 minutes
        enabled: !!regionCode,
    });
}

/**
 * Hook to fetch gap analysis for comparison with national average
 */
export function useGapAnalysis(year?: number) {
    return useQuery({
        queryKey: ['gap-analysis', year],
        queryFn: () => fetchGapAnalysis(year),
        staleTime: 120000,
    });
}

/**
 * Combined hook for region detail page - fetches all needed data
 */
export function useRegionDetail(regionCode: string, year?: number) {
    const scoreQuery = useRegionScore(regionCode, year);
    const historyQuery = useRegionScoreHistory(regionCode);
    const gapQuery = useGapAnalysis(year);

    return {
        score: scoreQuery.data,
        history: historyQuery.data,
        gapAnalysis: gapQuery.data,
        isLoading: scoreQuery.isLoading || historyQuery.isLoading || gapQuery.isLoading,
        isError: scoreQuery.isError || historyQuery.isError || gapQuery.isError,
        error: scoreQuery.error || historyQuery.error || gapQuery.error,
        refetch: () => {
            scoreQuery.refetch();
            historyQuery.refetch();
            gapQuery.refetch();
        },
    };
}
