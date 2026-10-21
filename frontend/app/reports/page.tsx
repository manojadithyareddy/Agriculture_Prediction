'use client';

import React, { useState } from 'react';
import { 
  FileText, 
  Plus, 
  Paperclip
} from 'lucide-react';
import { useGlobalContext } from '@/components/GlobalContext';
import DataTrustBadge from '@/components/DataTrustBadge';

interface FieldReport {
  id: string;
  farmId: string;
  parcelId: string;
  crop: string;
  date: string;
  inspector: string;
  observation: string;
  diseaseFound: string;
  treatmentAction: string;
  waterStatus: string;
  status: 'Draft' | 'Submitted' | 'Reviewed' | 'Approved' | 'Archived';
  attachmentsCount: number;
}

const INITIAL_REPORTS: FieldReport[] = [
  {
    id: 'REP-2026-0089',
    farmId: 'HYD-TEL-2026-04',
    parcelId: 'A4',
    crop: 'Cotton',
    date: 'Today 09:30 IST',
    inspector: 'M. Adithya Reddy (Lead Agronomist)',
    observation: 'Scouted southern edge following YOLOv8 foliar alert. Confirmed minor Cercospora spotting on lower third of canopy. No defoliation observed.',
    diseaseFound: 'Cercospora Leaf Spot (Low-to-Moderate)',
    treatmentAction: 'Morning spray scheduled with Mancozeb @ 2.5 g/L. Re-inspection set for Friday.',
    waterStatus: 'Soil moisture adequate at 58% field capacity.',
    status: 'Approved',
    attachmentsCount: 2,
  },
  {
    id: 'REP-2026-0084',
    farmId: 'HYD-TEL-2026-04',
    parcelId: 'A2',
    crop: 'Cotton',
    date: '18 Sep 2026',
    inspector: 'K. Venkatesh (Field Scout)',
    observation: 'Routine vegetative health check. Canopy cover homogeneous. No signs of sucking pests or pink bollworm.',
    diseaseFound: 'None (Healthy Specimen)',
    treatmentAction: 'None required. Soil nitrogen top-dress scheduled for next week.',
    waterStatus: 'Moisture optimal (64%).',
    status: 'Reviewed',
    attachmentsCount: 1,
  },
  {
    id: 'REP-2026-0078',
    farmId: 'WGL-TEL-2026-02',
    parcelId: 'N1',
    crop: 'Rice',
    date: '15 Sep 2026',
    inspector: 'S. Rao (Agronomy Specialist)',
    observation: 'Tillering stage assessment. Water depth maintained at 4 cm. Minor leaf folder activity along western bund below economic threshold.',
    diseaseFound: 'Leaf Folder (Sub-threshold)',
    treatmentAction: 'Installed 5 bird perches per acre for biological control.',
    waterStatus: 'Submerged panicle water level stable.',
    status: 'Approved',
    attachmentsCount: 3,
  },
];

