'use client';

import React from 'react';
import { AlertBadge } from './AlertBadge';

interface Alert {
  id: string;
  region_code: string;
  region_name?: string;
  severity: 'critical' | 'warning' | 'info';
  message: string;
  created_at: string;
  acknowledged?: boolean;
}

interface AlertListProps {
  alerts: Alert[];
  onAcknowledge?: (alertId: string) => void;
  onViewRegion?: (regionCode: string) => void;
  loading?: boolean;
}

export function AlertList({
  alerts,
  onAcknowledge,
  onViewRegion,
  loading = false,
}: AlertListProps) {
  if (loading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="h-20 bg-gray-100 animate-pulse rounded-lg" />
        ))}
      </div>
    );
  }

  if (alerts.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No active alerts</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {alerts.map((alert) => (
        <div 
          key={alert.id}
          className={`rounded-lg border-l-4 p-4 ${
            alert.severity === 'critical' 
              ? 'border-red-500 bg-red-50' 
              : alert.severity === 'warning'
              ? 'border-yellow-500 bg-yellow-50'
              : 'border-blue-500 bg-blue-50'
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <AlertBadge severity={alert.severity} />
                <span 
                  className="font-medium text-gray-900 hover:underline cursor-pointer"
                  onClick={() => onViewRegion?.(alert.region_code)}
                >
                  {alert.region_name || alert.region_code}
                </span>
              </div>
              <p className="text-sm text-gray-700">{alert.message}</p>
              <p className="text-xs text-gray-500 mt-1">
                {new Date(alert.created_at).toLocaleString()}
              </p>
            </div>
            {!alert.acknowledged && onAcknowledge && (
              <button
                onClick={() => onAcknowledge(alert.id)}
                className="ml-4 px-3 py-1 text-sm bg-white border rounded hover:bg-gray-50"
              >
                Acknowledge
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
