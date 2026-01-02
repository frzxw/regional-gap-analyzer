'use client';

import { useQuery } from '@tanstack/react-query';

interface RankingEntry {
  region_code: string;
  region_name?: string;
  score: number;
  rank: number;
  rank_delta?: number | null;
}

interface RankingsResponse {
  year: number;
  rankings: RankingEntry[];
}

export function useRankings(year?: number, limit: number = 38) {
  return useQuery<RankingsResponse>({
    queryKey: ['rankings', year, limit],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (year) params.set('year', year.toString());
      params.set('limit', limit.toString());

      const response = await fetch(`/api/v1/scores/rankings?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch rankings');
      }
      return response.json();
    },
    staleTime: 60000, // 1 minute
  });
}

export function useTopBottomRegions(year?: number, count: number = 5) {
  return useQuery({
    queryKey: ['top-bottom', year, count],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (year) params.set('year', year.toString());
      params.set('count', count.toString());

      const response = await fetch(`/api/v1/scores/top-bottom?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch top/bottom regions');
      }
      return response.json();
    },
    staleTime: 60000,
  });
}
