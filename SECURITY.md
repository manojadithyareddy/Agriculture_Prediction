# AgriFusion AI — Enterprise Security & Compliance Policy
**Document ID:** `SEC-AGRI-2026-V1`  
**Classification:** Enterprise Internal Security Standard  

---

## 1. Secrets Management & Environment Hygiene

- **Strict Environment Isolation:** No private API keys, database passwords, or JWT secrets may be committed to version control.
- **`.env.example` Templates:** Only sanitised placeholder configuration templates (`.env.example`) are committed to Git.
- **Client vs Server Key Boundary:**
  - Frontend (`VITE_*` or `NEXT_PUBLIC_*`) variables contain only public configuration values (e.g. Supabase anonymous key, Firebase public config).
  - Server credentials (`SUPABASE_SERVICE_KEY`, private tokens, DB connection strings) are strictly isolated to the server runtime.

---

## 2. API Security & Threat Mitigation

### 2.1 File Upload Protection
- **Size Limitation:** File uploads to `/api/v1/detect/disease` are strictly capped at 15 MB in memory.
- **MIME Type Validation:** Only `image/jpeg`, `image/png`, `image/webp`, and `image/jpg` headers are accepted.
- **Magic Byte Inspection:** Uploaded buffers are decoded using OpenCV and Pillow; corrupted, polyglot, or executable payloads are rejected immediately with HTTP 400.

### 2.2 Cross-Origin Resource Sharing (CORS)
- Production CORS policies restrict incoming cross-origin requests to authorized client domains.
- Default development permits localhost origin with explicit method/header allowlisting.

### 2.3 Injection & Parameter Tampering
- **No Raw SQL:** Database transactions interact through the parameterized PostgREST client, completely eliminating SQL injection attack surfaces.
- **Pydantic Validation:** All incoming request bodies undergo strict type coercion and boundary checks (e.g., pH between 0 and 14, rainfall $\ge 0$).

### 2.4 Error Sanitization & Anti-Leakage
- **No Raw Stack Traces:** Internal server errors (HTTP 500) return user-friendly, actionable diagnostic messages without leaking file paths, server OS details, or library stack traces.

---

## 3. Row-Level Security (RLS) & Access Control

- All Supabase tables enforce PostgreSQL Row-Level Security.
- Users can only read their own telemetry logs, while the backend service role is permitted insertion.
