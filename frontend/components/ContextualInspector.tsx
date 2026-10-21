'use client';

import React from 'react';
import { X, ShieldCheck } from 'lucide-react';
import DataTrustBadge, { ProvenanceType } from '@/components/DataTrustBadge';

interface ContextualInspectorProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  subtitle?: string;
  badgeType?: ProvenanceType;
  badgeSource?: string;
  children: React.ReactNode;
}

export default function ContextualInspector({
  isOpen,
  onClose,
  title,
  subtitle,
  badgeType = 'OBSERVED DATA',
  badgeSource,
  children,
}: ContextualInspectorProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-40 w-full sm:w-[480px] bg-white border-l border-slate-200 shadow-2xl flex flex-col animate-in slide-in-from-right duration-200 text-slate-900">
      {/* Top Bar */}
      <div className="p-4 border-b border-slate-200 bg-slate-50 flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <h3 className="text-sm font-bold text-slate-900 truncate">{title}</h3>
            {badgeType && <DataTrustBadge type={badgeType} source={badgeSource} />}
          </div>
          {subtitle && (
            <p className="text-xs text-slate-500 font-mono truncate">{subtitle}</p>
          )}
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg text-slate-400 hover:text-slate-800 hover:bg-slate-100 transition"
          title="Close Inspector"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-5 space-y-4">
        {children}
      </div>

      {/* Footer Info */}
      <div className="p-3.5 border-t border-slate-200 bg-slate-50 flex items-center justify-between text-[11px] font-mono text-slate-500">
        <span className="flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          <span>Verifiable Operational Log</span>
        </span>
        <button 
          onClick={onClose}
          className="px-3 py-1 bg-white hover:bg-slate-100 border border-slate-200 rounded text-slate-700 font-semibold transition"
        >
          Close Drawer
        </button>
      </div>
    </div>
  );
}
