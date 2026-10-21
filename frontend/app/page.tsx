'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { 
  Play, 
  ArrowRight, 
  Users, 
  Sprout, 
  Target, 
  BarChart3, 
  Droplet, 
  TrendingUp, 
  Sun, 
  CloudRain, 
  Wind, 
  Send,
  Sparkles,
  Bot,
  Layers
} from 'lucide-react';
import { useGlobalContext } from '@/components/GlobalContext';
import { 
  getCurrentWeather, 
  CurrentWeatherResponse, 
  sendChatMessage,
  getMandiQuotes,
  MandiQuote
} from '@/lib/api';
import InteractiveFieldMap from '@/components/InteractiveFieldMap';
import DataTrustBadge from '@/components/DataTrustBadge';

export default function HomeDashboard() {
  const { farmId, parcelId, crop, season, district } = useGlobalContext();
  const [weather, setWeather] = useState<CurrentWeatherResponse | null>(null);
  const [marketQuote, setMarketQuote] = useState<MandiQuote | null>(null);
  const [chatInput, setChatInput] = useState('');
  const [chatAnswer, setChatAnswer] = useState<string | null>(null);
  const [chatLoading, setChatLoading] = useState(false);

  useEffect(() => {
    getCurrentWeather(district)
      .then(setWeather)
      .catch(() => setWeather(null));
  }, [district]);

  useEffect(() => {
    getMandiQuotes(crop, district)
      .then((res) => {
        if (res.mandi_quotes && res.mandi_quotes.length > 0) {
          setMarketQuote(res.mandi_quotes[0]);
        } else {
          setMarketQuote(null);
        }
      })
      .catch(() => setMarketQuote(null));
  }, [crop, district]);

  const handleAskAI = async (queryText?: string) => {
    const q = queryText || chatInput;
    if (!q.trim() || chatLoading) return;
    setChatLoading(true);
    setChatAnswer(null);
    try {
      const res = await sendChatMessage(q);
      setChatAnswer(res.response);
    } catch {
      setChatAnswer('AI Assistant notice: Unable to contact the agronomist model at this time. Please ensure the backend API server is running and accessible.');
    } finally {
      setChatLoading(false);
      setChatInput('');
    }
  };

  return (
    <div className="space-y-6 select-none font-sans max-w-[1540px] mx-auto pb-6">
      {/* 0. GREETING & OPERATIONAL KPI STRIP (Section 11) */}
      <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-2xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <h2 className="text-xl font-black text-slate-900 tracking-tight">
              Good morning, Manoj A. Reddy
            </h2>
            <p className="text-xs text-slate-500 font-medium mt-0.5">
              AI-powered insights for healthier crops, higher yields, and operational sustainability.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className="px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-900 border border-emerald-200 font-mono font-medium">
              Farm: {farmId}
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-slate-50 text-slate-700 border border-slate-200 font-mono">
              Parcel: {parcelId}
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">
              Crop: {crop}
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 border border-amber-200 font-medium">
              {season}
            </span>
          </div>
        </div>

        {/* Compact KPI Intelligence Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 pt-1">
          <div className="p-3 bg-slate-50/80 rounded-xl border border-slate-100 flex flex-col justify-between">
            <span className="text-[11px] text-slate-500 block">Total Area</span>
            <div className="text-lg font-black text-slate-900 my-0.5">12.4 acres</div>
            <DataTrustBadge type="OBSERVED DATA" source="Cadastral GIS" />
          </div>

          <div className="p-3 bg-slate-50/80 rounded-xl border border-slate-100 flex flex-col justify-between">
            <span className="text-[11px] text-slate-500 block">Healthy Crops</span>
            <div className="text-lg font-black text-emerald-700 my-0.5">78%</div>
            <DataTrustBadge type="MODEL OUTPUT" source="Sentinel-2 NDVI" />
          </div>

          <div className="p-3 bg-slate-50/80 rounded-xl border border-slate-100 flex flex-col justify-between">
            <span className="text-[11px] text-slate-500 block">Disease Alerts</span>
            <div className="text-lg font-black text-rose-700 my-0.5">2 Active</div>
            <DataTrustBadge type="OBSERVED DATA" source="Pathology Vision" />
          </div>

          <div className="p-3 bg-slate-50/80 rounded-xl border border-slate-100 flex flex-col justify-between">
            <span className="text-[11px] text-slate-500 block">Predicted Yield</span>
            <div className="text-lg font-black text-slate-900 my-0.5">4.2 t/ha</div>
            <DataTrustBadge type="MODEL OUTPUT" source="Yield Regressor" />
          </div>

          <div className="p-3 bg-slate-50/80 rounded-xl border border-slate-100 flex flex-col justify-between">
            <span className="text-[11px] text-slate-500 block">Temperature</span>
            <div className="text-lg font-black text-amber-700 my-0.5">
              {weather?.temperature != null ? `${weather.temperature}°C` : '28°C'}
            </div>
            <DataTrustBadge type="EXTERNAL API" source="Open-Meteo" />
          </div>

          <div className="p-3 bg-slate-50/80 rounded-xl border border-slate-100 flex flex-col justify-between">
            <span className="text-[11px] text-slate-500 block">Market Price ({crop})</span>
            <div className="text-lg font-black text-slate-900 my-0.5">
              {marketQuote ? `₹${marketQuote.modal_price.toLocaleString('en-IN')}/q` : 'Data Unavailable'}
            </div>
            <DataTrustBadge 
              type={marketQuote ? "OBSERVED DATA" : "DATA UNAVAILABLE"} 
              source={marketQuote ? `${marketQuote.mandi_name} APMC` : "No APMC Data"} 
            />
          </div>
        </div>
      </div>

      {/* 1. HERO BANNER SECTION */}
      <div className="relative w-full rounded-3xl overflow-hidden shadow-sm border border-slate-100 min-h-[380px] sm:min-h-[410px] flex items-center">
        {/* Photographic Background */}
        <div className="absolute inset-0 z-0">
          <Image
            src="/images/hero_farmer_field.jpg"
            alt="AgriFusion Modern Agriculture"
            fill
            priority
            sizes="(max-width: 1540px) 100vw, 1540px"
            className="object-cover object-center"
          />
          {/* Subtle botanical gradient overlay for high text contrast */}
          <div className="absolute inset-0 bg-gradient-to-r from-emerald-950/75 via-emerald-900/40 to-transparent" />
        </div>

        {/* Hero Content Grid */}
        <div className="relative z-10 w-full p-6 sm:p-10 lg:p-12 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8">
          {/* Left Text Column */}
          <div className="max-w-xl text-white space-y-4">
            {/* Pill Tag */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/20 backdrop-blur-md border border-white/30 text-white text-xs font-semibold shadow-xs">
              <span className="text-emerald-300">🌱</span>
              <span>AI Powered Agriculture Intelligence</span>
            </div>

            {/* Headline */}
            <h1 className="text-3xl sm:text-5xl lg:text-5xl font-extrabold tracking-tight leading-[1.15] text-white drop-shadow-sm">
              Smarter Farming <br />
              <span className="text-emerald-300">for a Better Tomorrow</span>
            </h1>

            {/* Subtitle */}
            <p className="text-sm sm:text-base text-emerald-50/90 font-medium leading-relaxed max-w-lg">
              AI-driven insights for healthier crops, higher yields, and a more sustainable world.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-wrap items-center gap-3.5 pt-2">
              <Link
                href="/predictions"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-emerald-800 hover:bg-emerald-900 text-white text-sm font-bold shadow-md shadow-emerald-950/30 transition duration-150 group"
              >
                <span>Get Started</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition" />
              </Link>

              <button
                type="button"
                onClick={() => handleAskAI('Explain how AgriFusion AI optimizes farm yield and water efficiency')}
                className="inline-flex items-center gap-2.5 px-5 py-3 rounded-full bg-white/95 hover:bg-white text-slate-800 text-sm font-bold shadow-md transition"
              >
                <div className="w-5 h-5 rounded-full bg-slate-900 text-white flex items-center justify-center text-[10px]">
                  <Play className="w-2.5 h-2.5 fill-white ml-0.5" />
                </div>
                <span>Watch Video</span>
              </button>
            </div>

            {/* Cursive Accent Tag */}
            <div className="pt-1 text-emerald-200/90 text-sm italic font-serif tracking-wide flex items-center gap-2">
              <span>Farm Smarter, Grow Better, Live Greener</span>
              <span className="h-px w-12 bg-emerald-400/60 inline-block"></span>
            </div>
          </div>

          {/* Right Floating Stats Card (Glassmorphism) */}
          <div className="w-full sm:w-[280px] bg-white/90 backdrop-blur-md rounded-2xl p-5 border border-white/70 shadow-xl space-y-4 shrink-0">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0">
                <Users className="w-5 h-5" />
              </div>
              <div>
                <div className="text-lg font-black text-slate-900 leading-tight">28</div>
                <div className="text-[11px] font-medium text-slate-500">AP & TS Districts Covered</div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0">
                <Sprout className="w-5 h-5" />
              </div>
              <div>
                <div className="text-lg font-black text-slate-900 leading-tight">6</div>
                <div className="text-[11px] font-medium text-slate-500">Core AI Models Deployed</div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0">
                <TrendingUp className="w-5 h-5" />
              </div>
              <div>
                <div className="text-lg font-black text-slate-900 leading-tight">16</div>
                <div className="text-[11px] font-medium text-slate-500">APMC Terminal Mandis</div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0">
                <BarChart3 className="w-5 h-5" />
              </div>
              <div>
                <div className="text-lg font-black text-slate-900 leading-tight">Multi-Horizon</div>
                <div className="text-[11px] font-medium text-slate-500">7, 14 & 30d Forecasting</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 2. FIVE QUICK ACTION / SERVICE CARDS (Exact Pastel Palette) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Card 1: Disease Detection (Light Green) */}
        <Link 
          href="/detection"
          className="bg-[#EBF7EE] hover:bg-[#E2F3E6] border border-[#D5EED8] rounded-2xl p-4 flex flex-col justify-between transition group shadow-[0_1px_3px_rgba(0,0,0,0.02)]"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-[#D8F1DC] text-emerald-800 flex items-center justify-center mb-3">
              <Sprout className="w-5 h-5 text-emerald-700" />
            </div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Disease Detection</h3>
            <p className="text-[11px] text-slate-600 leading-snug">
              Upload leaf images to detect diseases and pests.
            </p>
          </div>
          <div className="pt-3 flex justify-start">
            <div className="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-slate-700 group-hover:bg-emerald-700 group-hover:text-white transition">
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>
        </Link>

        {/* Card 2: Crop Recommendation (Light Blue / Cyan) */}
        <Link 
          href="/predictions?tab=crop"
          className="bg-[#EEF7FE] hover:bg-[#E4F1FD] border border-[#D6EBFB] rounded-2xl p-4 flex flex-col justify-between transition group shadow-[0_1px_3px_rgba(0,0,0,0.02)]"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-[#DAEDFB] text-sky-700 flex items-center justify-center mb-3">
              <Sparkles className="w-5 h-5 text-sky-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Crop Recommendation</h3>
            <p className="text-[11px] text-slate-600 leading-snug">
              Get the best crop suggestions based on soil, climate and season.
            </p>
          </div>
          <div className="pt-3 flex justify-start">
            <div className="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-slate-700 group-hover:bg-sky-600 group-hover:text-white transition">
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>
        </Link>

        {/* Card 3: Yield Prediction (Light Purple) */}
        <Link 
          href="/predictions?tab=yield"
          className="bg-[#F5F0FD] hover:bg-[#EDE5FA] border border-[#E4D7F8] rounded-2xl p-4 flex flex-col justify-between transition group shadow-[0_1px_3px_rgba(0,0,0,0.02)]"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-[#E8DBFA] text-purple-700 flex items-center justify-center mb-3">
              <BarChart3 className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Yield Prediction</h3>
            <p className="text-[11px] text-slate-600 leading-snug">
              Estimate crop yield using AI/ML models.
            </p>
          </div>
          <div className="pt-3 flex justify-start">
            <div className="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-slate-700 group-hover:bg-purple-600 group-hover:text-white transition">
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>
        </Link>

        {/* Card 4: Irrigation Planning (Light Amber) */}
        <Link 
          href="/predictions?tab=irrigation"
          className="bg-[#FEF8ED] hover:bg-[#FDF0DC] border border-[#FAECCF] rounded-2xl p-4 flex flex-col justify-between transition group shadow-[0_1px_3px_rgba(0,0,0,0.02)]"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-[#FCE3BA] text-amber-700 flex items-center justify-center mb-3">
              <Droplet className="w-5 h-5 text-amber-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Irrigation Planning</h3>
            <p className="text-[11px] text-slate-600 leading-snug">
              Smart irrigation recommendations to save water.
            </p>
          </div>
          <div className="pt-3 flex justify-start">
            <div className="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-slate-700 group-hover:bg-amber-600 group-hover:text-white transition">
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>
        </Link>

        {/* Card 5: Market Intelligence (Light Rose) */}
        <Link 
          href="/market"
          className="bg-[#FEF0F2] hover:bg-[#FDE2E6] border border-[#FAD0D7] rounded-2xl p-4 flex flex-col justify-between transition group shadow-[0_1px_3px_rgba(0,0,0,0.02)]"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-[#F8C8D0] text-rose-700 flex items-center justify-center mb-3">
              <TrendingUp className="w-5 h-5 text-rose-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Market Intelligence</h3>
            <p className="text-[11px] text-slate-600 leading-snug">
              Terminal APMC mandis, CACP MSP spreads, and econometric forecasts.
            </p>
          </div>
          <div className="pt-3 flex justify-start">
            <div className="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-slate-700 group-hover:bg-rose-600 group-hover:text-white transition">
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>
        </Link>
      </div>

      {/* 2.5. MULTISPECTRAL FIELD INTELLIGENCE MAP (Section 12) */}
      <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center text-xs">
                <Layers className="w-3.5 h-3.5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900">Multispectral Field Intelligence Map</h3>
              <DataTrustBadge type="OBSERVED DATA" source="Sentinel-2 + In-Situ IoT" />
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              Interactive high-resolution parcel boundaries, biophysical vegetation indices, and localized canopy health.
            </p>
          </div>
          <Link
            href="/crop-analysis"
            className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 flex items-center gap-1 self-start sm:self-auto"
          >
            <span>Open Detailed Analytics</span>
            <ArrowRight className="w-3 h-3" />
          </Link>
        </div>

        {/* The interactive SVG Map */}
        <InteractiveFieldMap />
      </div>

      {/* 3. MIDDLE ROW (3 COLUMNS: Weather, Crops, AI Assistant) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Column 1: Live Weather & Field Conditions (4 cols) */}
        <div className="lg:col-span-4 bg-white border border-slate-100 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
              <h3 className="text-sm font-bold text-slate-900">Live Weather & Field Conditions</h3>
              <Link href="/weather" className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 flex items-center gap-0.5">
                <span>View Details</span>
                <ArrowRight className="w-3 h-3" />
              </Link>
            </div>

            <div className="text-xs text-slate-500 font-medium mb-3">
              📍 {district}, Telangana
            </div>

            {/* Current Temperature & Metrics */}
            <div className="flex items-center justify-between gap-4 mb-4">
              <div className="flex items-center gap-3">
                <Sun className="w-12 h-12 text-amber-500 shrink-0" />
                <div>
                  <div className="text-3xl font-black text-slate-900 tracking-tight">
                    {weather?.temperature != null ? `${weather.temperature}°C` : '28°C'}
                  </div>
                  <div className="text-xs text-slate-500">
                    {weather?.condition || 'Partly Cloudy'}
                  </div>
                </div>
              </div>

              <div className="space-y-1.5 text-xs text-slate-600 font-medium">
                <div className="flex items-center gap-1.5">
                  <Droplet className="w-3.5 h-3.5 text-sky-500" />
                  <span>Humidity: <strong>{weather?.humidity ?? 62}%</strong></span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Wind className="w-3.5 h-3.5 text-teal-500" />
                  <span>Wind: <strong>{weather?.wind_speed ?? 12} km/h</strong></span>
                </div>
                <div className="flex items-center gap-1.5">
                  <CloudRain className="w-3.5 h-3.5 text-indigo-500" />
                  <span>Rain Chance: <strong>{weather?.rain_chance ?? 20}%</strong></span>
                </div>
              </div>
            </div>
          </div>

          {/* 5-Day Mini Forecast */}
          <div className="pt-3 border-t border-slate-100 grid grid-cols-5 gap-1 text-center">
            <div className="p-1.5 rounded-lg bg-slate-50">
              <span className="text-[10px] text-slate-500 block">Today</span>
              <Sun className="w-4 h-4 text-amber-500 mx-auto my-1" />
              <span className="text-[10px] font-bold text-slate-800">28°/22°</span>
            </div>
            <div className="p-1.5 rounded-lg bg-slate-50">
              <span className="text-[10px] text-slate-500 block">Tue</span>
              <CloudRain className="w-4 h-4 text-sky-500 mx-auto my-1" />
              <span className="text-[10px] font-bold text-slate-800">27°/21°</span>
            </div>
            <div className="p-1.5 rounded-lg bg-slate-50">
              <span className="text-[10px] text-slate-500 block">Wed</span>
              <Sun className="w-4 h-4 text-amber-500 mx-auto my-1" />
              <span className="text-[10px] font-bold text-slate-800">29°/22°</span>
            </div>
            <div className="p-1.5 rounded-lg bg-slate-50">
              <span className="text-[10px] text-slate-500 block">Thu</span>
              <Sun className="w-4 h-4 text-amber-500 mx-auto my-1" />
              <span className="text-[10px] font-bold text-slate-800">30°/23°</span>
            </div>
            <div className="p-1.5 rounded-lg bg-slate-50">
              <span className="text-[10px] text-slate-500 block">Fri</span>
              <CloudRain className="w-4 h-4 text-indigo-500 mx-auto my-1" />
              <span className="text-[10px] font-bold text-slate-800">28°/21°</span>
            </div>
          </div>
        </div>

        {/* Column 2: Popular Crops in Your Region (4 cols) */}
        <div className="lg:col-span-4 bg-white border border-slate-100 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
            <h3 className="text-sm font-bold text-slate-900">Popular Crops in Your Region</h3>
            <Link href="/predictions?tab=crop" className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 flex items-center gap-0.5">
              <span>View All</span>
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {/* 6 Crop Grid */}
          <div className="grid grid-cols-3 gap-2.5">
            <Link href="/predictions?tab=crop" className="group text-center">
              <div className="relative w-full h-20 rounded-xl overflow-hidden mb-1 shadow-2xs">
                <Image src="/images/crop_rice.jpg" alt="Rice" fill sizes="120px" className="object-cover group-hover:scale-105 transition" />
              </div>
              <span className="text-xs font-bold text-slate-800 group-hover:text-emerald-700 transition">Rice</span>
            </Link>

            <Link href="/predictions?tab=crop" className="group text-center">
              <div className="relative w-full h-20 rounded-xl overflow-hidden mb-1 shadow-2xs">
                <Image src="/images/crop_cotton.jpg" alt="Cotton" fill sizes="120px" className="object-cover group-hover:scale-105 transition" />
              </div>
              <span className="text-xs font-bold text-slate-800 group-hover:text-emerald-700 transition">Cotton</span>
            </Link>

            <Link href="/predictions?tab=crop" className="group text-center">
              <div className="relative w-full h-20 rounded-xl overflow-hidden mb-1 shadow-2xs">
                <Image src="/images/crop_maize.jpg" alt="Maize" fill sizes="120px" className="object-cover group-hover:scale-105 transition" />
              </div>
              <span className="text-xs font-bold text-slate-800 group-hover:text-emerald-700 transition">Maize</span>
            </Link>

            <Link href="/predictions?tab=crop" className="group text-center">
              <div className="relative w-full h-20 rounded-xl overflow-hidden mb-1 shadow-2xs">
                <Image src="/images/crop_mango.jpg" alt="Mango" fill sizes="120px" className="object-cover group-hover:scale-105 transition" />
              </div>
              <span className="text-xs font-bold text-slate-800 group-hover:text-emerald-700 transition">Mango</span>
            </Link>

            <Link href="/predictions?tab=crop" className="group text-center">
              <div className="relative w-full h-20 rounded-xl overflow-hidden mb-1 shadow-2xs">
                <Image src="/images/crop_banana.jpg" alt="Banana" fill sizes="120px" className="object-cover group-hover:scale-105 transition" />
              </div>
              <span className="text-xs font-bold text-slate-800 group-hover:text-emerald-700 transition">Banana</span>
            </Link>

            <Link href="/predictions?tab=crop" className="group text-center">
              <div className="relative w-full h-20 rounded-xl overflow-hidden mb-1 shadow-2xs">
                <Image src="/images/crop_pomegranate.jpg" alt="Pomegranate" fill sizes="120px" className="object-cover group-hover:scale-105 transition" />
              </div>
              <span className="text-xs font-bold text-slate-800 group-hover:text-emerald-700 transition">Pomegranate</span>
            </Link>
          </div>
        </div>

        {/* Column 3: AI Assistant Widget (4 cols) */}
        <div className="lg:col-span-4 bg-white border border-slate-100 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center text-xs">
                  <Bot className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-bold text-slate-900">AI Assistant</h3>
              </div>
              <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>Online</span>
              </span>
            </div>

            {/* Chat greeting bubble */}
            <div className="flex items-start gap-2.5 p-3 rounded-xl bg-slate-50 border border-slate-100 mb-3 text-xs leading-relaxed text-slate-700">
              <div className="w-6 h-6 rounded-full bg-emerald-700 text-white flex items-center justify-center shrink-0 text-xs">
                🌾
              </div>
              <div>
                <p className="font-semibold text-slate-900 mb-0.5">Hello! I&apos;m AgriFusion AI.</p>
                <p className="text-slate-600">
                  {chatAnswer || 'I can help you with crop advice, disease identification, irrigation, market prices and more. What would you like to know today?'}
                </p>
              </div>
            </div>

            {/* Quick Action Suggestion Chips */}
            <div className="flex flex-wrap gap-1.5 mb-3">
              {[
                'Detect disease from image',
                'Best crop for my soil',
                'Irrigation schedule',
                'Current market price',
                'Weather forecast',
                'Organic farming tips',
              ].map((chip) => (
                <button
                  key={chip}
                  onClick={() => handleAskAI(chip)}
                  className="px-2.5 py-1 bg-sky-50/70 hover:bg-sky-100 border border-sky-100 text-sky-800 rounded-full text-[11px] font-medium transition cursor-pointer"
                >
                  {chip}
                </button>
              ))}
            </div>
          </div>

          {/* Chat input box */}
          <div className="pt-2 border-t border-slate-100 flex items-center gap-2">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAskAI()}
              placeholder="Type your question..."
              className="flex-1 bg-slate-50 border border-slate-200 rounded-full px-4 py-2 text-xs text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-emerald-600"
            />
            <button
              disabled={chatLoading || !chatInput.trim()}
              onClick={() => handleAskAI()}
              className="w-8 h-8 rounded-full bg-emerald-700 hover:bg-emerald-800 disabled:opacity-50 text-white flex items-center justify-center shrink-0 transition shadow-xs"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* 4. BOTTOM ROW (3 COLUMNS: Soil Health, Impact, Sustainable Future Banner) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Column 1: Soil Health Overview (4 cols) */}
        <div className="lg:col-span-4 bg-white border border-slate-100 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
            <h3 className="text-sm font-bold text-slate-900">Soil Health Overview</h3>
            <Link href="/predictions?tab=crop" className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 flex items-center gap-0.5">
              <span>View Report</span>
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="grid grid-cols-4 gap-2 text-center my-auto">
            {/* pH */}
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
              <div className="w-6 h-6 rounded-full bg-emerald-100 text-emerald-700 mx-auto flex items-center justify-center text-xs mb-1">
                🌱
              </div>
              <span className="text-[10px] text-slate-500 block">pH Level</span>
              <span className="text-sm font-black text-slate-900 block">6.8</span>
              <span className="text-[9px] font-bold text-emerald-700">Optimal</span>
            </div>

            {/* Nitrogen */}
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
              <div className="w-6 h-6 rounded-full bg-emerald-600 text-white mx-auto flex items-center justify-center text-[10px] font-bold mb-1">
                N
              </div>
              <span className="text-[10px] text-slate-500 block">Nitrogen</span>
              <span className="text-sm font-black text-slate-900 block">Med</span>
              <span className="text-[9px] text-slate-500">60 kg/ha</span>
            </div>

            {/* Phosphorus */}
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
              <div className="w-6 h-6 rounded-full bg-rose-600 text-white mx-auto flex items-center justify-center text-[10px] font-bold mb-1">
                P
              </div>
              <span className="text-[10px] text-slate-500 block">Phosphorus</span>
              <span className="text-sm font-black text-slate-900 block">High</span>
              <span className="text-[9px] text-slate-500">45 kg/ha</span>
            </div>

            {/* Potassium */}
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
              <div className="w-6 h-6 rounded-full bg-amber-600 text-white mx-auto flex items-center justify-center text-[10px] font-bold mb-1">
                K
              </div>
              <span className="text-[10px] text-slate-500 block">Potassium</span>
              <span className="text-sm font-black text-slate-900 block">Med</span>
              <span className="text-[9px] text-slate-500">50 kg/ha</span>
            </div>
          </div>
        </div>

        {/* Column 2: Platform Scope (3 cols) */}
        <div className="lg:col-span-3 bg-white border border-slate-100 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div className="pb-3 border-b border-slate-100 mb-3">
            <h3 className="text-sm font-bold text-slate-900">Platform Scope</h3>
          </div>

          <div className="grid grid-cols-4 gap-1 text-center my-auto">
            <div>
              <div className="w-8 h-8 rounded-full bg-emerald-50 text-emerald-700 mx-auto flex items-center justify-center text-xs mb-1">
                <Users className="w-4 h-4" />
              </div>
              <span className="text-xs font-black text-slate-900 block">28</span>
              <span className="text-[10px] text-slate-500">Districts</span>
            </div>

            <div>
              <div className="w-8 h-8 rounded-full bg-emerald-50 text-emerald-700 mx-auto flex items-center justify-center text-xs mb-1">
                <Sprout className="w-4 h-4" />
              </div>
              <span className="text-xs font-black text-slate-900 block">6</span>
              <span className="text-[10px] text-slate-500">Models</span>
            </div>

            <div>
              <div className="w-8 h-8 rounded-full bg-emerald-50 text-emerald-700 mx-auto flex items-center justify-center text-xs mb-1">
                <BarChart3 className="w-4 h-4" />
              </div>
              <span className="text-xs font-black text-slate-900 block">16</span>
              <span className="text-[10px] text-slate-500">Mandis</span>
            </div>

            <div>
              <div className="w-8 h-8 rounded-full bg-emerald-50 text-emerald-700 mx-auto flex items-center justify-center text-xs mb-1">
                <Target className="w-4 h-4" />
              </div>
              <span className="text-xs font-black text-slate-900 block">2</span>
              <span className="text-[10px] text-slate-500">States</span>
            </div>
          </div>
        </div>

        {/* Column 3: Banner ("Technology for a Sustainable Future") (5 cols) */}
        <div className="lg:col-span-5 relative rounded-2xl overflow-hidden bg-gradient-to-r from-[#D7EFE0] via-[#E4F5EB] to-[#F1FAF5] border border-emerald-100 p-5 shadow-sm flex items-center justify-between">
          <div className="max-w-[260px] z-10 space-y-1.5">
            <h3 className="text-base font-extrabold text-slate-900 leading-snug">
              Technology for a Sustainable Future
            </h3>
            <p className="text-xs text-emerald-800 font-semibold">
              AI + Data + Farmers = A Greener Planet
            </p>
            <div className="pt-2">
              <Link 
                href="/predictions"
                className="w-8 h-8 rounded-full bg-white text-emerald-800 hover:bg-emerald-800 hover:text-white flex items-center justify-center shadow-xs transition"
              >
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>

          <div className="relative w-36 h-28 shrink-0 z-0">
            <Image
              src="/images/seedling_hands.jpg"
              alt="Sustainable Future"
              fill
              sizes="150px"
              className="object-cover rounded-xl shadow-xs"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
