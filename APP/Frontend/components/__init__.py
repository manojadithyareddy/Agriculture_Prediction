"""
AgriPredict AI — Reusable Animation Components Library
"""
from .hero_animation import render_hero_animation, render_ecosystem_animation
from .ai_processing import render_ai_processing_animation
from .climate_animation import render_climate_animation
from .crop_animation import render_crop_animation
from .yield_animation import render_yield_animation
from .irrigation_animation import render_irrigation_animation
from .market_animation import render_market_animation
from .lottie_assets import load_lottie_url, render_lottie_or_fallback

__all__ = [
    "render_hero_animation",
    "render_ecosystem_animation",
    "render_ai_processing_animation",
    "render_climate_animation",
    "render_crop_animation",
    "render_yield_animation",
    "render_irrigation_animation",
    "render_market_animation",
    "load_lottie_url",
    "render_lottie_or_fallback",
]
