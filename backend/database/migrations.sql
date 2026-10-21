-- ==============================================================================
-- AgriPredict AI — Supabase Database Migrations
-- Tables: predictions, disease_detections, chat_history
-- Features: UUID PKs, JSONB storage, Timestamps, Row Level Security (RLS)
-- ==============================================================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ------------------------------------------------------------------------------
-- 1. PREDICTIONS TABLE (Unified for all 5 ML models)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    prediction_type TEXT NOT NULL CHECK (
        prediction_type IN (
            'crop_recommendation',
            'climate_risk',
            'yield',
            'irrigation',
            'market_price'
        )
    ),
    location TEXT NOT NULL,
    crop TEXT,
    inputs JSONB NOT NULL DEFAULT '{}'::jsonb,
    results JSONB NOT NULL DEFAULT '{}'::jsonb,
    model_source TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes for lightning-fast queries
CREATE INDEX IF NOT EXISTS idx_predictions_user_created 
    ON public.predictions (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_predictions_type 
    ON public.predictions (prediction_type);
CREATE INDEX IF NOT EXISTS idx_predictions_location 
    ON public.predictions (location);

-- ------------------------------------------------------------------------------
-- 2. DISEASE DETECTIONS TABLE (Computer Vision & YOLO)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.disease_detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    image_url TEXT,
    crop TEXT,
    condition TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('Disease', 'Pest', 'Healthy', 'Condition')),
    confidence NUMERIC(5, 4) NOT NULL,
    best_model TEXT,
    detections JSONB NOT NULL DEFAULT '[]'::jsonb,
    action_plan JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_disease_detections_user 
    ON public.disease_detections (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_disease_detections_crop 
    ON public.disease_detections (crop);

-- ------------------------------------------------------------------------------
-- 3. CHAT HISTORY TABLE (RAG & AI Agronomist)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    session_id UUID NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_chat_history_session 
    ON public.chat_history (session_id, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_chat_history_user 
    ON public.chat_history (user_id, created_at DESC);

-- ------------------------------------------------------------------------------
-- 4. ROW LEVEL SECURITY (RLS) POLICIES
-- ------------------------------------------------------------------------------

-- Enable RLS on all tables
ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.disease_detections ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_history ENABLE ROW LEVEL SECURITY;

-- PREDICTIONS RLS:
-- 1. Anyone (including anonymous/guest) can insert predictions
CREATE POLICY "Allow public insert for predictions" 
    ON public.predictions FOR INSERT 
    WITH CHECK (true);

-- 2. Users can view their own predictions (or public if no user_id)
CREATE POLICY "Users can view own predictions" 
    ON public.predictions FOR SELECT 
    USING (auth.uid() = user_id OR user_id IS NULL);

-- DISEASE DETECTIONS RLS:
CREATE POLICY "Allow public insert for detections" 
    ON public.disease_detections FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Users can view own detections" 
    ON public.disease_detections FOR SELECT 
    USING (auth.uid() = user_id OR user_id IS NULL);

-- CHAT HISTORY RLS:
CREATE POLICY "Allow public insert for chat" 
    ON public.chat_history FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Users can view own chat by session" 
    ON public.chat_history FOR SELECT 
    USING (auth.uid() = user_id OR user_id IS NULL);

-- Backwards compatibility policy for existing prediction_logs table:
DO $$ 
BEGIN
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'prediction_logs') THEN
        ALTER TABLE public.prediction_logs ENABLE ROW LEVEL SECURITY;
        DROP POLICY IF EXISTS "Allow anon insert prediction_logs" ON public.prediction_logs;
        CREATE POLICY "Allow anon insert prediction_logs" ON public.prediction_logs FOR INSERT WITH CHECK (true);
        DROP POLICY IF EXISTS "Allow anon select prediction_logs" ON public.prediction_logs;
        CREATE POLICY "Allow anon select prediction_logs" ON public.prediction_logs FOR SELECT USING (true);
    END IF;
END $$;
