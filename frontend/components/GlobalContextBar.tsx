'use client';

import React, { useState } from 'react';
import { useGlobalContext, FARMS } from '@/components/GlobalContext';
import { 
  Building2, 
  Grid, 
  Sprout, 
  Calendar, 
  MapPin, 
  RefreshCw, 
  ChevronDown 
} from 'lucide-react';
import DataTrustBadge from '@/components/DataTrustBadge';

export default function GlobalContextBar() {
  const {
    farmId,
    parcelId,
    crop,
    season,
    district,
    state,
    lastSynced,
    systemStatus,
    isSimulationMode,
    setSimulationMode,
    setFarmId,
    setParcelId,
    triggerSync,
  } = useGlobalContext();

  const [farmDropdownOpen, setFarmDropdownOpen] = useState(false);
  const [parcelDropdownOpen, setParcelDropdownOpen] = useState(false);

  const currentFarm = FARMS.find((f) => f.id === farmId) || FARMS[0];

  return (
    <div className="w-full bg-[#F0F6F0] text-slate-800 border-b border-emerald-100 px-4 py-2 flex flex-wrap items-center justify-between gap-3 text-xs shadow-2xs select-none">
      {/* Context Pills */}
      <div className="flex flex-wrap items-center gap-2 sm:gap-3">
        {/* Farm Selector */}
        <div className="relative">
          <button
            onClick={() => {
              setFarmDropdownOpen(!farmDropdownOpen);
              setParcelDropdownOpen(false);
            }}
            className="flex items-center gap-1.5 px-2.5 py-1 bg-white hover:bg-emerald-50/80 rounded-lg border border-emerald-200/80 font-medium text-[11px] transition text-slate-800 shadow-2xs"
            title="Switch Operational Farm"
          >
            <Building2 className="w-3.5 h-3.5 text-emerald-700" />
            <span className="text-slate-500">Farm:</span>
            <span className="font-bold text-slate-900">{currentFarm.name.split(' ')[0]} Farms ({farmId})</span>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {farmDropdownOpen && (
            <div className="absolute top-9 left-0 w-80 bg-white border border-slate-200 rounded-xl shadow-xl z-50 p-1.5 text-slate-800">
              <div className="px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-500 border-b border-slate-100">
                Switch Operational Farm
              </div>
              {FARMS.map((f) => (
                <button
                  key={f.id}
                  onClick={() => {
                    setFarmId(f.id);
                    setFarmDropdownOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 rounded-lg text-xs transition flex flex-col ${
                    f.id === farmId ? 'bg-emerald-50 text-emerald-900 font-bold border border-emerald-200' : 'hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <span className="font-semibold">{f.name}</span>
                  <span className="text-[10px] text-slate-500 font-mono">{f.id} • {f.district}, {f.state}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Parcel Selector */}
        <div className="relative">
          <button
            onClick={() => {
              setParcelDropdownOpen(!parcelDropdownOpen);
              setFarmDropdownOpen(false);
            }}
            className="flex items-center gap-1.5 px-2.5 py-1 bg-white hover:bg-emerald-50/80 rounded-lg border border-emerald-200/80 font-medium text-[11px] transition text-slate-800 shadow-2xs"
            title="Switch Parcel Focus"
          >
            <Grid className="w-3.5 h-3.5 text-emerald-700" />
            <span className="text-slate-500">Parcel:</span>
            <span className="font-bold text-emerald-900">{parcelId} — 5.2 acres</span>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {parcelDropdownOpen && (
            <div className="absolute top-9 left-0 w-44 bg-white border border-slate-200 rounded-xl shadow-xl z-50 p-1.5 text-slate-800">
              <div className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-500 border-b border-slate-100">
                Active Parcel
              </div>
              {currentFarm.parcels.map((p) => (
                <button
                  key={p}
                  onClick={() => {
                    setParcelId(p);
                    setParcelDropdownOpen(false);
                  }}
                  className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs transition font-mono ${
                    p === parcelId ? 'bg-emerald-50 text-emerald-900 font-bold' : 'hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  Parcel {p}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Crop Pill */}
        <div className="hidden sm:flex items-center gap-1 px-2.5 py-1 bg-white rounded-lg border border-emerald-200/80 text-[11px] font-medium text-slate-800 shadow-2xs">
          <Sprout className="w-3.5 h-3.5 text-emerald-700" />
          <span className="text-slate-500">Crop:</span>
          <span className="font-bold text-slate-900">{crop}</span>
        </div>

        {/* Season Pill */}
        <div className="hidden md:flex items-center gap-1 px-2.5 py-1 bg-white rounded-lg border border-emerald-200/80 text-[11px] font-medium text-slate-800 shadow-2xs">
          <Calendar className="w-3.5 h-3.5 text-emerald-700" />
          <span className="text-slate-500">Season:</span>
          <span className="font-bold text-slate-900">{season}</span>
        </div>

        {/* Location Pill */}
        <div className="hidden lg:flex items-center gap-1 px-2.5 py-1 bg-white rounded-lg border border-emerald-200/80 text-[11px] font-medium text-slate-800 shadow-2xs">
          <MapPin className="w-3.5 h-3.5 text-emerald-700" />
          <span className="text-slate-500">Location:</span>
          <span className="font-semibold text-slate-900">{district}, {state}</span>
        </div>
      </div>

      {/* Right Telemetry Controls */}
      <div className="flex items-center gap-3">
        {/* Sync Telemetry */}
        <button
          onClick={triggerSync}
          className="flex items-center gap-1 text-[11px] text-slate-600 hover:text-emerald-800 transition"
          title="Telemetry Sync with IoT / Cloud Edge"
        >
          <RefreshCw className="w-3 h-3 text-emerald-700" />
          <span className="hidden sm:inline">Sync:</span>
          <span className="font-mono text-slate-700">{lastSynced}</span>
        </button>

        <div className="h-3 w-px bg-slate-300 hidden sm:block"></div>

        {/* Mode Switcher: LIVE PROD vs SIMULATION */}
        <div className="flex items-center gap-1 bg-white p-0.5 rounded-lg border border-slate-200 text-[10px] font-mono shadow-2xs">
          <button
            onClick={() => setSimulationMode(false)}
            className={`px-2 py-0.5 rounded font-bold transition ${
              !isSimulationMode
                ? 'bg-emerald-700 text-white shadow-xs'
                : 'text-slate-500 hover:text-slate-800'
            }`}
            title="Production Mode: Connects to live FastAPI & databases."
          >
            LIVE PROD
          </button>
          <button
            onClick={() => setSimulationMode(true)}
            className={`px-2 py-0.5 rounded font-bold transition ${
              isSimulationMode
                ? 'bg-amber-500 text-white shadow-xs'
                : 'text-slate-500 hover:text-slate-800'
            }`}
            title="Simulation Mode: Pre-configured benchmark dataset for offline evaluation."
          >
            SIMULATION
          </button>
        </div>

        {/* Trust Indicator */}
        <DataTrustBadge 
          type={isSimulationMode ? "SIMULATION / DEMO" : (systemStatus === 'Operational' ? "OBSERVED" : "DATA UNAVAILABLE")} 
          source={isSimulationMode ? "Synthetic Fixture" : "Central Telemetry Bus"} 
        />
      </div>
    </div>
  );
}
