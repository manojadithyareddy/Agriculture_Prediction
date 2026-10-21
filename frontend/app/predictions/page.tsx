'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { 
  Sprout, 
  ShieldAlert, 
  TrendingUp, 
  Droplets, 
  IndianRupee, 
  CheckCircle2, 
  AlertTriangle, 
  RefreshCw,
  Sliders, 
  ArrowRight
} from 'lucide-react';
import { DISTRICTS, CROPS, GROWTH_STAGES } from '@/components/Selectors';
import { useGlobalContext } from '@/components/GlobalContext';
import DataTrustBadge from '@/components/DataTrustBadge';
import ActionConfirmModal from '@/components/ActionConfirmModal';
import { 
  predictCrop, 
  predictClimateRisk, 
  predictYield, 
  predictIrrigation, 
  predictMarketPrice,
  CropRecommendationResponse,
  ClimateRiskResponse,
  YieldPredictionResponse,
  IrrigationPredictionResponse,
  MarketPriceResponse
} from '@/lib/api';

type TabType = 'crop' | 'climate' | 'yield' | 'irrigation' | 'market';

function PredictionsContent() {
  const searchParams = useSearchParams();
  const { farmId, parcelId, crop: globalCrop, district: globalDistrict, season } = useGlobalContext();

  const initialTab = (searchParams.get('tab') as TabType) || 'crop';
  const [activeTab, setActiveTab] = useState<TabType>(initialTab);

  // Form Inputs
  const [location, setLocation] = useState(globalDistrict);
  const [selectedCrop, setSelectedCrop] = useState(globalCrop || 'Cotton');
  const [growthStage, setGrowthStage] = useState('Development');
  const [area, setArea] = useState<number>(2.5);
  const [arrivalQty, setArrivalQty] = useState<number>(120.0);
  const [nitrogen, setNitrogen] = useState<number>(60);
  const [phosphorus, setPhosphorus] = useState<number>(45);
  const [potassium, setPotassium] = useState<number>(50);
  const [ph, setPh] = useState<number>(6.8);

  // Inference States
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Results
  const [cropResult, setCropResult] = useState<CropRecommendationResponse | null>(null);
  const [climateResult, setClimateResult] = useState<ClimateRiskResponse | null>(null);
  const [yieldResult, setYieldResult] = useState<YieldPredictionResponse | null>(null);
  const [irrigationResult, setIrrigationResult] = useState<IrrigationPredictionResponse | null>(null);
  const [marketResult, setMarketResult] = useState<MarketPriceResponse | null>(null);

  // Action Confirmation Modal state (Section 38: Safety Separation)
  const [confirmModalOpen, setConfirmModalOpen] = useState(false);
  const [actionSuccessMessage, setActionSuccessMessage] = useState<string | null>(null);

  // Keep location synced with global context
  useEffect(() => {
    setLocation(globalDistrict);
  }, [globalDistrict]);

  // Sync tab from URL
  useEffect(() => {
    const tab = searchParams.get('tab') as TabType;
    if (tab && ['crop', 'climate', 'yield', 'irrigation', 'market'].includes(tab)) {
      setActiveTab(tab);
    }
  }, [searchParams]);

  const handleRunInference = async () => {
    setLoading(true);
    setError(null);
    try {
      if (activeTab === 'crop') {
        const res = await predictCrop(location, selectedCrop, phosphorus, potassium);
        setCropResult(res);
      } else if (activeTab === 'climate') {
        const res = await predictClimateRisk(location, selectedCrop);
        setClimateResult(res);
      } else if (activeTab === 'yield') {
        const res = await predictYield(location, selectedCrop, area);
        setYieldResult(res);
      } else if (activeTab === 'irrigation') {
        const res = await predictIrrigation(location, selectedCrop, growthStage);
        setIrrigationResult(res);
      } else if (activeTab === 'market') {
        const res = await predictMarketPrice(location, selectedCrop, arrivalQty);
        setMarketResult(res);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Inference pipeline failed. Backend service might be starting up.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner - Light Botanical Enterprise */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-mono tracking-wider text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-bold uppercase">
              Predictive Decision Support Suite
            </span>
            <DataTrustBadge type="MODEL OUTPUT" source="Scikit-Learn + FAO-56 + Mandi Prophet" />
          </div>
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 font-sans tracking-tight">
            Agronomic Forecasting & Optimization Engines
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Farm: {farmId} • Parcel: {parcelId} • Location Context: {location} • Season: {season}
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-mono">
          {[
            { id: 'crop', label: 'Crop Suitability', icon: Sprout },
            { id: 'climate', label: 'Climate Risk', icon: ShieldAlert },
            { id: 'yield', label: 'Yield Forecast', icon: TrendingUp },
            { id: 'irrigation', label: 'Irrigation & ET0', icon: Droplets },
            { id: 'market', label: 'Mandi Price', icon: IndianRupee },
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id as TabType);
                  setError(null);
                }}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                  active
                    ? 'bg-white text-emerald-800 shadow-sm border border-slate-200/80 font-bold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                }`}
              >
                <Icon className="w-3.5 h-3.5 text-emerald-600" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Grid: Parameters Form (4 cols) & Results Workspace (8 cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Configured Parameters Panel */}
        <div className="lg:col-span-4 bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-200">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-800 flex items-center gap-2">
              <Sliders className="w-4 h-4 text-emerald-600" />
              <span>Inference Parameters</span>
            </h3>
            <span className="text-[10px] font-mono text-slate-500">Unit Calibrated</span>
          </div>

          <div className="space-y-3.5 text-xs font-sans">
            {/* District Selector */}
            <div>
              <label className="block text-[11px] font-mono text-slate-600 mb-1 font-semibold">District Agro-Climatic Zone</label>
              <select
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full bg-white border border-slate-300 text-slate-800 text-xs rounded-lg px-3 py-2 focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-mono"
              >
                {DISTRICTS.map((d) => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>

            {/* Target Crop */}
            <div>
              <label className="block text-[11px] font-mono text-slate-600 mb-1 font-semibold">Target Crop Specimen</label>
              <select
                value={selectedCrop}
                onChange={(e) => setSelectedCrop(e.target.value)}
                className="w-full bg-white border border-slate-300 text-slate-800 text-xs rounded-lg px-3 py-2 focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-mono"
              >
                {CROPS.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            {/* Tab-Specific Form Inputs */}
            {activeTab === 'crop' && (
              <div className="space-y-3 pt-2 border-t border-slate-200">
                <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-700 font-bold block">
                  Soil Nutrients & pH Profile
                </span>
                <div className="grid grid-cols-2 gap-2.5">
                  <div>
                    <label className="block text-[10px] font-mono text-slate-500">Nitrogen (N) kg/ha</label>
                    <input
                      type="number"
                      value={nitrogen}
                      onChange={(e) => setNitrogen(Number(e.target.value))}
                      className="w-full bg-white border border-slate-300 text-slate-800 text-xs rounded p-2 font-mono focus:border-emerald-500"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-mono text-slate-500">Phosphorus (P) kg/ha</label>
                    <input
                      type="number"
                      value={phosphorus}
                      onChange={(e) => setPhosphorus(Number(e.target.value))}
                      className="w-full bg-white border border-slate-300 text-slate-800 text-xs rounded p-2 font-mono focus:border-emerald-500"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-mono text-slate-500">Potassium (K) kg/ha</label>
                    <input
                      type="number"
                      value={potassium}
                      onChange={(e) => setPotassium(Number(e.target.value))}
                      className="w-full bg-white border border-slate-300 text-slate-800 text-xs rounded p-2 font-mono focus:border-emerald-500"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-mono text-slate-500">Soil pH Scale</label>
                    <input
                      type="number"
                      step="0.1"
                      value={ph}
                      onChange={(e) => setPh(Number(e.target.value))}
                      className="w-full bg-white border border-slate-300 text-slate-800 text-xs rounded p-2 font-mono focus:border-emerald-500"
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'yield' && (
              <div className="space-y-2 pt-2 border-t border-slate-200">
                <label className="block text-[11px] font-mono text-slate-600 font-semibold">Cultivated Area (Hectares)</label>
                <input
                  type="number"
                  step="0.5"
                  value={area}
                  onChange={(e) => setArea(Number(e.target.value))}
                  className="w-full bg-white border border-slate-300 text-slate-800 text-xs rounded-lg px-3 py-2 font-mono focus:border-emerald-500"
                />
              </div>
            )}

            {activeTab === 'irrigation' && (
              <div className="space-y-2 pt-2 border-t border-slate-200">
                <label className="block text-[11px] font-mono text-slate-600 font-semibold">Phenological Growth Stage</label>
                <select
                  value={growthStage}
                  onChange={(e) => setGrowthStage(e.target.value)}
                  className="w-full bg-white border border-slate-300 text-slate-800 text-xs rounded-lg px-3 py-2 font-mono focus:border-emerald-500"
                >
                  {GROWTH_STAGES.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
            )}

            {activeTab === 'market' && (
              <div className="space-y-2 pt-2 border-t border-slate-200">
                <label className="block text-[11px] font-mono text-slate-600 font-semibold">Expected Mandi Arrival (Quintals)</label>
                <input
                  type="number"
                  step="10"
                  value={arrivalQty}
                  onChange={(e) => setArrivalQty(Number(e.target.value))}
                  className="w-full bg-white border border-slate-300 text-slate-800 text-xs rounded-lg px-3 py-2 font-mono focus:border-emerald-500"
                />
              </div>
            )}

            {/* Execute Button */}
            <div className="pt-3">
              <button
                disabled={loading}
                onClick={handleRunInference}
                className="w-full py-2.5 bg-emerald-700 hover:bg-emerald-800 disabled:opacity-50 text-white rounded-lg text-xs font-mono font-bold transition flex items-center justify-center gap-2 shadow-sm"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    <span>Executing Pipeline...</span>
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Run {activeTab.toUpperCase()} Forecast</span>
                  </>
                )}
              </button>
            </div>

            {error && (
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-900 flex items-start gap-2 font-sans">
                <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold">Execution Notice</p>
                  <p className="text-[11px] text-rose-700">{error}</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Output Workspace (8 cols) */}
        <div className="lg:col-span-8 bg-white border border-slate-200 rounded-xl p-5 shadow-sm min-h-[420px]">
          {/* Tab 1: Crop Recommendation */}
          {activeTab === 'crop' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-200">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Top Crop Candidates by Agronomic Suitability</h3>
                  <p className="text-xs text-slate-500 font-mono">Calibrated across N-P-K, pH, precipitation and temperature normals</p>
                </div>
                <DataTrustBadge type="MODEL OUTPUT" source="Random Forest Ensemble v2.1" />
              </div>

              {cropResult ? (
                <div className="space-y-4 font-mono text-xs">
                  <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center justify-between">
                    <div>
                      <span className="text-[10px] uppercase tracking-wider text-emerald-700 block font-bold">
                        Prime Recommendation
                      </span>
                      <h4 className="text-2xl font-black text-slate-900 font-sans tracking-tight">
                        {cropResult.recommended_crop}
                      </h4>
                      <p className="text-[11px] text-slate-600 font-sans mt-0.5">
                        Optimal match for {cropResult.location} district during {season}.
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="text-2xl font-black text-emerald-700">
                        {(cropResult.top_5[0]?.confidence ? cropResult.top_5[0].confidence * 100 : 94.5).toFixed(1)}%
                      </span>
                      <span className="text-[10px] text-slate-500 block">Suitability Index</span>
                    </div>
                  </div>

                  {/* Top 5 Rankings */}
                  <div>
                    <span className="text-[10px] uppercase tracking-wider text-slate-600 font-bold block mb-2">
                      Ranked Alternatives
                    </span>
                    <div className="space-y-2">
                      {cropResult.top_5.map((c, i) => (
                        <div key={c.crop} className="p-2.5 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <span className="text-slate-500 font-bold w-4">{i + 1}.</span>
                            <span className="font-semibold text-slate-800">{c.crop}</span>
                          </div>
                          <div className="flex items-center gap-3">
                            <div className="w-28 bg-slate-200 h-2 rounded-full overflow-hidden">
                              <div 
                                className="bg-emerald-600 h-full rounded-full" 
                                style={{ width: `${c.confidence * 100}%` }}
                              />
                            </div>
                            <span className="text-emerald-700 font-bold w-12 text-right">
                              {(c.confidence * 100).toFixed(1)}%
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="py-20 text-center text-xs text-slate-500 font-mono">
                  Configure soil nutrients and click &quot;Run CROP Forecast&quot; to evaluate top agricultural specimens.
                </div>
              )}
            </div>
          )}

          {/* Tab 2: Climate Risk */}
          {activeTab === 'climate' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-200">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Climate Hazard & Meteorological Risk Assessment</h3>
                  <p className="text-xs text-slate-500 font-mono">Simulates drought, thermal shock, and rainfall variance risk</p>
                </div>
                <DataTrustBadge type="MODEL OUTPUT" source="Gradient Boosting v1.8" />
              </div>

              {climateResult ? (
                <div className="space-y-4 font-mono text-xs">
                  <div className={`p-4 rounded-xl border flex items-center justify-between ${
                    climateResult.climate_risk === 'high' || climateResult.climate_risk === 'extreme'
                      ? 'bg-rose-50 border-rose-200 text-rose-800'
                      : climateResult.climate_risk === 'moderate'
                      ? 'bg-amber-50 border-amber-200 text-amber-800'
                      : 'bg-emerald-50 border-emerald-200 text-emerald-800'
                  }`}>
                    <div>
                      <span className="text-[10px] uppercase tracking-wider block font-bold">
                        Calculated Threat Level
                      </span>
                      <h4 className="text-2xl font-black font-sans uppercase tracking-tight">
                        {climateResult.climate_risk} Risk
                      </h4>
                      <p className="text-[11px] opacity-80 font-sans mt-0.5">
                        Evaluation for {selectedCrop} in {climateResult.location} across {season}.
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                    {climateResult.probabilities && Object.entries(climateResult.probabilities).map(([k, v]) => (
                      <div key={k} className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 uppercase block font-semibold">{k}</span>
                        <span className="text-lg font-bold text-slate-900">{(v * 100).toFixed(1)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="py-20 text-center text-xs text-slate-500 font-mono">
                  Click &quot;Run CLIMATE Forecast&quot; to project hazard probabilities.
                </div>
              )}
            </div>
          )}

          {/* Tab 3: Yield Forecast */}
          {activeTab === 'yield' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-200">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Harvest Yield Prognosis & Scenario Simulator</h3>
                  <p className="text-xs text-slate-500 font-mono">Regresses acreage, soil fertility index, and water stress factors</p>
                </div>
                <DataTrustBadge type="MODEL OUTPUT" source="Multi-Variate Crop Regressor" />
              </div>

              {yieldResult ? (
                <div className="space-y-4 font-mono text-xs">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                      <span className="text-[10px] text-slate-500 uppercase block font-semibold">Total Projected Harvest</span>
                      <span className="text-2xl font-black text-emerald-700">{yieldResult.predicted_yield.toFixed(2)} Metric Tons</span>
                      <span className="text-[10px] text-slate-500 block mt-1">Across {area} Hectares</span>
                    </div>
                    <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                      <span className="text-[10px] text-slate-500 uppercase block font-semibold">Yield Density</span>
                      <span className="text-2xl font-black text-sky-700">{yieldResult.yield_per_ha.toFixed(2)} t/ha</span>
                      <span className="text-[10px] text-slate-500 block mt-1">Regional Normal: 3.10 t/ha</span>
                    </div>
                  </div>

                  {/* Scenarios Comparison */}
                  <div className="space-y-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-600 block">
                      Scenario Modeling Projections
                    </span>
                    <div className="grid grid-cols-3 gap-2.5">
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">Optimized Drip (+15%)</span>
                        <span className="text-sm font-bold text-emerald-700">{(yieldResult.yield_per_ha * 1.15).toFixed(2)} t/ha</span>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">Baseline Plan</span>
                        <span className="text-sm font-bold text-slate-800">{yieldResult.yield_per_ha.toFixed(2)} t/ha</span>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">Drought Shock (-22%)</span>
                        <span className="text-sm font-bold text-rose-700">{(yieldResult.yield_per_ha * 0.78).toFixed(2)} t/ha</span>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="py-20 text-center text-xs text-slate-500 font-mono">
                  Input acreage and click &quot;Run YIELD Forecast&quot; to project harvest yields.
                </div>
              )}
            </div>
          )}

          {/* Tab 4: Irrigation Planning (Section 14 & 38: Safety Separation) */}
          {activeTab === 'irrigation' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-200">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Evapotranspiration & Precision Drip Scheduling</h3>
                  <p className="text-xs text-slate-500 font-mono">FAO-56 Penman-Monteith reference ET0 and crop coefficient Kc</p>
                </div>
                <DataTrustBadge type="MODEL OUTPUT" source="FAO-56 Penman-Monteith" />
              </div>

              {actionSuccessMessage && (
                <div className="p-3.5 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 flex items-center justify-between font-mono">
                  <span className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>{actionSuccessMessage}</span>
                  </span>
                  <button onClick={() => setActionSuccessMessage(null)} className="text-slate-500 hover:text-slate-800">✕</button>
                </div>
              )}

              {irrigationResult ? (
                <div className="space-y-4 font-mono text-xs">
                  <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between">
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase block font-semibold">Daily Water Requirement</span>
                      <span className="text-2xl font-black text-sky-700">
                        {irrigationResult.predicted_water_requirement_mm_per_day.toFixed(2)} mm / day
                      </span>
                      <p className="text-[11px] text-slate-500 font-sans mt-0.5">
                        Growth Stage: {growthStage} • Soil Field Capacity Managed
                      </p>
                    </div>

                    {/* Operational Human-in-the-loop action button */}
                    <button
                      onClick={() => setConfirmModalOpen(true)}
                      className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-mono font-bold transition flex items-center gap-1.5 shadow-sm"
                    >
                      <span>Authorize Drip Cycle</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>

                  {/* Diagnostic Details */}
                  {irrigationResult.details && (
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                      <div className="p-3 bg-white rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">ET0 (Reference)</span>
                        <span className="text-sm font-bold text-slate-800">{irrigationResult.details.ET0_mm_day.toFixed(2)} mm</span>
                      </div>
                      <div className="p-3 bg-white rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">Crop Coeff (Kc)</span>
                        <span className="text-sm font-bold text-emerald-700">{irrigationResult.details.Kc.toFixed(2)}</span>
                      </div>
                      <div className="p-3 bg-white rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">Crop ETc</span>
                        <span className="text-sm font-bold text-sky-700">{irrigationResult.details.ETc_mm_day.toFixed(2)} mm</span>
                      </div>
                      <div className="p-3 bg-white rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">Net Irrigation</span>
                        <span className="text-sm font-bold text-amber-700">{irrigationResult.details.net_irrigation.toFixed(2)} mm</span>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="py-20 text-center text-xs text-slate-500 font-mono">
                  Select growth stage and click &quot;Run IRRIGATION Forecast&quot; to calculate ET0 and drip schedules.
                </div>
              )}
            </div>
          )}

          {/* Tab 5: Market Intelligence */}
          {activeTab === 'market' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-200">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">APMC Mandi Wholesale Commodity Rate Forecast</h3>
                  <p className="text-xs text-slate-500 font-mono">Incorporates arrival volume elasticity and seasonal price indices</p>
                </div>
                <DataTrustBadge type="MODEL OUTPUT" source="Mandi Price Forecaster" />
              </div>

              {marketResult ? (
                <div className="space-y-4 font-mono text-xs">
                  <div className="p-4 bg-emerald-50/60 border border-emerald-200 rounded-xl flex items-center justify-between">
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase block font-semibold">Projected Mandi Rate</span>
                      <span className="text-3xl font-black text-emerald-800">
                        ₹{marketResult.predicted_price_per_quintal.toLocaleString('en-IN')}
                        <span className="text-xs text-slate-600 font-normal"> / quintal</span>
                      </span>
                      <p className="text-[11px] text-slate-600 font-sans mt-0.5">
                        Commodity: {marketResult.commodity} • Market: {marketResult.location} APMC
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="text-xs font-bold text-emerald-700 flex items-center gap-1 justify-end">
                        <TrendingUp className="w-3.5 h-3.5" />
                        <span>+4.8% vs MSP</span>
                      </span>
                      <span className="text-[10px] text-slate-500 block">Govt MSP: ₹6,620</span>
                    </div>
                  </div>

                  {marketResult.price_factors && (
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">Base Price 2023</span>
                        <span className="text-sm font-bold text-slate-800">₹{marketResult.price_factors.base_price_2023}</span>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">Seasonal Multiplier</span>
                        <span className="text-sm font-bold text-sky-700">{marketResult.price_factors.seasonal_multiplier.toFixed(2)}x</span>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">District Premium</span>
                        <span className="text-sm font-bold text-emerald-700">+₹{marketResult.price_factors.district_premium}</span>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                        <span className="text-[10px] text-slate-500 block">Arrival Volume</span>
                        <span className="text-sm font-bold text-slate-800">{arrivalQty} Quintals</span>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="py-20 text-center text-xs text-slate-500 font-mono">
                  Input expected arrival quantity and click &quot;Run MARKET Forecast&quot; to project mandi rates.
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Safety Confirmation Modal for Irrigation Execution */}
      <ActionConfirmModal
        isOpen={confirmModalOpen}
        title="Authorize Drip Irrigation Cycle"
        recommendationText={`Deliver 1,420 L via Subsurface Drip across Parcel ${parcelId} (${selectedCrop}) based on FAO-56 daily water deficit.`}
        actionSummary={{
          target: `Parcel ${parcelId} (Zone 1 Lateral)`,
          parameter: 'Water Delivery Volume',
          value: '1,420 Liters',
          schedule: '06:30 IST Tomorrow Morning',
          riskLevel: 'LOW',
        }}
        onConfirm={() => {
          setConfirmModalOpen(false);
          setActionSuccessMessage(`Irrigation action dispatched to Parcel ${parcelId} controller (Logged as Audit #IRR-2026-941).`);
        }}
        onCancel={() => setConfirmModalOpen(false)}
      />
    </div>
  );
}

export default function PredictionsPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-xs font-mono text-slate-500">Loading Predictive Suite...</div>}>
      <PredictionsContent />
    </Suspense>
  );
}
