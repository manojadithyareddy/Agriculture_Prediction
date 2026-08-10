from __future__ import annotations
from datetime import date as _date

def _resolve_date(predict_date: str | None) -> _date:
    """Return a date object from an ISO string, or today if None/empty."""
    if predict_date:
        try:
            # Strictly expects YYYY-MM-DD
            return _date.fromisoformat(predict_date)
        except ValueError as e:
            # Print a warning to your console so you know the frontend sent bad data!
            print(f"[WARNING]: Date parsing failed for '{predict_date}'. Defaulting to today. Error: {e}")

    return _date.today()


def climate_season(predict_date: str | None = None) -> str:
    """Return the climate season matching the model encoder categories.

    Encoder categories: ['monsoon', 'post-monsoon', 'summer', 'winter']
    Mapping:
      Jun–Sep  → monsoon       (SW monsoon)
      Oct–Nov  → post-monsoon  (NE monsoon / retreating)
      Dec–Feb  → winter
      Mar–May  → summer
    """
    month = _resolve_date(predict_date).month
    if 6 <= month <= 9:
        return "monsoon"
    if month in (10, 11):
        return "post-monsoon"
    if month in (12, 1, 2):
        return "winter"
    return "summer"  # March–May


def yield_season(predict_date: str | None = None) -> str:
    """Return the yield/agricultural season (Kharif / Rabi / Zaid)."""
    month = _resolve_date(predict_date).month
    if 6 <= month <= 10:
        return "Kharif"
    if month <= 3 or month >= 11:
        return "Rabi"
    return "Zaid"  # April–May