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

/**
 * Response types for Imports API
 */
export interface ImportResult {
  success: boolean;
  message: string;
  records_processed: number;
  records_imported: number;
  duration_seconds: number;
}

export interface ImportHistoryItem {
  _id: string;
  name: string;
  indicator_code?: string;
  tahun?: number;
  source_type: string;
  created_at: string;
  records_count?: number;
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
  preview: unknown[];
  total_rows: number;
}

/**
 * Imports API calls for CSV/Excel/JSON file uploads.
 */
export const importsApi = {
  /**
   * Upload and import a file.
   */
  uploadFile: async (
    file: File,
    indicatorCode: string,
    year: number,
    sourceName?: string
  ): Promise<ImportResult> => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("indicator_code", indicatorCode);
    formData.append("year", year.toString());
    if (sourceName) {
      formData.append("source_name", sourceName);
    }

    const url = `${BACKEND_URL}/api/imports/file`;
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: `HTTP ${response.status}: ${response.statusText}`,
      }));
      throw new Error(error.detail || error.message || "Upload failed");
    }

    return response.json();
  },

  /**
   * Validate a file without importing.
   */
  validateFile: async (file: File): Promise<ValidationResult> => {
    const formData = new FormData();
    formData.append("file", file);

    const url = `${BACKEND_URL}/api/imports/validate`;
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: `HTTP ${response.status}: ${response.statusText}`,
      }));
      throw new Error(error.detail || "Validation failed");
    }

    return response.json();
  },

  /**
   * Get import history.
   */
  getHistory: (skip = 0, limit = 20) =>
    fetchApi<{ imports: ImportHistoryItem[]; total: number }>(
      `/api/imports/history?skip=${skip}&limit=${limit}`
    ),

  /**
   * Rollback an import by source ID.
   */
  rollback: (sourceId: string) =>
    fetchApi<{ source_id: string; indicators_deleted: number; status: string }>(
      `/api/imports/rollback/${sourceId}`,
      { method: "POST" }
    ),
};
