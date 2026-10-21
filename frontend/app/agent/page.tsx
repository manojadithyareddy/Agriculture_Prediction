'use client';

import React, { useState } from 'react';
import { 
  Activity, 
  CheckCircle2, 
  ChevronRight
} from 'lucide-react';
import { useGlobalContext } from '@/components/GlobalContext';
import DataTrustBadge from '@/components/DataTrustBadge';
import ContextualInspector from '@/components/ContextualInspector';

interface TraceNode {
  id: string;
  stepNumber: number;
  name: string;
  category: 'INGEST' | 'VISION' | 'RETRIEVAL' | 'SYNTHESIS' | 'VALIDATION';
  tool: string;
  model: string;
  durationMs: number;
  status: 'SUCCESS' | 'RUNNING' | 'PENDING' | 'ERROR';
  inputSummary: string;
  outputSummary: string;
  detailsJson: Record<string, unknown>;
}

const SAMPLE_TRACE: TraceNode[] = [
  {
    id: 'node-1',
    stepNumber: 1,
    name: 'Operator Input Ingestion & Sanitation',
    category: 'INGEST',
    tool: 'Pydantic Input Validator',
    model: 'Rule-Based Engine',
    durationMs: 12,
    status: 'SUCCESS',
    inputSummary: 'Multipart file: leaf_sample_A4.jpg (480x480 RGB)',
    outputSummary: 'Payload normalized, EXIF metadata parsed, GPS coordinates validated',
    detailsJson: {
      format: 'JPEG',
      dimensions: '480x480',
      channels: 3,
      gps_lat: 17.385,
      gps_lon: 78.4867,
    },
  },
  {
    id: 'node-2',
    stepNumber: 2,
    name: 'Multi-Model YOLO Vision Inference',
    category: 'VISION',
    tool: 'Roboflow Universe Multi-Model Router',
    model: 'YOLOv8 Citrus & Cotton Pathology Ensemble',
    durationMs: 310,
    status: 'SUCCESS',
    inputSummary: 'Target Crop: Cotton; Normalized Tensor: [1, 3, 640, 640]',
    outputSummary: 'Detected: Cercospora Leaf Spot (Confidence: 94.2%, 2 Bounding Boxes)',
    detailsJson: {
      model_id: 'cotton-leaf-pathology-v8',
      detections_count: 2,
      primary_class: 'Cercospora',
      confidence: 0.942,
      bounding_boxes: [[42, 55, 180, 210], [195, 140, 290, 260]],
    },
  },
  {
    id: 'node-3',
    stepNumber: 3,
    name: 'Agronomic Urgency Classification',
    category: 'VALIDATION',
    tool: 'LangGraph Severity Classifier Node',
    model: 'Pathology Severity Heuristic',
    durationMs: 8,
    status: 'SUCCESS',
    inputSummary: 'Detected Condition: Cercospora; Confidence: 94.2%',
    outputSummary: 'Urgency Level Assigned: HIGH (Spore dispersal window open)',
    detailsJson: {
      urgency_level: 'HIGH',
      pathogen_type: 'Fungal',
      incubation_period_days: 7,
    },
  },
  {
    id: 'node-4',
    stepNumber: 4,
    name: 'District Microclimate Ingestion',
    category: 'RETRIEVAL',
    tool: 'Open-Meteo REST Client',
    model: 'Numerical Weather Integration',
    durationMs: 64,
    status: 'SUCCESS',
    inputSummary: 'Location: Hyderabad, Telangana (Lat: 17.38, Lon: 78.48)',
    outputSummary: 'Temp: 28.5°C, RH: 84% night peak, Precipitation: 0 mm, Wind: 11 km/h',
    detailsJson: {
      temperature_c: 28.5,
      relative_humidity_pct: 84,
      wind_kmh: 11,
      spray_window: 'OPTIMAL_MORNING',
    },
  },
  {
    id: 'node-5',
    stepNumber: 5,
    name: 'ChromaDB Knowledge Base Retrieval',
    category: 'RETRIEVAL',
    tool: 'Hybrid BM25 + Vector Semantic Search',
    model: 'Agronomy Embedding Model',
    durationMs: 82,
    status: 'SUCCESS',
    inputSummary: 'Query: "Cotton Cercospora foliar treatment ANGRAU PJTSAU"',
    outputSummary: 'Retrieved 3 authoritative university extension treatment protocols',
    detailsJson: {
      top_k: 3,
      sources: [
        'ANGRAU Cotton Disease Management Bulletin 2024 (Section 4.2)',
        'PJTSAU Integrated Pest & Disease Control Manual',
        'ICAR Standard Crop Protection Handbook',
      ],
      similarity_scores: [0.912, 0.884, 0.835],
    },
  },
  {
    id: 'node-6',
    stepNumber: 6,
    name: 'Action Plan Synthesis & Chemical Validation',
    category: 'SYNTHESIS',
    tool: 'LLM Reasoning Node',
    model: 'Gemini 1.5 / OpenAI Agronomy Planner',
    durationMs: 440,
    status: 'SUCCESS',
    inputSummary: 'Synthesize Vision Output + Microclimate + University RAG protocols',
    outputSummary: 'Synthesized 4-stage management directive with strict dosage checks',
    detailsJson: {
      immediate_action: 'Scout South-East perimeter of Parcel A4 to confirm lesion density.',
      within_24h: 'Apply Mancozeb 75% WP @ 2.5 g/L or Copper Oxychloride @ 3 g/L during morning spray window (06:30–09:00 IST).',
      within_3d: 'Re-evaluate canopy with multispectral drone or follow-up phone scan.',
      dosage_safety_check: 'VERIFIED_COMPLIANT',
    },
  },
];

