'use client';

import React, { useState } from 'react';
import { useGlobalContext } from '@/components/GlobalContext';
import DataTrustBadge from '@/components/DataTrustBadge';
import { Layers, AlertTriangle, Maximize2, ZoomIn, ZoomOut } from 'lucide-react';

export type MapLayer = 'Satellite' | 'NDVI' | 'NDRE' | 'Thermal' | 'Moisture' | 'Disease' | 'Yield';

interface ParcelMetric {
  id: string;
  name: string;
  crop: string;
  areaAcres: number;
  ndvi: number;
  ndre: number;
  temp: number; // Celsius
  moisture: number; // percentage
  diseaseRisk: 'Low' | 'Moderate' | 'High';
  yieldPrediction: string;
  coordinates: string; // SVG path
}

const SAMPLE_PARCELS: Record<string, ParcelMetric> = {
  A1: { id: 'A1', name: 'North Boundary', crop: 'Cotton', areaAcres: 4.8, ndvi: 0.81, ndre: 0.44, temp: 27.2, moisture: 68, diseaseRisk: 'Low', yieldPrediction: '4.4 t/ha', coordinates: 'M 40 40 L 180 40 L 180 140 L 40 140 Z' },
  A2: { id: 'A2', name: 'Northeast Ridge', crop: 'Cotton', areaAcres: 3.6, ndvi: 0.76, ndre: 0.39, temp: 28.1, moisture: 62, diseaseRisk: 'Low', yieldPrediction: '4.1 t/ha', coordinates: 'M 190 40 L 330 40 L 330 140 L 190 140 Z' },
  A3: { id: 'A3', name: 'Central Basin', crop: 'Paddy', areaAcres: 6.2, ndvi: 0.88, ndre: 0.52, temp: 26.5, moisture: 82, diseaseRisk: 'Low', yieldPrediction: '5.2 t/ha', coordinates: 'M 340 40 L 480 40 L 480 140 L 340 140 Z' },
  A4: { id: 'A4', name: 'South Slope', crop: 'Cotton', areaAcres: 5.2, ndvi: 0.62, ndre: 0.31, temp: 31.4, moisture: 44, diseaseRisk: 'High', yieldPrediction: '3.6 t/ha', coordinates: 'M 40 150 L 180 150 L 180 250 L 40 250 Z' },
  B1: { id: 'B1', name: 'Canal Adjacent', crop: 'Maize', areaAcres: 4.5, ndvi: 0.79, ndre: 0.42, temp: 28.0, moisture: 74, diseaseRisk: 'Moderate', yieldPrediction: '4.8 t/ha', coordinates: 'M 190 150 L 330 150 L 330 250 L 190 250 Z' },
  B2: { id: 'B2', name: 'Southwest Terrace', crop: 'Chilli', areaAcres: 3.2, ndvi: 0.73, ndre: 0.38, temp: 29.8, moisture: 58, diseaseRisk: 'Low', yieldPrediction: '2.9 t/ha', coordinates: 'M 340 150 L 480 150 L 480 250 L 340 250 Z' },
};

