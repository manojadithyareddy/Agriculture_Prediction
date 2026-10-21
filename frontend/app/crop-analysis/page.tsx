'use client';

import React, { useState } from 'react';
import { useGlobalContext } from '@/components/GlobalContext';
import DataTrustBadge from '@/components/DataTrustBadge';
import InteractiveFieldMap from '@/components/InteractiveFieldMap';
import ContextualInspector from '@/components/ContextualInspector';
import { 
  Calendar, 
  ShieldAlert,
  ChevronRight
} from 'lucide-react';

interface Anomaly {
  id: string;
  parcel: string;
  crop: string;
  severity: 'HIGH' | 'MODERATE' | 'LOW';
  confidence: number;
  type: string;
  detectedAt: string;
  spectralSignature: string;
  possibleCauses: string[];
  evidence: string[];
  recommendedInspection: string;
}

const SAMPLE_ANOMALIES: Anomaly[] = [
  {
    id: 'ANOM-0481',
    parcel: 'A4',
    crop: 'Cotton',
    severity: 'HIGH',
    confidence: 94.2,
    type: 'Localized Canopy Desiccation & Chlorophyll Drop',
    detectedAt: 'Today 08:30 IST',
    spectralSignature: 'NDVI dropped 0.74 → 0.62 in 48h; Red-Edge shift detected',
    possibleCauses: [
      'Early foliar pathogen invasion (Cercospora or Alternaria)',
      'Subsurface drip line localized clogging causing water stress',
      'Micro-nutrient deficiency (Magnesium / Potassium)'
    ],
    evidence: [
      'Sentinel-2 L2A Band 4/8 anomaly',
      'Canopy thermal delta: +3.3°C above parcel average',
      'Microclimate: 84% night humidity promoting fungal incubation'
    ],
    recommendedInspection: 'Inspect south-east perimeter of Parcel A4 (Rows 12–28). Check emitter pressure at lateral manifold and inspect lower canopy for circular lesions with concentric rings.'
  },
  {
    id: 'ANOM-0479',
    parcel: 'B1',
    crop: 'Maize',
    severity: 'MODERATE',
    confidence: 88.5,
    type: 'Canopy Nitrogen Heterogeneity',
    detectedAt: 'Yesterday 14:15 IST',
    spectralSignature: 'NDRE index depression along canal boundary (0.42 → 0.35)',
    possibleCauses: [
      'Fertilizer leaching due to drainage runoff near canal',
      'Uneven basal urea top-dressing application'
    ],
    evidence: [
      'NDRE vegetative index dip',
      'Recent precipitation: 22 mm runoff on canal-facing slope'
    ],
    recommendedInspection: 'Inspect border rows adjacent to drainage canal. Check for interveinal chlorosis.'
  }
];

