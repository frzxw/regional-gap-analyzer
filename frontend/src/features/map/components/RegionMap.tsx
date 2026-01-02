'use client';

import React, { useMemo } from 'react';
import dynamic from 'next/dynamic';
import { MapLegend } from './MapLegend';

// Dynamic import to avoid SSR issues with Leaflet
const MapComponent = dynamic(
  () => import('@/components/map/MapComponent').then(mod => mod.default),
  { 
    ssr: false,
    loading: () => (
      <div className="w-full h-[500px] bg-gray-100 animate-pulse flex items-center justify-center">
        <span className="text-gray-500">Loading map...</span>
      </div>
    ),
  }
);

interface RegionMapProps {
  year?: number;
  metric?: string;
  onRegionClick?: (regionCode: string) => void;
  className?: string;
}

export function RegionMap({
  year,
  metric = 'composite_score',
  onRegionClick,
  className = '',
}: RegionMapProps) {
  return (
    <div className={`relative ${className}`}>
      <MapComponent />
      <div className="absolute bottom-4 left-4 z-[1000]">
        <MapLegend metric={metric} />
      </div>
    </div>
  );
}