export default function ReportsPage() {
  const { farmId, parcelId, crop, district } = useGlobalContext();
  const [reports, setReports] = useState<FieldReport[]>(INITIAL_REPORTS);
  const [showForm, setShowForm] = useState(false);

  // Form State
  const [observation, setObservation] = useState('');
  const [diseaseFound, setDiseaseFound] = useState('None');
  const [treatmentAction, setTreatmentAction] = useState('');
  const [inspectorName, setInspectorName] = useState('M. Adithya Reddy');

  const handleCreateReport = (e: React.FormEvent) => {
    e.preventDefault();
    if (!observation.trim()) return;

    const newRep: FieldReport = {
      id: `REP-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      farmId,
      parcelId,
      crop,
      date: 'Just now',
      inspector: inspectorName,
      observation,
      diseaseFound,
      treatmentAction: treatmentAction || 'Standard cultural monitoring.',
      waterStatus: 'Recorded from field observation.',
      status: 'Submitted',
      attachmentsCount: 1,
    };

    setReports([newRep, ...reports]);
    setObservation('');
    setTreatmentAction('');
    setShowForm(false);
  };

  return (
    <div className="space-y-6">
      {/* Top Banner - Light Botanical Enterprise */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-mono tracking-wider text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-bold uppercase">
              Field Operations & Inspection Logs
            </span>
            <DataTrustBadge type="OBSERVED DATA" source="Field Agronomist Scouting Records" />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 font-sans tracking-tight">
            Field Reports & Agronomic Auditing
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Operational Field Records for Farm: {farmId} • Parcel: {parcelId} • Region: {district}
          </p>
        </div>

        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-bold transition flex items-center gap-1.5 shadow-sm"
        >
          <Plus className="w-4 h-4" />
          <span>{showForm ? 'Cancel Form' : 'File Field Report'}</span>
        </button>
      </div>

      {/* Submission Form Modal / Collapsible */}
      {showForm && (
        <form onSubmit={handleCreateReport} className="bg-white border border-slate-300 rounded-xl p-5 shadow-md space-y-4 animate-in fade-in">
          <div className="flex items-center justify-between pb-3 border-b border-slate-200">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900">
              New Agronomic Inspection Log
            </h3>
            <span className="text-xs font-mono text-emerald-700 font-semibold">Parcel {parcelId} ({crop})</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-sans">
            <div>
              <label className="block text-[11px] font-mono text-slate-600 mb-1 font-semibold">Inspector / Scout Name</label>
              <input
                type="text"
                value={inspectorName}
                onChange={(e) => setInspectorName(e.target.value)}
                className="w-full bg-white border border-slate-300 text-slate-900 text-xs rounded-lg px-3 py-2 font-mono focus:ring-1 focus:ring-emerald-500"
                required
              />
            </div>
            <div>
              <label className="block text-[11px] font-mono text-slate-600 mb-1 font-semibold">Pathogen / Pest Status</label>
              <input
                type="text"
                value={diseaseFound}
                onChange={(e) => setDiseaseFound(e.target.value)}
                placeholder="e.g. Cercospora Leaf Spot, Fall Armyworm, None"
                className="w-full bg-white border border-slate-300 text-slate-900 text-xs rounded-lg px-3 py-2 font-mono focus:ring-1 focus:ring-emerald-500"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-[11px] font-mono text-slate-600 mb-1 font-semibold">Field Observation & Symptom Notes</label>
              <textarea
                rows={3}
                value={observation}
                onChange={(e) => setObservation(e.target.value)}
                placeholder="Describe canopy conditions, lesion density, vegetative vigour..."
                className="w-full bg-white border border-slate-300 text-slate-900 text-xs rounded-lg px-3 py-2 font-sans focus:ring-1 focus:ring-emerald-500"
                required
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-[11px] font-mono text-slate-600 mb-1 font-semibold">Executed or Prescribed Management Action</label>
              <input
                type="text"
                value={treatmentAction}
                onChange={(e) => setTreatmentAction(e.target.value)}
                placeholder="e.g. Dispatched spray rig with copper fungicide; adjusted drip schedule..."
                className="w-full bg-white border border-slate-300 text-slate-900 text-xs rounded-lg px-3 py-2 font-sans focus:ring-1 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="pt-2 flex items-center justify-end gap-2 border-t border-slate-200">
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="px-4 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-bold transition shadow-sm"
            >
              Submit Audit Report
            </button>
          </div>
        </form>
      )}

      {/* Reports Timeline Feed */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3.5 border-b border-slate-200">
          <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
            <FileText className="w-4 h-4 text-emerald-600" />
            <span>Field Inspection Records & Audit Trail</span>
          </h3>
          <span className="text-[10px] font-mono text-slate-500 bg-slate-50 px-2 py-1 rounded border border-slate-200">Verifiable Operational History</span>
        </div>

        <div className="space-y-3 font-sans text-xs">
          {reports.map((rep) => (
            <div key={rep.id} className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-2.5">
                <div className="flex items-center gap-2 font-mono">
                  <span className="text-emerald-700 font-bold">{rep.id}</span>
                  <span className="text-slate-300">•</span>
                  <span className="text-slate-900 font-semibold">{rep.farmId} (Parcel {rep.parcelId})</span>
                  <span className="text-slate-300">•</span>
                  <span className="text-slate-600">{rep.crop}</span>
                </div>
                <div className="flex items-center gap-2 font-mono">
                  <span className="text-slate-500 text-[11px]">{rep.date}</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${
                    rep.status === 'Approved' 
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : rep.status === 'Reviewed'
                      ? 'bg-sky-50 text-sky-700 border-sky-200'
                      : 'bg-amber-50 text-amber-700 border-amber-200'
                  }`}>
                    {rep.status}
                  </span>
                </div>
              </div>

              <div>
                <p className="text-slate-800 leading-relaxed text-xs">
                  {rep.observation}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] font-mono">
                <div className="p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-slate-500 block text-[10px]">Pathology Observed:</span>
                  <span className="text-slate-900 font-medium">{rep.diseaseFound}</span>
                </div>
                <div className="p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-slate-500 block text-[10px]">Management Action:</span>
                  <span className="text-emerald-800 font-semibold">{rep.treatmentAction}</span>
                </div>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-slate-200 text-[10px] font-mono text-slate-500">
                <span>Inspector: <strong className="text-slate-800">{rep.inspector}</strong></span>
                <span className="flex items-center gap-1">
                  <Paperclip className="w-3 h-3 text-slate-400" />
                  <span>{rep.attachmentsCount} Photographic Evidence Attachments</span>
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
