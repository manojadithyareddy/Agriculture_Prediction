'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  BrainCircuit,
  ScanEye,
  MessageSquareText,
  BarChart3,
  MoreHorizontal,
  ChevronDown,
  Search,
  Bell,
  User,
  LogOut,
  Shield,
  Sliders,
  Menu,
  X,
  Leaf,
  ChevronRight,

  // AI Predictions
  Sprout,
  BarChart2,
  CloudLightning,
  Droplets,
  TrendingUp,
  Clock,
  Bookmark,
  GitCompare,
  CloudSun,

  // Vision AI
  Bug,
  Microscope,
  ScanSearch,
  ImagePlus,
  Layers,
  Eye,
  Cpu,
  Wand2,

  // AI Assistant
  MessagesSquare,
  Sparkles,
  Bot,
  BookOpen,
  Upload,
  FileText,
  Type,
  Lightbulb,

  // Analytics
  LineChart,
  Gauge,
  Activity,
  PieChart,
  ClipboardList,

  // More
  Boxes,
  History,
  HelpCircle,
  Settings,
  Database,
  Info,
} from 'lucide-react';

/* ═══════════════════════════════════════════════════════════
   TYPE SYSTEM
   ═══════════════════════════════════════════════════════════ */

interface DropdownItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  description?: string;
}

interface DropdownSection {
  title: string;
  icon: React.ComponentType<{ className?: string }>;
  items: DropdownItem[];
}

interface NavItem {
  id: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  href?: string;
  sections?: DropdownSection[];
  cols?: number;
}

/* ═══════════════════════════════════════════════════════════
   NAVIGATION DATA
   ═══════════════════════════════════════════════════════════ */

