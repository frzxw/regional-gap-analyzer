'use client';

import React from 'react';

interface MapLegendProps {
  metric?: string;
  title?: string;
}

const colorStops = [
  { value: 0, color: '#d73027', label: '0-20' },
  { value: 20, color: '#fc8d59', label: '20-40' },
  { value: 40, color: '#fee08b', label: '40-60' },
  { value: 60, color: '#d9ef8b', label: '60-80' },
  { value: 80, color: '#91cf60', label: '80-100' },
];

export function MapLegend({ 
  metric = 'composite_score',
  title = 'Score',
}: MapLegendProps) {
  const formattedTitle = metric
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());

  return (
    <div className="bg-white rounded-lg shadow-lg p-3 min-w-[120px]">
      <h4 className="text-sm font-semibold text-gray-700 mb-2">
        {title || formattedTitle}
      </h4>
      <div className="space-y-1">
        {colorStops.map((stop, index) => (
          <div key={index} className="flex items-center gap-2">
            <div 
              className="w-4 h-4 rounded"
              style={{ backgroundColor: stop.color }}
            />
            <span className="text-xs text-gray-600">{stop.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