export default function AgentTracePage() {
  const { farmId, parcelId, crop, district } = useGlobalContext();
  const [selectedNode, setSelectedNode] = useState<TraceNode | null>(SAMPLE_TRACE[1]);
  const [inspectorOpen, setInspectorOpen] = useState(false);

  const handleNodeClick = (node: TraceNode) => {
    setSelectedNode(node);
    setInspectorOpen(true);
  };

  const totalDuration = SAMPLE_TRACE.reduce((acc, n) => acc + n.durationMs, 0);

  return (
    <div className="space-y-6">
      {/* Top Banner - Light Botanical Enterprise */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-mono tracking-wider text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-bold uppercase">
              Agent Observability & Tracing
            </span>
            <DataTrustBadge type="AI INTERPRETATION" source="LangGraph Orchestration Trace #RUN-8421" />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 font-sans tracking-tight">
            Multi-Modal Agronomist Execution DAG
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Farm {farmId} • Parcel {parcelId} ({crop}) • District: {district} • End-to-End Latency: {totalDuration} ms
          </p>
        </div>

        {/* Execution Summary Pill */}
        <div className="flex items-center gap-3 bg-slate-50 px-3.5 py-2 rounded-xl border border-slate-200 font-mono text-xs">
          <div className="flex items-center gap-1.5 text-emerald-700 font-bold">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>6/6 Nodes Succeeded</span>
          </div>
          <span className="text-slate-300">|</span>
          <span className="text-slate-600">Total Latency: <strong className="text-slate-900">{totalDuration}ms</strong></span>
        </div>
      </div>

      {/* DAG Flow Visualizer */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3.5 border-b border-slate-200">
          <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-600" />
            <span>Sequential Execution Graph (Click node to inspect payloads)</span>
          </h3>
          <span className="text-[10px] font-mono text-slate-500">Interactive DAG Nodes</span>
        </div>

        {/* Node Sequence List */}
        <div className="space-y-2.5 font-mono text-xs">
          {SAMPLE_TRACE.map((node) => (
            <div
              key={node.id}
              onClick={() => handleNodeClick(node)}
              className={`p-3.5 rounded-xl border transition cursor-pointer flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 ${
                selectedNode?.id === node.id
                  ? 'bg-emerald-50/70 border-emerald-300 text-slate-900 shadow-sm'
                  : 'bg-slate-50 border-slate-200 hover:border-slate-300 text-slate-700'
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold shrink-0 text-xs border ${
                  selectedNode?.id === node.id ? 'bg-emerald-700 text-white border-emerald-700' : 'bg-white text-slate-700 border-slate-200'
                }`}>
                  {node.stepNumber}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-900 text-sm font-sans">{node.name}</span>
                    <span className="text-[9px] px-1.5 py-0.5 rounded bg-white border border-slate-200 text-slate-600 uppercase font-mono font-semibold">
                      {node.category}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-500 mt-0.5 font-sans">
                    Tool: <span className="text-slate-800 font-medium font-mono">{node.tool}</span> • Model: <span className="text-slate-800 font-medium font-mono">{node.model}</span>
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-4 self-end sm:self-center shrink-0">
                <div className="text-right">
                  <span className="text-xs font-bold text-emerald-700 block">{node.durationMs} ms</span>
                  <span className="text-[10px] text-emerald-700 font-semibold uppercase">{node.status}</span>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-400" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Contextual Inspector Drawer */}
      {selectedNode && (
        <ContextualInspector
          isOpen={inspectorOpen}
          onClose={() => setInspectorOpen(false)}
          title={`Node Trace: Step ${selectedNode.stepNumber}`}
          subtitle={`${selectedNode.name} • Latency: ${selectedNode.durationMs}ms`}
          badgeType="MODEL OUTPUT"
          badgeSource={selectedNode.tool}
        >
          <div className="space-y-4 text-xs font-sans">
            {/* Input Summary */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
                Input Payload
              </span>
              <p className="text-slate-800 font-mono text-xs leading-relaxed">
                {selectedNode.inputSummary}
              </p>
            </div>

            {/* Output Summary */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-700 font-bold block">
                Output Artifact
              </span>
              <p className="text-slate-800 font-mono text-xs leading-relaxed">
                {selectedNode.outputSummary}
              </p>
            </div>

            {/* Raw JSON Inspect */}
            <div className="space-y-1">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
                Telemetry State (JSON)
              </span>
              <pre className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 font-mono text-[11px] text-slate-800 overflow-x-auto">
                {JSON.stringify(selectedNode.detailsJson, null, 2)}
              </pre>
            </div>
          </div>
        </ContextualInspector>
      )}
    </div>
  );
}
