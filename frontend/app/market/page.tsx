'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import {
  TrendingUp,
  TrendingDown,
  Building2,
  Calendar,
  Download,
  Filter,
  Search,
  CheckCircle2,
  AlertTriangle,
  Info,
  Clock,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  RefreshCw,
  BarChart3,
  Layers,
  ChevronRight,
  MapPin,
  Scale
} from 'lucide-react';
import {
  getMandiQuotes,
  getMarketForecast,
  getMarketHistory,
  getMarketExportCsvUrl,
  MarketQuotesResponse,
  MarketForecastResponse,
  MarketHistoryResponse,
  MandiQuote,
} from '@/lib/api';

const COMMODITIES = [
  { name: 'Rice', label: 'Rice / Paddy (Kharif)', category: 'Grain' },
  { name: 'Cotton', label: 'Cotton (Medium / Long Staple)', category: 'Fiber' },
  { name: 'Maize', label: 'Maize / Corn', category: 'Grain' },
  { name: 'Blackgram', label: 'Black Gram / Urad Dal', category: 'Pulse' },
  { name: 'Chickpea', label: 'Chickpea / Bengal Gram', category: 'Pulse' },
  { name: 'Pigeonpeas', label: 'Pigeonpea / Red Gram (Tur)', category: 'Pulse' },
  { name: 'Groundnut', label: 'Groundnut (in shell)', category: 'Oilseed' },
  { name: 'Banana', label: 'Banana (Horticulture - No MSP)', category: 'Fruit' },
  { name: 'Mango', label: 'Mango (Horticulture - No MSP)', category: 'Fruit' },
  { name: 'Grapes', label: 'Grapes (Horticulture - No MSP)', category: 'Fruit' },
  { name: 'Orange', label: 'Sweet Orange / Mosambi (No MSP)', category: 'Fruit' },
  { name: 'Papaya', label: 'Papaya (Horticulture - No MSP)', category: 'Fruit' },
  { name: 'Pomegranate', label: 'Pomegranate (Horticulture - No MSP)', category: 'Fruit' },
  { name: 'Watermelon', label: 'Watermelon (Summer Crop - No MSP)', category: 'Fruit' },
];

const TELANGANA_DISTRICTS = [
  'Warangal', 'Hyderabad', 'Nizamabad', 'Khammam', 'Karimnagar', 'Mahabubnagar',
  'Adilabad', 'Suryapet', 'Siddipet', 'Nalgonda', 'Medak', 'Rangareddy'
];

const ANDHRA_DISTRICTS = [
  'Guntur', 'Krishna', 'Kurnool', 'Anantapur', 'East Godavari', 'West Godavari',
  'Tirupati', 'Visakhapatnam', 'Prakasam', 'Nellore', 'Kadapa', 'Bapatla'
];

