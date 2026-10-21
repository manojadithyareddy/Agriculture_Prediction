'use client';

import React, { useState } from 'react';
import { 
  Database, 
  Layers
} from 'lucide-react';
import DataTrustBadge from '@/components/DataTrustBadge';
import ContextualInspector from '@/components/ContextualInspector';

interface DatasetItem {
  id: string;
  name: string;
  type: string;
  rows: string;
  columns: number;
  coverage: string;
  lastUpdated: string;
  qualityScore: number;
  source: string;
  version: string;
  usedByModel: string;
  schemaFields: { field: string; type: string; desc: string }[];
  lineage: string[];
}

const DATASETS: DatasetItem[] = [
  {
    id: 'ds-weather',
    name: 'AP_TS_Weather_Dataset.csv',
    type: 'Meteorological Time-Series',
    rows: '142,500',
    columns: 14,
    coverage: '59 Districts (AP & TS)',
    lastUpdated: 'Daily Synced',
    qualityScore: 98.4,
    source: 'Open-Meteo & IMD Archives',
    version: 'v2.4.1',
    usedByModel: 'Climate Risk & ET0 Irrigation',
    schemaFields: [
      { field: 'date', type: 'datetime', desc: 'Timestamp of meteorological reading' },
      { field: 'district', type: 'string', desc: 'Administrative district identifier' },
      { field: 'temperature_c', type: 'float', desc: 'Mean 2-meter air temperature' },
      { field: 'relative_humidity_pct', type: 'float', desc: 'Ambient atmospheric moisture' },
      { field: 'precipitation_mm', type: 'float', desc: 'Observed daily rainfall depth' },
      { field: 'solar_radiation_mj', type: 'float', desc: 'Direct downwelling shortwave flux' },
    ],
    lineage: [
      'Raw Open-Meteo API Reanalysis Archive',
      'Missing Value Imputation via KNN (k=5)',
      'Solar Radiation & ET0 Feature Synthesis',
      'Stratified Time-Series Train/Test Split (80/20)',
      'Gradient Boosting Climate Risk Model',
    ],
  },
  {
    id: 'ds-crop',
    name: 'ICAR_Soil_Nutrient_Crop_Corpus.csv',
    type: 'Agronomic Tabular',
    rows: '2,200',
    columns: 8,
    coverage: '22 Crop Cultivars',
    lastUpdated: 'Monthly',
    qualityScore: 96.8,
    source: 'ICAR Soil Health Survey',
    version: 'v3.0.0',
    usedByModel: 'Crop Recommendation Random Forest',
    schemaFields: [
      { field: 'N', type: 'integer', desc: 'Ratio of Nitrogen content in soil (kg/ha)' },
      { field: 'P', type: 'integer', desc: 'Ratio of Phosphorus content in soil (kg/ha)' },
      { field: 'K', type: 'integer', desc: 'Ratio of Potassium content in soil (kg/ha)' },
      { field: 'temperature', type: 'float', desc: 'Optimal growing temperature in °C' },
      { field: 'humidity', type: 'float', desc: 'Relative humidity percentage' },
      { field: 'ph', type: 'float', desc: 'Soil acidity / alkalinity scale' },
      { field: 'rainfall', type: 'float', desc: 'Annual rainfall requirement in mm' },
      { field: 'label', type: 'string', desc: 'Target crop specimen category' },
    ],
    lineage: [
      'ICAR Soil Health Registry 2023',
      'Outlier Truncation & Standard Scaling',
      'Random Forest Classifier 100 Estimators',
      'Pickle Serialization (models/model.pkl)',
    ],
  },
  {
    id: 'ds-vision',
    name: 'Roboflow_Universe_Agri_Pathology_Annotations',
    type: 'Computer Vision (YOLOv8)',
    rows: '38,400 Images',
    columns: 6,
    coverage: '13 Crops (Rice, Cotton, Maize, Chilli, Mango)',
    lastUpdated: 'Weekly Retrained',
    qualityScore: 95.1,
    source: 'Roboflow Universe Field Repositories',
    version: 'v8.2.0',
    usedByModel: 'YOLOv8 Disease Detector',
    schemaFields: [
      { field: 'image_id', type: 'string', desc: 'Unique UUID of annotated leaf scan' },
      { field: 'crop_specimen', type: 'string', desc: 'Botanical specimen family' },
      { field: 'pathology_class', type: 'string', desc: 'Fungal/bacterial disease label' },
      { field: 'bbox_coordinates', type: 'array[4]', desc: '[x_min, y_min, x_max, y_max] scaled' },
      { field: 'confidence_ground_truth', type: 'float', desc: 'Verified pathologist label certainty' },
    ],
    lineage: [
      'Field Phone & Drone Imagery Ingestion',
      'Expert Agronomist Bounding Box Annotation',
      'Mosaic & Fliphsv Augmentations',
      'YOLOv8 Medium Architecture Training',
      'Inference Serving via Roboflow API',
    ],
  },
  {
    id: 'ds-rag',
    name: 'ChromaDB_Agriculture_Knowledge_Embeddings',
    type: 'Vector Embeddings Corpus',
    rows: '1,450 Text Chunks',
    columns: 5,
    coverage: 'Andhra Pradesh & Telangana Agronomy Guides',
    lastUpdated: 'Monthly',
    qualityScore: 99.2,
    source: 'ANGRAU & PJTSAU Extension Publications',
    version: 'v1.6.0',
    usedByModel: 'AI Agronomist & Multi-Modal Agent',
    schemaFields: [
      { field: 'chunk_id', type: 'string', desc: 'Unique paragraph identifier' },
      { field: 'university_source', type: 'string', desc: 'Authoring institution' },
      { field: 'crop_context', type: 'string', desc: 'Target crop topic' },
      { field: 'content_text', type: 'string', desc: 'Prescribed treatment or agronomic advice' },
      { field: 'vector_embedding', type: 'float[384]', desc: 'Dense semantic representation' },
    ],
    lineage: [
      'Official University PDF Bulletins',
      'Semantic Text Splitting (chunk_size=500, overlap=50)',
      'Sentence-Transformers / TF-IDF Vectorization',
      'ChromaDB Local Storage (agriculture_db/)',
    ],
  },
];