const NAV_ITEMS: NavItem[] = [
  {
    id: 'dashboard',
    name: 'Dashboard',
    icon: LayoutDashboard,
    href: '/',
  },
  {
    id: 'market',
    name: 'Market Intelligence',
    icon: TrendingUp,
    href: '/market',
  },
  {
    id: 'predictions',
    name: 'AI Predictions',
    icon: BrainCircuit,
    cols: 2,
    sections: [
      {
        title: 'Machine Learning',
        icon: BrainCircuit,
        items: [
          { name: 'Climate Risk Prediction', href: '/predictions?tab=climate', icon: CloudLightning, description: 'Assess climate risks for crops' },
          { name: 'Crop Recommendation', href: '/predictions?tab=crop', icon: Sprout, description: 'AI-powered crop selection' },
          { name: 'Yield Prediction', href: '/predictions?tab=yield', icon: BarChart2, description: 'Estimate harvest outcomes' },
          { name: 'Irrigation Prediction', href: '/predictions?tab=irrigation', icon: Droplets, description: 'Optimize water usage' },
          { name: 'Market Price Prediction', href: '/market', icon: TrendingUp, description: 'Commodity price forecasting' },
        ],
      },
      {
        title: 'Quick Access',
        icon: Clock,
        items: [
          { name: 'Prediction History', href: '/history?filter=ml', icon: Clock, description: 'View past predictions' },
          { name: 'Saved Predictions', href: '/history', icon: Bookmark, description: 'Bookmarked results' },
          { name: 'Compare Results', href: '/datasets', icon: GitCompare, description: 'Side-by-side analysis' },
          { name: 'Weather & Climate', href: '/weather', icon: CloudSun, description: 'Current conditions' },
        ],
      },
    ],
  },
  {
    id: 'vision',
    name: 'AI Vision',
    icon: ScanEye,
    cols: 3,
    sections: [
      {
        title: 'Computer Vision',
        icon: ScanEye,
        items: [
          { name: 'Disease Detection', href: '/detection', icon: Bug, description: 'Identify crop diseases' },
          { name: 'Pest Detection', href: '/detection?mode=pest', icon: Microscope, description: 'Insect & pest identification' },
          { name: 'Crop Detection', href: '/detection?mode=object', icon: ScanSearch, description: 'Crop type recognition' },
          { name: 'Image Analysis', href: '/crop-analysis', icon: ImagePlus, description: 'Upload & analyze images' },
        ],
      },
      {
        title: 'Deep Learning',
        icon: Layers,
        items: [
          { name: 'Object Detection', href: '/detection?mode=object', icon: Eye, description: 'YOLO-based detection' },
          { name: 'Image Classification', href: '/crop-analysis', icon: Layers, description: 'CNN classification' },
          { name: 'Model Results', href: '/system-health', icon: Gauge, description: 'Performance metrics' },
        ],
      },
      {
        title: 'Image Processing',
        icon: Wand2,
        items: [
          { name: 'OpenCV Processing', href: '/crop-analysis?mode=opencv', icon: Cpu, description: 'Advanced image filters' },
          { name: 'Image Enhancement', href: '/crop-analysis', icon: Wand2, description: 'Preprocessing pipeline' },
          { name: 'Visualization', href: '/detection', icon: Eye, description: 'Detection overlays' },
        ],
      },
    ],
  },
  {
    id: 'assistant',
    name: 'AI Assistant',
    icon: MessageSquareText,
    cols: 2,
    sections: [
      {
        title: 'AI Assistant',
        icon: MessagesSquare,
        items: [
          { name: 'Bilingual AI Assistant', href: '/ai-assistant', icon: MessagesSquare, description: 'Agronomist with Telugu & source citations' },
          { name: 'Agriculture Chat', href: '/chat', icon: Bot, description: 'Talk to your AI agronomist' },
          { name: 'AI Recommendations', href: '/chat?mode=recommend', icon: Lightbulb, description: 'Get actionable insights' },
          { name: 'Prediction Explanation', href: '/chat?mode=explain', icon: Info, description: 'Understand AI decisions' },
        ],
      },
      {
        title: 'RAG Knowledge',
        icon: BookOpen,
        items: [
          { name: 'Chat with Documents', href: '/models', icon: BookOpen, description: 'Query your knowledge base' },
          { name: 'Upload Documents', href: '/models', icon: Upload, description: 'Add new sources' },
          { name: 'Knowledge Base', href: '/models', icon: Database, description: 'Browse indexed content' },
        ],
      },
      {
        title: 'NLP & Text',
        icon: Type,
        items: [
          { name: 'Text Analysis', href: '/chat', icon: Type, description: 'Analyze agricultural text' },
          { name: 'Text Classification', href: '/chat', icon: FileText, description: 'Classify documents' },
        ],
      },
      {
        title: 'Generative AI',
        icon: Sparkles,
        items: [
          { name: 'AI Generation', href: '/chat?mode=genai', icon: Sparkles, description: 'Generate reports & insights' },
          { name: 'AI Agent', href: '/agent', icon: Bot, description: 'Autonomous AI operations' },
          { name: 'AI Reports', href: '/reports', icon: FileText, description: 'Auto-generated reports' },
        ],
      },
    ],
  },
  {
    id: 'analytics',
    name: 'Analytics',
    icon: BarChart3,
    cols: 1,
    sections: [
      {
        title: 'Analytics',
        icon: BarChart3,
        items: [
          { name: 'Analytics Dashboard', href: '/datasets', icon: PieChart, description: 'Overview metrics' },
          { name: 'Prediction Analytics', href: '/datasets', icon: LineChart, description: 'ML performance analysis' },
          { name: 'Model Performance', href: '/system-health', icon: Gauge, description: 'Accuracy & latency' },
          { name: 'Usage Analytics', href: '/reports', icon: Activity, description: 'Platform utilization' },
          { name: 'AI Activity', href: '/history', icon: ClipboardList, description: 'System activity log' },
          { name: 'Reports', href: '/reports', icon: FileText, description: 'Export & download' },
        ],
      },
    ],
  },
  {
    id: 'more',
    name: 'More',
    icon: MoreHorizontal,
    cols: 1,
    sections: [
      {
        title: 'Platform',
        icon: Boxes,
        items: [
          { name: 'About AgriFusion AI', href: '/about', icon: Info, description: 'Architecture, methodology & ethics' },
          { name: 'Models', href: '/models', icon: Boxes },
          { name: 'Model Status', href: '/system-health', icon: Activity },
          { name: 'Datasets', href: '/datasets', icon: Database },
          { name: 'Documents', href: '/models', icon: FileText },
          { name: 'Prediction History', href: '/history', icon: History },
          { name: 'System Status', href: '/system-health', icon: Gauge },
          { name: 'Help & Documentation', href: '/models', icon: HelpCircle },
          { name: 'Settings', href: '/settings', icon: Settings },
        ],
      },
    ],
  },
];

