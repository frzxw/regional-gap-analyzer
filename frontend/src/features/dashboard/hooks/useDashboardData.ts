'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

interface DashboardData {
  regions: number;
  alerts: number;
  avgScore: number;
  gapIndex: number;
  rankings: Array<{
    region_code: string;
    region_name: string;
    score: number;
    rank: number;
  }>;
}

export function useDashboardData(year?: number) {
  return useQuery<DashboardData>({
    queryKey: ['dashboard', year],
    queryFn: async () => {
      // Fetch data from multiple endpoints
      const [regionsRes, alertsRes, scoresRes] = await Promise.all([
        api.getRegions(),
        fetch('/api/v1/alerts/active').then(r => r.json()).catch(() => ({ alerts: [] })),
        fetch(`/api/v1/scores/rankings${year ? `?year=${year}` : ''}`).then(r => r.json()).catch(() => ({ rankings: [] })),
      ]);

      const rankings = scoresRes.rankings || [];
      const scores = rankings.map((r: { score: number }) => r.score);
      const avgScore = scores.length > 0 
        ? scores.reduce((a: number, b: number) => a + b, 0) / scores.length 
        : 0;

      // Calculate gap index (coefficient of variation)
      const gapIndex = scores.length > 1
        ? Math.sqrt(
            scores.reduce((sum: number, s: number) => sum + Math.pow(s - avgScore, 2), 0) / scores.length
          ) / avgScore
        : 0;

      return {
        regions: regionsRes.length,
        alerts: (alertsRes.alerts || []).length,
        avgScore,
        gapIndex,
        rankings,
      };
    },
    staleTime: 60000, // 1 minute
  });
}
