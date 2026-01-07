/**
 * React hooks for unemployment analysis data
 */

'use client';

import { useQuery } from '@tanstack/react-query';
import { unemploymentAnalysisApi } from '@/utils/unemploymentApi';

/**
 * Hook to fetch regional gap analysis for a specific year
 */
export function useRegionalGapAnalysis(year: number) {
    return useQuery({
        queryKey: ['unemployment-regional-gap', year],
        queryFn: () => unemploymentAnalysisApi.getRegionalGap(year),
        staleTime: 5 * 60 * 1000, // 5 minutes
        enabled: year >= 2020 && year <= 2030,
    });
}

/**
 * Hook to fetch year-over-year comparison
 */
export function useYearComparison(yearFrom: number, yearTo: number) {
    return useQuery({
        queryKey: ['unemployment-comparison', yearFrom, yearTo],
        queryFn: () => unemploymentAnalysisApi.compareYears(yearFrom, yearTo),
        staleTime: 5 * 60 * 1000,
        enabled: yearFrom < yearTo && yearFrom >= 2020 && yearTo <= 2030,
    });
}

/**
 * Hook to fetch critical alerts for a specific year
 */
export function useCriticalAlerts(year: number) {
    return useQuery({
        queryKey: ['unemployment-critical-alerts', year],
        queryFn: () => unemploymentAnalysisApi.getCriticalAlerts(year),
        staleTime: 5 * 60 * 1000,
        enabled: year >= 2020 && year <= 2030,
    });
}
