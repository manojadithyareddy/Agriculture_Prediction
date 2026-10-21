'use client';

import React from 'react';

export type ProvenanceType = 
  | 'OBSERVED DATA'
  | 'MODEL OUTPUT'
  | 'RETRIEVED KNOWLEDGE'
  | 'AI INTERPRETATION'
  | 'USER INPUT'
  | 'EXTERNAL API'
  | 'SIMULATION / DEMO'
  | 'DATA UNAVAILABLE'
  | 'OBSERVED'
  | 'FORECAST'
  | 'PREDICTED'
  | 'AI GENERATED'
  | 'EXTERNAL SOURCE'
  | 'SIMULATION';

interface DataTrustBadgeProps {
  type: ProvenanceType;
  source?: string;
  timestamp?: string;
  className?: string;
}

const BADGE_CONFIG: Record<string, { label: string; bg: string; text: string; border: string }> = {
  'OBSERVED DATA': {
    label: 'OBSERVED DATA',
    bg: 'bg-emerald-50',
    text: 'text-emerald-800',
    border: 'border-emerald-300',
  },
  'MODEL OUTPUT': {
    label: 'MODEL OUTPUT',
    bg: 'bg-teal-50',
    text: 'text-teal-800',
    border: 'border-teal-300',
  },
  'RETRIEVED KNOWLEDGE': {
    label: 'RETRIEVED KNOWLEDGE',
    bg: 'bg-blue-50',
    text: 'text-blue-800',
    border: 'border-blue-300',
  },
  'AI INTERPRETATION': {
    label: 'AI INTERPRETATION',
    bg: 'bg-purple-50',
    text: 'text-purple-800',
    border: 'border-purple-300',
  },
  'USER INPUT': {
    label: 'USER INPUT',
    bg: 'bg-slate-100',
    text: 'text-slate-700',
    border: 'border-slate-300',
  },
  'EXTERNAL API': {
    label: 'EXTERNAL SOURCE',
    bg: 'bg-sky-50',
    text: 'text-sky-800',
    border: 'border-sky-300',
  },
  'SIMULATION / DEMO': {
    label: 'SIMULATION / DEMO',
    bg: 'bg-amber-50',
    text: 'text-amber-900',
    border: 'border-amber-300',
  },
  'DATA UNAVAILABLE': {
    label: 'DATA UNAVAILABLE',
    bg: 'bg-rose-50',
    text: 'text-rose-800',
    border: 'border-rose-300',
  },
  // Compatibility aliases
  OBSERVED: {
    label: 'OBSERVED DATA',
    bg: 'bg-emerald-50',
    text: 'text-emerald-800',
    border: 'border-emerald-300',
  },
  FORECAST: {
    label: 'FORECAST',
    bg: 'bg-sky-50',
    text: 'text-sky-800',
    border: 'border-sky-300',
  },
  PREDICTED: {
    label: 'MODEL OUTPUT',
    bg: 'bg-teal-50',
    text: 'text-teal-800',
    border: 'border-teal-300',
  },
  'AI GENERATED': {
    label: 'AI INTERPRETATION',
    bg: 'bg-purple-50',
    text: 'text-purple-800',
    border: 'border-purple-300',
  },
  'EXTERNAL SOURCE': {
    label: 'EXTERNAL SOURCE',
    bg: 'bg-sky-50',
    text: 'text-sky-800',
    border: 'border-sky-300',
  },
  SIMULATION: {
    label: 'SIMULATION / DEMO',
    bg: 'bg-amber-50',
    text: 'text-amber-900',
    border: 'border-amber-300',
  },
};

export default function DataTrustBadge({
  type,
  source,
  timestamp,
  className = '',
}: DataTrustBadgeProps) {
  const conf = BADGE_CONFIG[type] || BADGE_CONFIG['OBSERVED DATA'];

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md border text-[10px] font-mono tracking-tight transition shadow-2xs ${conf.bg} ${conf.text} ${conf.border} ${className}`}
      title={source ? `Source Provenance: ${source}${timestamp ? ` (${timestamp})` : ''}` : `Provenance: ${conf.label}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current opacity-80 shrink-0"></span>
      <span className="font-bold uppercase tracking-wider">{conf.label}</span>
      {source && (
        <span className="opacity-75 font-normal truncate max-w-[120px] hidden sm:inline">
          • {source}
        </span>
      )}
    </span>
  );
}
