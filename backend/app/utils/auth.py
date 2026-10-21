"""
auth.py — Authentication & JWT helpers for Supabase integration.
"""
from __future__ import annotations
import logging
from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, Depends
from app.config import settings
from app.database.supabase import get_client

logger = logging.getLogger(__name__)


async def get_optional_user(
    authorization: Optional[str] = Header(None)
) -> Optional[Dict[str, Any]]:
    """
    Extract user from Bearer JWT token via Supabase Auth if provided.
    Does NOT raise an error if absent (allows public/guest access).
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.split("Bearer ")[1].strip()
    if not token:
        return None

    try:
        client = get_client()
        user_res = client.auth.get_user(token)
        if user_res and hasattr(user_res, "user") and user_res.user:
            return {
                "id": str(user_res.user.id),
                "email": user_res.user.email,
                "role": getattr(user_res.user, "role", "authenticated")
            }
    except Exception as e:
        logger.debug(f"Optional token validation failed: {e}")

    return None


async def get_required_user(
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """Requires authenticated user with valid Supabase session."""
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please provide a valid Bearer token."
        )
    return user
