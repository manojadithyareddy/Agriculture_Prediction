'use client';

import React, { useState } from 'react';
import { Search, Download } from 'lucide-react';
import DataTrustBadge from '@/components/DataTrustBadge';
import ContextualInspector from '@/components/ContextualInspector';

interface AuditEvent {
  id: string;
  timestamp: string;
  type: 'PREDICTION' | 'DETECTION' | 'AGENT_RUN' | 'IRRIGATION' | 'FIELD_REPORT' | 'WEATHER';
  farmId: string;
  parcelId: string;
  summary: string;
  modelOrActor: string;
  severity: 'INFO' | 'WARNING' | 'CRITICAL' | 'OPTIMAL';
  payloadJson: Record<string, unknown>;
}

const SAMPLE_EVENTS: AuditEvent[] = [
  {
    id: 'EVT-8941',
    timestamp: 'Today 10:42:18 IST',
    type: 'PREDICTION',
    farmId: 'HYD-TEL-2026-04',
    parcelId: 'A4',
    summary: 'Yield Forecast: 3.42 t/ha for Cotton (Area: 2.5 ha)',
    modelOrActor: 'Harvest Yield Regressor v3.0',
    severity: 'OPTIMAL',
    payloadJson: {
      crop: 'Cotton',
      area_ha: 2.5,
      predicted_yield: 3.42,
      model: 'Yield-Regressor-v3.0.1',
      inputs: { soil_fertility: 0.82, water_stress: 0.12 },
    },
  },
  {
    id: 'EVT-8939',
    timestamp: 'Today 09:15:04 IST',
    type: 'DETECTION',
    farmId: 'HYD-TEL-2026-04',
    parcelId: 'A4',
    summary: 'Foliar Vision Pathology: Cercospora Leaf Spot (Conf: 94.2%)',
    modelOrActor: 'YOLOv8 Citrus/Cotton Ensemble',
    severity: 'WARNING',
    payloadJson: {
      condition: 'Cercospora Leaf Spot',
      confidence: 0.942,
      detections_count: 2,
      bounding_boxes: [[42, 55, 180, 210]],
    },
  },
  {
    id: 'EVT-8935',
    timestamp: 'Today 08:30:22 IST',
    type: 'AGENT_RUN',
    farmId: 'HYD-TEL-2026-04',
    parcelId: 'A4',
    summary: 'Autonomous Agent Diagnostic Run #RUN-8421 (6/6 nodes completed)',
    modelOrActor: 'LangGraph Agriculture Agent',
    severity: 'INFO',
    payloadJson: {
      run_id: 'RUN-8421',
      status: 'SUCCESS',
      latency_ms: 890,
      sources_retrieved: 3,
    },
  },
  {
    id: 'EVT-8928',
    timestamp: 'Yesterday 18:40:11 IST',
    type: 'IRRIGATION',
    farmId: 'HYD-TEL-2026-04',
    parcelId: 'A2',
    summary: 'Operator Executed Drip Cycle: 1,800 L delivered to Zone A2',
    modelOrActor: 'M. Adithya Reddy (Authorized)',
    severity: 'INFO',
    payloadJson: {
      action: 'DELIVER_DRIP',
      volume_liters: 1800,
      duration_minutes: 28,
      status: 'VERIFIED_DELIVERY',
    },
  },
  {
    id: 'EVT-8920',
    timestamp: 'Yesterday 14:15:30 IST',
    type: 'FIELD_REPORT',
    farmId: 'HYD-TEL-2026-04',
    parcelId: 'A4',
    summary: 'Field Inspection REP-2026-0089 filed and approved',
    modelOrActor: 'M. Adithya Reddy (Lead Agronomist)',
    severity: 'INFO',
    payloadJson: {
      report_id: 'REP-2026-0089',
      disease_found: 'Cercospora Leaf Spot',
      attachments: 2,
    },
  },
];

