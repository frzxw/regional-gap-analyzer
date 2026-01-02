import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 font-sans">
      <main className="flex w-full max-w-4xl flex-col items-center justify-center py-16 px-8 text-center">
        {/* Hero Section */}
        <div className="mb-12">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Regional Gap Analyzer
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl">
            Province-level inequality analysis system with scoring and
            geospatial heatmap visualization
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 w-full">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Multi-dimensional Scoring
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Economic, infrastructure, health, and education indicators
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="text-3xl mb-3">🗺️</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Interactive Map
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Geospatial heatmap visualization with Leaflet
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="text-3xl mb-3">📈</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Gap Analysis
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Compare regions and identify development priorities
            </p>
          </div>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <Link
            href="/dashboard"
            className="flex h-12 items-center justify-center rounded-full bg-blue-600 px-8 text-white font-medium transition-colors hover:bg-blue-700"
          >
            Open Dashboard
          </Link>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="flex h-12 items-center justify-center rounded-full border border-gray-300 dark:border-gray-600 px-8 text-gray-700 dark:text-gray-300 font-medium transition-colors hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            View Documentation
          </a>
        </div>

        {/* Demo Notice */}
        <div className="mt-12 px-4 py-2 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg">
          <p className="text-sm text-yellow-800 dark:text-yellow-200">
            ⚠️ Demo data only — Not for official use
          </p>
        </div>
      </main>
    </div>
  );
}
