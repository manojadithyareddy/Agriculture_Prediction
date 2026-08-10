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
