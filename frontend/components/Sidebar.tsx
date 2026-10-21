'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  BrainCircuit,
  ScanEye,
  MessageSquareText,
  History,
  BarChart3,
  Boxes,
  Settings,
  ChevronRight,
  PanelLeftClose,
  PanelLeft,
  Sprout,
  BarChart2,
  CloudLightning,
  Droplets,
  TrendingUp,
  Bug,
  Microscope,
  ScanSearch,
  ImagePlus,
  Cpu,
  MessagesSquare,
  BookOpen,
  Sparkles,
  Bot,
  ClipboardList,
  Eye,
  LineChart,
  Activity,
  Gauge,
  PieChart,
  Layers,
  Info,
  User,
  Shield,
  KeyRound,
  Sliders,
  Menu,
  X,
  Leaf
} from 'lucide-react';

/* ─────────────────────────────────────────────
   Navigation Architecture
   ───────────────────────────────────────────── */

interface NavChild {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
}

interface NavGroup {
  id: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  href?: string;          // direct link (no children)
  children?: NavChild[];
  separated?: boolean;    // visual divider above
}

const NAV_GROUPS: NavGroup[] = [
  {
    id: 'overview',
    name: 'Overview',
    icon: LayoutDashboard,
    href: '/',
  },
  {
    id: 'predictions',
    name: 'AI Predictions',
    icon: BrainCircuit,
    children: [
      { name: 'Crop Recommendation', href: '/predictions?tab=crop', icon: Sprout },
      { name: 'Yield Prediction', href: '/predictions?tab=yield', icon: BarChart2 },
      { name: 'Climate Risk', href: '/predictions?tab=climate', icon: CloudLightning },
      { name: 'Irrigation', href: '/predictions?tab=irrigation', icon: Droplets },
      { name: 'Market Analysis', href: '/predictions?tab=market', icon: TrendingUp },
    ],
  },
  {
    id: 'vision',
    name: 'Vision AI',
    icon: ScanEye,
    children: [
      { name: 'Disease Detection', href: '/detection', icon: Bug },
      { name: 'Pest Detection', href: '/detection?mode=pest', icon: Microscope },
      { name: 'Object Detection', href: '/detection?mode=object', icon: ScanSearch },
      { name: 'Image Analysis', href: '/crop-analysis', icon: ImagePlus },
      { name: 'OpenCV Processing', href: '/crop-analysis?mode=opencv', icon: Cpu },
    ],
  },
  {
    id: 'assistant',
    name: 'AI Assistant',
    icon: MessageSquareText,
    children: [
      { name: 'NLP Chat', href: '/chat', icon: MessagesSquare },
      { name: 'RAG Knowledge', href: '/models', icon: BookOpen },
      { name: 'GenAI Studio', href: '/chat?mode=genai', icon: Sparkles },
      { name: 'AI Agent', href: '/agent', icon: Bot },
    ],
  },
  {
    id: 'history',
    name: 'History',
    icon: History,
    children: [
      { name: 'All Records', href: '/history', icon: ClipboardList },
      { name: 'ML History', href: '/history?filter=ml', icon: BrainCircuit },
      { name: 'Vision History', href: '/history?filter=vision', icon: Eye },
      { name: 'AI Conversations', href: '/history?filter=chat', icon: MessagesSquare },
    ],
  },
  {
    id: 'analytics',
    name: 'Analytics',
    icon: BarChart3,
    children: [
      { name: 'Prediction Analytics', href: '/datasets', icon: LineChart },
      { name: 'Model Performance', href: '/system-health', icon: Gauge },
      { name: 'Usage Analytics', href: '/reports', icon: PieChart },
    ],
  },
  {
    id: 'models',
    name: 'Models',
    icon: Boxes,
    children: [
      { name: 'Available Models', href: '/models', icon: Layers },
      { name: 'Model Status', href: '/system-health', icon: Activity },
      { name: 'Model Information', href: '/datasets', icon: Info },
    ],
  },
  {
    id: 'settings',
    name: 'Settings',
    icon: Settings,
    separated: true,
    children: [
      { name: 'Profile', href: '/settings', icon: User },
      { name: 'Preferences', href: '/settings?tab=preferences', icon: Sliders },
      { name: 'Security', href: '/settings?tab=security', icon: Shield },
      { name: 'API / Configuration', href: '/settings?tab=api', icon: KeyRound },
    ],
  },
];

/* ─────────────────────────────────────────────
   AI System Status (bottom panel)
   ───────────────────────────────────────────── */

interface SystemService {
  name: string;
  status: 'operational' | 'degraded' | 'offline';
}

const AI_SERVICES: SystemService[] = [
  { name: 'ML', status: 'operational' },
  { name: 'Vision AI', status: 'operational' },
  { name: 'RAG', status: 'operational' },
  { name: 'GenAI', status: 'operational' },
];

const statusDot: Record<string, string> = {
  operational: 'bg-emerald-500',
  degraded: 'bg-amber-500',
  offline: 'bg-rose-500',
};

