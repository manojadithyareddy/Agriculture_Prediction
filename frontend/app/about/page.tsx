'use client';

import React from 'react';
import Link from 'next/link';
import {
  Sprout,
  BrainCircuit,
  ScanEye,
  MessageSquareText,
  ShieldAlert,
  Database,
  Cpu,
  CheckCircle2,
  AlertTriangle,
  Layers,
  Scale,
  Sparkles,
  ArrowRight,
  ExternalLink,
  Code2
} from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="space-y-8 font-sans max-w-[1300px] mx-auto pb-16">
      {/* 1. HERO HEADER */}
      <div className="bg-gradient-to-br from-slate-900 via-emerald-950 to-slate-900 rounded-3xl p-8 sm:p-12 text-white border border-emerald-900/40 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="max-w-3xl space-y-4 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold tracking-wide">
            <Sprout className="w-3.5 h-3.5" />
            <span>Platform Overview & Architecture</span>
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-white">
            AgriFusion AI
          </h1>
          <p className="text-base sm:text-lg text-slate-300 leading-relaxed font-normal">
            A production-oriented multimodal agricultural intelligence platform engineered for
            farmers, agronomists, and researchers across <strong>Andhra Pradesh</strong> and <strong>Telangana</strong>.
          </p>
        </div>
      </div>

      {/* 2. CORE CAPABILITIES SUMMARY */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2">
          <div className="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center font-bold">
            <BrainCircuit className="w-5 h-5" />
          </div>
          <h3 className="text-base font-extrabold text-slate-900">Predictive ML</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Crop recommendation, yield estimation, FAO-56 irrigation water requirements, and climate risk modeling calibrated to regional district soils.
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2">
          <div className="w-9 h-9 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center font-bold">
            <ScanEye className="w-5 h-5" />
          </div>
          <h3 className="text-base font-extrabold text-slate-900">Computer Vision</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            13 specialized YOLO disease and pest object detection models for Rice, Maize, Banana, Mango, Citrus, Grapes, and Beans.
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2">
          <div className="w-9 h-9 rounded-xl bg-indigo-50 text-indigo-700 flex items-center justify-center font-bold">
            <MessageSquareText className="w-5 h-5" />
          </div>
          <h3 className="text-base font-extrabold text-slate-900">Grounded RAG</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Retrieval-Augmented Generation across verified agricultural extension handbooks with dual English & Telugu language synthesis.
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2">
          <div className="w-9 h-9 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center font-bold">
            <Scale className="w-5 h-5" />
          </div>
          <h3 className="text-base font-extrabold text-slate-900">Market Intelligence</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Official Agmarknet APMC mandi spot rates, CACP Minimum Support Price (MSP) comparisons, and multi-horizon price forecasting.
          </p>
        </div>
      </div>

      {/* 3. TECHNICAL ARCHITECTURE SPECIFICATION */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-xs space-y-6">
        <div className="border-b border-slate-100 pb-4">
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight">
            System & Engineering Architecture
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Engineered modular architecture verified against the actual repository codebase.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Component 1: Machine Learning */}
          <div className="p-5 rounded-2xl bg-slate-50/70 border border-slate-200/70 space-y-3">
            <div className="flex items-center gap-2 text-emerald-800 font-extrabold text-sm">
              <BrainCircuit className="w-4 h-4 text-emerald-600" />
              <span>1. Tabular Machine Learning Layer</span>
            </div>
            <ul className="text-xs text-slate-600 space-y-2 leading-relaxed">
              <li>
                <strong>Climate Risk Model</strong>: Scikit-learn RandomForestClassifier trained on 24 weather and soil features across Kharif, Rabi, and Zaid seasons.
              </li>
              <li>
                <strong>Crop Recommendation</strong>: Calibrated multi-class model utilizing soil N, P, K, pH, and local weather telemetry.
              </li>
              <li>
                <strong>Yield Prediction</strong>: Dual-track engine combining fitted regression with FAO-calibrated environmental response curves (temperature, water stress, soil fertility).
              </li>
              <li>
                <strong>Irrigation Modeling</strong>: FAO-56 Penman-Monteith reference evapotranspiration (ET₀) adjusted for crop coefficients (Kc) and effective rainfall.
              </li>
            </ul>
          </div>

          {/* Component 2: Deep Learning Vision */}
          <div className="p-5 rounded-2xl bg-slate-50/70 border border-slate-200/70 space-y-3">
            <div className="flex items-center gap-2 text-blue-800 font-extrabold text-sm">
              <ScanEye className="w-4 h-4 text-blue-600" />
              <span>2. Deep Learning & Computer Vision</span>
            </div>
            <ul className="text-xs text-slate-600 space-y-2 leading-relaxed">
              <li>
                <strong>Architecture</strong>: 13 specialized YOLO object detection models hosted on Roboflow Universe and evaluated sequentially or by prioritized crop filter.
              </li>
              <li>
                <strong>Annotation Pipeline</strong>: OpenCV bounded visualization with distinct color-coding for Diseases (Red), Pests (Orange), and Healthy Tissue (Green).
              </li>
              <li>
                <strong>Honest Confidence Handling</strong>: Returns zero-detection status with 0.0 confidence when symptoms fall below the 40% threshold; never fabricates positive classifications.
              </li>
            </ul>
          </div>

          {/* Component 3: RAG & GenAI */}
          <div className="p-5 rounded-2xl bg-slate-50/70 border border-slate-200/70 space-y-3">
            <div className="flex items-center gap-2 text-indigo-800 font-extrabold text-sm">
              <MessageSquareText className="w-4 h-4 text-indigo-600" />
              <span>3. Grounded Retrieval-Augmented Generation</span>
            </div>
            <ul className="text-xs text-slate-600 space-y-2 leading-relaxed">
              <li>
                <strong>Knowledge Base</strong>: Verified extension publications and agronomic protocols covering foliar symptoms, chemical recommendations, and IPM cultural practices.
              </li>
              <li>
                <strong>Retrieval Mechanism</strong>: BM25 keyword matching with agricultural synonym query expansion and ChromaDB vector search fallback.
              </li>
              <li>
                <strong>Multilingual Synthesis</strong>: Full natural-language support for Telugu and English with localized agricultural terms and safety warnings.
              </li>
            </ul>
          </div>

          {/* Component 4: Agent Orchestration */}
          <div className="p-5 rounded-2xl bg-slate-50/70 border border-slate-200/70 space-y-3">
            <div className="flex items-center gap-2 text-amber-800 font-extrabold text-sm">
              <Cpu className="w-4 h-4 text-amber-600" />
              <span>4. Agent Reasoning & Orchestration</span>
            </div>
            <ul className="text-xs text-slate-600 space-y-2 leading-relaxed">
              <li>
                <strong>LangGraph State Graph</strong>: 3-node sequential agent combining visual symptom detection, documentary RAG retrieval, and action plan formulation.
              </li>
              <li>
                <strong>Urgency Classification</strong>: Rule-based severity rating (High, Moderate, Low) with automatic escalation for virulent pathogens like Blast or Wilt.
              </li>
              <li>
                <strong>Safety Guards</strong>: Explicitly flags missing crop or growth stage context when users inquire about chemical spraying or dosage.
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* 4. DATA SOURCES & LIMITATIONS */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-xs space-y-6">
        <div className="border-b border-slate-100 pb-4">
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight">
            Data Sources, Calibration & Known Limitations
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Transparent disclosure of system boundaries and underlying datasets.
          </p>
        </div>

        <div className="space-y-4">
          <div className="p-4 rounded-2xl bg-amber-50/60 border border-amber-200/70 text-amber-950 text-xs space-y-2">
            <div className="flex items-center gap-2 font-bold text-sm text-amber-900">
              <AlertTriangle className="w-4 h-4 text-amber-700 shrink-0" />
              <span>Critical Operational & Advisory Disclaimers</span>
            </div>
            <ul className="list-disc list-inside space-y-1 pl-1 text-amber-900">
              <li>
                <strong>Advisory Nature</strong>: All recommendations generated by AgriFusion AI are supplementary decision-support tools and do not substitute for official laboratory diagnostic tests or licensed local agricultural extension officer (AEO) field inspections.
              </li>
              <li>
                <strong>Geographic Boundaries</strong>: Soil profiles and weather data are specifically calibrated for the 57 districts of Andhra Pradesh and Telangana. Models may produce out-of-distribution errors if queried for unrelated geographies.
              </li>
              <li>
                <strong>Chemical Spraying Precaution</strong>: Always verify pesticide trade names, technical formulations, dosages, and Pre-Harvest Intervals (PHI) against the physical product container label approved by the Central Insecticides Board & Registration Committee (CIB&RC).
              </li>
              <li>
                <strong>Market Volatility</strong>: Price forecasts are statistical projections based on historical Agmarknet elasticity. Actual mandi rates fluctuate with daily weather, local arrivals, road blockages, and state procurement policies.
              </li>
            </ul>
          </div>

          {/* Data Sources Table */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="bg-slate-100/70 border-b border-slate-200 text-slate-600 font-bold uppercase tracking-wider">
                  <th className="py-2.5 px-4">Domain</th>
                  <th className="py-2.5 px-4">Primary Source</th>
                  <th className="py-2.5 px-4">Update Cadence</th>
                  <th className="py-2.5 px-4">Limitations</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-sans text-slate-700">
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Weather Telemetry</td>
                  <td className="py-3 px-4">AP/TS Regional Dataset & Open-Meteo</td>
                  <td className="py-3 px-4">Daily snapshot</td>
                  <td className="py-3 px-4 text-slate-500">Subject to micro-climate variations not captured at district grid scale.</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Soil Profiles</td>
                  <td className="py-3 px-4">Regional District Soil Classification Database</td>
                  <td className="py-3 px-4">Static reference profile</td>
                  <td className="py-3 px-4 text-slate-500">District-average values; farm-specific soil testing (SHC) takes precedence.</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Market Prices</td>
                  <td className="py-3 px-4">Agmarknet / DMI, Ministry of Agriculture</td>
                  <td className="py-3 px-4">Daily APMC auction feed</td>
                  <td className="py-3 px-4 text-slate-500">Reflects modal rates; actual realizations vary by moisture & foreign matter.</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Govt. MSP Rates</td>
                  <td className="py-3 px-4">Commission for Agricultural Costs & Prices (CACP)</td>
                  <td className="py-3 px-4">Annual central notification</td>
                  <td className="py-3 px-4 text-slate-500">Applies only to notified crops; perishables trade strictly on open auctions.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* 5. VERIFIED REPOSITORY TECH STACK */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-xs space-y-4">
        <div className="flex items-center gap-2 text-slate-900 font-extrabold text-base border-b border-slate-100 pb-3">
          <Code2 className="w-5 h-5 text-emerald-600" />
          <span>Technology Stack (Verified Codebase)</span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-slate-400 block font-medium">Backend Framework</span>
            <span className="font-bold text-slate-800 text-sm">FastAPI 0.110+</span>
            <span className="text-[11px] text-slate-500 block mt-0.5">Python 3.10+ / ASGI</span>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-slate-400 block font-medium">Frontend Framework</span>
            <span className="font-bold text-slate-800 text-sm">Next.js 14 (App Router)</span>
            <span className="text-[11px] text-slate-500 block mt-0.5">TypeScript & Tailwind CSS</span>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-slate-400 block font-medium">Machine Learning</span>
            <span className="font-bold text-slate-800 text-sm">Scikit-Learn & Joblib</span>
            <span className="text-[11px] text-slate-500 block mt-0.5">RandomForest, FAO-56 Penman</span>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-slate-400 block font-medium">Agent & RAG</span>
            <span className="font-bold text-slate-800 text-sm">LangGraph & BM25</span>
            <span className="text-[11px] text-slate-500 block mt-0.5">ChromaDB semantic search</span>
          </div>
        </div>
      </div>
    </div>
  );
}