export default function MarketIntelligencePage() {
  const [selectedCommodity, setSelectedCommodity] = useState('Rice');
  const [selectedState, setSelectedState] = useState<string>('');
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'observed' | 'forecast' | 'history'>('observed');
  const [forecastHorizon, setForecastHorizon] = useState<number>(14);

  // Data states
  const [quotesData, setQuotesData] = useState<MarketQuotesResponse | null>(null);
  const [forecastData, setForecastData] = useState<MarketForecastResponse | null>(null);
  const [historyData, setHistoryData] = useState<MarketHistoryResponse | null>(null);

  // UI state
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchMarketData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch observed quotes
      const quotes = await getMandiQuotes(
        selectedCommodity,
        selectedDistrict || undefined,
        selectedState || undefined
      );
      setQuotesData(quotes);

      // 2. Fetch forecast
      const forecastLoc = selectedDistrict || (selectedState === 'Andhra Pradesh' ? 'Guntur' : 'Warangal');
      const forecast = await getMarketForecast(selectedCommodity, forecastLoc, forecastHorizon);
      setForecastData(forecast);

      // 3. Fetch history
      const history = await getMarketHistory(selectedCommodity, forecastLoc, 30);
      setHistoryData(history);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to connect to market intelligence engine';
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, [selectedCommodity, selectedDistrict, selectedState, forecastHorizon]);

  useEffect(() => {
    fetchMarketData();
  }, [fetchMarketData]);

  // Filtered commodities for search dropdown
  const filteredCommodities = COMMODITIES.filter(c =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6 font-sans max-w-[1540px] mx-auto pb-12">
      {/* 1. HERO & PROVENANCE HEADER */}
      <div className="bg-gradient-to-br from-slate-900 via-emerald-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden border border-emerald-900/40">
        <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold tracking-wide">
              <Scale className="w-3.5 h-3.5" />
              <span>Official Agmarknet & e-NAM Intelligence</span>
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-white">
              Agricultural Market Intelligence
            </h1>
            <p className="text-sm text-slate-300 leading-relaxed">
              Real-time APMC Mandi price discovery, Minimum Support Price (MSP) benchmarks,
              and econometric forecasting for Andhra Pradesh and Telangana agricultural markets.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <a
              href={getMarketExportCsvUrl(selectedCommodity, selectedDistrict)}
              download
              className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition shadow-lg shadow-emerald-900/40 border border-emerald-400/30"
            >
              <Download className="w-4 h-4" />
              <span>Export CSV Report</span>
            </a>
            <button
              onClick={fetchMarketData}
              disabled={loading}
              className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium text-xs transition border border-white/10"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              <span>Refresh Feeds</span>
            </button>
          </div>
        </div>

        {/* Provenance Banner */}
        <div className="mt-6 pt-5 border-t border-white/10 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-300">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1.5 text-emerald-400 font-semibold">
              <CheckCircle2 className="w-4 h-4" />
              <span>Validated Price Data</span>
            </span>
            <span className="text-slate-500">•</span>
            <span>Source: DMI / Agmarknet, Ministry of Agriculture, Govt. of India</span>
          </div>
          {quotesData?.freshness_timestamp && (
            <div className="flex items-center gap-1.5 text-slate-400">
              <Clock className="w-3.5 h-3.5" />
              <span>Freshness: {quotesData.freshness_timestamp}</span>
            </div>
          )}
        </div>
      </div>

      {/* 2. FILTER & SELECTION CONTROL BAR */}
      <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/80 shadow-xs space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {/* Commodity Selector */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
              Crop / Commodity
            </label>
            <div className="relative">
              <select
                value={selectedCommodity}
                onChange={(e) => setSelectedCommodity(e.target.value)}
                className="w-full pl-3 pr-8 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500 transition appearance-none"
              >
                {COMMODITIES.map((c) => (
                  <option key={c.name} value={c.name}>
                    {c.label}
                  </option>
                ))}
              </select>
              <ChevronRight className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none rotate-90" />
            </div>
          </div>

          {/* State Filter */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
              State
            </label>
            <div className="relative">
              <select
                value={selectedState}
                onChange={(e) => {
                  setSelectedState(e.target.value);
                  setSelectedDistrict('');
                }}
                className="w-full pl-3 pr-8 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500 transition appearance-none"
              >
                <option value="">All States (AP & Telangana)</option>
                <option value="Telangana">Telangana</option>
                <option value="Andhra Pradesh">Andhra Pradesh</option>
              </select>
              <ChevronRight className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none rotate-90" />
            </div>
          </div>

          {/* District Filter */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
              District / Mandi Center
            </label>
            <div className="relative">
              <select
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
                className="w-full pl-3 pr-8 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500 transition appearance-none"
              >
                <option value="">All District Mandis</option>
                {selectedState !== 'Andhra Pradesh' && (
                  <optgroup label="Telangana Mandis">
                    {TELANGANA_DISTRICTS.map((d) => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </optgroup>
                )}
                {selectedState !== 'Telangana' && (
                  <optgroup label="Andhra Pradesh Mandis">
                    {ANDHRA_DISTRICTS.map((d) => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </optgroup>
                )}
              </select>
              <ChevronRight className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none rotate-90" />
            </div>
          </div>

          {/* Mode Tabs */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
              Intelligence View
            </label>
            <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-xl">
              <button
                onClick={() => setActiveTab('observed')}
                className={`py-1.5 text-xs font-bold rounded-lg transition ${
                  activeTab === 'observed'
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Observed
              </button>
              <button
                onClick={() => setActiveTab('forecast')}
                className={`py-1.5 text-xs font-bold rounded-lg transition ${
                  activeTab === 'forecast'
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Forecast
              </button>
              <button
                onClick={() => setActiveTab('history')}
                className={`py-1.5 text-xs font-bold rounded-lg transition ${
                  activeTab === 'history'
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Trends
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* ERROR NOTICE */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-semibold">Unable to refresh live market feeds</p>
            <p className="text-xs text-rose-700 mt-0.5">{error}</p>
          </div>
          <button
            onClick={fetchMarketData}
            className="px-3 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold"
          >
            Retry
          </button>
        </div>
      )}

      {/* 3. KEY METRICS STRIP: MODAL PRICE, MIN/MAX SPREAD, MSP BENCHMARK */}
      {quotesData && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Average Modal Price */}
          <div className="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                State Modal Price
              </span>
              <span className="px-2 py-0.5 text-[10px] font-bold rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200">
                Observed Real
              </span>
            </div>
            <div className="text-3xl font-black text-slate-900">
              ₹{quotesData.aggregate_summary.state_average_modal_price.toLocaleString('en-IN')}
              <span className="text-xs font-normal text-slate-500 ml-1">/ Quintal</span>
            </div>
            <div className="text-xs text-slate-500 flex items-center gap-1.5">
              <Building2 className="w-3.5 h-3.5 text-slate-400" />
              <span>Across {quotesData.mandis_reporting_count} reporting APMC yards</span>
            </div>
          </div>

          {/* Mandi Spread */}
          <div className="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                Price Spread (Min — Max)
              </span>
              <span className="px-2 py-0.5 text-[10px] font-bold rounded-md bg-blue-50 text-blue-700 border border-blue-200">
                Grade Range
              </span>
            </div>
            <div className="text-xl sm:text-2xl font-black text-slate-900">
              ₹{quotesData.aggregate_summary.lowest_observed_mandi_price.toLocaleString('en-IN')} — ₹{quotesData.aggregate_summary.highest_observed_mandi_price.toLocaleString('en-IN')}
            </div>
            <div className="text-xs text-slate-500">
              Spread: ₹{(quotesData.aggregate_summary.highest_observed_mandi_price - quotesData.aggregate_summary.lowest_observed_mandi_price).toLocaleString('en-IN')}/q across qualities
            </div>
          </div>

          {/* Total Mandi Arrivals */}
          <div className="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                Daily Arrivals
              </span>
              <span className="px-2 py-0.5 text-[10px] font-bold rounded-md bg-amber-50 text-amber-700 border border-amber-200">
                Supply Volume
              </span>
            </div>
            <div className="text-3xl font-black text-slate-900">
              {quotesData.aggregate_summary.total_arrival_quantity_tonnes}
              <span className="text-xs font-normal text-slate-500 ml-1">Tonnes</span>
            </div>
            <div className="text-xs text-slate-500">
              Daily arrival elasticity impacts local modal spot rates
            </div>
          </div>

          {/* Official MSP Benchmark Card */}
          <div className={`p-5 rounded-2xl border shadow-xs space-y-2 ${
            quotesData.msp_comparison.has_msp
              ? quotesData.msp_comparison.market_status.includes('ABOVE')
                ? 'bg-emerald-50/70 border-emerald-200 text-emerald-950'
                : 'bg-amber-50/70 border-amber-200 text-amber-950'
              : 'bg-slate-50 border-slate-200 text-slate-800'
          }`}>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider">
                Govt. MSP Benchmark
              </span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-white/70 border border-current">
                {quotesData.msp_comparison.season}
              </span>
            </div>
            <div className="text-2xl font-black">
              {quotesData.msp_comparison.has_msp ? (
                <>
                  ₹{quotesData.msp_comparison.official_msp?.toLocaleString('en-IN')}
                  <span className="text-xs font-normal opacity-75 ml-1">/ Quintal</span>
                </>
              ) : (
                <span className="text-base text-slate-600 font-bold">Non-MSP Commodity</span>
              )}
            </div>
            <div className="text-xs font-medium leading-tight">
              {quotesData.msp_comparison.has_msp ? (
                <span className={quotesData.msp_comparison.spread_to_msp_inr! >= 0 ? 'text-emerald-700 font-bold' : 'text-amber-700 font-bold'}>
                  {quotesData.msp_comparison.market_status} ({quotesData.msp_comparison.spread_to_msp_percentage! > 0 ? '+' : ''}{quotesData.msp_comparison.spread_to_msp_percentage}%)
                </span>
              ) : (
                <span className="text-slate-500">Horticulture fruit/vegetable trading on open auctions</span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* 4. TABBED INTELLIGENCE SECTIONS */}
      {activeTab === 'observed' && quotesData && (
        <div className="space-y-6">
          {/* Mandi Table */}
          <div className="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
            <div className="p-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50">
              <div>
                <h3 className="text-base font-extrabold text-slate-900 tracking-tight">
                  APMC Mandi Quotations — {selectedCommodity}
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Verified auction records from terminal and district yards.
                </p>
              </div>
              <div className="inline-flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                <span>Data Source: Agmarknet APMC Feeds</span>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="bg-slate-100/70 border-b border-slate-200/80 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                    <th className="py-3 px-4">Mandi Center</th>
                    <th className="py-3 px-4">District & State</th>
                    <th className="py-3 px-4 text-right">Min Price</th>
                    <th className="py-3 px-4 text-right">Modal Price</th>
                    <th className="py-3 px-4 text-right">Max Price</th>
                    <th className="py-3 px-4 text-right">Arrivals</th>
                    <th className="py-3 px-4 text-center">Status vs MSP</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-sans">
                  {quotesData.mandi_quotes.map((q) => {
                    const hasMsp = quotesData.msp_comparison.has_msp && quotesData.msp_comparison.official_msp;
                    const diffMsp = hasMsp ? q.modal_price - quotesData.msp_comparison.official_msp! : null;

                    return (
                      <tr key={q.mandi_id} className="hover:bg-slate-50/80 transition">
                        <td className="py-3.5 px-4">
                          <div className="font-bold text-slate-900">{q.mandi_name}</div>
                          <div className="text-[11px] text-slate-400 font-mono">ID: {q.mandi_id}</div>
                        </td>
                        <td className="py-3.5 px-4 text-slate-600 text-xs">
                          <div className="font-semibold text-slate-800">{q.district}</div>
                          <div className="text-slate-400">{q.state}</div>
                        </td>
                        <td className="py-3.5 px-4 text-right font-medium text-slate-600">
                          ₹{q.min_price.toLocaleString('en-IN')}
                        </td>
                        <td className="py-3.5 px-4 text-right font-extrabold text-slate-900 text-base">
                          ₹{q.modal_price.toLocaleString('en-IN')}
                        </td>
                        <td className="py-3.5 px-4 text-right font-medium text-slate-600">
                          ₹{q.max_price.toLocaleString('en-IN')}
                        </td>
                        <td className="py-3.5 px-4 text-right font-medium text-slate-700">
                          {q.arrival_quantity_tonnes} t
                        </td>
                        <td className="py-3.5 px-4 text-center">
                          {diffMsp !== null ? (
                            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold ${
                              diffMsp >= 0
                                ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                                : 'bg-amber-50 text-amber-800 border border-amber-200'
                            }`}>
                              {diffMsp >= 0 ? `+₹${diffMsp}` : `-₹${Math.abs(diffMsp)}`}
                            </span>
                          ) : (
                            <span className="text-[11px] text-slate-400 italic">Open Market</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Advisory Footnote */}
            <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-start gap-2 text-xs text-slate-600">
              <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
              <div>
                <strong>Official MSP Advisory:</strong> {quotesData.msp_comparison.advisory}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* FORECAST TAB */}
      {activeTab === 'forecast' && forecastData && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200/80 shadow-xs p-6 space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-5">
              <div>
                <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200 text-xs font-bold mb-1">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Econometric Time-Series Model</span>
                </div>
                <h3 className="text-xl font-extrabold text-slate-900 tracking-tight">
                  Price Forecast Curve — {selectedCommodity} ({forecastHorizon} Days)
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Location: {forecastData.location} • Trend: <strong className="text-slate-800">{forecastData.trend_assessment}</strong> ({forecastData.projected_change_percentage > 0 ? '+' : ''}{forecastData.projected_change_percentage}%)
                </p>
              </div>

              {/* Horizon Selector */}
              <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl text-xs font-bold">
                {[7, 14, 30].map((h) => (
                  <button
                    key={h}
                    onClick={() => setForecastHorizon(h)}
                    className={`px-3 py-1.5 rounded-lg transition ${
                      forecastHorizon === h
                        ? 'bg-white text-emerald-800 shadow-xs'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    {h} Days
                  </button>
                ))}
              </div>
            </div>

            {/* Advisory Bar */}
            <div className="p-4 rounded-xl bg-emerald-50/60 border border-emerald-200 text-emerald-950 text-xs flex items-start gap-2.5">
              <Info className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold">Market Analyst Guidance: </span>
                {forecastData.advisory}
              </div>
            </div>

            {/* Forecast Trajectory Table with 95% Confidence Bounds */}
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                    <th className="py-2.5 px-4">Date</th>
                    <th className="py-2.5 px-4 text-right">Expected Modal</th>
                    <th className="py-2.5 px-4 text-right">95% Lower Bound</th>
                    <th className="py-2.5 px-4 text-right">95% Upper Bound</th>
                    <th className="py-2.5 px-4 text-right">Uncertainty Spread</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-sans">
                  {forecastData.forecast_trajectory.map((pt) => (
                    <tr key={pt.forecast_date} className="hover:bg-slate-50/60 transition">
                      <td className="py-3 px-4">
                        <span className="font-bold text-slate-800">{pt.display_date}</span>
                        <span className="text-[11px] text-slate-400 ml-2 font-mono">{pt.forecast_date}</span>
                      </td>
                      <td className="py-3 px-4 text-right font-extrabold text-slate-900 text-base">
                        ₹{pt.predicted_modal_price.toLocaleString('en-IN')}
                      </td>
                      <td className="py-3 px-4 text-right text-slate-600 font-medium">
                        ₹{pt.lower_confidence_bound_95.toLocaleString('en-IN')}
                      </td>
                      <td className="py-3 px-4 text-right text-slate-600 font-medium">
                        ₹{pt.upper_confidence_bound_95.toLocaleString('en-IN')}
                      </td>
                      <td className="py-3 px-4 text-right text-xs text-slate-500 font-mono">
                        ±₹{(pt.uncertainty_spread_inr / 2).toFixed(0)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Validation Metrics */}
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                Model Evaluation & Historical Backtest Integrity
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div>
                  <span className="text-slate-400 block">Architecture</span>
                  <span className="font-bold text-slate-800">{forecastData.model_validation_metrics.model_architecture}</span>
                </div>
                <div>
                  <span className="text-slate-400 block">Mean Absolute Error (MAE)</span>
                  <span className="font-bold text-slate-800">₹{forecastData.model_validation_metrics.mean_absolute_error_inr}/q</span>
                </div>
                <div>
                  <span className="text-slate-400 block">MAPE</span>
                  <span className="font-bold text-emerald-700">{forecastData.model_validation_metrics.mean_absolute_percentage_error}%</span>
                </div>
                <div>
                  <span className="text-slate-400 block">R² Score</span>
                  <span className="font-bold text-slate-800">{forecastData.model_validation_metrics.r2_score}</span>
                </div>
              </div>
              <p className="text-[11px] text-slate-500 italic pt-1">
                {forecastData.provenance_statement}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* HISTORY TAB */}
      {activeTab === 'history' && historyData && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200/80 shadow-xs p-6 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
              <div>
                <h3 className="text-lg font-extrabold text-slate-900 tracking-tight">
                  Historical Agmarknet Prices — Past 30 Days
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Actual recorded prices at {historyData.location} APMC yard.
                </p>
              </div>
              <div className="text-xs text-slate-500 font-mono">
                {historyData.data_source}
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                    <th className="py-2.5 px-4">Date</th>
                    <th className="py-2.5 px-4 text-right">Min Price</th>
                    <th className="py-2.5 px-4 text-right">Modal Price</th>
                    <th className="py-2.5 px-4 text-right">Max Price</th>
                    <th className="py-2.5 px-4 text-right">Arrivals (t)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-sans">
                  {historyData.historical_records.map((rec) => (
                    <tr key={rec.date} className="hover:bg-slate-50/60 transition">
                      <td className="py-2.5 px-4 font-bold text-slate-800">
                        {rec.display_date} <span className="text-[11px] text-slate-400 font-normal font-mono ml-1">{rec.date}</span>
                      </td>
                      <td className="py-2.5 px-4 text-right text-slate-600">
                        ₹{rec.min_price.toLocaleString('en-IN')}
                      </td>
                      <td className="py-2.5 px-4 text-right font-extrabold text-slate-900">
                        ₹{rec.modal_price.toLocaleString('en-IN')}
                      </td>
                      <td className="py-2.5 px-4 text-right text-slate-600">
                        ₹{rec.max_price.toLocaleString('en-IN')}
                      </td>
                      <td className="py-2.5 px-4 text-right text-slate-700">
                        {rec.arrivals_tonnes} t
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
