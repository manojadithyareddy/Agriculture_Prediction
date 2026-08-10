"""
AgriPredict AI — Lottie Animation Manager & Asset Cache
"""
import requests
import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def load_lottie_url(url: str):
    """Fetch and cache Lottie JSON animation from URL with safe error handling."""
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

# Curated agricultural Lottie animation endpoints (Open CDN sources)
LOTTIE_URLS = {
    "plant_grow": "https://lottie.host/809c90b6-17b5-4b4d-94cb-9c1694ebf4b6/w0uU7Q6KxP.json",
    "cloud_rain": "https://lottie.host/d4e9f7eb-3f0e-436f-b258-45b0a7019ed7/59iGvM4ZtC.json",
    "ai_brain": "https://lottie.host/9e41ee44-9340-41ff-80c4-fa73aa496ce1/Kz7Fq6g61O.json",
    "water_drop": "https://lottie.host/3e7284b3-2b21-4fec-886d-672df7a7604f/V41dOa9dY3.json",
    "market_chart": "https://lottie.host/238a2e5d-752e-43d4-b97c-9df5b7ab4532/U4d9J2f2j8.json",
}

def render_lottie_or_fallback(key_name: str, height: int = 150, fallback_text: str = ""):
    """Render Lottie animation if available, otherwise display clean fallback."""
    url = LOTTIE_URLS.get(key_name)
    lottie_json = load_lottie_url(url) if url else None

    if lottie_json:
        try:
            from streamlit_lottie import st_lottie
            st_lottie(lottie_json, height=height, key=f"lottie_{key_name}_{height}")
            return True
        except Exception:
            pass

    if fallback_text:
        st.caption(fallback_text)
    return False
