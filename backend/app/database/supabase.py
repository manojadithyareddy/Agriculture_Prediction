"""
supabase.py — Supabase client singleton for backend.
Lazy initialization using app.config.settings.
"""
from __future__ import annotations
import threading
import logging

try:
    from app.config import settings
    SUPABASE_URL = settings.SUPABASE_URL
    SUPABASE_KEY = settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_KEY
except Exception:
    import os
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_client = None

def get_client():
    """Return the Supabase client, creating it on first call."""
    global _client
    if _client is not None:
        return _client

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be set in the environment or .env file "
            "before using the database client."
        )

    from supabase import create_client
    _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client

def _perform_supabase_insert(payload: dict):
    try:
        client = get_client()
        # Insert into prediction_logs (existing table)
        client.table("prediction_logs").insert(payload).execute()
    except Exception as e:
        logging.warning(f"Supabase auto-save skipped/failed: {e}")

def save_prediction_to_supabase(
    prediction_type: str,
    location: str | None = None,
    crop: str | None = None,
    inputs: dict | None = None,
    results: dict | None = None,
    model_source: str | None = None,
    user_id: str | None = None
):
    """
    Save a prediction event to Supabase asynchronously in a background thread.
    Never blocks or throws exception to the caller.
    """
    payload = {
        "prediction_type": prediction_type,
        "location": location,
        "crop": crop,
        "inputs": inputs or {},
        "results": results or {},
        "model_source": model_source
    }
    if user_id:
        payload["user_id"] = user_id

    thread = threading.Thread(target=_perform_supabase_insert, args=(payload,), daemon=True)
    thread.start()
