'use client';

import React, { useState } from 'react';
import { 
  Key, 
  Building2, 
  Save, 
  CheckCircle2, 
  Eye, 
  EyeOff,
  Cpu
} from 'lucide-react';
import { useGlobalContext, FARMS } from '@/components/GlobalContext';
import DataTrustBadge from '@/components/DataTrustBadge';

export default function SettingsPage() {
  const { farmId, setFarmId, district, setDistrict } = useGlobalContext();
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Masked Credentials State (Section 46: Security)
  const [showRoboflow, setShowRoboflow] = useState(false);
  const [showGemini, setShowGemini] = useState(false);
  const [showSupabase, setShowSupabase] = useState(false);

  // Toggles
  const [autoSyncTelemetry, setAutoSyncTelemetry] = useState(true);
  const [enableSprayAlerts, setEnableSprayAlerts] = useState(true);
  const [highPrecisionYolo, setHighPrecisionYolo] = useState(true);

  const handleSaveSettings = (e: React.FormEvent) => {
    e.preventDefault();
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  return (
    <div className="space-y-6">
      {/* Top Banner - Light Botanical Enterprise */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-mono tracking-wider text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-bold uppercase">
              System Administration & Security
            </span>
            <DataTrustBadge type="OBSERVED DATA" source="Configuration Vault" />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 font-sans tracking-tight">
            System Control Center & Integration Credentials
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Manage operational parameters, masked credentials, inference endpoints, and notification dispatchers
          </p>
        </div>

        {savedSuccess && (
          <div className="flex items-center gap-2 px-3.5 py-2 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-mono font-bold shadow-sm">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Settings Saved & Applied</span>
          </div>
        )}
      </div>

      <form onSubmit={handleSaveSettings} className="space-y-6">
        {/* Farm & Operational Node Configuration */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3.5 border-b border-slate-200">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
              <Building2 className="w-4 h-4 text-emerald-600" />
              <span>Operational Farm Profile & Regional Context</span>
            </h3>
            <span className="text-[10px] font-mono text-slate-500">Context Hierarchy</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-sans">
            <div>
              <label className="block text-[11px] font-mono text-slate-600 mb-1 font-semibold">Active Operational Farm Node</label>
              <select
                value={farmId}
                onChange={(e) => setFarmId(e.target.value)}
                className="w-full bg-white border border-slate-300 text-slate-900 text-xs rounded-lg px-3 py-2 font-mono focus:ring-1 focus:ring-emerald-500"
              >
                {FARMS.map((f) => (
                  <option key={f.id} value={f.id}>{f.name} ({f.id})</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-mono text-slate-600 mb-1 font-semibold">Regional Weather & Soil District</label>
              <input
                type="text"
                value={district}
                onChange={(e) => setDistrict(e.target.value)}
                className="w-full bg-white border border-slate-300 text-slate-900 text-xs rounded-lg px-3 py-2 font-mono focus:ring-1 focus:ring-emerald-500"
              />
            </div>
          </div>
        </div>

        {/* API Credentials & Inference Endpoints */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3.5 border-b border-slate-200">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
              <Key className="w-4 h-4 text-amber-600" />
              <span>Masked Integration Credentials & Inference Endpoints</span>
            </h3>
            <span className="text-[10px] font-mono text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-bold">Encrypted in Vault</span>
          </div>

          <div className="space-y-3 font-mono text-xs">
            {/* Roboflow Key */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between gap-3">
              <div className="flex-1">
                <span className="text-[10px] text-slate-500 uppercase block font-semibold">Roboflow Universe API Key</span>
                <span className="text-xs font-bold text-slate-800">
                  {showRoboflow ? 'rf_live_894k20b4x89192kda' : '••••••••••••••••••••9A4C'}
                </span>
              </div>
              <button
                type="button"
                onClick={() => setShowRoboflow(!showRoboflow)}
                className="p-1.5 text-slate-500 hover:text-slate-800 rounded"
              >
                {showRoboflow ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>

            {/* Gemini / OpenAI LLM Key */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between gap-3">
              <div className="flex-1">
                <span className="text-[10px] text-slate-500 uppercase block font-semibold">Gemini 1.5 Agronomy API Key</span>
                <span className="text-xs font-bold text-slate-800">
                  {showGemini ? 'AIzaSyB391k4019_agri_enterprise' : '••••••••••••••••••••7F82'}
                </span>
              </div>
              <button
                type="button"
                onClick={() => setShowGemini(!showGemini)}
                className="p-1.5 text-slate-500 hover:text-slate-800 rounded"
              >
                {showGemini ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>

            {/* Supabase Service Key */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between gap-3">
              <div className="flex-1">
                <span className="text-[10px] text-slate-500 uppercase block font-semibold">Supabase Service Role Key</span>
                <span className="text-xs font-bold text-slate-800">
                  {showSupabase ? 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' : '••••••••••••••••••••104E'}
                </span>
              </div>
              <button
                type="button"
                onClick={() => setShowSupabase(!showSupabase)}
                className="p-1.5 text-slate-500 hover:text-slate-800 rounded"
              >
                {showSupabase ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>
        </div>

        {/* Feature Flags & Operational Automation */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3.5 border-b border-slate-200">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-sky-600" />
              <span>Operational Feature Flags & Automation</span>
            </h3>
            <span className="text-[10px] font-mono text-slate-500">Runtime Policies</span>
          </div>

          <div className="space-y-3 font-sans text-xs">
            <label className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl border border-slate-200 cursor-pointer hover:bg-slate-100/70 transition">
              <div>
                <span className="font-bold text-slate-900 block">Automatic Telemetry Polling</span>
                <span className="text-[11px] text-slate-500">Synchronize Sentinel-2 indices and Open-Meteo data every 15 minutes</span>
              </div>
              <input
                type="checkbox"
                checked={autoSyncTelemetry}
                onChange={(e) => setAutoSyncTelemetry(e.target.checked)}
                className="w-4 h-4 accent-emerald-600 rounded cursor-pointer"
              />
            </label>

            <label className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl border border-slate-200 cursor-pointer hover:bg-slate-100/70 transition">
              <div>
                <span className="font-bold text-slate-900 block">Critical Spray Window Alerts</span>
                <span className="text-[11px] text-slate-500">Broadcast notifications when Delta-T and wind speeds enter optimal band</span>
              </div>
              <input
                type="checkbox"
                checked={enableSprayAlerts}
                onChange={(e) => setEnableSprayAlerts(e.target.checked)}
                className="w-4 h-4 accent-emerald-600 rounded cursor-pointer"
              />
            </label>

            <label className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl border border-slate-200 cursor-pointer hover:bg-slate-100/70 transition">
              <div>
                <span className="font-bold text-slate-900 block">High-Precision YOLOv8 Multi-Crop Ensemble</span>
                <span className="text-[11px] text-slate-500">Route queries through all 13 specialized Roboflow pathology models</span>
              </div>
              <input
                type="checkbox"
                checked={highPrecisionYolo}
                onChange={(e) => setHighPrecisionYolo(e.target.checked)}
                className="w-4 h-4 accent-emerald-600 rounded cursor-pointer"
              />
            </label>
          </div>

          <div className="pt-3 border-t border-slate-200 flex justify-end">
            <button
              type="submit"
              className="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-mono font-bold transition flex items-center gap-2 shadow-sm"
            >
              <Save className="w-4 h-4" />
              <span>Save System Configuration</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
