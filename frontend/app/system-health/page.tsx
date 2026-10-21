'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Activity, 
  Server, 
  Database, 
  Cpu, 
  Layers, 
  RefreshCw,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  HelpCircle
} from 'lucide-react';
import DataTrustBadge from '@/components/DataTrustBadge';
import { useGlobalContext } from '@/components/GlobalContext';
import { getHealthStatus, HealthStatusResponse, ServiceProbe } from '@/lib/api';

export default function SystemHealthPage() {
  const { isSimulationMode, setSimulationMode } = useGlobalContext();
  const [health, setHealth] = useState<HealthStatusResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [clientLatency, setClientLatency] = useState<number | null>(null);
  const [lastCheckTime, setLastCheckTime] = useState<string>('Just now');

  const checkHealth = useCallback(async () => {
    setLoading(true);
    const t0 = performance.now();
    try {
      const data = await getHealthStatus();
      const elapsed = Math.round(performance.now() - t0);
      setClientLatency(elapsed);
      setHealth(data);
      setError(null);
    } catch (err: unknown) {
      const elapsed = Math.round(performance.now() - t0);
      setClientLatency(elapsed);
      if (isSimulationMode) {
        // Benchmark simulation telemetry
        setHealth({
          status: 'ok',
          app_name: 'AgriPredict AI Gateway (Simulated)',
          version: 'v1.4.2-sim',
          environment: 'simulation',
          gateway_latency_ms: 1.8,
          uptime_seconds: 4820,
          database: {
            supabase: 'connected',
            latency_ms: 72.4,
          },
          models: {
            climate_risk_model: 'loaded',
            encoders: 'loaded',
            crop_recommendation: 'active (physics/dataset calibrated)',
            yield_prediction: 'active (FAO calibrated)',
            irrigation: 'active (FAO-56 Penman-Monteith)',
            market_price: 'active (APMC seasonal Prophet)',
          },
          data_sources: {
            weather_csv: 'available',
            chroma_vector_db: 'available',
          },
          services: [
            { name: 'FastAPI Gateway', role: 'Core Inference Engine', status: 'Operational', latency_ms: 1.8, details: 'Simulated Gateway Node' },
            { name: 'Supabase PostgreSQL', role: 'Cloud Persistence & Telemetry', status: 'Operational', latency_ms: 72.4, details: 'Simulated Cloud Pool' },
            { name: 'ChromaDB Store', role: 'RAG Agronomic Embeddings', status: 'Operational', latency_ms: 2.1, details: 'Vector Store Benchmark' },
            { name: 'Open-Meteo & Weather Pipeline', role: 'Microclimate Ingestion', status: 'Operational', latency_ms: 45.0, details: 'Grid Resolution: 0.1 deg' },
            { name: 'Roboflow Vision Service', role: 'Plant Pathology YOLOv8', status: 'Operational', latency_ms: 210.0, details: 'Simulated Model Endpoint' },
          ],
        });
        setError(null);
      } else {
        setHealth(null);
        setError(err instanceof Error ? err.message : 'Backend connection refused at http://127.0.0.1:8000.');
      }
    } finally {
      setLoading(false);
      setLastCheckTime(new Intl.DateTimeFormat('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(new Date()));
    }
  }, [isSimulationMode]);

  useEffect(() => {
    checkHealth();
  }, [checkHealth]);

  const getServiceIcon = (name: string) => {
    if (name.toLowerCase().includes('database') || name.toLowerCase().includes('supabase')) return Database;
    if (name.toLowerCase().includes('chroma') || name.toLowerCase().includes('store')) return Layers;
    if (name.toLowerCase().includes('vision') || name.toLowerCase().includes('roboflow')) return Cpu;
    if (name.toLowerCase().includes('weather') || name.toLowerCase().includes('meteo')) return Activity;
    return Server;
  };

  const getStatusBadge = (status: string) => {
    const s = status.toLowerCase();
    if (s.includes('operational') || s === 'ok' || s === 'connected' || s === 'available' || s === 'loaded' || s.includes('active')) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
          <CheckCircle2 className="w-3 h-3 text-emerald-600" />
          <span>Operational</span>
        </span>
      );
    }
    if (s.includes('degraded')) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-50 text-amber-700 border border-amber-200">
          <AlertTriangle className="w-3 h-3 text-amber-600" />
          <span>Degraded</span>
        </span>
      );
    }
    if (s.includes('unconfigured') || s.includes('unset')) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-slate-100 text-slate-600 border border-slate-200">
          <HelpCircle className="w-3 h-3 text-slate-400" />
          <span>Unconfigured</span>
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-50 text-rose-700 border border-rose-200">
        <XCircle className="w-3 h-3 text-rose-600" />
        <span>Offline</span>
      </span>
    );
  };

  return (
    <div className="space-y-6">
      {/* Top Banner - Light Botanical Enterprise */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-mono tracking-wider text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-bold uppercase">
              Technical Observability & Health
            </span>
            <DataTrustBadge 
              type={isSimulationMode ? "SIMULATION / DEMO" : (health ? "OBSERVED DATA" : "DATA UNAVAILABLE")} 
              source={isSimulationMode ? "Synthetic Telemetry Simulator" : "Live HTTP Diagnostic Probes"} 
            />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 font-sans tracking-tight">
            Microservice Dependency Graph & SLA Metrics
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Gateway: {health?.app_name || 'FastAPI Microservice Node'} • Status: {health?.status === 'ok' ? 'Online' : (loading ? 'Probing' : 'Offline')} • Environment: {health?.environment || 'production'}
          </p>
        </div>

        <button
          onClick={checkHealth}
          disabled={loading}
          className="px-4 py-2 bg-white hover:bg-slate-50 disabled:opacity-50 text-slate-800 rounded-lg text-xs font-semibold font-mono transition flex items-center gap-2 border border-slate-300 shadow-sm"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-emerald-600' : 'text-slate-500'}`} />
          <span>Probe Gateway ({lastCheckTime})</span>
        </button>
      </div>

      {/* Offline Alert Box */}
      {error && !isSimulationMode && (
        <div className="p-5 bg-rose-50 border border-rose-200 rounded-xl text-xs font-mono text-rose-900 space-y-3">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0" />
            <span className="font-bold text-sm">FastAPI Inference Gateway Unreachable</span>
          </div>
          <p className="text-slate-700 leading-relaxed font-sans">
            The frontend attempted a live HTTP GET request to <code className="px-1.5 py-0.5 bg-white border border-slate-200 rounded font-mono text-rose-700">/api/v1/health</code> but the connection was refused. 
            Ensure the Python backend is running locally with <code className="px-1.5 py-0.5 bg-white border border-slate-200 rounded font-mono text-emerald-700 font-bold">python app.py</code> or switch to Simulation Mode.
          </p>
          <div className="flex items-center gap-3 pt-1">
            <button
              onClick={checkHealth}
              className="px-3.5 py-1.5 bg-rose-700 hover:bg-rose-800 text-white rounded-lg text-xs font-bold transition shadow-sm"
            >
              Retry Connection
            </button>
            <button
              onClick={() => setSimulationMode(true)}
              className="px-3.5 py-1.5 bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 rounded-lg text-xs font-bold transition shadow-sm"
            >
              Switch to Simulation Mode
            </button>
          </div>
        </div>
      )}

      {/* Latency & SLA Real-Time Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-sm">
          <span className="text-[10px] text-slate-500 uppercase block font-semibold">Client-to-Gateway SLA</span>
          <span className="text-2xl font-black text-emerald-700">
            {clientLatency != null ? `${clientLatency} ms` : 'Offline'}
          </span>
          <span className="text-[10px] text-slate-500 block mt-1">HTTP Round-Trip Latency</span>
        </div>

        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-sm">
          <span className="text-[10px] text-slate-500 uppercase block font-semibold">Gateway Internal Time</span>
          <span className="text-2xl font-black text-slate-900">
            {health?.gateway_latency_ms != null ? `${health.gateway_latency_ms} ms` : 'N/A'}
          </span>
          <span className="text-[10px] text-emerald-700 block mt-1 font-semibold">Python Profiling Trace</span>
        </div>

        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-sm">
          <span className="text-[10px] text-slate-500 uppercase block font-semibold">Database Ping</span>
          <span className="text-2xl font-black text-sky-700">
            {health?.database?.latency_ms != null ? `${health.database.latency_ms} ms` : (health?.database?.supabase === 'connected' ? '< 50 ms' : 'Unconfigured')}
          </span>
          <span className="text-[10px] text-slate-500 block mt-1">Supabase PostgreSQL</span>
        </div>

        <div className="p-4 bg-white border border-slate-200 rounded-xl shadow-sm">
          <span className="text-[10px] text-slate-500 uppercase block font-semibold">Active ML Registry</span>
          <span className="text-2xl font-black text-amber-700">
            {health?.models ? `${Object.values(health.models).filter((v) => v.includes('active') || v.includes('loaded')).length} / 6` : '0 Ready'}
          </span>
          <span className="text-[10px] text-slate-500 block mt-1">Pipelines Operational</span>
        </div>
      </div>

      {/* Service Dependency Graph */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3.5 border-b border-slate-200">
          <div>
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
              <Layers className="w-4 h-4 text-emerald-600" />
              <span>Agricultural Microservice Dependency Graph</span>
            </h3>
            <p className="text-[11px] text-slate-500 font-sans mt-0.5">Real-time health probes across live microservices</p>
          </div>
          <span className="text-[10px] font-mono px-2.5 py-1 bg-slate-50 text-slate-700 border border-slate-200 rounded font-bold">
            {health?.services ? `${health.services.filter(s => s.status.toLowerCase().includes('operational')).length} of ${health.services.length} Healthy` : 'Probes Offline'}
          </span>
        </div>

        {/* Microservices Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 font-mono text-xs">
          {(health?.services || [
            { name: 'FastAPI Gateway', role: 'Core Inference Engine', status: 'Offline', latency_ms: null, details: 'Endpoint /api/v1/health' },
            { name: 'Supabase PostgreSQL', role: 'Cloud Persistence & Telemetry', status: 'Unconfigured', latency_ms: null, details: 'Configured in backend/.env' },
            { name: 'ChromaDB Store', role: 'RAG Agronomic Embeddings', status: 'Unconfigured', latency_ms: null, details: 'Vector Knowledge Store' },
            { name: 'Open-Meteo API', role: 'Microclimate Ingestion', status: 'Degraded', latency_ms: null, details: 'Weather station client' },
            { name: 'Roboflow Vision', role: 'Plant Pathology YOLOv8', status: 'Unconfigured', latency_ms: null, details: 'Roboflow API token' },
          ]).map((srv: ServiceProbe, i: number) => {
            const Icon = getServiceIcon(srv.name);
            const isHealthy = srv.status.toLowerCase().includes('operational');

            return (
              <div key={i} className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between space-y-3">
                <div className="flex items-center justify-between">
                  <div className="p-2 rounded-lg bg-white text-emerald-700 border border-slate-200 shadow-sm">
                    <Icon className="w-4 h-4" />
                  </div>
                  {getStatusBadge(srv.status)}
                </div>

                <div>
                  <h4 className="font-bold text-slate-900 text-sm truncate font-sans">{srv.name}</h4>
                  <span className="text-[10px] text-slate-500 block truncate">{srv.role}</span>
                  {srv.details && (
                    <span className="text-[10px] text-slate-400 block truncate mt-0.5 font-sans">{srv.details}</span>
                  )}
                </div>

                <div className="pt-2 border-t border-slate-200 flex items-center justify-between text-[10px]">
                  <span className="text-slate-500">Latency:</span>
                  <span className={`font-bold ${isHealthy ? 'text-emerald-700' : 'text-slate-500'}`}>
                    {srv.latency_ms != null ? `${srv.latency_ms} ms` : 'N/A'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Model Registry & Data Sources Breakdown */}
      {health?.models && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono text-xs">
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 mb-3 pb-2 border-b border-slate-200">
              Active Agronomic Models
            </h3>
            <div className="space-y-2">
              {Object.entries(health.models).map(([modelKey, modelStatus]) => (
                <div key={modelKey} className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                  <span className="text-slate-800 capitalize font-sans text-xs">{modelKey.replace(/_/g, ' ')}</span>
                  {getStatusBadge(modelStatus)}
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 mb-3 pb-2 border-b border-slate-200">
              Connected Data Sources & Embeddings
            </h3>
            <div className="space-y-2">
              {Object.entries(health.data_sources || {}).map(([sourceKey, sourceStatus]) => (
                <div key={sourceKey} className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                  <span className="text-slate-800 capitalize font-sans text-xs">{sourceKey.replace(/_/g, ' ')}</span>
                  {getStatusBadge(sourceStatus)}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
