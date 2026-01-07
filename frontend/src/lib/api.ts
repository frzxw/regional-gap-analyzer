/**
 * API client for communicating with the backend.
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export interface HealthResponse {
  status: string;
}

export interface HealthDetailedResponse {
  status: string;
  database: string;
}

export interface ApiError {
  detail: string;
}

/**
 * Fetch wrapper with error handling.
 */
async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      detail: `HTTP ${response.status}: ${response.statusText}`,
    }));
    throw new Error(error.detail);
  }

  return response.json();
}

/**
 * Health check API calls.
 */
export const healthApi = {
  /**
   * Basic health check.
   */
  check: () => fetchApi<HealthResponse>("/health"),

  /**
   * Detailed health check including database status.
   */
  checkDetailed: () => fetchApi<HealthDetailedResponse>("/health/detailed"),
};

/**
 * Geo API calls.
 */
export const geoApi = {
  /**
   * Get choropleth data (GeoJSON with scores).
   */
  getChoropleth: (year?: number, metric: string = "composite_score") => {
    const query = new URLSearchParams();
    if (year) query.append("year", year.toString());
    if (metric) query.append("metric", metric);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return fetchApi<any>(`/geo/choropleth?${query.toString()}`);
  },
};

/**
 * Regions API calls.
 */
export const regionsApi = {
  /**
   * Get all regions.
   */
  getAll: () =>
    fetchApi<{ regions: unknown[]; total: number }>("/api/v1/regions"),

  /**
   * Get a single region by ID.
   */
  getById: (id: string) => fetchApi<unknown>(`/api/v1/regions/${id}`),
};
