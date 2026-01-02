'use client';

import React from 'react';

interface RankingCardProps {
  rank: number;
  regionName: string;
  regionCode: string;
  score: number;
  type: 'top' | 'bottom';
  onClick?: () => void;
}

export function RankingCard({
  rank,
  regionName,
  regionCode,
  score,
  type,
  onClick,
}: RankingCardProps) {
  const isTop = type === 'top';

  return (
    <div 
      onClick={onClick}
      className={`rounded-lg p-4 border-2 ${onClick ? 'cursor-pointer' : ''} ${
        isTop 
          ? 'bg-green-50 border-green-200 hover:border-green-300' 
          : 'bg-red-50 border-red-200 hover:border-red-300'
      }`}
    >
      <div className="flex items-center gap-3">
        <div className={`flex items-center justify-center w-10 h-10 rounded-full text-lg font-bold ${
          isTop ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
        }`}>
          {rank}
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900">{regionName}</h4>
          <p className="text-sm text-gray-500">{regionCode}</p>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${
            isTop ? 'text-green-700' : 'text-red-700'
          }`}>
            {score.toFixed(1)}
          </div>
          <div className="text-xs text-gray-500">score</div>
        </div>
      </div>
    </div>
  );
}
