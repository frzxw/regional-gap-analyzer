/**
 * Regions feature types - TypeScript interfaces for region detail pages
 */

export interface CategoryScore {
    economic: number;
    infrastructure: number;
    health: number;
    education: number;
}

export interface RegionScore {
    region_code: string;
    region_name: string;
    year: number;
    composite_score: number;
    category_scores: CategoryScore;
    rank: number;
    rank_delta?: number | null;
    gap_from_average: number;
}

export interface ScoreHistoryEntry {
    year: number;
    composite_score: number;
    category_scores?: CategoryScore;
    rank?: number;
}

export interface ScoreHistoryResponse {
    region_code: string;
    start_year: number;
    end_year: number;
    history: ScoreHistoryEntry[];
}

export interface GapAnalysis {
    year: number;
    national_average: number;
    std_deviation: number;
    coefficient_of_variation: number;
    max_score: number;
    min_score: number;
    gap_range: number;
}

/**
 * Score interpretation based on scoring-method.md
 */
export type ScoreLevel =
    | 'very-high'   // 80-100: Dark Green
    | 'high'        // 60-79: Light Green
    | 'medium'      // 40-59: Yellow
    | 'low'         // 20-39: Orange
    | 'very-low';   // 0-19: Red

export function getScoreLevel(score: number): ScoreLevel {
    if (score >= 80) return 'very-high';
    if (score >= 60) return 'high';
    if (score >= 40) return 'medium';
    if (score >= 20) return 'low';
    return 'very-low';
}

export function getScoreColor(score: number): string {
    const level = getScoreLevel(score);
    switch (level) {
        case 'very-high': return '#166534'; // dark green
        case 'high': return '#22c55e';      // light green
        case 'medium': return '#eab308';    // yellow
        case 'low': return '#f97316';       // orange
        case 'very-low': return '#ef4444';  // red
    }
}

export function getScoreBgColor(score: number): string {
    const level = getScoreLevel(score);
    switch (level) {
        case 'very-high': return 'bg-green-800 dark:bg-green-900';
        case 'high': return 'bg-green-500 dark:bg-green-600';
        case 'medium': return 'bg-yellow-500 dark:bg-yellow-600';
        case 'low': return 'bg-orange-500 dark:bg-orange-600';
        case 'very-low': return 'bg-red-500 dark:bg-red-600';
    }
}

export function getScoreLabel(score: number): string {
    const level = getScoreLevel(score);
    switch (level) {
        case 'very-high': return 'Sangat Tinggi';
        case 'high': return 'Tinggi';
        case 'medium': return 'Sedang';
        case 'low': return 'Rendah';
        case 'very-low': return 'Sangat Rendah';
    }
}

/**
 * Category configuration for indicator breakdown
 */
export const CATEGORY_CONFIG = {
    economic: { label: 'Ekonomi', weight: 0.30, color: '#3b82f6' },
    infrastructure: { label: 'Infrastruktur', weight: 0.25, color: '#8b5cf6' },
    health: { label: 'Kesehatan', weight: 0.25, color: '#10b981' },
    education: { label: 'Pendidikan', weight: 0.20, color: '#f59e0b' },
} as const;

export type CategoryKey = keyof typeof CATEGORY_CONFIG;