/* ─────────────────────────────────────────────
   Sidebar Component
   ───────────────────────────────────────────── */

export default function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);

  // Determine which group is active based on current route
  const getActiveGroupId = useCallback((): string | null => {
    for (const group of NAV_GROUPS) {
      if (group.href) {
        const [gPath] = group.href.split('?');
        if (gPath === '/' && pathname === '/') return group.id;
        if (gPath !== '/' && pathname.startsWith(gPath)) return group.id;
      }
      if (group.children) {
        for (const child of group.children) {
          const [cPath] = child.href.split('?');
          if (pathname === cPath || pathname.startsWith(cPath + '/')) return group.id;
        }
      }
    }
    return null;
  }, [pathname]);

  // Auto-expand the group that contains the active route
  useEffect(() => {
    const activeGroup = getActiveGroupId();
    if (activeGroup && !collapsed) {
      setExpandedId(activeGroup);
    }
  }, [pathname, collapsed, getActiveGroupId]);

  // Close mobile drawer on route change
  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  const isChildActive = (href: string): boolean => {
    const [childPath, childQuery] = href.split('?');
    if (pathname !== childPath) return false;
    if (!childQuery) return true;
    // If there's a query parameter in the href, check if the current URL has it
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const [key, value] = childQuery.split('=');
      return params.get(key) === value;
    }
    return true;
  };

  const toggleGroup = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  /* ──── Render ──── */

  const renderNavContent = () => (
    <div className="flex flex-col h-full">
      {/* ─── Brand ─── */}
      <div className={`flex items-center gap-3 px-4 h-16 shrink-0 border-b border-slate-100 ${collapsed ? 'justify-center px-0' : ''}`}>
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-600 to-green-500 flex items-center justify-center text-white shrink-0 shadow-sm shadow-emerald-600/25">
          <Leaf className="w-5 h-5" />
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <div className="text-[15px] font-extrabold text-slate-900 tracking-tight leading-tight truncate">
              AI <span className="text-emerald-700">AGRI</span>
            </div>
            <div className="text-[10px] text-slate-400 font-medium tracking-wide truncate">
              Intelligence Platform
            </div>
          </div>
        )}
      </div>

      {/* ─── Navigation ─── */}
      <nav className="flex-1 overflow-y-auto py-3 px-2.5 space-y-0.5 scrollbar-thin">
        {NAV_GROUPS.map((group) => {
          const Icon = group.icon;
          const isActive = getActiveGroupId() === group.id;
          const isExpanded = expandedId === group.id;
          const hasChildren = !!group.children?.length;

          return (
            <div key={group.id}>
              {/* Separator */}
              {group.separated && (
                <div className="my-3 mx-2 border-t border-slate-100" />
              )}

              {/* Group Header */}
              {group.href && !hasChildren ? (
                /* Direct-link items (Overview) */
                <Link
                  href={group.href}
                  className={`group flex items-center gap-2.5 w-full rounded-xl transition-all duration-200 ${
                    collapsed ? 'justify-center px-0 py-2.5 mx-auto' : 'px-3 py-2.5'
                  } ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-900'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                  title={collapsed ? group.name : undefined}
                >
                  <div className="relative shrink-0 flex items-center justify-center">
                    {isActive && (
                      <span className="absolute -left-[13px] w-[3px] h-5 rounded-r-full bg-emerald-600" />
                    )}
                    <Icon className={`w-[18px] h-[18px] ${isActive ? 'text-emerald-700' : 'text-slate-500 group-hover:text-slate-700'}`} />
                  </div>
                  {!collapsed && (
                    <span className={`text-[13px] truncate ${isActive ? 'font-semibold' : 'font-medium'}`}>
                      {group.name}
                    </span>
                  )}
                </Link>
              ) : (
                /* Expandable group headers */
                <button
                  onClick={() => toggleGroup(group.id)}
                  className={`group flex items-center gap-2.5 w-full rounded-xl transition-all duration-200 ${
                    collapsed ? 'justify-center px-0 py-2.5 mx-auto' : 'px-3 py-2.5'
                  } ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-900'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                  title={collapsed ? group.name : undefined}
                >
                  <div className="relative shrink-0 flex items-center justify-center">
                    {isActive && (
                      <span className="absolute -left-[13px] w-[3px] h-5 rounded-r-full bg-emerald-600" />
                    )}
                    <Icon className={`w-[18px] h-[18px] ${isActive ? 'text-emerald-700' : 'text-slate-500 group-hover:text-slate-700'}`} />
                  </div>
                  {!collapsed && (
                    <>
                      <span className={`text-[13px] truncate flex-1 text-left ${isActive ? 'font-semibold' : 'font-medium'}`}>
                        {group.name}
                      </span>
                      <ChevronRight className={`w-3.5 h-3.5 text-slate-400 shrink-0 transition-transform duration-200 ${isExpanded ? 'rotate-90' : ''}`} />
                    </>
                  )}
                </button>
              )}

              {/* Expanded Children */}
              {hasChildren && !collapsed && (
                <div
                  className={`overflow-hidden transition-all duration-250 ease-in-out ${
                    isExpanded ? 'max-h-96 opacity-100 mt-0.5' : 'max-h-0 opacity-0'
                  }`}
                >
                  <div className="ml-[18px] pl-3 border-l border-slate-200/80 space-y-0.5 py-0.5">
                    {group.children!.map((child) => {
                      const ChildIcon = child.icon;
                      const childActive = isChildActive(child.href);

                      return (
                        <Link
                          key={child.href + child.name}
                          href={child.href}
                          className={`group/child flex items-center gap-2 px-2.5 py-[7px] rounded-lg transition-all duration-150 ${
                            childActive
                              ? 'bg-emerald-600 text-white shadow-sm shadow-emerald-600/20'
                              : 'text-slate-500 hover:text-slate-800 hover:bg-slate-50'
                          }`}
                        >
                          <ChildIcon className={`w-3.5 h-3.5 shrink-0 ${childActive ? 'text-emerald-100' : 'text-slate-400 group-hover/child:text-slate-600'}`} />
                          <span className={`text-[12px] truncate ${childActive ? 'font-semibold' : 'font-medium'}`}>
                            {child.name}
                          </span>
                        </Link>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </nav>

      {/* ─── AI System Status ─── */}
      <div className={`shrink-0 border-t border-slate-100 ${collapsed ? 'px-2 py-3' : 'px-4 py-3'}`}>
        {!collapsed ? (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-slate-400 tracking-wider uppercase">AI Systems</span>
              <span className="text-[10px] font-semibold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded-md">Live</span>
            </div>
            <div className="grid grid-cols-2 gap-x-3 gap-y-1">
              {AI_SERVICES.map((svc) => (
                <div key={svc.name} className="flex items-center gap-1.5">
                  <span className={`w-1.5 h-1.5 rounded-full ${statusDot[svc.status]} shrink-0`} />
                  <span className="text-[11px] text-slate-500 truncate">{svc.name}</span>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-1.5" title="AI Systems Operational">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-[9px] text-slate-400 font-medium">Live</span>
          </div>
        )}
      </div>

      {/* ─── User Profile ─── */}
      <div className={`shrink-0 border-t border-slate-100 ${collapsed ? 'px-2 py-3 flex justify-center' : 'px-3 py-3'}`}>
        {!collapsed ? (
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-slate-900 text-white flex items-center justify-center text-[11px] font-bold shrink-0">
              MR
            </div>
            <div className="min-w-0">
              <div className="text-[12px] font-semibold text-slate-800 truncate">Manoj A. Reddy</div>
              <div className="text-[10px] text-slate-400 truncate">Administrator</div>
            </div>
          </div>
        ) : (
          <div className="w-8 h-8 rounded-lg bg-slate-900 text-white flex items-center justify-center text-[11px] font-bold" title="Manoj A. Reddy">
            MR
          </div>
        )}
      </div>

      {/* ─── Collapse Toggle (Desktop) ─── */}
      <div className="shrink-0 border-t border-slate-100 hidden lg:block">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="w-full flex items-center justify-center py-2.5 text-slate-400 hover:text-slate-600 hover:bg-slate-50 transition"
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <PanelLeft className="w-4 h-4" /> : <PanelLeftClose className="w-4 h-4" />}
        </button>
      </div>
    </div>
  );

  return (
    <>
      {/* ─── Mobile Menu Button ─── */}
      <button
        onClick={() => setMobileOpen(true)}
        className="lg:hidden fixed top-[18px] left-3 z-50 w-9 h-9 rounded-xl bg-white border border-slate-200 shadow-sm flex items-center justify-center text-slate-700 hover:bg-slate-50 transition"
        aria-label="Open navigation"
      >
        <Menu className="w-4.5 h-4.5" />
      </button>

      {/* ─── Mobile Drawer Overlay ─── */}
      {mobileOpen && (
        <div className="lg:hidden fixed inset-0 z-50">
          <div
            className="absolute inset-0 bg-black/30 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
          />
          <aside className="absolute left-0 top-0 bottom-0 w-[270px] bg-white shadow-2xl animate-in slide-in-from-left duration-200">
            <button
              onClick={() => setMobileOpen(false)}
              className="absolute top-4 right-3 p-1.5 rounded-lg hover:bg-slate-100 text-slate-500 transition"
              aria-label="Close navigation"
            >
              <X className="w-4 h-4" />
            </button>
            {renderNavContent()}
          </aside>
        </div>
      )}

      {/* ─── Desktop Sidebar ─── */}
      <aside
        className={`hidden lg:flex flex-col bg-white border-r border-slate-100 min-h-[calc(100vh-72px)] select-none shrink-0 transition-all duration-250 ease-in-out ${
          collapsed ? 'w-[68px]' : 'w-[252px]'
        }`}
      >
        {renderNavContent()}
      </aside>
    </>
  );
}
