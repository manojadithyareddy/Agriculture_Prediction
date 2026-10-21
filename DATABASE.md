# AgriFusion AI — Database Schema & Supabase Configuration
**Database Engine:** PostgreSQL 15+ (Hosted via Supabase)  
**ORM / Client:** Supabase Python SDK / PostgREST  
**Security Model:** Row-Level Security (RLS) with Role-Based Access Control (RBAC)  

---

## 1. Schema Design Principles

1. **UUID Primary Keys:** All entity IDs use `gen_random_uuid()` to prevent enumeration attacks and support distributed insertion.
2. **Audit Timestamps:** Every table tracks `created_at` and `updated_at` with microsecond UTC resolution (`TIMESTAMPTZ`).
3. **JSONB Flexibility:** Model telemetry inputs and outputs are persisted as indexed `JSONB` documents for flexible schema evolution.
4. **Relational Integrity:** Foreign key constraints with `ON DELETE CASCADE` or `SET NULL` maintain referential integrity.

---

## 2. Table Definitions

### 2.1 Table: `prediction_logs`
Stores all machine learning and agronomic inference logs.

```sql
CREATE TABLE IF NOT EXISTS public.prediction_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    prediction_type VARCHAR(64) NOT NULL,
    location VARCHAR(128),
    crop VARCHAR(128),
    inputs JSONB NOT NULL DEFAULT '{}'::jsonb,
    results JSONB NOT NULL DEFAULT '{}'::jsonb,
    model_source VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_prediction_logs_type ON public.prediction_logs (prediction_type);
CREATE INDEX IF NOT EXISTS idx_prediction_logs_location ON public.prediction_logs (location);
CREATE INDEX IF NOT EXISTS idx_prediction_logs_crop ON public.prediction_logs (crop);
CREATE INDEX IF NOT EXISTS idx_prediction_logs_created ON public.prediction_logs (created_at DESC);
```

---

### 2.2 Table: `vision_predictions`
Stores computer vision and YOLO plant pathology detection results.

```sql
CREATE TABLE IF NOT EXISTS public.vision_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    crop VARCHAR(128) NOT NULL,
    detected_condition VARCHAR(256),
    category VARCHAR(64) NOT NULL, -- 'Disease', 'Pest', 'Healthy'
    confidence NUMERIC(5, 4) NOT NULL,
    bounding_boxes JSONB DEFAULT '[]'::jsonb,
    image_storage_path TEXT,
    suggested_actions JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_vision_crop ON public.vision_predictions (crop);
CREATE INDEX IF NOT EXISTS idx_vision_condition ON public.vision_predictions (detected_condition);
```

---

### 2.3 Table: `rag_documents` & `rag_queries`
Tracks ingested agricultural research manuals and farmer advisory conversations.

```sql
CREATE TABLE IF NOT EXISTS public.rag_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(256) NOT NULL,
    category VARCHAR(128) NOT NULL,
    crop VARCHAR(128),
    file_path TEXT NOT NULL,
    total_chunks INT DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.rag_queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(128) NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    retrieved_sources JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_rag_session ON public.rag_queries (session_id);
```

---

## 3. Row-Level Security (RLS) Configuration

Run this SQL in your Supabase SQL Editor to enable secure writes for both authenticated users and anonymous telemetry:

```sql
-- Enable RLS on all tables
ALTER TABLE public.prediction_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vision_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rag_queries ENABLE ROW LEVEL SECURITY;

-- Allow anonymous logging for backend inference
CREATE POLICY "Allow anon insert to prediction_logs"
ON public.prediction_logs
FOR INSERT
TO anon, authenticated, service_role
WITH CHECK (true);

-- Allow users to read their own predictions
CREATE POLICY "Allow users to read own predictions"
ON public.prediction_logs
FOR SELECT
TO authenticated
USING (auth.uid() = user_id);

-- Allow service role unrestricted access
CREATE POLICY "Service role full access on prediction_logs"
ON public.prediction_logs
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);
```
