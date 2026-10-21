'use client';

import React, { useState, useEffect } from 'react';
import { Calendar } from 'lucide-react';
import { useGlobalContext } from '@/components/GlobalContext';
import DataTrustBadge from '@/components/DataTrustBadge';
import { 
  getCurrentWeather, 
  getWeatherForecast, 
  CurrentWeatherResponse, 
  WeatherForecastDay 
} from '@/lib/api';

export default function WeatherPage() {
  const { farmId, parcelId, district, state, isSimulationMode, setSimulationMode } = useGlobalContext();
  const [current, setCurrent] = useState<CurrentWeatherResponse | null>(null);
  const [forecast, setForecast] = useState<WeatherForecastDay[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    Promise.all([
      getCurrentWeather(district),
      getWeatherForecast(district, 7),
    ])
      .then(([cur, fcast]) => {
        setCurrent(cur);
        setForecast(fcast.forecast || []);
      })
      .catch((err: unknown) => {
        if (isSimulationMode) {
          // Explicit simulated benchmark dataset
          setCurrent({
            location: district,
            full_location: `${district}, ${state}`,
            date: new Date().toISOString().split('T')[0],
            day_of_week: 'Wednesday',
            day_short: 'Wed',
            formatted_date: 'September 19, 2026',
            temperature: 28.5,
            feels_like: 30.0,
            temp_min: 22.0,
            temp_max: 33.0,
            humidity: 62.0,
            wind_speed: 12.0,
            precipitation: 0.0,
            rain_chance: 20,
            condition: 'Partly Cloudy (Simulated)',
            icon: '🌤️',
          });
          setForecast([
            { day: 'Wed', full_day: 'Wednesday', date: '2026-09-19', display_date: 'Sep 19', temperature: 28, temp_max: 33, temp_min: 22, temp_range: '22° / 33°', condition: 'Sunny', icon: '☀️', rain_chance: 10 },
            { day: 'Thu', full_day: 'Thursday', date: '2026-09-20', display_date: 'Sep 20', temperature: 29, temp_max: 34, temp_min: 23, temp_range: '23° / 34°', condition: 'Clear', icon: '🌤️', rain_chance: 15 },
            { day: 'Fri', full_day: 'Friday', date: '2026-09-21', display_date: 'Sep 21', temperature: 27, temp_max: 31, temp_min: 21, temp_range: '21° / 31°', condition: 'Rain', icon: '🌧️', rain_chance: 65 },
            { day: 'Sat', full_day: 'Saturday', date: '2026-09-22', display_date: 'Sep 22', temperature: 26, temp_max: 30, temp_min: 20, temp_range: '20° / 30°', condition: 'Showers', icon: '🌦️', rain_chance: 45 },
            { day: 'Sun', full_day: 'Sunday', date: '2026-09-23', display_date: 'Sep 23', temperature: 28, temp_max: 32, temp_min: 22, temp_range: '22° / 32°', condition: 'Partly Cloudy', icon: '🌤️', rain_chance: 20 },
            { day: 'Mon', full_day: 'Monday', date: '2026-09-24', display_date: 'Sep 24', temperature: 30, temp_max: 35, temp_min: 24, temp_range: '24° / 35°', condition: 'Sunny', icon: '☀️', rain_chance: 5 },
            { day: 'Tue', full_day: 'Tuesday', date: '2026-09-25', display_date: 'Sep 25', temperature: 31, temp_max: 35, temp_min: 24, temp_range: '24° / 35°', condition: 'Sunny', icon: '☀️', rain_chance: 10 },
          ]);
        } else {
          setCurrent(null);
          setForecast([]);
          setError(err instanceof Error ? err.message : 'Weather station telemetry unavailable.');
        }
      })
      .finally(() => setLoading(false));
  }, [district, isSimulationMode, state]);

  // Compute Agricultural Spray Window ONLY when valid telemetry exists
  // Safe criteria: Wind 3–15 km/h, Rain chance < 25%, Temp <= 32°C, Humidity 40–80%
  const wind = current?.wind_speed ?? null;
  const rainChance = current?.rain_chance ?? null;
  const temp = current?.temperature ?? null;
  const humidity = current?.humidity ?? null;

  const windSafe = wind != null ? (wind >= 3 && wind <= 15) : null;
  const rainSafe = rainChance != null ? (rainChance < 25) : null;
  const tempSafe = temp != null ? (temp <= 32) : null;
  const humiditySafe = humidity != null ? (humidity >= 40 && humidity <= 80) : null;

  const isSprayWindowOptimal = (windSafe && rainSafe && tempSafe && humiditySafe) ? true : (windSafe === false || rainSafe === false || tempSafe === false || humiditySafe === false ? false : null);

  return (
    <div className="space-y-6">
      {/* Top Banner - Light Botanical Enterprise */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-mono tracking-wider text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-bold uppercase">
              Meteorological Intelligence
            </span>
            <DataTrustBadge type="OBSERVED DATA" source="Open-Meteo High-Resolution Numerical Model" />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 font-sans tracking-tight">
            Microclimate Diagnostics & Spray Windows
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            District: {district}, {state} • Weather Station Focus: Farm {farmId} (Parcel {parcelId})
          </p>
        </div>

        {/* Live Weather Capsule */}
        <div className="flex items-center gap-4 bg-slate-50 px-4 py-3 rounded-xl border border-slate-200 font-mono">
          <div className="text-3xl">{current?.icon || '📡'}</div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl font-black text-slate-900">
                {current?.temperature != null ? `${current.temperature}°C` : 'Data unavailable'}
              </span>
              <span className="text-xs text-slate-500 font-sans">
                {current?.feels_like != null ? `Feels like ${current.feels_like}°C` : 'Probe offline'}
              </span>
            </div>
            <div className="text-xs text-emerald-700 font-semibold font-sans">
              {loading ? 'Probing station telemetry...' : (current?.condition || 'Weather Station Offline')}
            </div>
          </div>
        </div>
      </div>

      {/* Meteorological Probe Error Alert */}
      {error && !isSimulationMode && (
        <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-xs font-mono text-amber-800 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-bold">Weather Station Offline:</span>
            <span>{error}</span>
          </div>
          <button
            onClick={() => setSimulationMode(true)}
            className="px-3 py-1 bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-300 rounded-lg text-xs font-bold transition"
          >
            Switch to Simulation Mode
          </button>
        </div>
      )}

      {/* Spray Window Intelligence Panel */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3.5 border-b border-slate-200">
          <div>
            <div className="flex items-center gap-2">
              <span className={`w-2.5 h-2.5 rounded-full ${
                isSprayWindowOptimal === true ? 'bg-emerald-500 animate-pulse' : (isSprayWindowOptimal === false ? 'bg-amber-500' : 'bg-slate-400')
              }`}></span>
              <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900">
                Pesticide & Foliar Spray Window Evaluation
              </h3>
            </div>
            <p className="text-[11px] text-slate-500 font-sans mt-0.5">
              Calculates spray droplet drift risk and evaporation losses across current humidity and thermal bands
            </p>
          </div>
          <span className={`text-[10px] font-mono px-3 py-1 rounded font-bold border uppercase ${
            isSprayWindowOptimal === true
              ? 'bg-emerald-50 text-emerald-700 border-emerald-200' 
              : isSprayWindowOptimal === false
              ? 'bg-amber-50 text-amber-700 border-amber-200'
              : 'bg-slate-100 text-slate-600 border-slate-200'
          }`}>
            {isSprayWindowOptimal === true ? 'Optimal Spray Window Active' : (isSprayWindowOptimal === false ? 'Spray Window Marginal' : 'Telemetry Offline')}
          </span>
        </div>

        {/* Evaluation Metrics Breakdown */}
        {current ? (
          <>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
              <div className={`p-3.5 rounded-xl border ${windSafe ? 'bg-slate-50 border-slate-200' : 'bg-rose-50 border-rose-200'}`}>
                <span className="text-[10px] text-slate-500 uppercase block font-semibold">Wind Drift Hazard</span>
                <span className="text-lg font-bold text-slate-900">{wind} km/h</span>
                <span className={`text-[11px] block mt-1 ${windSafe ? 'text-emerald-700' : 'text-rose-700 font-bold'}`}>
                  {windSafe ? '✓ Within 3–15 km/h limit' : '⚠ Drift risk exceeds threshold'}
                </span>
              </div>

              <div className={`p-3.5 rounded-xl border ${rainSafe ? 'bg-slate-50 border-slate-200' : 'bg-rose-50 border-rose-200'}`}>
                <span className="text-[10px] text-slate-500 uppercase block font-semibold">Wash-Off Rain Risk</span>
                <span className="text-lg font-bold text-slate-900">{rainChance}%</span>
                <span className={`text-[11px] block mt-1 ${rainSafe ? 'text-emerald-700' : 'text-rose-700 font-bold'}`}>
                  {rainSafe ? '✓ Rain chance < 25%' : '⚠ Foliar wash-off danger'}
                </span>
              </div>

              <div className={`p-3.5 rounded-xl border ${tempSafe ? 'bg-slate-50 border-slate-200' : 'bg-rose-50 border-rose-200'}`}>
                <span className="text-[10px] text-slate-500 uppercase block font-semibold">Thermal Evaporation</span>
                <span className="text-lg font-bold text-slate-900">{temp}°C</span>
                <span className={`text-[11px] block mt-1 ${tempSafe ? 'text-emerald-700' : 'text-rose-700 font-bold'}`}>
                  {tempSafe ? '✓ Below 32°C threshold' : '⚠ High vapor droplet loss'}
                </span>
              </div>

              <div className={`p-3.5 rounded-xl border ${humiditySafe ? 'bg-slate-50 border-slate-200' : 'bg-rose-50 border-rose-200'}`}>
                <span className="text-[10px] text-slate-500 uppercase block font-semibold">Relative Humidity</span>
                <span className="text-lg font-bold text-slate-900">{humidity}%</span>
                <span className={`text-[11px] block mt-1 ${humiditySafe ? 'text-emerald-700' : 'text-amber-700 font-bold'}`}>
                  {humiditySafe ? '✓ Optimal 40–80% band' : '⚠ Marginal droplet retention'}
                </span>
              </div>
            </div>

            {/* Explainable Rationale */}
            <div className="p-4 bg-emerald-50/50 rounded-xl border border-emerald-100 text-xs font-sans text-slate-700 leading-relaxed">
              <span className="font-mono text-emerald-800 font-bold block mb-1 text-xs">
                Meteorological Recommendation:
              </span>
              {isSprayWindowOptimal ? (
                <p>
                  Current microclimate parameters in {district} are within the safe threshold band for foliar systemic fungicide or insecticide application. Safe application window remains open until 11:30 IST before afternoon canopy thermal convection peaks.
                </p>
              ) : (
                <p>
                  Avoid foliar applications during current window. Recommend delaying until early morning (06:00–08:30 IST) when wind speeds fall below 10 km/h and thermal updrafts stabilize.
                </p>
              )}
            </div>
          </>
        ) : (
          <div className="p-8 text-center bg-slate-50 rounded-xl border border-dashed border-slate-300 text-xs font-mono text-slate-500 space-y-3">
            <p>Station telemetry offline. Microclimate spray window evaluation requires active Open-Meteo or IoT probe telemetry.</p>
            <button
              onClick={() => setSimulationMode(true)}
              className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-bold transition shadow-sm"
            >
              Activate Simulation Mode to Inspect Sample Window
            </button>
          </div>
        )}
      </div>

      {/* 7-Day Microclimate Trend Table */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
        <div className="flex items-center justify-between pb-3.5 border-b border-slate-200 mb-4">
          <div>
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
              <Calendar className="w-4 h-4 text-emerald-600" />
              <span>7-Day Agricultural Microclimate Forecast</span>
            </h3>
            <p className="text-[11px] text-slate-500 font-sans mt-0.5">Dynamic daily projections for {district}, {state}</p>
          </div>
          <DataTrustBadge type="EXTERNAL SOURCE" source="Open-Meteo Numerical Weather Prediction" />
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3 font-mono text-xs">
          {forecast.map((f, i) => (
            <div key={i} className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between text-center space-y-2">
              <div className="border-b border-slate-200 pb-1.5">
                <span className="text-xs font-bold text-slate-800 block">{f.day}</span>
                <span className="text-[10px] text-slate-500 block">{f.display_date}</span>
              </div>
              <div className="text-2xl py-1">{f.icon}</div>
              <div>
                <span className="text-base font-black text-slate-900 block">{f.temperature}°C</span>
                <span className="text-[10px] text-slate-500 block">{f.temp_range}</span>
              </div>
              <div className="pt-1.5 border-t border-slate-200 text-[11px] font-semibold text-sky-700">
                Rain: {f.rain_chance}%
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
