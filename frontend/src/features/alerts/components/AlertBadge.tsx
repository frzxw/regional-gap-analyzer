'use client';

import React from 'react';

interface AlertBadgeProps {
  severity: 'critical' | 'warning' | 'info';
  size?: 'sm' | 'md';
}

const severityStyles = {
  critical: 'bg-red-100 text-red-800 border-red-200',
  warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  info: 'bg-blue-100 text-blue-800 border-blue-200',
};

const severityLabels = {
  critical: 'Critical',
  warning: 'Warning',
  info: 'Info',
};

export function AlertBadge({ severity, size = 'sm' }: AlertBadgeProps) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full border text-xs font-medium ${severityStyles[severity]} ${
      size === 'md' ? 'px-3 py-1 text-sm' : ''
    }`}>
      {severityLabels[severity]}
    </span>
  );
}
