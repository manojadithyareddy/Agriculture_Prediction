'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Sprout, 
  BarChart3, 
  Scan, 
  MessageSquare, 
  Bot, 
  History, 
  TrendingUp,
  Info,
  Settings as SettingsIcon
} from 'lucide-react';

const NAV_ITEMS = [
  { name: 'Dashboard', href: '/', icon: BarChart3 },
  { name: 'Market', href: '/market', icon: TrendingUp },
  { name: 'AI Assistant', href: '/ai-assistant', icon: MessageSquare },
  { name: 'Predictions', href: '/predictions', icon: Sprout },
  { name: 'Vision', href: '/detection', icon: Scan },
  { name: 'About', href: '/about', icon: Info },
  { name: 'History', href: '/history', icon: History },
  { name: 'System', href: '/settings', icon: SettingsIcon },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 50,
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      background: 'rgba(8, 13, 9, 0.85)',
      borderBottom: '1px solid var(--border-subtle)',
    }}>
      <div className="container" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: '70px',
      }}>
        {/* Brand Logo */}
        <Link href="/" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          textDecoration: 'none',
        }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 15px rgba(16, 185, 129, 0.4)',
          }}>
            <Sprout size={24} color="#ffffff" />
          </div>
          <div>
            <div style={{ fontWeight: 800, fontSize: '1.2rem', letterSpacing: '-0.02em', color: '#ffffff' }}>
              Agri<span className="gradient-text">Fusion</span> AI
            </div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
              Andhra Pradesh & Telangana Agriculture System
            </div>
          </div>
        </Link>

        {/* Navigation Items */}
        <nav style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
        }}>
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));
            return (
              <Link
                key={item.name}
                href={item.href}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 14px',
                  borderRadius: '10px',
                  fontSize: '0.88rem',
                  fontWeight: isActive ? 700 : 500,
                  textDecoration: 'none',
                  color: isActive ? '#34d399' : 'var(--text-secondary)',
                  background: isActive ? 'rgba(16, 185, 129, 0.12)' : 'transparent',
                  border: isActive ? '1px solid rgba(16, 185, 129, 0.25)' : '1px solid transparent',
                  transition: 'all 0.2s ease',
                }}
              >
                <Icon size={16} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* Status indicator */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div className="badge badge-emerald">
            <span style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: '#34d399',
              boxShadow: '0 0 8px #34d399',
              display: 'inline-block',
            }} />
            <span>FastAPI v1 Ready</span>
          </div>
        </div>
      </div>
    </header>
  );
}
