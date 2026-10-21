'use client';

import React from 'react';
import { AlertTriangle, ShieldAlert, CheckCircle2, X } from 'lucide-react';
import DataTrustBadge from '@/components/DataTrustBadge';

interface ActionConfirmModalProps {
  isOpen: boolean;
  title: string;
  recommendationText: string;
  actionSummary: {
    target: string;
    parameter: string;
    value: string;
    schedule: string;
    riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  };
  onConfirm: () => void;
  onCancel: () => void;
}

export default function ActionConfirmModal({
  isOpen,
  title,
  recommendationText,
  actionSummary,
  onConfirm,
  onCancel,
}: ActionConfirmModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="w-full max-w-lg bg-white border border-slate-200 rounded-2xl shadow-2xl p-6 text-slate-800 animate-in fade-in zoom-in-95">
        {/* Header */}
        <div className="flex items-start justify-between pb-4 border-b border-slate-200">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-amber-100 text-amber-800 border border-amber-300">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">{title}</h3>
              <p className="text-xs text-slate-500 font-sans">Operational Human-in-the-Loop Safeguard</p>
            </div>
          </div>
          <button 
            onClick={onCancel}
            className="text-slate-400 hover:text-slate-600 p-1"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* AI Advisory Section */}
        <div className="mt-4 p-3.5 bg-slate-50 rounded-xl border border-slate-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold">
              AI Recommendation
            </span>
            <DataTrustBadge type="AI GENERATED" source="Agronomy Decision Engine" />
          </div>
          <p className="text-xs text-slate-700 leading-relaxed font-sans italic">
            &quot;{recommendationText}&quot;
          </p>
        </div>

        {/* Proposed Physical Action Details */}
        <div className="mt-4 space-y-2">
          <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
            Execution Parameters
          </span>
          <div className="grid grid-cols-2 gap-2 text-xs font-mono">
            <div className="p-2 bg-slate-50 rounded-lg border border-slate-200">
              <span className="text-slate-500 block text-[10px]">Target Zone</span>
              <span className="font-semibold text-emerald-800">{actionSummary.target}</span>
            </div>
            <div className="p-2 bg-slate-50 rounded-lg border border-slate-200">
              <span className="text-slate-500 block text-[10px]">Parameter</span>
              <span className="font-semibold text-slate-800">{actionSummary.parameter}</span>
            </div>
            <div className="p-2 bg-slate-50 rounded-lg border border-slate-200">
              <span className="text-slate-500 block text-[10px]">Delivery Rate</span>
              <span className="font-semibold text-sky-800">{actionSummary.value}</span>
            </div>
            <div className="p-2 bg-slate-50 rounded-lg border border-slate-200">
              <span className="text-slate-500 block text-[10px]">Timing / Window</span>
              <span className="font-semibold text-amber-800">{actionSummary.schedule}</span>
            </div>
          </div>
        </div>

        {/* Operational Warning */}
        <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-start gap-2.5 text-xs text-amber-900">
          <AlertTriangle className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
          <div>
            <p className="font-bold text-[11px]">Physical Equipment Dispatch</p>
            <p className="text-[10px] text-amber-800/90 leading-normal font-sans">
              Authorizing this action creates an immutable log entry and dispatches command signals to zone solenoid valves.
            </p>
          </div>
        </div>

        {/* Buttons */}
        <div className="mt-6 flex items-center justify-end gap-3 pt-4 border-t border-slate-200">
          <button
            onClick={onCancel}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition border border-slate-300"
          >
            Cancel / Dismiss
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 rounded-xl text-xs font-bold bg-emerald-700 hover:bg-emerald-800 text-white transition flex items-center gap-1.5 shadow-xs"
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Authorize & Execute Action</span>
          </button>
        </div>
      </div>
    </div>
  );
}
