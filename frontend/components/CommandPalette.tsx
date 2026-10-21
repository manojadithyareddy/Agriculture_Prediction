'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  Search, 
  Sprout, 
  Bug, 
  BarChart3, 
  TrendingUp, 
  Droplets, 
  SunMedium, 
  MessageSquare, 
  Activity, 
  Database, 
  FileText, 
  ShieldCheck, 
  Settings as SettingsIcon, 
  Layers, 
  Calendar, 
  Server
} from 'lucide-react';
import { useGlobalContext, FARMS } from '@/components/GlobalContext';

interface PaletteItem {
  id: string;
  title: string;
  category: 'NAVIGATION' | 'FARM ENTITY' | 'AI ACTION' | 'DATASET';
  subtitle?: string;
  icon: React.ComponentType<{ className?: string }>;
  action: () => void;
}

export default function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const router = useRouter();
  const { setFarmId, setParcelId } = useGlobalContext();

  // Keyboard shortcut listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setOpen((prev) => !prev);
      } else if (e.key === 'Escape' && open) {
        setOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open]);

  // Reset selected index when query changes
  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  // Navigate helper
  const navigateTo = (path: string) => {
    setOpen(false);
    setQuery('');
    router.push(path);
  };

  // Commands and entities database
  const items: PaletteItem[] = [
    // Navigation
    { id: 'nav-overview', title: 'Operations Overview', category: 'NAVIGATION', subtitle: 'Main agricultural telemetry & health hub', icon: Layers, action: () => navigateTo('/') },
    { id: 'nav-crop-analysis', title: 'Multispectral Crop Intelligence', category: 'NAVIGATION', subtitle: 'NDVI, NDRE & Thermal field maps', icon: BarChart3, action: () => navigateTo('/crop-analysis') },
    { id: 'nav-disease', title: 'Disease & Pest Vision Detection', category: 'NAVIGATION', subtitle: 'YOLOv8 leaf pathology classifier', icon: Bug, action: () => navigateTo('/detection') },
    { id: 'nav-crop-rec', title: 'Crop Recommendation', category: 'NAVIGATION', subtitle: 'NPK & agro-climate suitability decision engine', icon: Sprout, action: () => navigateTo('/predictions?tab=crop') },
    { id: 'nav-yield', title: 'Yield Prediction', category: 'NAVIGATION', subtitle: 'Acreage & fertilizer regression forecasting', icon: TrendingUp, action: () => navigateTo('/predictions?tab=yield') },
    { id: 'nav-irrigation', title: 'Irrigation Planning', category: 'NAVIGATION', subtitle: 'Root-zone moisture & FAO-56 scheduling', icon: Droplets, action: () => navigateTo('/predictions?tab=irrigation') },
    { id: 'nav-market', title: 'Market Price Intelligence', category: 'NAVIGATION', subtitle: 'APMC Mandi rate forecasts & MSP benchmarks', icon: TrendingUp, action: () => navigateTo('/predictions?tab=market') },
    { id: 'nav-weather', title: 'Weather & Microclimate', category: 'NAVIGATION', subtitle: '7-day forecast & safe spray windows', icon: SunMedium, action: () => navigateTo('/weather') },
    { id: 'nav-chat', title: 'AI Agronomist Workspace', category: 'NAVIGATION', subtitle: 'Multilingual RAG consultation with citations', icon: MessageSquare, action: () => navigateTo('/chat') },
    { id: 'nav-agent', title: 'Agent Execution Trace', category: 'NAVIGATION', subtitle: 'LangGraph multi-modal diagnostic DAG', icon: Activity, action: () => navigateTo('/agent') },
    { id: 'nav-datasets', title: 'Datasets & Agricultural Lab', category: 'NAVIGATION', subtitle: 'Corpus schemas, quality scores & lineage', icon: Database, action: () => navigateTo('/datasets') },
    { id: 'nav-reports', title: 'Field Operations & Reports', category: 'NAVIGATION', subtitle: 'Scouting logs, approvals & field audit trail', icon: FileText, action: () => navigateTo('/reports') },
    { id: 'nav-models', title: 'Model Registry', category: 'NAVIGATION', subtitle: 'Active ML/DL architectures, latencies & artifacts', icon: Server, action: () => navigateTo('/models') },
    { id: 'nav-health', title: 'System Observability', category: 'NAVIGATION', subtitle: 'FastAPI, Supabase & RAG latency metrics', icon: ShieldCheck, action: () => navigateTo('/system-health') },
    { id: 'nav-history', title: 'Audit History', category: 'NAVIGATION', subtitle: 'Unified prediction & diagnostic event logs', icon: Calendar, action: () => navigateTo('/history') },
    { id: 'nav-settings', title: 'System Settings', category: 'NAVIGATION', subtitle: 'API keys, farm profile & configuration', icon: SettingsIcon, action: () => navigateTo('/settings') },

    // Farms & Parcels
    ...FARMS.map((f) => ({
      id: `farm-${f.id}`,
      title: f.name,
      category: 'FARM ENTITY' as const,
      subtitle: `${f.id} • ${f.district}, ${f.state} (${f.parcels.length} parcels)`,
      icon: Layers,
      action: () => {
        setFarmId(f.id);
        setParcelId(f.parcels[0] || 'A1');
        setOpen(false);
        setQuery('');
      },
    })),

    // Fast AI Actions
    {
      id: 'ai-diag',
      title: 'Run Multi-Modal Field Diagnosis',
      category: 'AI ACTION',
      subtitle: 'Upload leaf scan and trigger autonomous LangGraph workflow',
      icon: Activity,
      action: () => navigateTo('/agent'),
    },
    {
      id: 'ai-spray',
      title: 'Compute Current Spray Window',
      category: 'AI ACTION',
      subtitle: 'Evaluate wind, delta-T and rain probability for today',
      icon: SunMedium,
      action: () => navigateTo('/weather'),
    },
  ];

  const filteredItems = query.trim() === ''
    ? items.slice(0, 10)
    : items.filter((item) => 
        item.title.toLowerCase().includes(query.toLowerCase()) ||
        item.subtitle?.toLowerCase().includes(query.toLowerCase()) ||
        item.category.toLowerCase().includes(query.toLowerCase())
      );

  const handleKeyDownInList = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % filteredItems.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + filteredItems.length) % filteredItems.length);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredItems[selectedIndex]) {
        filteredItems[selectedIndex].action();
      }
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-start justify-center p-4 sm:p-6 md:p-20 overflow-y-auto">
      <div 
        className="w-full max-w-2xl bg-white border border-slate-200 rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150 text-slate-800"
        onKeyDown={handleKeyDownInList}
      >
        {/* Search Input */}
        <div className="flex items-center px-4 py-3 border-b border-slate-200 gap-3">
          <Search className="w-5 h-5 text-emerald-700 shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search farms, parcels, crops, diseases, or ask AI..."
            className="w-full bg-transparent text-sm placeholder-slate-400 focus:outline-none text-slate-900"
            autoFocus
          />
          <kbd className="px-2 py-0.5 bg-slate-100 border border-slate-300 rounded text-[10px] font-mono text-slate-500">
            ESC
          </kbd>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-2 divide-y divide-slate-100">
          {filteredItems.length === 0 ? (
            <div className="py-8 text-center text-xs text-slate-500">
              No matching commands or agricultural entities found for &quot;{query}&quot;
            </div>
          ) : (
            filteredItems.map((item, idx) => {
              const Icon = item.icon;
              const isSelected = idx === selectedIndex;
              return (
                <button
                  key={item.id}
                  onClick={item.action}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`w-full text-left px-3 py-2.5 rounded-xl flex items-center gap-3 transition-colors ${
                    isSelected ? 'bg-emerald-50 text-emerald-950 border border-emerald-300' : 'hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className={`p-2 rounded-lg shrink-0 ${isSelected ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-500'}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold truncate text-slate-900">{item.title}</span>
                      <span className="text-[9px] px-1.5 py-0.2 bg-slate-100 text-slate-600 rounded font-mono uppercase border border-slate-200">
                        {item.category}
                      </span>
                    </div>
                    {item.subtitle && (
                      <p className="text-[11px] text-slate-500 truncate">{item.subtitle}</p>
                    )}
                  </div>
                  <span className="text-[10px] font-mono text-slate-400">↵ Open</span>
                </button>
              );
            })
          )}
        </div>

        {/* Footer info */}
        <div className="px-4 py-2.5 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-[11px] text-slate-500 font-mono">
          <div className="flex items-center gap-2">
            <span>↑↓ Navigate</span>
            <span>•</span>
            <span>↵ Select</span>
            <span>•</span>
            <span>ESC Close</span>
          </div>
          <span className="text-emerald-700 font-semibold">AgriFusion Command Palette</span>
        </div>
      </div>
    </div>
  );
}