export default function HistoryPage() {
  const [events] = useState<AuditEvent[]>(SAMPLE_EVENTS);
  const [filterType, setFilterType] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedEvent, setSelectedEvent] = useState<AuditEvent | null>(null);
  const [inspectorOpen, setInspectorOpen] = useState(false);

  const filteredEvents = events.filter((ev) => {
    const matchesType = filterType === 'ALL' || ev.type === filterType;
    const matchesQuery = 
      ev.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ev.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ev.modelOrActor.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesType && matchesQuery;
  });

  const handleOpenInspector = (ev: AuditEvent) => {
    setSelectedEvent(ev);
    setInspectorOpen(true);
  };

  const exportJson = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(filteredEvents, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `agrifusion_audit_log_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="space-y-6">
      {/* Top Banner - Light Botanical Enterprise */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-mono tracking-wider text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-bold uppercase">
              Institutional Governance & Auditing
            </span>
            <DataTrustBadge type="OBSERVED DATA" source="Unified Telemetry Bus" />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 font-sans tracking-tight">
            Comprehensive Operational Audit Trail
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Immutable log of predictions, computer vision detections, agent executions, and operator authorizations
          </p>
        </div>

        <button
          onClick={exportJson}
          className="px-4 py-2 bg-white hover:bg-slate-50 text-slate-800 rounded-lg text-xs font-semibold font-mono transition flex items-center gap-1.5 border border-slate-300 shadow-sm"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export Audit Log (JSON)</span>
        </button>
      </div>

      {/* Filter & Search Controls */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
        <div className="flex items-center gap-2 flex-1 max-w-md bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200">
          <Search className="w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Filter by event ID, model, or summary keywords..."
            className="w-full bg-transparent text-slate-900 focus:outline-none text-xs font-sans"
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto">
          {['ALL', 'PREDICTION', 'DETECTION', 'AGENT_RUN', 'IRRIGATION', 'FIELD_REPORT'].map((t) => (
            <button
              key={t}
              onClick={() => setFilterType(t)}
              className={`px-3 py-1 rounded-lg transition font-semibold text-xs ${
                filterType === t
                  ? 'bg-emerald-700 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 text-[10px] uppercase bg-slate-50/50">
                <th className="py-2.5 px-3">Event ID & Timestamp</th>
                <th className="py-2.5 px-3">Type</th>
                <th className="py-2.5 px-3">Farm Context</th>
                <th className="py-2.5 px-3">Operational Summary</th>
                <th className="py-2.5 px-3">Actor / Model</th>
                <th className="py-2.5 px-3 text-right">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {filteredEvents.map((ev) => (
                <tr
                  key={ev.id}
                  onClick={() => handleOpenInspector(ev)}
                  className="hover:bg-slate-50/80 transition cursor-pointer"
                >
                  <td className="py-3 px-3">
                    <span className="font-bold text-slate-900 block">{ev.id}</span>
                    <span className="text-[10px] text-slate-500">{ev.timestamp}</span>
                  </td>
                  <td className="py-3 px-3">
                    <span className="text-[10px] px-2 py-0.5 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded font-bold uppercase">
                      {ev.type}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-600">
                    {ev.farmId} (P-{ev.parcelId})
                  </td>
                  <td className="py-3 px-3 text-slate-800 font-sans text-xs max-w-md">
                    {ev.summary}
                  </td>
                  <td className="py-3 px-3 text-sky-700 font-semibold">{ev.modelOrActor}</td>
                  <td className="py-3 px-3 text-right">
                    <button className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-xs font-medium transition">
                      Inspect →
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Contextual Inspector Side Drawer */}
      {selectedEvent && (
        <ContextualInspector
          isOpen={inspectorOpen}
          onClose={() => setInspectorOpen(false)}
          title={`Audit Event: ${selectedEvent.id}`}
          subtitle={`${selectedEvent.type} • ${selectedEvent.timestamp}`}
          badgeType="OBSERVED DATA"
          badgeSource={selectedEvent.modelOrActor}
        >
          <div className="space-y-4 text-xs font-sans">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
                Summary
              </span>
              <p className="text-slate-800 leading-normal text-xs">{selectedEvent.summary}</p>
            </div>

            <div className="space-y-1">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
                Recorded Telemetry Payload (JSON)
              </span>
              <pre className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 font-mono text-[11px] text-slate-800 overflow-x-auto">
                {JSON.stringify(selectedEvent.payloadJson, null, 2)}
              </pre>
            </div>
          </div>
        </ContextualInspector>
      )}
    </div>
  );
}
