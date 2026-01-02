'use client';

import React from 'react';

interface RankingEntry {
  region_code: string;
  region_name: string;
  score: number;
  rank: number;
  rank_delta?: number | null;
}

interface RankingsTableProps {
  rankings: RankingEntry[];
  onRowClick?: (regionCode: string) => void;
  loading?: boolean;
}

export function RankingsTable({
  rankings,
  onRowClick,
  loading = false,
}: RankingsTableProps) {
  if (loading) {
    return (
      <div className="animate-pulse">
        {Array.from({ length: 10 }).map((_, i) => (
          <div key={i} className="h-12 bg-gray-100 mb-2 rounded" />
        ))}
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Rank
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Region
            </th>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Score
            </th>
            <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
              Change
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {rankings.map((entry) => (
            <tr 
              key={entry.region_code}
              onClick={() => onRowClick?.(entry.region_code)}
              className={onRowClick ? 'cursor-pointer hover:bg-gray-50' : ''}
            >
              <td className="px-4 py-3 whitespace-nowrap">
                <span className={`inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium ${
                  entry.rank <= 3 
                    ? 'bg-green-100 text-green-800' 
                    : entry.rank >= rankings.length - 2
                    ? 'bg-red-100 text-red-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {entry.rank}
                </span>
              </td>
              <td className="px-4 py-3 whitespace-nowrap">
                <div>
                  <div className="text-sm font-medium text-gray-900">
                    {entry.region_name}
                  </div>
                  <div className="text-xs text-gray-500">{entry.region_code}</div>
                </div>
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-right">
                <span className="text-sm font-semibold text-gray-900">
                  {entry.score.toFixed(1)}
                </span>
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-center">
                {entry.rank_delta !== null && entry.rank_delta !== undefined ? (
                  <span className={`inline-flex items-center text-sm ${
                    entry.rank_delta > 0 
                      ? 'text-green-600' 
                      : entry.rank_delta < 0 
                      ? 'text-red-600' 
                      : 'text-gray-400'
                  }`}>
                    {entry.rank_delta > 0 ? '↑' : entry.rank_delta < 0 ? '↓' : '–'}
                    {entry.rank_delta !== 0 && Math.abs(entry.rank_delta)}
                  </span>
                ) : (
                  <span className="text-gray-400">–</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
