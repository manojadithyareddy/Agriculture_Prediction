# AgriFusion AI — Troubleshooting & Incident Response Guide
**Document ID:** `TRBL-AGRI-2026-V1`  
**Platform Version:** `1.0.0 Enterprise Ready`  

---

## 1. Top Diagnostic Quick-Checks

Run these commands first if any part of the system appears degraded:
```bash
# 1. Check if backend is alive
curl http://127.0.0.1:8000/api/v1/health

# 2. Check if frontend routes are healthy
python scratch/test_all_endpoints.py

# 3. Check pytest automated tests
python -m pytest backend/tests -v
```

---

## 2. Known Issues, Root Causes & Verified Solutions

### Issue 1: OpenBLAS Crash on Windows (`Memory allocation failed` / `Exit 0xC0000005`)
- **Root Cause:** NumPy / Scikit-learn OpenBLAS threading library thread collision on certain Intel/AMD Windows chipsets when running Uvicorn.
- **Solution:** Configured in `app/main.py`:
  ```python
  import os
  os.environ["OPENBLAS_NUM_THREADS"] = "1"
  os.environ["OPENBLAS_CORETYPE"] = "HASWELL"
  ```

---

### Issue 2: Next.js Frontend Raw HTML / Missing CSS (`GET /_next/static/css/... 404`)
- **Root Cause:** Next.js dev cache corruption in `.next` directory after changing layouts or dynamic imports.
- **Solution:**
  1. Stop dev server.
  2. Remove the corrupted build folder:
     ```powershell
     Remove-Item -Recurse -Force .next
     ```
  3. Restart dev server:
     ```powershell
     npm run dev
     ```

---

### Issue 3: Supabase RLS Policy Violation (`42501 - new row violates row-level security policy`)
- **Root Cause:** Table `prediction_logs` has Row-Level Security enabled, but lacks an `INSERT` policy for the anonymous client key.
- **Solution:** Execute the following SQL in the Supabase SQL Editor:
  ```sql
  CREATE POLICY "Allow anon insert to prediction_logs"
  ON public.prediction_logs
  FOR INSERT
  TO anon, authenticated, service_role
  WITH CHECK (true);
  ```
  *(Note: The backend wraps Supabase insertions in a non-blocking daemon thread so user requests never fail even if database connectivity drops.)*

---

### Issue 4: Scikit-learn Pickle Version Incompatibility Warning
- **Root Cause:** Model `climate_risk_model.pkl` was saved with an earlier version of Scikit-learn than the active environment.
- **Solution:** The model loader in `backend/app/ml/predict_climate_risk.py` catches version warnings safely and provides a validated agronomic calculation fallback if unpickling ever fails.

---

### Issue 5: Roboflow Vision API Key Missing / Offline Mode
- **Root Cause:** Missing `ROBOFLOW_API_KEY` in new developer environments.
- **Solution:** `backend/app/dl/disease_detector.py` provides an automatic OpenCV local heuristic fallback. The endpoint still returns a valid diagnostic assessment, bounding box calculations, and agronomic management protocol without throwing 500 errors.

---

### Issue 6: Port Conflicts (Port 3000 / Port 8000 in use)
- **Root Cause:** Background instances of previous runs holding TCP sockets.
- **Solution:**
  ```powershell
  # Find PID holding port 8000 or 3000
  netstat -ano | findstr :8000
  netstat -ano | findstr :3000

  # Terminate by PID
  taskkill /F /PID <PID>
  ```
