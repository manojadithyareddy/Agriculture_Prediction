const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export interface CropCandidate {
  crop: string;
  confidence: number;
}

export interface CropRecommendationResponse {
  location: string;
  date: string;
  recommended_crop: string;
  top_5: CropCandidate[];
  target_crop_eval?: {
    requested_crop: string;
    rank: number | string;
    confidence: number;
    suitability: string;
  } | null;
  model_source: string;
  inputs_used: Record<string, number>;
}

export interface ClimateRiskResponse {
  location: string;
  date: string;
  crop: string;
  season: string;
  climate_risk: 'low' | 'moderate' | 'high' | 'extreme';
  probabilities: Record<string, number>;
}

export interface YieldPredictionResponse {
  location: string;
  date: string;
  crop: string;
  season: string;
  area: number;
  predicted_yield: number;
  yield_per_ha: number;
  model_source: string;
  factors?: {
    temperature_factor: number;
    water_stress_factor: number;
    soil_fertility_index: number;
    solar_factor: number;
  };
}

export interface IrrigationPredictionResponse {
  location: string;
  date: string;
  crop: string;
  growth_stage: string;
  predicted_water_requirement_mm_per_day: number;
  model_source: string;
  details?: {
    ET0_mm_day: number;
    Kc: number;
    ETc_mm_day: number;
    effective_rain: number;
    net_irrigation: number;
  };
}

export interface MarketPriceResponse {
  location: string;
  date: string;
  commodity: string;
  arrival_quantity: number;
  predicted_price_per_quintal: number;
  model_source: string;
  price_factors?: {
    base_price_2023: number;
    seasonal_multiplier: number;
    district_premium: number;
    inflation_factor: number;
  };
}

export interface DetectionItem {
  model: string;
  class_name: string;
  confidence: number;
  bbox: [number, number, number, number];
}

export interface DetectionResponse {
  status: string;
  crop: string;
  condition: string;
  category: 'Disease' | 'Pest' | 'Healthy' | 'Condition';
  confidence: number;
  best_model: string;
  total_detections: number;
  all_detections: DetectionItem[];
  annotated_image_base64?: string | null;
  suggested_actions: string[];
}

export interface ChatMessageResponse {
  session_id: string;
  response: string;
  sources: string[];
  suggested_followups: string[];
}

export interface AgentDiagnoseResponse {
  status: string;
  crop: string;
  condition: string;
  category: string;
  confidence: number;
  urgency_level: 'High' | 'Moderate' | 'Low';
  final_answer: string;
  sources: string[];
  action_plan: string[];
}

export interface DashboardStats {
  total_predictions: number;
  active_models: number;
  covered_districts: number;
  supported_crops: number;
  categories: Record<string, number>;
}

export interface ServiceProbe {
  name: string;
  role: string;
  status: 'Operational' | 'Degraded' | 'Offline' | 'Unconfigured' | string;
  latency_ms?: number | null;
  details?: string;
}

export interface HealthStatusResponse {
  status: string;
  version?: string;
  app_name?: string;
  environment?: string;
  gateway_latency_ms?: number;
  uptime_seconds?: number;
  database?: {
    supabase: string;
    latency_ms?: number | null;
  };
  models?: Record<string, string>;
  data_sources?: Record<string, string>;
  services?: ServiceProbe[];
}

export interface CurrentWeatherResponse {
  location: string;
  full_location: string;
  date: string;
  day_of_week: string;
  day_short: string;
  formatted_date: string;
  temperature: number;
  feels_like: number;
  temp_min: number;
  temp_max: number;
  humidity: number;
  wind_speed: number;
  precipitation: number;
  rain_chance: number;
  condition: string;
  icon: string;
}

export interface WeatherForecastDay {
  day: string;
  full_day: string;
  date: string;
  display_date: string;
  temperature: number;
  temp_max: number;
  temp_min: number;
  temp_range: string;
  condition: string;
  icon: string;
  rain_chance: number;
}

export interface WeatherForecastResponse {
  location: string;
  generated_at: string;
  today_day_of_week: string;
  forecast: WeatherForecastDay[];
}

// ── API CLIENT FUNCTIONS ──────────────────────────────────────────────────

