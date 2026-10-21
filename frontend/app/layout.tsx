import type { Metadata } from 'next';
import './globals.css';
import Header from '@/components/Header';
import GlobalContextBar from '@/components/GlobalContextBar';
import CommandPalette from '@/components/CommandPalette';
import { GlobalContextProvider } from '@/components/GlobalContext';
import Link from 'next/link';
import { Suspense } from 'react';

export const metadata: Metadata = {
  title: 'AgriFusion AI — Smart Farming. Brighter Tomorrow.',
  description: 'AI-driven insights for healthier crops, higher yields, and a more sustainable world.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#F7FAF7] text-slate-800 antialiased selection:bg-emerald-600 selection:text-white font-sans flex flex-col">
        <GlobalContextProvider>
          {/* Global Cmd+K Command Palette */}
          <CommandPalette />

          {/* Premium Horizontal Navigation */}
          <Header />

          {/* Main Application Workspace — Full Width */}
          <div className="flex-1 flex flex-col w-full">
            {/* Persistent Agricultural Context Bar */}
            <GlobalContextBar />

            <main className="flex-1 p-4 lg:p-6 w-full max-w-[1600px] mx-auto">
              {children}
            </main>

            {/* Reference Footer */}
            <footer className="mt-auto border-t border-slate-200/80 bg-white">
              <div className="max-w-[1600px] mx-auto px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500 font-sans">
                <div>
                  © 2026 AgriFusion AI. All rights reserved.
                </div>

                <div className="flex items-center gap-6 font-medium text-slate-600">
                  <Link href="/about" className="hover:text-emerald-700 transition">About</Link>
                  <Link href="/market" className="hover:text-emerald-700 transition">Market Intelligence</Link>
                  <Link href="/ai-assistant" className="hover:text-emerald-700 transition">AI Assistant</Link>
                  <Link href="/predictions" className="hover:text-emerald-700 transition">Predictions</Link>
                </div>

                <div className="flex items-center gap-2 text-emerald-800 font-semibold">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-700 text-xs">
                    🌱
                  </div>
                  <span>Together for a Greener Tomorrow</span>
                </div>
              </div>
            </footer>
          </div>
        </GlobalContextProvider>
      </body>
    </html>
  );
}