const PROFILE_LINKS: DropdownItem[] = [
  { name: 'Profile', href: '/settings', icon: User },
  { name: 'Preferences', href: '/settings?tab=preferences', icon: Sliders },
  { name: 'Security', href: '/settings?tab=security', icon: Shield },
];

/* ═══════════════════════════════════════════════════════════
   HEADER COMPONENT
   ═══════════════════════════════════════════════════════════ */

export default function Header() {
  const pathname = usePathname();
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const [profileOpen, setProfileOpen] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileExpanded, setMobileExpanded] = useState<string | null>(null);
  const navRef = useRef<HTMLElement>(null);
  const profileRef = useRef<HTMLDivElement>(null);

  /* ── Route-based active detection ── */
  const isNavActive = useCallback((item: NavItem): boolean => {
    if (item.href) {
      const [path] = item.href.split('?');
      if (path === '/' && pathname === '/') return true;
      if (path !== '/' && pathname.startsWith(path)) return true;
    }
    if (item.sections) {
      for (const section of item.sections) {
        for (const child of section.items) {
          const [cPath] = child.href.split('?');
          if (pathname === cPath || (cPath !== '/' && pathname.startsWith(cPath))) return true;
        }
      }
    }
    return false;
  }, [pathname]);

  /* ── Close handlers ── */
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (navRef.current && !navRef.current.contains(e.target as Node)) {
        setActiveDropdown(null);
      }
      if (profileRef.current && !profileRef.current.contains(e.target as Node)) {
        setProfileOpen(false);
      }
    };
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setActiveDropdown(null);
        setProfileOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, []);

  useEffect(() => {
    setActiveDropdown(null);
    setProfileOpen(false);
    setMobileOpen(false);
    setMobileExpanded(null);
  }, [pathname]);

  const toggleDropdown = (id: string) => {
    setActiveDropdown((prev) => (prev === id ? null : id));
    setProfileOpen(false);
  };

  const openCommandPalette = () => {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', metaKey: true }));
  };

  /* ═══════════════════════════════════════════════════════════
     MEGA DROPDOWN RENDERER
     ═══════════════════════════════════════════════════════════ */

  const renderMegaMenu = (item: NavItem) => {
    if (!item.sections) return null;
    const cols = item.cols || 1;
    const isRight = item.id === 'more' || item.id === 'analytics';

    return (
      <div
        className={`absolute top-full pt-2 z-50 ${isRight ? 'right-0' : 'left-1/2 -translate-x-1/2'}`}
      >
        <div
          className={`mega-dropdown bg-[#0d1526]/[0.97] backdrop-blur-2xl border border-white/[0.08] rounded-2xl shadow-2xl shadow-black/40 overflow-hidden ${
            cols === 1 ? 'w-[300px]' : cols === 2 ? 'w-[540px]' : 'w-[720px]'
          }`}
        >
          {/* Dropdown Header */}
          <div className="px-5 pt-4 pb-3 border-b border-white/[0.06]">
            <div className="flex items-center gap-2">
              <item.icon className="w-4 h-4 text-emerald-400" />
              <span className="text-[13px] font-semibold text-white">{item.name}</span>
            </div>
          </div>

          {/* Sections Grid */}
          <div className={`p-4 grid gap-4 ${
            cols === 1 ? 'grid-cols-1' : cols === 2 ? 'grid-cols-2' : 'grid-cols-3'
          }`}>
            {item.sections.map((section) => (
              <div key={section.title} className="space-y-2">
                {/* Section Title */}
                <div className="flex items-center gap-1.5 px-1">
                  <section.icon className="w-3.5 h-3.5 text-emerald-500/80" />
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                    {section.title}
                  </span>
                </div>
                {/* Section Items */}
                <div className="space-y-0.5">
                  {section.items.map((link) => {
                    const LinkIcon = link.icon;
                    return (
                      <Link
                        key={link.name + link.href}
                        href={link.href}
                        onClick={() => setActiveDropdown(null)}
                        className="group flex items-start gap-2.5 px-2.5 py-2 rounded-lg hover:bg-white/[0.06] transition-colors duration-150"
                      >
                        <LinkIcon className="w-4 h-4 text-slate-500 group-hover:text-emerald-400 mt-0.5 shrink-0 transition-colors" />
                        <div className="min-w-0">
                          <div className="text-[12.5px] font-medium text-slate-200 group-hover:text-white truncate transition-colors">
                            {link.name}
                          </div>
                          {link.description && (
                            <div className="text-[10.5px] text-slate-500 group-hover:text-slate-400 truncate transition-colors">
                              {link.description}
                            </div>
                          )}
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  /* ═══════════════════════════════════════════════════════════
     DESKTOP NAV
     ═══════════════════════════════════════════════════════════ */

  return (
    <>
      <header className="sticky top-0 z-40 w-full">
        <nav
          ref={navRef}
          className="h-[60px] bg-[#0B1121]/92 backdrop-blur-2xl border-b border-white/[0.06] px-4 lg:px-6 flex items-center justify-between gap-2 select-none shadow-[0_1px_20px_rgba(0,0,0,0.12)]"
        >
          {/* ─── Left: Logo ─── */}
          <Link href="/" className="flex items-center gap-2.5 shrink-0 group mr-2">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center text-white shadow-lg shadow-emerald-600/25 group-hover:shadow-emerald-500/35 transition-shadow">
              <Leaf className="w-[18px] h-[18px]" />
            </div>
            <div className="hidden sm:block">
              <div className="text-[15px] font-extrabold tracking-tight leading-none">
                <span className="text-white">Agri</span>
                <span className="text-emerald-400">Fusion</span>
                <span className="text-slate-400 font-medium text-[11px] ml-1">AI</span>
              </div>
              <p className="text-[9px] text-slate-500 tracking-wide font-medium">
                Intelligence Platform
              </p>
            </div>
          </Link>

          {/* ─── Center: Main Navigation (Desktop) ─── */}
          <div className="hidden lg:flex items-center gap-0.5 flex-1 justify-center">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const active = isNavActive(item);
              const hasDropdown = !!item.sections;
              const isOpen = activeDropdown === item.id;

              return (
                <div key={item.id} className="relative">
                  {item.href && !hasDropdown ? (
                    /* Direct link (Dashboard) */
                    <Link
                      href={item.href}
                      className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-[13px] font-medium transition-all duration-200 ${
                        active
                          ? 'text-white bg-white/[0.08]'
                          : 'text-slate-400 hover:text-white hover:bg-white/[0.05]'
                      }`}
                    >
                      <Icon className={`w-4 h-4 ${active ? 'text-emerald-400' : ''}`} />
                      <span>{item.name}</span>
                      {active && (
                        <span className="absolute bottom-0 left-3 right-3 h-[2px] bg-emerald-500 rounded-full" />
                      )}
                    </Link>
                  ) : (
                    /* Dropdown trigger */
                    <button
                      onClick={() => toggleDropdown(item.id)}
                      className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-[13px] font-medium transition-all duration-200 ${
                        isOpen
                          ? 'text-white bg-white/[0.1]'
                          : active
                          ? 'text-white bg-white/[0.08]'
                          : 'text-slate-400 hover:text-white hover:bg-white/[0.05]'
                      }`}
                    >
                      <Icon className={`w-4 h-4 ${active || isOpen ? 'text-emerald-400' : ''}`} />
                      <span>{item.name}</span>
                      <ChevronDown className={`w-3 h-3 text-slate-500 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
                      {(active && !isOpen) && (
                        <span className="absolute bottom-0 left-3 right-3 h-[2px] bg-emerald-500 rounded-full" />
                      )}
                    </button>
                  )}

                  {/* Mega Menu */}
                  {isOpen && renderMegaMenu(item)}
                </div>
              );
            })}
          </div>

          {/* ─── Right: Controls ─── */}
          <div className="flex items-center gap-1 shrink-0">
            {/* Search */}
            <button
              onClick={openCommandPalette}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] transition-colors"
              title="Search (⌘K)"
            >
              <Search className="w-[18px] h-[18px]" />
            </button>

            {/* Notifications */}
            <button
              className="relative p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] transition-colors"
              title="Notifications"
            >
              <Bell className="w-[18px] h-[18px]" />
              <span className="absolute top-1 right-1 w-4 h-4 bg-rose-500 text-white text-[8px] font-bold rounded-full flex items-center justify-center ring-2 ring-[#0B1121]">
                3
              </span>
            </button>

            {/* Divider */}
            <div className="w-px h-6 bg-white/[0.08] mx-1.5 hidden sm:block" />

            {/* Profile */}
            <div ref={profileRef} className="relative">
              <button
                onClick={() => {
                  setProfileOpen(!profileOpen);
                  setActiveDropdown(null);
                }}
                className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-white/[0.06] transition-colors"
              >
                <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-emerald-600 to-green-700 text-white flex items-center justify-center text-[10px] font-bold shadow-sm">
                  MR
                </div>
                <div className="hidden xl:block text-left">
                  <div className="text-[12px] font-semibold text-slate-200 leading-tight">Manoj A. Reddy</div>
                  <div className="text-[9px] text-slate-500 leading-tight">Administrator</div>
                </div>
                <ChevronDown className={`w-3 h-3 text-slate-500 hidden xl:block transition-transform ${profileOpen ? 'rotate-180' : ''}`} />
              </button>

              {/* Profile Dropdown */}
              {profileOpen && (
                <div className="absolute top-full right-0 pt-2 z-50">
                  <div className="mega-dropdown w-[220px] bg-[#0d1526]/[0.97] backdrop-blur-2xl border border-white/[0.08] rounded-xl shadow-2xl shadow-black/40 overflow-hidden py-1.5">
                    {/* Profile Header */}
                    <div className="px-4 py-3 border-b border-white/[0.06]">
                      <div className="text-[13px] font-semibold text-white">Manoj A. Reddy</div>
                      <div className="text-[11px] text-slate-400">manoj@agrifusion.ai</div>
                    </div>

                    {/* Links */}
                    <div className="py-1.5 px-1.5">
                      {PROFILE_LINKS.map((link) => {
                        const PIcon = link.icon;
                        return (
                          <Link
                            key={link.name}
                            href={link.href}
                            onClick={() => setProfileOpen(false)}
                            className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-[12.5px] font-medium text-slate-300 hover:text-white hover:bg-white/[0.06] transition-colors"
                          >
                            <PIcon className="w-4 h-4 text-slate-500" />
                            {link.name}
                          </Link>
                        );
                      })}
                    </div>

                    {/* Logout */}
                    <div className="border-t border-white/[0.06] pt-1.5 px-1.5 pb-0.5">
                      <button className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-[12.5px] font-medium text-rose-400 hover:text-rose-300 hover:bg-rose-500/[0.08] transition-colors">
                        <LogOut className="w-4 h-4" />
                        Sign Out
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileOpen(true)}
              className="lg:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] transition-colors ml-1"
              aria-label="Open navigation menu"
            >
              <Menu className="w-5 h-5" />
            </button>
          </div>
        </nav>
      </header>

      {/* ═══════════════════════════════════════════════════════════
         MOBILE DRAWER
         ═══════════════════════════════════════════════════════════ */}
      {mobileOpen && (
        <div className="lg:hidden fixed inset-0 z-50">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
          />

          {/* Drawer */}
          <aside className="absolute right-0 top-0 bottom-0 w-[300px] bg-[#0B1121] shadow-2xl mega-dropdown overflow-y-auto">
            {/* Drawer Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/[0.06]">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center text-white">
                  <Leaf className="w-[18px] h-[18px]" />
                </div>
                <span className="text-[15px] font-extrabold text-white tracking-tight">
                  Agri<span className="text-emerald-400">Fusion</span>
                </span>
              </div>
              <button
                onClick={() => setMobileOpen(false)}
                className="p-1.5 rounded-lg hover:bg-white/[0.06] text-slate-400 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Mobile Nav Items */}
            <nav className="py-3 px-3 space-y-0.5">
              {NAV_ITEMS.map((item) => {
                const Icon = item.icon;
                const hasChildren = !!item.sections;
                const isExpanded = mobileExpanded === item.id;
                const active = isNavActive(item);

                return (
                  <div key={item.id}>
                    {item.href && !hasChildren ? (
                      <Link
                        href={item.href}
                        onClick={() => setMobileOpen(false)}
                        className={`flex items-center gap-3 px-4 py-3 rounded-xl text-[14px] font-medium transition-colors ${
                          active
                            ? 'text-white bg-white/[0.08]'
                            : 'text-slate-300 hover:text-white hover:bg-white/[0.05]'
                        }`}
                      >
                        <Icon className={`w-5 h-5 ${active ? 'text-emerald-400' : 'text-slate-500'}`} />
                        {item.name}
                      </Link>
                    ) : (
                      <button
                        onClick={() => setMobileExpanded(isExpanded ? null : item.id)}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-[14px] font-medium transition-colors ${
                          active
                            ? 'text-white bg-white/[0.08]'
                            : 'text-slate-300 hover:text-white hover:bg-white/[0.05]'
                        }`}
                      >
                        <Icon className={`w-5 h-5 ${active ? 'text-emerald-400' : 'text-slate-500'}`} />
                        <span className="flex-1 text-left">{item.name}</span>
                        <ChevronRight className={`w-4 h-4 text-slate-500 transition-transform duration-200 ${isExpanded ? 'rotate-90' : ''}`} />
                      </button>
                    )}

                    {/* Mobile Expanded Children */}
                    {hasChildren && (
                      <div className={`overflow-hidden transition-all duration-250 ease-in-out ${isExpanded ? 'max-h-[1200px] opacity-100' : 'max-h-0 opacity-0'}`}>
                        <div className="pl-6 pr-2 pb-2 space-y-3 pt-2">
                          {item.sections!.map((section) => (
                            <div key={section.title}>
                              <div className="flex items-center gap-1.5 px-3 py-1">
                                <section.icon className="w-3 h-3 text-emerald-500/70" />
                                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                  {section.title}
                                </span>
                              </div>
                              {section.items.map((link) => {
                                const LIcon = link.icon;
                                return (
                                  <Link
                                    key={link.name + link.href}
                                    href={link.href}
                                    onClick={() => setMobileOpen(false)}
                                    className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-[12.5px] text-slate-400 hover:text-white hover:bg-white/[0.05] transition-colors"
                                  >
                                    <LIcon className="w-3.5 h-3.5 text-slate-600" />
                                    {link.name}
                                  </Link>
                                );
                              })}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </nav>

            {/* Mobile Profile */}
            <div className="border-t border-white/[0.06] px-4 py-4 mt-2">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-600 to-green-700 text-white flex items-center justify-center text-[11px] font-bold">
                  MR
                </div>
                <div>
                  <div className="text-[13px] font-semibold text-white">Manoj A. Reddy</div>
                  <div className="text-[11px] text-slate-500">Administrator</div>
                </div>
              </div>
              <div className="space-y-0.5">
                {PROFILE_LINKS.map((link) => {
                  const PIcon = link.icon;
                  return (
                    <Link
                      key={link.name}
                      href={link.href}
                      onClick={() => setMobileOpen(false)}
                      className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-[12.5px] text-slate-400 hover:text-white hover:bg-white/[0.05] transition-colors"
                    >
                      <PIcon className="w-4 h-4 text-slate-500" />
                      {link.name}
                    </Link>
                  );
                })}
                <button className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-[12.5px] text-rose-400 hover:text-rose-300 hover:bg-rose-500/[0.06] transition-colors">
                  <LogOut className="w-4 h-4" />
                  Sign Out
                </button>
              </div>
            </div>
          </aside>
        </div>
      )}
    </>
  );
}