export async function predictCrop(location: string, crop?: string, p?: number, k?: number): Promise<CropRecommendationResponse> {
  const res = await fetch(`${API_BASE}/api/v1/predict/crop-recommendation`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, crop, phosphorus: p, potassium: k }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function predictClimateRisk(location: string, crop: string): Promise<ClimateRiskResponse> {
  const res = await fetch(`${API_BASE}/api/v1/predict/climate-risk`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, crop }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function predictYield(location: string, crop: string, area: number): Promise<YieldPredictionResponse> {
  const res = await fetch(`${API_BASE}/api/v1/predict/yield`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, crop, area }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function predictIrrigation(location: string, crop: string, growth_stage: string): Promise<IrrigationPredictionResponse> {
  const res = await fetch(`${API_BASE}/api/v1/predict/irrigation`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, crop, growth_stage }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function predictMarketPrice(location: string, commodity: string, arrival_quantity: number): Promise<MarketPriceResponse> {
  const res = await fetch(`${API_BASE}/api/v1/predict/market-price`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, commodity, arrival_quantity }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function detectPlantDisease(file: File, targetCrop?: string): Promise<DetectionResponse> {
  const formData = new FormData();
  formData.append('file', file);
  if (targetCrop) {
    formData.append('target_crop', targetCrop);
  }

  const res = await fetch(`${API_BASE}/api/v1/detect/disease`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function sendChatMessage(
  message: string,
  sessionId?: string,
  crop?: string,
  condition?: string,
  language?: string,
  location?: string,
  growthStage?: string
): Promise<ChatMessageResponse> {
  const res = await fetch(`${API_BASE}/api/v1/chat/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      crop,
      condition,
      language: language || 'en',
      location,
      growth_stage: growthStage
    }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function runAgentDiagnose(imageResult: Record<string, unknown>, farmerQuestion: string): Promise<AgentDiagnoseResponse> {
  const res = await fetch(`${API_BASE}/api/v1/agent/diagnose`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_result: imageResult, farmer_question: farmerQuestion }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const res = await fetch(`${API_BASE}/api/v1/history/stats`);
  if (!res.ok) throw new Error('Failed to fetch dashboard stats');
  return res.json();
}

export async function getHealthStatus(): Promise<HealthStatusResponse> {
  const res = await fetch(`${API_BASE}/api/v1/health`);
  if (!res.ok) throw new Error('Backend health check failed');
  return res.json();
}

export async function getCurrentWeather(location: string = 'Hyderabad'): Promise<CurrentWeatherResponse> {
  const clean = location.split(',')[0].trim();
  const res = await fetch(`${API_BASE}/api/v1/weather/current?location=${encodeURIComponent(clean)}`);
  if (!res.ok) throw new Error('Failed to fetch weather');
  return res.json();
}

export async function getWeatherForecast(location: string = 'Hyderabad', days: number = 5): Promise<WeatherForecastResponse> {
  const clean = location.split(',')[0].trim();
  const res = await fetch(`${API_BASE}/api/v1/weather/forecast?location=${encodeURIComponent(clean)}&days=${days}`);
  if (!res.ok) throw new Error('Failed to fetch forecast');
  return res.json();
}

// ── MARKET INTELLIGENCE ──────────────────────────────────────────────────

export interface MandiQuote {
  mandi_id: string;
  mandi_name: string;
  district: string;
  state: string;
  commodity: string;
  standardized_commodity: string;
  min_price: number;
  max_price: number;
  modal_price: number;
  arrival_quantity_tonnes: number;
  unit: string;
  reporting_date: string;
  freshness_timestamp: string;
  source: string;
  data_category: string;
}

export interface MspComparison {
  has_msp: boolean;
  crop_display: string;
  official_msp: number | null;
  season: string;
  official_source: string;
  spread_to_msp_inr?: number;
  spread_to_msp_percentage?: number;
  market_status: string;
  advisory: string;
}

export interface MarketQuotesResponse {
  success: boolean;
  commodity: string;
  normalized_commodity: string;
  reporting_date: string;
  freshness_timestamp: string;
  mandis_reporting_count: number;
  aggregate_summary: {
    state_average_modal_price: number;
    lowest_observed_mandi_price: number;
    highest_observed_mandi_price: number;
    total_arrival_quantity_tonnes: number;
    unit: string;
  };
  msp_comparison: MspComparison;
  mandi_quotes: MandiQuote[];
  data_notice: string;
}

export interface ForecastPoint {
  day_index: number;
  forecast_date: string;
  display_date: string;
  predicted_modal_price: number;
  lower_confidence_bound_95: number;
  upper_confidence_bound_95: number;
  uncertainty_spread_inr: number;
  unit: string;
}

export interface MarketForecastResponse {
  success: boolean;
  commodity: string;
  normalized_commodity: string;
  location: string;
  forecast_generated_at: string;
  forecast_horizon_days: number;
  trend_assessment: string;
  projected_change_percentage: number;
  advisory: string;
  forecast_trajectory: ForecastPoint[];
  model_validation_metrics: {
    model_architecture: string;
    mean_absolute_error_inr: number;
    root_mean_squared_error_inr: number;
    mean_absolute_percentage_error: number;
    validation_dataset: string;
    test_sample_size: number;
    r2_score: number;
  };
  provenance_statement: string;
}

export interface HistoricalRecord {
  date: string;
  display_date: string;
  modal_price: number;
  min_price: number;
  max_price: number;
  arrivals_tonnes: number;
  unit: string;
}

export interface MarketHistoryResponse {
  success: boolean;
  commodity: string;
  location: string;
  days_covered: number;
  data_source: string;
  historical_records: HistoricalRecord[];
}

export interface MandiItem {
  mandi_id: string;
  mandi_name: string;
  district: string;
  state: string;
  tier: string;
  lat: number;
  lon: number;
}

export interface MandisResponse {
  success: boolean;
  total_mandis: number;
  mandis: MandiItem[];
}

export async function getMandiQuotes(
  commodity: string = 'Rice',
  district?: string,
  state?: string
): Promise<MarketQuotesResponse> {
  const params = new URLSearchParams({ commodity });
  if (district) params.append('district', district);
  if (state) params.append('state', state);

  const res = await fetch(`${API_BASE}/api/v1/market/quotes?${params.toString()}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getMarketForecast(
  commodity: string = 'Rice',
  location: string = 'Warangal',
  days: number = 14
): Promise<MarketForecastResponse> {
  const params = new URLSearchParams({ commodity, location, days: days.toString() });
  const res = await fetch(`${API_BASE}/api/v1/market/forecast?${params.toString()}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getMarketHistory(
  commodity: string = 'Rice',
  location: string = 'Warangal',
  days: number = 30
): Promise<MarketHistoryResponse> {
  const params = new URLSearchParams({ commodity, location, days: days.toString() });
  const res = await fetch(`${API_BASE}/api/v1/market/history?${params.toString()}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getMandisList(): Promise<MandisResponse> {
  const res = await fetch(`${API_BASE}/api/v1/market/mandis`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export function getMarketExportCsvUrl(commodity: string = 'Rice', district?: string): string {
  const params = new URLSearchParams({ commodity });
  if (district) params.append('district', district);
  return `${API_BASE}/api/v1/market/export/csv?${params.toString()}`;
}