export default function CropAnalysisPage() {
  const { farmId, parcelId, crop, district, state, isSimulationMode } = useGlobalContext();
  const [selectedAnomaly, setSelectedAnomaly] = useState<Anomaly | null>(null);
  const [comparisonMode, setComparisonMode] = useState<boolean>(false);
  const [timeStep, setTimeStep] = useState<string>('T0'); // T0 (current), T-7d, T-14d

  const spectralMetrics = isSimulationMode ? [
    { name: 'NDVI Biomass', current: '0.78', previous: '0.74', delta: '+0.04', status: 'Optimal' },
    { name: 'NDRE Chlorophyll', current: '0.41', previous: '0.38', delta: '+0.03', status: 'Optimal' },
    { name: 'Canopy Coverage', current: '84%', previous: '81%', delta: '+3%', status: 'Normal' },
    { name: 'Vegetation Stress', current: '12%', previous: '15%', delta: '-3%', status: 'Favorable' },
    { name: 'Root Moisture', current: '58%', previous: '62%', delta: '-4%', status: 'Normal' },
  ] : [
    { name: 'NDVI Biomass', current: 'Data unavailable', previous: 'N/A', delta: 'Pending pass', status: 'Offline' },
    { name: 'NDRE Chlorophyll', current: 'Data unavailable', previous: 'N/A', delta: 'Pending pass', status: 'Offline' },
    { name: 'Canopy Coverage', current: 'Data unavailable', previous: 'N/A', delta: 'Pending pass', status: 'Offline' },
    { name: 'Vegetation Stress', current: 'Data unavailable', previous: 'N/A', delta: 'Pending pass', status: 'Offline' },
    { name: 'Root Moisture', current: 'Data unavailable', previous: 'N/A', delta: 'Pending pass', status: 'Offline' },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner (Prompt Section 9) */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              Field Health Analysis
            </span>
            <DataTrustBadge 
              type={isSimulationMode ? "SIMULATION / DEMO" : "DATA UNAVAILABLE"} 
              source={isSimulationMode ? "Sentinel-2 Multi-Spectral Ingestion" : "Raster Pipeline Disconnected"} 
            />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 font-sans tracking-tight">
            Crop Health & Multispectral Vegetative Diagnostics
          </h1>
          <p className="text-xs text-slate-600 font-sans mt-1">
            Focus: Farm {farmId} • Parcel {parcelId} ({crop}) • District: {district}, {state}
          </p>
        </div>

        {/* Comparison & Time Slider Controls */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => setComparisonMode(!comparisonMode)}
            className={`px-3 py-1.5 rounded-xl border text-xs font-mono font-semibold transition ${
              comparisonMode
                ? 'bg-emerald-700 text-white border-emerald-700 shadow-xs'
                : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
            }`}
          >
            {comparisonMode ? '✓ Comparison Mode Active' : 'Enable Current vs Previous'}
          </button>

          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-mono">
            <Calendar className="w-3.5 h-3.5 text-slate-500 ml-1.5" />
            <button
              onClick={() => setTimeStep('T-14d')}
              className={`px-2 py-1 rounded-lg text-[11px] font-semibold transition ${timeStep === 'T-14d' ? 'bg-white text-slate-900 shadow-2xs font-bold' : 'text-slate-500 hover:text-slate-800'}`}
            >
              T-14d
            </button>
            <button
              onClick={() => setTimeStep('T-7d')}
              className={`px-2 py-1 rounded-lg text-[11px] font-semibold transition ${timeStep === 'T-7d' ? 'bg-white text-slate-900 shadow-2xs font-bold' : 'text-slate-500 hover:text-slate-800'}`}
            >
              T-7d
            </button>
            <button
              onClick={() => setTimeStep('T0')}
              className={`px-2 py-1 rounded-lg text-[11px] font-semibold transition ${timeStep === 'T0' ? 'bg-emerald-700 text-white shadow-2xs font-bold' : 'text-slate-500 hover:text-slate-800'}`}
            >
              Current Pass
            </button>
          </div>
        </div>
      </div>

      {/* Spectral Indices Matrix */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5 font-mono text-xs">
        {spectralMetrics.map((m) => (
          <div key={m.name} className="p-4 bg-white border border-slate-200 rounded-2xl shadow-xs flex flex-col justify-between">
            <div>
              <span className="text-[10px] text-slate-500 uppercase tracking-wider block">{m.name}</span>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="text-xl font-black text-slate-900">{m.current}</span>
                {comparisonMode && m.previous !== 'N/A' && (
                  <span className="text-xs text-slate-400 line-through">{m.previous}</span>
                )}
              </div>
            </div>
            <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
              <span className="text-slate-500 font-sans">Status:</span>
              <span className="text-emerald-700 font-bold">{m.status}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Large Field Map Canvas */}
      <div>
        <InteractiveFieldMap />
      </div>

      {/* Change Detection & Anomaly Table */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
        <div className="flex items-center justify-between pb-3 border-b border-slate-200 mb-4">
          <div>
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-emerald-700" />
              <span>Multi-Temporal Anomaly Detection Feed</span>
            </h3>
            <p className="text-xs text-slate-500 font-sans mt-0.5">
              Differential canopy analysis comparing multispectral passes
            </p>
          </div>
          <span className="text-xs font-mono px-2.5 py-0.5 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-lg font-bold">
            {isSimulationMode ? `${SAMPLE_ANOMALIES.length} Flagged Anomalies` : '0 Active Flagged'}
          </span>
        </div>

        {isSimulationMode ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-slate-100 text-slate-500 text-[10px] uppercase">
                  <th className="py-2.5 px-3">Anomaly ID</th>
                  <th className="py-2.5 px-3">Parcel</th>
                  <th className="py-2.5 px-3">Crop</th>
                  <th className="py-2.5 px-3">Severity</th>
                  <th className="py-2.5 px-3">Confidence</th>
                  <th className="py-2.5 px-3">Diagnosis Lead</th>
                  <th className="py-2.5 px-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {SAMPLE_ANOMALIES.map((anom) => (
                  <tr key={anom.id} className="hover:bg-slate-50 transition">
                    <td className="py-3 px-3 font-bold text-slate-900">{anom.id}</td>
                    <td className="py-3 px-3 font-semibold text-emerald-800">Parcel {anom.parcel}</td>
                    <td className="py-3 px-3">{anom.crop}</td>
                    <td className="py-3 px-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        anom.severity === 'HIGH' ? 'bg-rose-100 text-rose-800 border border-rose-300' : 'bg-amber-100 text-amber-800 border border-amber-300'
                      }`}>
                        {anom.severity}
                      </span>
                    </td>
                    <td className="py-3 px-3 font-bold text-slate-800">{anom.confidence}%</td>
                    <td className="py-3 px-3 text-slate-600 truncate max-w-xs font-sans">{anom.type}</td>
                    <td className="py-3 px-3 text-right">
                      <button
                        onClick={() => setSelectedAnomaly(anom)}
                        className="px-2.5 py-1 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 text-emerald-800 rounded-lg text-xs font-bold transition inline-flex items-center gap-1 shadow-2xs"
                      >
                        <span>Inspect</span>
                        <ChevronRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center bg-slate-50 rounded-xl border border-dashed border-slate-200 text-xs font-mono text-slate-500 space-y-2">
            <p>No active multispectral anomalies flagged for Farm {farmId}. To inspect benchmark anomalies, toggle Simulation Mode.</p>
          </div>
        )}
      </div>

      {/* Contextual Side Inspector Drawer */}
      <ContextualInspector
        isOpen={!!selectedAnomaly}
        onClose={() => setSelectedAnomaly(null)}
        title={selectedAnomaly ? `${selectedAnomaly.id}: ${selectedAnomaly.type}` : 'Anomaly Inspector'}
      >
        {selectedAnomaly && (
          <div className="space-y-4 text-xs font-sans">
            <div>
              <span className="text-[10px] font-mono uppercase text-slate-500 font-bold block">Detection Signature</span>
              <p className="mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl font-mono text-slate-800">
                {selectedAnomaly.spectralSignature}
              </p>
            </div>

            <div>
              <span className="text-[10px] font-mono uppercase text-slate-500 font-bold block">Hypothesized Agronomic Causes</span>
              <ul className="mt-1 space-y-1.5 list-disc pl-4 text-slate-700">
                {selectedAnomaly.possibleCauses.map((c, i) => (
                  <li key={i}>{c}</li>
                ))}
              </ul>
            </div>

            <div>
              <span className="text-[10px] font-mono uppercase text-slate-500 font-bold block">Multi-Modal Sensor Evidence</span>
              <ul className="mt-1 space-y-1.5 list-disc pl-4 text-slate-700">
                {selectedAnomaly.evidence.map((ev, i) => (
                  <li key={i}>{ev}</li>
                ))}
              </ul>
            </div>

            <div className="pt-2 border-t border-slate-200">
              <span className="text-[10px] font-mono uppercase text-slate-500 font-bold block">Recommended Action</span>
              <p className="mt-1 p-3 bg-emerald-50 border border-emerald-200 text-emerald-900 rounded-xl leading-relaxed">
                {selectedAnomaly.recommendedInspection}
              </p>
            </div>
          </div>
        )}
      </ContextualInspector>
    </div>
  );
}
