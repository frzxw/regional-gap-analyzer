"use client";

import { useState } from "react";
import { YearScoreDisplay } from "@/components/scoring/YearScoreDisplay";
import { ScoreBreakdownDisplay } from "@/components/scoring/ScoreBreakdownDisplay";

export default function YearScoringPage() {
    const [selectedProvinceId, setSelectedProvinceId] = useState<string | null>(null);
    const [selectedYear, setSelectedYear] = useState<number>(2024);
    const [viewMode, setViewMode] = useState<"all" | "top-bottom" | "breakdown">("all");

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
                    <h1 className="text-3xl font-bold text-gray-900">
                        Sistem Scoring Berbasis Tahun
                    </h1>
                    <p className="mt-1 text-sm text-gray-500">
                        Analisis skor komposit provinsi berdasarkan 9 indikator pembangunan
                    </p>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                {/* View Mode Selector */}
                <div className="bg-white rounded-lg shadow p-6 mb-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">
                        Mode Tampilan
                    </h2>
                    <div className="flex gap-4">
                        <button
                            onClick={() => {
                                setViewMode("all");
                                setSelectedProvinceId(null);
                            }}
                            className={`px-4 py-2 rounded-lg font-medium transition-colors ${viewMode === "all"
                                    ? "bg-blue-600 text-white"
                                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                                }`}
                        >
                            Semua Provinsi
                        </button>
                        <button
                            onClick={() => {
                                setViewMode("top-bottom");
                                setSelectedProvinceId(null);
                            }}
                            className={`px-4 py-2 rounded-lg font-medium transition-colors ${viewMode === "top-bottom"
                                    ? "bg-blue-600 text-white"
                                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                                }`}
                        >
                            Top & Bottom 5
                        </button>
                        <button
                            onClick={() => setViewMode("breakdown")}
                            className={`px-4 py-2 rounded-lg font-medium transition-colors ${viewMode === "breakdown"
                                    ? "bg-blue-600 text-white"
                                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                                }`}
                        >
                            Detail Breakdown
                        </button>
                    </div>
                </div>

                {/* Content Area */}
                <div className="bg-white rounded-lg shadow p-6">
                    {viewMode === "breakdown" ? (
                        <div>
                            {!selectedProvinceId ? (
                                <div className="text-center py-12">
                                    <p className="text-gray-500 mb-4">
                                        Pilih provinsi dari daftar untuk melihat breakdown detail
                                    </p>
                                    <div className="max-w-md mx-auto">
                                        <label htmlFor="province-select" className="block text-sm font-medium text-gray-700 mb-2">
                                            Pilih Provinsi:
                                        </label>
                                        <input
                                            type="text"
                                            id="province-select"
                                            placeholder="Masukkan Province ID (contoh: 507f1f77bcf86cd799439011)"
                                            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            onKeyPress={(e) => {
                                                if (e.key === "Enter") {
                                                    const value = (e.target as HTMLInputElement).value.trim();
                                                    if (value) {
                                                        setSelectedProvinceId(value);
                                                    }
                                                }
                                            }}
                                        />
                                        <p className="mt-2 text-xs text-gray-500">
                                            Tekan Enter untuk melihat breakdown
                                        </p>
                                    </div>
                                </div>
                            ) : (
                                <div>
                                    <button
                                        onClick={() => setSelectedProvinceId(null)}
                                        className="mb-4 text-blue-600 hover:text-blue-800 text-sm font-medium"
                                    >
                                        ← Kembali ke pilihan provinsi
                                    </button>
                                    <ScoreBreakdownDisplay
                                        provinceId={selectedProvinceId}
                                        year={selectedYear}
                                    />
                                </div>
                            )}
                        </div>
                    ) : (
                        <YearScoreDisplay
                            showTopBottom={viewMode === "top-bottom"}
                            topBottomCount={5}
                        />
                    )}
                </div>

                {/* Info Card */}
                <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h3 className="text-lg font-semibold text-blue-900 mb-2">
                        Tentang Sistem Scoring
                    </h3>
                    <div className="text-sm text-blue-800 space-y-2">
                        <p>
                            <strong>Metodologi:</strong> Sistem ini menggunakan min-max normalization
                            untuk menghitung skor setiap indikator (0-100), kemudian merata-ratakan
                            semua skor untuk mendapatkan skor komposit.
                        </p>
                        <p>
                            <strong>Indikator yang di-score:</strong>
                        </p>
                        <ul className="list-disc list-inside ml-4 space-y-1">
                            <li>Gini Ratio (lebih rendah lebih baik)</li>
                            <li>Indeks Pembangunan Manusia (lebih tinggi lebih baik)</li>
                            <li>Tingkat Pengangguran Terbuka (lebih rendah lebih baik)</li>
                            <li>Persentase Penduduk Miskin (lebih rendah lebih baik)</li>
                            <li>PDRB Per Kapita (lebih tinggi lebih baik)</li>
                            <li>Rata-rata Upah Bersih (lebih tinggi lebih baik)</li>
                            <li>Inflasi Tahunan (lebih rendah lebih baik)</li>
                            <li>Indeks Harga Konsumen (lebih rendah lebih baik)</li>
                            <li>Angkatan Kerja - TPAK (lebih tinggi lebih baik)</li>
                        </ul>
                    </div>
                </div>
            </main>
        </div>
    );
}