export default function InteractiveFieldMap({ onSelectParcel }: { onSelectParcel?: (parcel: ParcelMetric) => void }) {
  const { parcelId, setParcelId, farmId, isSimulationMode, setSimulationMode } = useGlobalContext();
  const [activeLayer, setActiveLayer] = useState<MapLayer>('NDVI');
  const [hoveredParcel, setHoveredParcel] = useState<ParcelMetric | null>(null);
  const [zoomLevel, setZoomLevel] = useState<number>(1);

  const getFillColor = (p: ParcelMetric) => {
    const isSelected = p.id === parcelId;

    if (activeLayer === 'Satellite') {
      return isSelected ? '#15803D' : '#16A34A';
    }
    if (activeLayer === 'NDVI') {
      if (p.ndvi >= 0.8) return isSelected ? '#15803D' : '#22C55E';
      if (p.ndvi >= 0.7) return isSelected ? '#16A34A' : '#4ADE80';
      return isSelected ? '#D97706' : '#FBBF24';
    }
    if (activeLayer === 'NDRE') {
      if (p.ndre >= 0.45) return isSelected ? '#166534' : '#15803D';
      return isSelected ? '#B45309' : '#F59E0B';
    }
    if (activeLayer === 'Thermal') {
      if (p.temp > 30) return isSelected ? '#B91C1C' : '#EF4444';
      if (p.temp > 28) return isSelected ? '#D97706' : '#F59E0B';
      return isSelected ? '#1D4ED8' : '#3B82F6';
    }
    if (activeLayer === 'Moisture') {
      if (p.moisture < 50) return isSelected ? '#DC2626' : '#F87171';
      if (p.moisture < 70) return isSelected ? '#0284C7' : '#38BDF8';
      return isSelected ? '#2563EB' : '#60A5FA';
    }
    if (activeLayer === 'Disease') {
      if (p.diseaseRisk === 'High') return isSelected ? '#DC2626' : '#EF4444';
      if (p.diseaseRisk === 'Moderate') return isSelected ? '#D97706' : '#F59E0B';
      return isSelected ? '#15803D' : '#22C55E';
    }
    if (activeLayer === 'Yield') {
      return isSelected ? '#047857' : '#10B981';
    }
    return '#16A34A';
  };

  const currentParcel = SAMPLE_PARCELS[parcelId] || SAMPLE_PARCELS.A4;

  const handleParcelClick = (p: ParcelMetric) => {
    setParcelId(p.id);
    if (onSelectParcel) {
      onSelectParcel(p);
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-xs text-slate-800">
      {/* Map Control Bar */}
      <div className="px-4 py-3 bg-slate-50/80 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <div className="p-1 rounded-lg bg-emerald-100/80 text-emerald-800">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <span className="text-xs font-bold text-slate-900 uppercase tracking-wider font-mono">
              Field Intelligence Map
            </span>
            <span className="text-[11px] text-slate-500 font-mono hidden sm:inline ml-2">
              Farm {farmId} • Layer: {activeLayer}
            </span>
          </div>
          <DataTrustBadge 
            type={isSimulationMode ? "SIMULATION / DEMO" : "DATA UNAVAILABLE"} 
            source={isSimulationMode ? "Calibrated Sentinel-2 Vector" : "Satellite Service Offline"} 
          />
        </div>

        {/* Layer Switches */}
        {isSimulationMode && (
          <div className="flex items-center gap-1 bg-white p-1 rounded-xl border border-slate-200 text-xs font-mono shadow-2xs">
            {(['Satellite', 'NDVI', 'NDRE', 'Thermal', 'Moisture', 'Disease', 'Yield'] as MapLayer[]).map((layer) => (
              <button
                key={layer}
                onClick={() => setActiveLayer(layer)}
                className={`px-2 py-1 rounded-lg transition-all font-semibold ${
                  activeLayer === layer
                    ? 'bg-emerald-700 text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                {layer}
              </button>
            ))}
          </div>
        )}
      </div>

      {!isSimulationMode ? (
        <div className="p-10 text-center bg-slate-50/60 flex flex-col items-center justify-center min-h-[300px]">
          <div className="w-12 h-12 rounded-2xl bg-amber-100 border border-amber-300 flex items-center justify-center text-amber-800 mb-3 shadow-2xs">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider font-mono">
            Satellite Multispectral Telemetry Unavailable
          </h3>
          <p className="text-xs text-slate-600 max-w-lg mt-2 mb-4 leading-relaxed font-sans">
            In Live Production Mode, multispectral layers require an active Sentinel-2 / Landsat-9 API connection or drone orthomosaic ingestion for Farm {farmId}. Synthetic parcel indices are isolated in Simulation Mode to prevent data fabrication.
          </p>
          <button
            onClick={() => setSimulationMode(true)}
            className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-xl transition shadow-xs"
          >
            Activate Simulation Mode to Inspect Sample Parcels
          </button>
        </div>
      ) : (
        /* SVG Map Canvas & Inspector Split View */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-0">
          {/* SVG Field Grid */}
          <div className="lg:col-span-2 p-4 bg-[#F2F6F2] flex flex-col items-center justify-center relative min-h-[320px]">
            <div className="w-full mb-2 flex items-center justify-between text-[10px] font-mono text-amber-900 bg-amber-50 px-3 py-1.5 rounded-lg border border-amber-200 shadow-2xs">
              <span>⚠️ SIMULATION MODE: Displaying synthetic multispectral parcel topology for {farmId}</span>
              <span className="font-bold uppercase">Benchmark Only</span>
            </div>

            {/* Map Canvas with SVG Geometry */}
            <div className="relative w-full max-w-xl">
              <svg
                viewBox="0 0 520 290"
                style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'center center', transition: 'transform 0.2s ease' }}
                className="w-full h-auto drop-shadow-sm select-none"
              >
                {/* Field Boundary Background */}
                <rect x="25" y="25" width="470" height="240" rx="14" fill="#E2EBE2" stroke="#CBD5E1" strokeWidth="2" />

                {/* Parcels */}
                {Object.values(SAMPLE_PARCELS).map((p) => {
                  const isSelected = p.id === parcelId;
                  const fillColor = getFillColor(p);

                  return (
                    <g key={p.id}>
                      <path
                        d={p.coordinates}
                        fill={fillColor}
                        fillOpacity={isSelected ? 1 : 0.85}
                        stroke={isSelected ? '#0F172A' : '#FFFFFF'}
                        strokeWidth={isSelected ? 3 : 1.5}
                        className="cursor-pointer transition-all duration-150 hover:fill-opacity-100"
                        onClick={() => handleParcelClick(p)}
                        onMouseEnter={() => setHoveredParcel(p)}
                        onMouseLeave={() => setHoveredParcel(null)}
                      />
                      {/* Parcel ID */}
                      <text
                        x={
                          p.id === 'A1' || p.id === 'A4' ? 110 :
                          p.id === 'A2' || p.id === 'B1' ? 260 : 410
                        }
                        y={p.id.startsWith('A') ? 85 : 195}
                        textAnchor="middle"
                        fill="#FFFFFF"
                        fontSize="14"
                        fontWeight="bold"
                        fontFamily="monospace"
                        pointerEvents="none"
                        className="drop-shadow-xs"
                      >
                        {p.id}
                      </text>
                      {/* Parcel Crop Name */}
                      <text
                        x={
                          p.id === 'A1' || p.id === 'A4' ? 110 :
                          p.id === 'A2' || p.id === 'B1' ? 260 : 410
                        }
                        y={p.id.startsWith('A') ? 105 : 215}
                        textAnchor="middle"
                        fill="#F8FAFC"
                        fontSize="10"
                        fontWeight="600"
                        pointerEvents="none"
                        className="drop-shadow-xs"
                      >
                        {p.crop} ({p.areaAcres} ac)
                      </text>
                    </g>
                  );
                })}
              </svg>

              {/* Floating Canvas Controls */}
              <div className="absolute bottom-2 right-2 flex items-center gap-1 bg-white/90 backdrop-blur-sm p-1 rounded-xl border border-slate-200 shadow-xs">
                <button
                  onClick={() => setZoomLevel((z) => Math.max(0.8, z - 0.1))}
                  className="p-1 hover:bg-slate-100 text-slate-600 rounded"
                  title="Zoom Out"
                >
                  <ZoomOut className="w-3.5 h-3.5" />
                </button>
                <span className="text-[10px] font-mono px-1 text-slate-700">{Math.round(zoomLevel * 100)}%</span>
                <button
                  onClick={() => setZoomLevel((z) => Math.min(1.5, z + 0.1))}
                  className="p-1 hover:bg-slate-100 text-slate-600 rounded"
                  title="Zoom In"
                >
                  <ZoomIn className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => setZoomLevel(1)}
                  className="p-1 hover:bg-slate-100 text-slate-600 rounded ml-1"
                  title="Reset Zoom"
                >
                  <Maximize2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Layer Legend Strip */}
            <div className="mt-3 flex flex-wrap items-center justify-center gap-4 text-[10px] font-mono text-slate-600">
              <span className="font-bold uppercase tracking-wider text-slate-500">Legend:</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-emerald-600"></span> High Biomass / Safe</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Moderate Stress</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-rose-600"></span> Pathology Anomaly</span>
            </div>
          </div>

          {/* Right Inspector Panel */}
          <div className="p-4 bg-slate-50/70 border-l border-slate-200 flex flex-col justify-between text-slate-800">
            <div>
              <div className="flex items-start justify-between pb-3 border-b border-slate-200 mb-3">
                <div>
                  <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider">Active Parcel</span>
                  <h4 className="text-base font-bold text-slate-900 flex items-center gap-2">
                    <span>Parcel {currentParcel.id}</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-700 font-normal">
                      {currentParcel.name}
                    </span>
                  </h4>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold text-emerald-800 block">{currentParcel.crop}</span>
                  <span className="text-[10px] text-slate-500 font-mono">{currentParcel.areaAcres} acres</span>
                </div>
              </div>

              {/* Dense Telemetry Grid */}
              <div className="grid grid-cols-2 gap-2 text-xs font-mono mb-4">
                <div className="p-2.5 bg-white rounded-xl border border-slate-200 shadow-2xs">
                  <span className="text-[10px] text-slate-500 block">NDVI Biomass</span>
                  <span className={`text-sm font-bold ${currentParcel.ndvi >= 0.75 ? 'text-emerald-700' : 'text-amber-700'}`}>
                    {currentParcel.ndvi.toFixed(2)}
                  </span>
                  <span className="text-[9px] text-slate-400 block mt-0.5">Canopy vigour</span>
                </div>

                <div className="p-2.5 bg-white rounded-xl border border-slate-200 shadow-2xs">
                  <span className="text-[10px] text-slate-500 block">NDRE Chlorophyll</span>
                  <span className="text-sm font-bold text-sky-700">
                    {currentParcel.ndre.toFixed(2)}
                  </span>
                  <span className="text-[9px] text-slate-400 block mt-0.5">Nitrogen index</span>
                </div>

                <div className="p-2.5 bg-white rounded-xl border border-slate-200 shadow-2xs">
                  <span className="text-[10px] text-slate-500 block">Thermal Canopy</span>
                  <span className="text-sm font-bold text-slate-800">
                    {currentParcel.temp.toFixed(1)}°C
                  </span>
                  <span className="text-[9px] text-slate-400 block mt-0.5">Infrared probe</span>
                </div>

                <div className="p-2.5 bg-white rounded-xl border border-slate-200 shadow-2xs">
                  <span className="text-[10px] text-slate-500 block">Root Moisture</span>
                  <span className={`text-sm font-bold ${currentParcel.moisture < 50 ? 'text-rose-700' : 'text-emerald-700'}`}>
                    {currentParcel.moisture}%
                  </span>
                  <span className="text-[9px] text-slate-400 block mt-0.5">0–30 cm profile</span>
                </div>
              </div>

              {/* Pathology Alert Card */}
              <div className={`p-3 rounded-xl border flex items-start gap-2.5 text-xs ${
                currentParcel.diseaseRisk === 'High'
                  ? 'bg-rose-50 border-rose-200 text-rose-900'
                  : currentParcel.diseaseRisk === 'Moderate'
                  ? 'bg-amber-50 border-amber-200 text-amber-900'
                  : 'bg-emerald-50 border-emerald-200 text-emerald-900'
              }`}>
                <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold block">Status: {currentParcel.diseaseRisk} Risk</span>
                  <span className="text-[11px] leading-tight opacity-90 block mt-0.5 font-sans">
                    {currentParcel.diseaseRisk === 'High' 
                      ? 'Spectral anomaly detected on southern boundary. Field scouting recommended.'
                      : 'Canopy vegetative reflectance is homogeneous without foliar pathogen signatures.'}
                  </span>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-200 flex items-center justify-between text-[10px] font-mono text-slate-500 mt-4">
              <span>Hover: {hoveredParcel ? `Parcel ${hoveredParcel.id}` : 'None'}</span>
              <span className="text-emerald-800 font-bold">Yield: {currentParcel.yieldPrediction}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
