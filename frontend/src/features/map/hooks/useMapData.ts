'use client';

import { useQuery } from '@tanstack/react-query';

interface ChoroplethData {
  type: string;
  metadata: {
    year: number;
    metric: string;
    total_regions: number;
  };
  features: Array<{
    type: string;
    properties: {
      code: string;
      name: string;
      year?: number;
      composite_score?: number;
      rank?: number;
      rank_delta?: number;
    };
    geometry: object;
  }>;
}

export function useMapData(year?: number, metric: string = 'composite_score') {
  return useQuery<ChoroplethData>({
    queryKey: ['choropleth', year, metric],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (year) params.set('year', year.toString());
      params.set('metric', metric);

      const response = await fetch(`/api/v1/geo/choropleth?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch map data');
      }
      return response.json();
    },
    staleTime: 300000, // 5 minutes
  });
}
