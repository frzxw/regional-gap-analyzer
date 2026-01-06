"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { healthApi, type HealthDetailedResponse } from "@/utils/api";

// Dynamic import for Leaflet (client-side only)
const MapComponent = dynamic(() => import("@/components/map/MapComponent"), {
  ssr: false,
  loading: () => (
    <div className="h-96 bg-gray-100 rounded-lg flex items-center justify-center">
      <span className="text-gray-500">Loading map...</span>
    </div>
  ),
});

export default function DashboardPage() {
  const [health, setHealth] = useState<HealthDetailedResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await healthApi.checkDetailed();
        setHealth(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to connect to backend");
        setHealth(null);
      } finally {
        setLoading(false);
      }
    };

    fetchHealth();

    // Refresh every 30 seconds
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Regional Gap Analyzer
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Province-level inequality analysis dashboard
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* API Status Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-2">
              API Status
            </h2>
            {loading ? (
              <div className="flex items-center">
                <div className="animate-pulse h-4 w-24 bg-gray-200 rounded"></div>
              </div>
            ) : error ? (
              <div className="flex items-center">
                <span className="h-3 w-3 rounded-full bg-red-500 mr-2"></span>
                <span className="text-red-600">Disconnected</span>
              </div>
            ) : (
              <div className="flex items-center">
                <span className="h-3 w-3 rounded-full bg-green-500 mr-2"></span>
                <span className="text-green-600 capitalize">
                  {health?.status}
                </span>
              </div>
            )}
          </div>

          {/* Database Status Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-2">
              Database
            </h2>
            {loading ? (
              <div className="flex items-center">
                <div className="animate-pulse h-4 w-24 bg-gray-200 rounded"></div>
              </div>
            ) : error ? (
              <div className="flex items-center">
                <span className="h-3 w-3 rounded-full bg-gray-400 mr-2"></span>
                <span className="text-gray-500">Unknown</span>
              </div>
            ) : (
              <div className="flex items-center">
                <span
                  className={`h-3 w-3 rounded-full mr-2 ${health?.database === "connected"
                      ? "bg-green-500"
                      : "bg-yellow-500"
                    }`}
                ></span>
                <span
                  className={
                    health?.database === "connected"
                      ? "text-green-600"
                      : "text-yellow-600"
                  }
                >
                  {health?.database === "connected"
                    ? "Connected"
                    : "Disconnected"}
                </span>
              </div>
            )}
          </div>

          {/* Backend URL Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-2">
              Backend URL
            </h2>
            <code className="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded">
              {process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"}
            </code>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-red-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Connection Error
                </h3>
                <p className="mt-1 text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Map Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Regional Map
          </h2>
          <p className="text-sm text-gray-500 mb-4">
            Interactive map showing province-level data. Click on a region for details.
          </p>
          <MapComponent />
        </div>

        {/* Placeholder Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Scoring Summary */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Scoring Summary
            </h2>
            <p className="text-gray-500 text-sm">
              TODO: Display aggregate scoring statistics and trends.
            </p>
            <div className="mt-4 h-48 bg-gray-100 rounded flex items-center justify-center">
              <span className="text-gray-400">Chart placeholder</span>
            </div>
          </div>

          {/* Top/Bottom Regions */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Regional Rankings
            </h2>
            <p className="text-gray-500 text-sm">
              TODO: Display top and bottom performing regions.
            </p>
            <div className="mt-4 h-48 bg-gray-100 rounded flex items-center justify-center">
              <span className="text-gray-400">Rankings placeholder</span>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500">
            Regional Gap Analyzer — Demo data only. Not for official use.
          </p>
        </div>
      </footer>
    </div>
  );
}