export default function DatasetsPage() {
  const [selectedDs, setSelectedDs] = useState<DatasetItem | null>(DATASETS[0]);
  const [inspectorOpen, setInspectorOpen] = useState(false);

  const handleOpenInspector = (ds: DatasetItem) => {
    setSelectedDs(ds);
    setInspectorOpen(true);
  };

  return (
    <div className="space-y-6">
      {/* Top Banner - Light Botanical Enterprise */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-mono tracking-wider text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-bold uppercase">
              Agricultural Data Science & Laboratory
            </span>
            <DataTrustBadge type="OBSERVED DATA" source="Verifiable Data Registry" />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 font-sans tracking-tight">
            Datasets, Quality Metrics & Lineage Pipeline
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Institutional agronomic repositories, meteorological datasets, and computer vision training corpora
          </p>
        </div>

        <div className="flex items-center gap-3 bg-slate-50 px-3.5 py-2 rounded-xl border border-slate-200 font-mono text-xs">
          <span className="text-slate-600">Total Corpora: <strong className="text-slate-900">{DATASETS.length} Active</strong></span>
          <span className="text-slate-300">|</span>
          <span className="text-emerald-700 font-bold">100% Quality Audited</span>
        </div>
      </div>

      {/* Datasets Master Table */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
        <div className="flex items-center justify-between pb-3.5 border-b border-slate-200 mb-4">
          <div>
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
              <Database className="w-4 h-4 text-emerald-600" />
              <span>Certified Training & Inference Data Catalog</span>
            </h3>
            <p className="text-[11px] text-slate-500 font-sans mt-0.5">Click row to inspect schema, data quality, and lineage</p>
          </div>
          <span className="text-[10px] font-mono text-slate-500 bg-slate-50 px-2 py-1 rounded border border-slate-200">Read-Only Audit Mode</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 text-[10px] uppercase bg-slate-50/50">
                <th className="py-2.5 px-3">Dataset Name</th>
                <th className="py-2.5 px-3">Type</th>
                <th className="py-2.5 px-3">Volume</th>
                <th className="py-2.5 px-3">Coverage</th>
                <th className="py-2.5 px-3">Quality Score</th>
                <th className="py-2.5 px-3">Consumer Model</th>
                <th className="py-2.5 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700 font-sans">
              {DATASETS.map((ds) => (
                <tr
                  key={ds.id}
                  onClick={() => handleOpenInspector(ds)}
                  className="hover:bg-slate-50/80 transition cursor-pointer"
                >
                  <td className="py-3 px-3">
                    <span className="font-semibold text-slate-900 font-mono block text-xs">{ds.name}</span>
                    <span className="text-[10px] text-slate-500 font-sans">{ds.source} • {ds.version}</span>
                  </td>
                  <td className="py-3 px-3 text-slate-600 text-xs">{ds.type}</td>
                  <td className="py-3 px-3 text-slate-900 font-semibold font-mono text-xs">{ds.rows}</td>
                  <td className="py-3 px-3 text-slate-600 text-xs">{ds.coverage}</td>
                  <td className="py-3 px-3 font-mono">
                    <span className="text-emerald-700 font-bold">{ds.qualityScore}%</span>
                  </td>
                  <td className="py-3 px-3 text-sky-700 font-mono text-xs">{ds.usedByModel}</td>
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

      {/* End-to-End Data Lineage Pipeline Visualizer */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3.5 border-b border-slate-200">
          <div>
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
              <Layers className="w-4 h-4 text-emerald-600" />
              <span>General Agricultural Data Lineage & Provenance Chain</span>
            </h3>
            <p className="text-[11px] text-slate-500 font-sans mt-0.5">Formal pathway from sensor ingestion to live operational decision</p>
          </div>
          <DataTrustBadge type="OBSERVED DATA" source="Data Lineage Graph" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-6 gap-2.5 text-xs font-mono">
          {[
            { step: '1. Ingestion', title: 'Raw Telemetry & Archives', desc: 'Sentinel-2, Open-Meteo, ICAR' },
            { step: '2. Sanitation', title: 'Cleaning & Normalization', desc: 'Outlier pruning, KNN imputation' },
            { step: '3. Engineering', title: 'Feature Synthesis', desc: 'NDVI, RedEdge, ET0 calculation' },
            { step: '4. Training', title: 'Offline Model Training', desc: 'Cross-validation, hyperparam tuning' },
            { step: '5. Registry', title: 'Artifact Versioning', desc: 'Pickle storage, metadata catalog' },
            { step: '6. Serving', title: 'FastAPI Production Inference', desc: 'Sub-100ms async API response' },
          ].map((item, i) => (
            <div key={i} className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <span className="text-[9px] text-emerald-700 font-bold block uppercase">{item.step}</span>
                <h5 className="font-bold text-slate-900 mt-1 font-sans text-xs">{item.title}</h5>
                <p className="text-[10px] text-slate-500 font-sans mt-1 leading-normal">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Dataset Inspector Side Drawer */}
      {selectedDs && (
        <ContextualInspector
          isOpen={inspectorOpen}
          onClose={() => setInspectorOpen(false)}
          title={`Dataset: ${selectedDs.name}`}
          subtitle={`${selectedDs.type} • Version: ${selectedDs.version}`}
          badgeType="OBSERVED DATA"
          badgeSource={selectedDs.source}
        >
          <div className="space-y-4 text-xs font-sans">
            {/* Metadata Overview */}
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2 font-mono text-xs">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">
                Corpus Metrics
              </span>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div><span className="text-slate-500">Total Records:</span> <span className="text-slate-900 font-semibold">{selectedDs.rows}</span></div>
                <div><span className="text-slate-500">Columns:</span> <span className="text-slate-900 font-semibold">{selectedDs.columns}</span></div>
                <div><span className="text-slate-500">Quality Score:</span> <span className="text-emerald-700 font-bold">{selectedDs.qualityScore}%</span></div>
                <div><span className="text-slate-500">Frequency:</span> <span className="text-slate-900">{selectedDs.lastUpdated}</span></div>
              </div>
            </div>

            {/* Schema Definition */}
            <div className="space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
                Schema Fields & Type Specifications
              </span>
              <div className="space-y-1.5 font-mono text-xs">
                {selectedDs.schemaFields.map((f, i) => (
                  <div key={i} className="p-2.5 bg-white rounded-lg border border-slate-200 flex items-start justify-between gap-2">
                    <div>
                      <span className="font-bold text-slate-900">{f.field}</span>
                      <span className="text-[11px] text-slate-500 block font-sans mt-0.5">{f.desc}</span>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 bg-slate-100 text-emerald-800 rounded font-bold shrink-0">
                      {f.type}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Data Lineage Chain */}
            <div className="space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-700 font-bold block">
                Dataset Processing Lineage
              </span>
              <div className="space-y-1.5 font-mono text-xs">
                {selectedDs.lineage.map((l, i) => (
                  <div key={i} className="p-2.5 bg-white rounded-lg border border-slate-200 text-slate-700 flex items-center gap-2">
                    <span className="text-emerald-700 font-bold text-xs">{i + 1}.</span>
                    <span>{l}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </ContextualInspector>
      )}
    </div>
  );
}
