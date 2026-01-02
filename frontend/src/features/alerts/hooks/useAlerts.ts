'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

interface Alert {
  id: string;
  region_code: string;
  severity: 'critical' | 'warning' | 'info';
  message: string;
  created_at: string;
  acknowledged?: boolean;
}

export function useAlerts(regionCode?: string) {
  return useQuery<Alert[]>({
    queryKey: ['alerts', regionCode],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (regionCode) params.set('region_code', regionCode);
      params.set('status', 'active');

      const response = await fetch(`/api/v1/alerts/active?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch alerts');
      }
      const data = await response.json();
      return data.alerts || [];
    },
    staleTime: 30000, // 30 seconds
  });
}

export function useAcknowledgeAlert() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ alertId, acknowledgedBy }: { alertId: string; acknowledgedBy: string }) => {
      const response = await fetch(`/api/v1/alerts/${alertId}/acknowledge`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ acknowledged_by: acknowledgedBy }),
      });
      if (!response.ok) {
        throw new Error('Failed to acknowledge alert');
      }
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
}

export function useAlertsSummary() {
  return useQuery({
    queryKey: ['alerts-summary'],
    queryFn: async () => {
      const response = await fetch('/api/v1/alerts/summary');
      if (!response.ok) {
        throw new Error('Failed to fetch alerts summary');
      }
      return response.json();
    },
    staleTime: 60000,
  });
}
