'use client';

import React from 'react';
import { StatCard } from './StatCard';

interface QuickStatsProps {
  totalRegions?: number;
  activeAlerts?: number;
  avgScore?: number;
  gapIndex?: number;
}

export function QuickStats({
  totalRegions = 38,
  activeAlerts = 0,
  avgScore = 0,
  gapIndex = 0,
}: QuickStatsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard
        title="Total Regions"
        value={totalRegions}
        subtitle="Indonesian provinces"
        color="blue"
      />
      <StatCard
        title="Active Alerts"
        value={activeAlerts}
        subtitle="Requiring attention"
        color={activeAlerts > 0 ? 'red' : 'green'}
      />
      <StatCard
        title="Average Score"
        value={avgScore.toFixed(1)}
        subtitle="Composite index"
        color="purple"
      />
      <StatCard
        title="Gap Index"
        value={gapIndex.toFixed(2)}
        subtitle="Inequality measure"
        color="yellow"
      />
    </div>
  );
}
