"""
database.py — Supabase client singleton.

The client is created lazily (on first access) so that importing this module
never crashes if the .env file is missing or the Supabase credentials are
incomplete.  Use `get_client()` instead of the bare `supabase` name.
"""
from __future__ import annotations

from config import SUPABASE_URL, SUPABASE_KEY

_client = None


def get_client():
    """Return the Supabase client, creating it on first call."""
    global _client
    if _client is not None:
        return _client

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be set in the .env file "
            "before using the database client."
        )

    from supabase import create_client  # imported lazily so tests don't need the library
    _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


import threading
import logging

def _perform_supabase_insert(payload: dict):
    try:
        client = get_client()
        client.table("prediction_logs").insert(payload).execute()
    except Exception as e:
        logging.warning(f"Supabase auto-save skipped/failed: {e}")

def save_prediction_to_supabase(
    prediction_type: str,
    location: str | None = None,
    crop: str | None = None,
    inputs: dict | None = None,
    results: dict | None = None,
    model_source: str | None = None
):
    """
    Save a prediction event to Supabase `prediction_logs` asynchronously in a background thread.
    Will never block or throw an exception to the caller.
    """
    payload = {
        "prediction_type": prediction_type,
        "location": location,
        "crop": crop,
        "inputs": inputs or {},
        "results": results or {},
        "model_source": model_source
    }
    thread = threading.Thread(target=_perform_supabase_insert, args=(payload,), daemon=True)
    thread.start()

