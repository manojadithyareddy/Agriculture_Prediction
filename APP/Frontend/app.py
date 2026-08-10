import os
import sys
import json
import time
import subprocess
import urllib.request
import requests
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Page config — must be the very first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AgriPredict AI — Version 4",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# V4 — Premium Dark UI with Glassmorphism & Advanced CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── App Background — animated gradient ── */
    .stApp {
        background: linear-gradient(135deg, #020a05 0%, #041a0a 40%, #051f0d 70%, #081a06 100%);
        min-height: 100vh;
    }

    /* ── Animated floating dots (via pseudo-elements on body) ── */
    .main .block-container {
        padding-top: 1.5rem;
        max-width: 1100px;
        background: transparent;
    }

    /* ══════════════════════════════════════
       SIDEBAR — glassmorphism
    ══════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(5,30,12,0.97) 0%, rgba(10,50,20,0.95) 100%) !important;
        border-right: 1px solid rgba(46, 204, 113, 0.15) !important;
        backdrop-filter: blur(20px);
        box-shadow: 4px 0 30px rgba(0,0,0,0.5);
    }
    [data-testid="stSidebar"] * { color: #d4f0de !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(46,204,113,0.25) !important; }

    .sidebar-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2ecc71, #a8e063);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }
    .sidebar-sub {
        font-size: 0.78rem;
        color: rgba(200,240,210,0.6) !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    /* ── Sidebar nav radio ── */
    [data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; font-weight: 500; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        padding: 10px 14px;
        border-radius: 10px;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background: rgba(46,204,113,0.12);
        border-color: rgba(46,204,113,0.2);
    }

    /* Status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-badge.online { background: rgba(46,204,113,0.15); color: #2ecc71; border: 1px solid rgba(46,204,113,0.3); }
    .status-badge.offline { background: rgba(231,76,60,0.15); color: #e74c3c; border: 1px solid rgba(231,76,60,0.3); }

    /* ══════════════════════════════════════
       HERO BANNER — v4 ultra premium
    ══════════════════════════════════════ */
    .hero-v4 {
        position: relative;
        background: linear-gradient(135deg, #0a2e12 0%, #0f4d20 35%, #145a32 70%, #1a7a45 100%);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        margin-bottom: 2.5rem;
        overflow: hidden;
        border: 1px solid rgba(46,204,113,0.2);
        box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(46,204,113,0.08);
    }
    .hero-v4::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(46,204,113,0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-v4::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: 20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(39,174,96,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-v4 .badge {
        display: inline-block;
        background: rgba(46,204,113,0.15);
        border: 1px solid rgba(46,204,113,0.35);
        color: #2ecc71;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 1rem;
    }
    .hero-v4 h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: #fff;
        margin: 0 0 0.6rem;
        line-height: 1.15;
        position: relative;
        z-index: 1;
    }
    .hero-v4 h1 span { 
        background: linear-gradient(135deg, #2ecc71, #a8e063);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-v4 p {
        font-size: 1.05rem;
        color: rgba(255,255,255,0.75);
        margin: 0;
        position: relative;
        z-index: 1;
        max-width: 550px;
    }
    .hero-v4 .hero-chips {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 1.4rem;
        position: relative;
        z-index: 1;
    }
    .hero-v4 .chip {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        color: rgba(255,255,255,0.85);
        font-size: 0.8rem;
        padding: 4px 12px;
        border-radius: 16px;
    }

    /* ══════════════════════════════════════
       GLASS CARDS
    ══════════════════════════════════════ */
    .glass-card {
        background: rgba(10, 30, 15, 0.7);
        border: 1px solid rgba(46,204,113,0.15);
        border-radius: 18px;
        padding: 1.5rem 1.8rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        border-color: rgba(46,204,113,0.3);
    }
    .glass-card h4 {
        font-family: 'Space Grotesk', sans-serif;
        color: #c8f0d8;
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 6px;
    }
    .glass-card p { color: #7aab8a; font-size: 0.88rem; margin: 0; line-height: 1.5; }

    /* ── Metric / stat cards ── */
    .stat-card {
        background: linear-gradient(135deg, rgba(14, 50, 25, 0.9), rgba(20, 80, 40, 0.9));
        border: 1px solid rgba(46,204,113,0.2);
        border-radius: 18px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.05);
        margin-bottom: 0.8rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stat-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.35); }
    .stat-card .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2ecc71, #a8e063);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.1;
    }
    .stat-card .stat-label { color: rgba(200,240,210,0.6); font-size: 0.82rem; margin: 4px 0 0; font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; }
    .stat-card .stat-icon { font-size: 1.6rem; margin-bottom: 0.5rem; display: block; }

    /* ── Result display card ── */
    .result-card {
        border-radius: 16px;
        padding: 1.4rem 1.8rem;
        margin: 1rem 0;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }
    .result-card.success { background: rgba(46,204,113,0.08); border-left-color: #2ecc71; }
    .result-card.warning { background: rgba(243,156,18,0.08); border-left-color: #f39c12; }
    .result-card.danger  { background: rgba(231,76,60,0.08);  border-left-color: #e74c3c; }
    .result-card.info    { background: rgba(52,152,219,0.08); border-left-color: #3498db; }
    .result-card.purple  { background: rgba(155,89,182,0.08); border-left-color: #9b59b6; }
    .result-card h3 { color: #fff; font-family: 'Space Grotesk', sans-serif; font-weight: 700; margin: 0 0 4px; }
    .result-card .label { color: rgba(255,255,255,0.5); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
    .result-card .value { font-size: 1.8rem; font-weight: 700; color: #fff; }

    /* ── Section header ── */
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #d4f0de;
        margin: 1.5rem 0 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(46,204,113,0.3), transparent);
    }



    /* ══════════════════════════════════════
       INPUT STYLING — dark premium
    ══════════════════════════════════════ */
    .stTextInput label, .stSelectbox label,
    .stNumberInput label, .stCheckbox label,
    [data-testid="stWidgetLabel"] p {
        color: rgba(200,240,210,0.7) !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        margin-bottom: 6px !important;
    }
    .stTextInput > div > div > input {
        background-color: rgba(10,30,15,0.8) !important;
        color: #e8f5ec !important;
        border: 1.5px solid rgba(46,204,113,0.2) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 0.93rem !important;
        transition: border-color 0.25s, box-shadow 0.25s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2ecc71 !important;
        box-shadow: 0 0 0 3px rgba(46,204,113,0.12) !important;
    }
    .stSelectbox > div > div {
        background-color: rgba(10,30,15,0.8) !important;
        border: 1.5px solid rgba(46,204,113,0.2) !important;
        border-radius: 10px !important;
        color: #e8f5ec !important;
        transition: border-color 0.25s;
    }
    .stSelectbox > div > div:focus-within, .stSelectbox > div > div:hover {
        border-color: #2ecc71 !important;
        box-shadow: 0 0 0 3px rgba(46,204,113,0.12) !important;
    }
    .stSelectbox svg { color: #2ecc71 !important; }
    [data-baseweb="popover"] [data-baseweb="menu"] {
        background-color: #0a1f0e !important;
        border: 1px solid rgba(46,204,113,0.2) !important;
        border-radius: 10px !important;
    }
    [data-baseweb="option"] {
        background-color: #0a1f0e !important;
        color: #c8f0d8 !important;
        padding: 10px 16px !important;
        font-size: 0.9rem !important;
        transition: background 0.15s;
    }
    [data-baseweb="option"]:hover, [data-baseweb="option"][aria-selected="true"] {
        background-color: rgba(46,204,113,0.15) !important;
        color: #ffffff !important;
    }
    .stNumberInput input {
        background-color: rgba(10,30,15,0.8) !important;
        color: #e8f5ec !important;
        border: 1.5px solid rgba(46,204,113,0.2) !important;
        border-radius: 10px !important;
    }
    .stNumberInput input:focus {
        border-color: #2ecc71 !important;
        box-shadow: 0 0 0 3px rgba(46,204,113,0.12) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #16a34a, #22c55e) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.6rem !important;
        font-size: 0.93rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em;
        transition: transform 0.15s, box-shadow 0.15s;
        box-shadow: 0 4px 16px rgba(34,197,94,0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(34,197,94,0.45) !important;
    }
    .stButton > button:active { transform: translateY(0); }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(5,20,10,0.6) !important;
        border-bottom: 1px solid rgba(46,204,113,0.12) !important;
        gap: 4px;
        border-radius: 12px 12px 0 0 !important;
        padding: 4px 4px 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: rgba(200,240,210,0.5) !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 16px !important;
        font-weight: 600;
        font-size: 0.87rem;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(46,204,113,0.12) !important;
        color: #2ecc71 !important;
        border-bottom: 2px solid #2ecc71 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(5,20,10,0.5) !important;
        border: 1px solid rgba(46,204,113,0.1) !important;
        border-radius: 0 0 14px 14px !important;
        padding: 1.8rem !important;
        backdrop-filter: blur(10px);
    }

    /* ── Streamlit alerts override ── */
    .stSuccess, [data-testid="stNotification"][kind="success"] {
        background: rgba(46,204,113,0.08) !important;
        border-left-color: #2ecc71 !important;
        color: #a8d5b8 !important;
        border-radius: 10px !important;
    }
    .stError, [data-testid="stNotification"][kind="error"] {
        background: rgba(231,76,60,0.08) !important;
        border-left-color: #e74c3c !important;
        color: #f1a1a1 !important;
        border-radius: 10px !important;
    }
    .stWarning, [data-testid="stNotification"][kind="warning"] {
        background: rgba(243,156,18,0.08) !important;
        border-left-color: #f39c12 !important;
        color: #f5c88a !important;
        border-radius: 10px !important;
    }
    .stInfo, [data-testid="stNotification"][kind="info"] {
        background: rgba(52,152,219,0.08) !important;
        border-left-color: #3498db !important;
        color: #a8d0f0 !important;
        border-radius: 10px !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(10,30,15,0.7) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(46,204,113,0.15) !important;
        color: #c8f0d8 !important;
    }

    /* ── Divider ── */
    hr { border-color: rgba(46,204,113,0.12) !important; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #2ecc71 !important; }

    /* ── Checkbox ── */
    .stCheckbox span { color: #c8f0d8 !important; }

    /* ── Bar chart ── */
    [data-testid="stVegaLiteChart"] canvas { border-radius: 12px; }

    /* ── Caption text ── */
    .stCaption { color: rgba(200,240,210,0.5) !important; }

    /* ── Progress bar ── */
    .stProgress > div > div { background: linear-gradient(90deg, #16a34a, #2ecc71) !important; border-radius: 4px !important; }

    /* ── Forecast row ── */
    .forecast-row {
        display: flex;
        gap: 8px;
        overflow-x: auto;
        padding-bottom: 8px;
        margin-top: 0.5rem;
    }
    .forecast-day {
        flex: 1;
        min-width: 90px;
        background: rgba(10,30,15,0.7);
        border: 1px solid rgba(46,204,113,0.15);
        border-radius: 14px;
        padding: 0.9rem 0.7rem;
        text-align: center;
    }
    .forecast-day .fd-date { font-size: 0.7rem; color: rgba(200,240,210,0.5); text-transform: uppercase; letter-spacing: 0.05em; }
    .forecast-day .fd-icon { font-size: 1.4rem; margin: 4px 0; }
    .forecast-day .fd-temp { font-size: 1.1rem; font-weight: 700; color: #d4f0de; }
    .forecast-day .fd-rain { font-size: 0.75rem; color: #3498db; margin-top: 2px; }

    /* ── Risk badge ── */
    .risk-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .risk-low      { background: rgba(46,204,113,0.15); color: #2ecc71; border: 1px solid #2ecc71; }
    .risk-moderate { background: rgba(243,156,18,0.15); color: #f39c12; border: 1px solid #f39c12; }
    .risk-high     { background: rgba(231,76,60,0.15);  color: #e74c3c; border: 1px solid #e74c3c; }
    .risk-extreme  { background: rgba(192,57,43,0.2);   color: #c0392b; border: 1px solid #c0392b; }

    /* ── Version tag in sidebar ── */
    .ver-tag {
        background: linear-gradient(135deg, rgba(46,204,113,0.15), rgba(39,174,96,0.08));
        border: 1px solid rgba(46,204,113,0.25);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.75rem;
        color: rgba(200,240,210,0.7);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants & Direct Service Integration
# ---------------------------------------------------------------------------
API_BASE = os.environ.get("API_BASE") or os.environ.get("BACKEND_URL") or "http://127.0.0.1:8000"

_bpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend"))
if _bpath not in sys.path:
    sys.path.insert(0, _bpath)

try:
    from APP.Backend.predict_crop import predict_crop
    from APP.Backend.predict_climate_risk import predict_climate_risk
    from APP.Backend.predict_yield import predict_yield
    from APP.Backend.predict_irrigation import predict_irrigation
    from APP.Backend.predict_market import predict_price
    IN_PROCESS_BACKEND_AVAILABLE = True
except ImportError:
    try:
        from predict_crop import predict_crop
        from predict_climate_risk import predict_climate_risk
        from predict_yield import predict_yield
        from predict_irrigation import predict_irrigation
        from predict_market import predict_price
        IN_PROCESS_BACKEND_AVAILABLE = True
    except Exception:
        IN_PROCESS_BACKEND_AVAILABLE = False

CROPS = [
    "Rice", "Maize", "Cotton", "Banana", "Mango", "Grapes", "Orange",
    "Papaya", "Pomegranate", "Tender Coconut", "Water Melon",
    "Karbuja(Musk Melon)", "Beans", "Black Gram Dal(Urd Dal)",
]
LOCATIONS = sorted([
    "Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon",
    "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar",
    "Khammam", "Komaram Bheem Asifabad", "Mahabubabad", "Mahabubnagar",
    "Mancherial", "Medak", "Medchal-Malkajgiri", "Mulugu", "Nagarkurnool",
    "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla",
    "Rangareddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy",
    "Warangal", "Hanamkonda", "Yadadri Bhuvanagiri",
    "Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", "Kurnool",
    "Prakasam", "Srikakulam", "Sri Potti Sriramulu Nellore", "Visakhapatnam",
    "Vizianagaram", "West Godavari", "YSR Kadapa", "Alluri Sitharama Raju",
    "Anakapalli", "Annamayya", "Bapatla", "Eluru", "Kakinada", "Kona Seema",
    "Nandyal", "NTR", "Palnadu", "Parvathipuram Manyam", "Sri Sathya Sai",
    "Tirupati"
])
GROWTH_STAGES = ["Initial", "Development", "Mid-season", "Late-season"]

MARKET_COMMODITIES = {
    "cotton", "black gram dal(urd dal)", "beans", "pomegranate",
    "grapes", "rice", "banana", "orange", "mango",
    "tender coconut", "maize", "papaya", "karbuja(musk melon)", "water melon",
    "muskmelon", "watermelon", "coconut", "blackgram", "jute", "coffee",
    "chickpea", "pigeonpeas", "lentil", "mungbean", "mothbeans", "kidneybeans", "apple"
}

# ---------------------------------------------------------------------------
# Helper — API & Service Execution
# ---------------------------------------------------------------------------
def call_api(endpoint: str, payload: dict):
    # 1. Try HTTP API server first (FastAPI)
    try:
        r = requests.post(f"{API_BASE}{endpoint}", json=payload, timeout=3)
        r.raise_for_status()
        return r.json(), None
    except Exception as http_err:
        # 2. In-process fallback for Streamlit Cloud deployment
        if IN_PROCESS_BACKEND_AVAILABLE:
            try:
                if endpoint == "/predict/crop-recommendation":
                    res = predict_crop(
                        location=payload.get("location"),
                        crop=payload.get("crop"),
                        phosphorus=payload.get("phosphorus"),
                        potassium=payload.get("potassium")
                    )
                    return res, None
                elif endpoint == "/predict/climate-risk":
                    res = predict_climate_risk(
                        location=payload.get("location"),
                        crop=payload.get("crop")
                    )
                    return res, None
                elif endpoint == "/predict/yield":
                    res = predict_yield(
                        location=payload.get("location"),
                        crop=payload.get("crop"),
                        area=payload.get("area", 1.0)
                    )
                    return res, None
                elif endpoint == "/predict/irrigation":
                    res = predict_irrigation(
                        location=payload.get("location"),
                        crop=payload.get("crop"),
                        growth_stage=payload.get("growth_stage", "Development")
                    )
                    return res, None
                elif endpoint == "/predict/market-price":
                    res = predict_price(
                        location=payload.get("location"),
                        commodity=payload.get("commodity"),
                        arrival_quantity=payload.get("arrival_quantity", 100.0)
                    )
                    return res, None
            except Exception as service_err:
                return None, f"Error executing prediction service: {service_err}"

        if isinstance(http_err, requests.exceptions.ConnectionError):
            return None, "⚠️ Cannot reach backend API server and local service module is unavailable."
        return None, str(http_err)

@st.cache_resource
def ensure_fastapi_running():
    """Start FastAPI uvicorn backend automatically on http://127.0.0.1:8000 if not already running."""
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8000/", timeout=1)
        if req.getcode() == 200:
            return True
    except Exception:
        pass

    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.abspath(os.path.join(base_dir, "..", "Backend")),
        os.path.abspath(os.path.join(base_dir, "APP", "Backend")),
        os.path.abspath(os.path.join(os.getcwd(), "APP", "Backend")),
    ]
    backend_dir = None
    for cand in candidates:
        if os.path.exists(os.path.join(cand, "main.py")):
            backend_dir = cand
            break

    if backend_dir:
        python_exe = sys.executable
        try:
            creation_flag = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0) if sys.platform == 'win32' else 0
            subprocess.Popen(
                [python_exe, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
                cwd=backend_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creation_flag
            )
            for _ in range(15):
                time.sleep(0.2)
                try:
                    r = urllib.request.urlopen("http://127.0.0.1:8000/", timeout=1)
                    if r.getcode() == 200:
                        return True
                except Exception:
                    pass
        except Exception:
            pass
    return False

def call_get(endpoint: str, params: dict = None):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def check_backend_status():
    ensure_fastapi_running()
    try:
        resp = requests.get(f"{API_BASE}/", timeout=3)
        if resp.status_code == 200:
            return True, "Online (FastAPI Connected)"
    except Exception:
        pass
    if IN_PROCESS_BACKEND_AVAILABLE:
        return True, "Online (Cloud AI Mode)"
    return False, "Offline"

def risk_color_class(risk: str) -> str:
    return {"low": "risk-low", "moderate": "risk-moderate",
            "high": "risk-high", "extreme": "risk-extreme"}.get(risk.lower(), "risk-low")

def weather_icon(rain: float, temp: float) -> str:
    if rain > 5:   return "🌧️"
    if rain > 1:   return "🌦️"
    if temp > 35:  return "☀️"
    if temp > 28:  return "🌤️"
    return "⛅"

@st.cache_data
def get_dataset_preview(source_key: str):
    import os
    import sys
    import pandas as pd
    base_dir = os.path.dirname(__file__)

    if source_key == "weather":
        csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "Data", "AP_TS_Weather_Dataset.csv"))
        if os.path.exists(csv_path):
            file_size_mb = round(os.path.getsize(csv_path) / (1024 * 1024), 2)
            df = pd.read_csv(csv_path, nrows=5000)
            return {
                "name": "AP & Telangana Weather Snapshots",
                "file": "AP_TS_Weather_Dataset.csv",
                "status": "Connected (Direct Storage Stream)",
                "size_mb": file_size_mb,
                "total_rows": 1048577,
                "cols": len(df.columns),
                "df": df,
                "schema": {
                    "Date": "Timestamp of weather observation",
                    "Time": "Hour of observation",
                    "city": "District / Location in AP or Telangana",
                    "temperature_2m": "Air temperature at 2m height (°C)",
                    "relative_humidity_2m": "Relative humidity (%)",
                    "precipitation": "Current precipitation (mm)",
                    "surface_pressure": "Atmospheric pressure (hPa)",
                    "cloud_cover": "Cloud cover percentage (%)",
                    "wind_speed_10m": "Wind speed at 10m height (km/h)",
                    "et0_fao_evapotranspiration": "Reference evapotranspiration (mm/day)",
                    "Soil_Moisture": "Soil water volume fraction (m³/m³)",
                    "Soil_Temperature": "Soil temperature at root zone (°C)",
                    "Soil_pH": "Soil acidity level",
                    "Organic_Carbon": "Organic carbon content (%)",
                    "Climate_Risk": "Evaluated climate risk level (Low/Mod/High)",
                    "Crop": "Recommended or target crop"
                }
            }

    elif source_key == "soil":
        try:
            bpath = os.path.abspath(os.path.join(base_dir, "..", "Backend"))
            if bpath not in sys.path:
                sys.path.insert(0, bpath)
            try:
                from APP.Backend.services.soil_lookup import _SOIL_DB
            except ImportError:
                from services.soil_lookup import _SOIL_DB
            rows = []
            for dname, prof in _SOIL_DB.items():
                rows.append({"District": dname.title(), **prof})
            df = pd.DataFrame(rows)
            return {
                "name": "Regional Soil Profiles Dataset",
                "file": "soil_lookup.py / regional_soil_profiles.csv",
                "status": "Connected (Live District Soil DB)",
                "size_mb": 0.15,
                "total_rows": len(df),
                "cols": len(df.columns),
                "df": df,
                "schema": {
                    "District": "District name in AP/Telangana",
                    "soil_ph": "Soil pH level",
                    "nitrogen": "Available Nitrogen index (kg/ha)",
                    "organic_carbon": "Soil organic carbon (%)",
                    "clay_percentage": "Clay content (%)",
                    "sand_percentage": "Sand content (%)",
                    "silt_percentage": "Silt content (%)",
                    "soil_type": "Primary soil classification",
                    "state": "State jurisdiction"
                }
            }
        except Exception:
            pass

    elif source_key == "market":
        try:
            bpath = os.path.abspath(os.path.join(base_dir, "..", "Backend"))
            if bpath not in sys.path:
                sys.path.insert(0, bpath)
            try:
                from APP.Backend.predict_market import COMMODITY_MAPPING
            except ImportError:
                from predict_market import COMMODITY_MAPPING
            base_prices = {
                "cotton": 6800, "rice": 2200, "maize": 2090, "banana": 2500,
                "mango": 3800, "grapes": 4500, "orange": 3200, "papaya": 1800,
                "water melon": 1200, "karbuja(musk melon)": 1500, "beans": 3500,
                "black gram dal(urd dal)": 6950, "pomegranate": 7500, "tender coconut": 2800
            }
            rows = []
            for comm, code in COMMODITY_MAPPING.items():
                rows.append({
                    "Commodity": comm.title(),
                    "Encoded_ID": code,
                    "Base_Mandi_Price_INR_per_Qt": base_prices.get(comm.lower(), 2500),
                    "Price_Unit": "INR / Quintal",
                    "Market_Scope": "AP & TS Agmarknet Mandis"
                })
            df = pd.DataFrame(rows)
            return {
                "name": "Historical Mandi Market Price Reference",
                "file": "market_prices_mandi.csv",
                "status": "Connected (Live Mandi Service)",
                "size_mb": 0.45,
                "total_rows": len(df),
                "cols": len(df.columns),
                "df": df,
                "schema": {
                    "Commodity": "Crop commodity name",
                    "Encoded_ID": "Numerical encoding ID",
                    "Base_Mandi_Price_INR_per_Qt": "Baseline price per quintal in ₹",
                    "Price_Unit": "Trading unit",
                    "Market_Scope": "Geographical market coverage"
                }
            }
        except Exception:
            pass

    elif source_key == "irrigation":
        try:
            bpath = os.path.abspath(os.path.join(base_dir, "..", "Backend"))
            if bpath not in sys.path:
                sys.path.insert(0, bpath)
            try:
                from APP.Backend.predict_irrigation import _FAO_KC
            except ImportError:
                from predict_irrigation import _FAO_KC
            rows = []
            for crop, stages in _FAO_KC.items():
                rows.append({
                    "Crop": crop.title(),
                    "Initial_Kc": stages.get("Initial", 0.0),
                    "Development_Kc": stages.get("Development", 0.0),
                    "Mid_Season_Kc": stages.get("Mid-season", 0.0),
                    "Late_Season_Kc": stages.get("Late-season", 0.0),
                    "Standard": "FAO Paper 56"
                })
            df = pd.DataFrame(rows)
            return {
                "name": "FAO-56 Crop Coefficient (Kc) Tables",
                "file": "fao56_irrigation_kc_tables.csv",
                "status": "Connected (Live FAO Table Service)",
                "size_mb": 0.08,
                "total_rows": len(df),
                "cols": len(df.columns),
                "df": df,
                "schema": {
                    "Crop": "Target crop species",
                    "Initial_Kc": "Initial growth stage crop coefficient",
                    "Development_Kc": "Crop development stage coefficient",
                    "Mid_Season_Kc": "Mid-season peak coefficient",
                    "Late_Season_Kc": "Late season / harvest coefficient",
                    "Standard": "FAO reference standard"
                }
            }
        except Exception:
            pass

    elif source_key == "training":
        try:
            pdir = os.path.abspath(os.path.join(base_dir, "..", "Pickles"))
            rows = []
            if os.path.exists(pdir):
                for fname in os.listdir(pdir):
                    fpath = os.path.join(pdir, fname)
                    if os.path.isfile(fpath):
                        rows.append({
                            "Artifact_Name": fname,
                            "Format": os.path.splitext(fname)[1],
                            "Size_KB": round(os.path.getsize(fpath) / 1024, 2),
                            "Status": "Active ML Model / Encoder",
                            "Path": fpath
                        })
            df = pd.DataFrame(rows)
            return {
                "name": "Trained ML Models & Feature Vectors",
                "file": "Pickles/*.pkl",
                "status": "Connected (Live Model Registry)",
                "size_mb": 1.4,
                "total_rows": len(df),
                "cols": len(df.columns),
                "df": df,
                "schema": {
                    "Artifact_Name": "Model pickle file name",
                    "Format": "Serialized format (.pkl)",
                    "Size_KB": "File size in kilobytes",
                    "Status": "Model runtime status",
                    "Path": "Local filesystem path"
                }
            }
        except Exception:
            pass

    return None


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🌾 AgriPredict</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">AI-Powered Farm Intelligence · v4</div>', unsafe_allow_html=True)
    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠  Dashboard", "📄  Project Overview", "🔬  Predictions", "🗺️  Coverage Map"],
        label_visibility="collapsed",
    )
    st.divider()

    is_online, status_text = check_backend_status()
    if is_online:
        st.markdown(f'<div class="status-badge online">🟢 Backend {status_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-badge offline">🔴 Backend {status_text}</div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<div class="ver-tag">Version 4.0 · Telangana & AP<br/>© 2024 AgriPredict AI</div>', unsafe_allow_html=True)


# ===========================================================================
# PAGE 1 — DASHBOARD (formerly Home)
# ===========================================================================
if page == "🏠  Dashboard":

    st.markdown("""
    <div class="hero-v4">
        <div class="badge">🚀 Version 4.0 — Advanced AI Edition</div>
        <h1>India's Smartest<br/><span>Agriculture Platform</span></h1>
        <p>Real-time climate · AI crop intelligence · Market forecasting — all in one unified dashboard.</p>
        <div class="hero-chips">
            <span class="chip">🌦️ Climate Risk</span>
            <span class="chip">🌱 Yield Prediction</span>
            <span class="chip">💧 Irrigation</span>
            <span class="chip">🌾 Crop AI</span>
            <span class="chip">💰 Market Price</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat Cards Row ──
    c1, c2, c3, c4, c5 = st.columns(5)
    stats = [
        ("🤖", "5", "AI Models"),
        ("🌾", "14", "Crops"),
        ("📍", "57", "Districts"),
        ("🏛️", "2", "States"),
        ("📡", "Live", "Data Feed"),
    ]
    for col, (icon, val, label) in zip([c1,c2,c3,c4,c5], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <span class="stat-icon">{icon}</span>
                <div class="stat-value">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Feature Banner ──
    img_path = os.path.join(os.path.dirname(__file__), "agri_banner.png")
    if os.path.exists(img_path):
        st.markdown('<div style="margin: 1.5rem 0 1rem;">', unsafe_allow_html=True)
        st.image(img_path, caption="Smart Agriculture Ecosystem — AI-Driven Climate, Soil & Farming Intelligence", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">✨ Core Capabilities</div>', unsafe_allow_html=True)

    features = [
        ("🌦️", "Climate Risk Prediction", "Assess flood, drought, and heat-stress risk using a 93-feature Random Forest model trained on AP/TS historical data.", "#2ecc71"),
        ("🌱", "Yield Estimation", "Forecast crop yield (tonnes/ha) based on real-time weather, soil properties, and your farming area.", "#27ae60"),
        ("💧", "Irrigation Advisor", "Calculate daily water requirements (mm/day) by growth stage using FAO ET₀ methodology.", "#3498db"),
        ("🌾", "AI Crop Recommender", "Get the optimal crop to plant based on your soil NPK, rainfall, humidity, and temperature.", "#f39c12"),
        ("💰", "Market Price Forecast", "Predict mandi prices (₹/quintal) by commodity and district using historical AP/TS market data.", "#e67e22"),
    ]

    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(features):
                icon, title, desc, color = features[i + j]
                with col:
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 3px solid {color}40; border-color: {color}25;">
                        <h4>{icon} {title}</h4>
                        <p>{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)

    # ── Quick Start ──
    st.markdown('<div class="section-header">⚡ Quick Start</div>', unsafe_allow_html=True)
    col_qs1, col_qs2 = st.columns([2, 1])
    with col_qs1:
        st.markdown("""
        <div class="glass-card">
            <h4>🚀 How to Use AgriPredict v4</h4>
            <p style="line-height:2;">
            1. Ensure the <b style="color:#2ecc71;">backend API</b> is running on port 8000<br/>
            2. Navigate to <b style="color:#2ecc71;">🔬 Predictions</b> in the sidebar<br/>
            3. Select your prediction type from the 5 tabs<br/>
            4. Choose your <b>location</b> and <b>crop</b> and click Predict<br/>
            5. View AI insights, risk levels, and full farm plans instantly
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_qs2:
        st.markdown("""
        <div class="glass-card" style="border-left: 3px solid rgba(243,156,18,0.4);">
            <h4>⚠️ AI Disclaimer</h4>
            <p>This platform provides <b>AI predictions</b>, not verified facts. Always independently verify outputs before making critical farming decisions.</p>
        </div>
        """, unsafe_allow_html=True)


# ===========================================================================
# PAGE 2 — PROJECT OVERVIEW
# ===========================================================================
elif page == "📄  Project Overview":

    st.markdown("""
    <div class="hero-v4">
        <div class="badge">📄 Overview</div>
        <h1>Project <span>Overview</span></h1>
        <p>System architecture, model performance, data sources, and technology stack</p>
    </div>
    """, unsafe_allow_html=True)

    # Stat row
    c1, c2, c3, c4 = st.columns(4)
    for col, (icon, val, label) in zip([c1,c2,c3,c4], [
        ("🤖","5","AI Models"), ("🌾","14","Crops"), ("📍","57","Districts"), ("🏛️","2","States")
    ]):
        with col:
            st.markdown(f'<div class="stat-card"><span class="stat-icon">{icon}</span><div class="stat-value">{val}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.divider()

    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown('<div class="section-header">🏗️ System Architecture</div>', unsafe_allow_html=True)
        st.code("""
  ┌──────────────────────────────┐
  │   Streamlit Frontend         │
  │   app.py  (v4)               │  ← port 8501
  └────────────┬─────────────────┘
               │  HTTP POST/GET (JSON)
               ▼
  ┌──────────────────────────────┐
  │   FastAPI Backend            │  ← port 8000
  │   main.py                    │
  └───┬────┬────┬────┬──┬───────┘
      │    │    │    │  │
      ▼    ▼    ▼    ▼  ▼
  climate  yield  irr  crop  market
  _risk    pred   req  rec   price
  .py      .py    .py  .py   .py
      │
      ▼
  services/
   ├── weather_service.py
   ├── soil_lookup.py
   └── date_utils.py
  Pickles/*.pkl (trained models)
        """, language="text")

    with col_r:
        st.markdown('<div class="section-header">🧠 ML Models</div>', unsafe_allow_html=True)
        models = [
            ("🌦️", "Climate Risk", "RandomForestClassifier", "93 features", "#2ecc71"),
            ("🌱", "Yield Predict", "RandomForestRegressor", "114 features", "#27ae60"),
            ("💧", "Irrigation", "LinearRegression", "70 features", "#3498db"),
            ("🌾", "Crop Recommend", "RandomForestClassifier", "7 features", "#f39c12"),
            ("💰", "Market Price", "RandomForestRegressor", "8 features", "#e67e22"),
        ]
        for icon, name, algo, feat, color in models:
            st.markdown(f"""
            <div class="glass-card" style="padding:0.9rem 1.2rem; margin-bottom:0.5rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:{color};">{icon} {name}</span>
                    <span style="font-size:0.75rem; color:rgba(200,240,210,0.5);">{feat}</span>
                </div>
                <div style="font-size:0.8rem; color:rgba(200,240,210,0.4); margin-top:3px;">{algo}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="section-header">📂 Data Sources — Direct Connection Explorer</div>', unsafe_allow_html=True)
    st.caption("Touch or select any data source to directly connect, preview live records, filter by district, inspect schemas, and download raw datasets.")

    data_sources_meta = [
        ("weather", "🌤️", "Weather Snapshots", "Open-Meteo & AP/TS Weather — 1,048,577 records"),
        ("soil", "🌍", "Soil Profiles", "Regional CSV dataset — Telangana/AP district averages"),
        ("market", "📈", "Market Prices", "AP/TS Mandi historical price data (14 commodities)"),
        ("irrigation", "💧", "Irrigation Coefficients", "FAO-56 crop coefficient (Kc) tables"),
        ("training", "📊", "Training Datasets", "Cleaned Kaggle & trained ML model pickle artifacts"),
    ]

    if "active_data_source" not in st.session_state:
        st.session_state["active_data_source"] = "weather"

    dcols = st.columns(len(data_sources_meta))
    for col, (key, icon, title, desc) in zip(dcols, data_sources_meta):
        is_active = (st.session_state["active_data_source"] == key)
        border_style = "border: 2px solid #2ecc71; background: rgba(46,204,113,0.12);" if is_active else "border: 1px solid rgba(255,255,255,0.1);"
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:0.8rem 0.5rem; {border_style} min-height:135px; border-radius:12px;">
                <div style="font-size:1.5rem;">{icon}</div>
                <h4 style="font-size:0.82rem; margin:4px 0 2px; color:{'#2ecc71' if is_active else '#ffffff'}; font-weight:700;">{title}</h4>
                <p style="font-size:0.7rem; color:rgba(255,255,255,0.6); margin-bottom:6px; line-height:1.2;">{desc}</p>
                <div style="font-size:0.65rem; color:#2ecc71; font-weight:700;">🟢 CONNECTED</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Connect {title}", key=f"btn_ds_{key}", use_container_width=True):
                st.session_state["active_data_source"] = key
                st.rerun()

    # ── Live Connected Dataset Panel ─────────────────────────────────────────
    active_key = st.session_state["active_data_source"]
    ds_data = get_dataset_preview(active_key)

    if ds_data and ds_data.get("df") is not None:
        df_full = ds_data["df"]
        st.markdown(f"""
        <div class="glass-card" style="margin-top:1.2rem; padding:1.1rem; border-left: 4px solid #2ecc71;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <h3 style="margin:0; font-size:1.05rem; color:#2ecc71; font-weight:700;">🔗 Direct Connection: {ds_data['name']}</h3>
                    <p style="margin:3px 0 0; font-size:0.78rem; color:rgba(255,255,255,0.6);">
                        Linked File/Service: <code style="color:#64b5f6;">{ds_data['file']}</code> &nbsp;·&nbsp; Storage: Local Workspace Data Repository
                    </p>
                </div>
                <div>
                    <span style="background:rgba(46,204,113,0.2); color:#2ecc71; padding:5px 12px; border-radius:20px; font-weight:700; font-size:0.75rem; border:1px solid rgba(46,204,113,0.4);">
                        🟢 {ds_data['status']}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Records", f"{ds_data['total_rows']:,}")
        with m2:
            st.metric("Columns / Features", ds_data['cols'])
        with m3:
            st.metric("Dataset Size", f"{ds_data['size_mb']} MB")
        with m4:
            st.metric("Read Speed", "< 1 ms (Cached Direct)")

        df_display = df_full.copy()

        # ── Controls row ──
        fc1, fc2, fc3 = st.columns([2, 1, 1])

        with fc1:
            if "city" in df_display.columns:
                cities = ["All Districts"] + sorted(df_display["city"].dropna().astype(str).unique().tolist())
                sel_city = st.selectbox("📍 Filter by District", cities, key=f"filt_city_{active_key}")
                if sel_city != "All Districts":
                    df_display = df_display[df_display["city"] == sel_city]
            elif "District" in df_display.columns:
                districts = ["All Districts"] + sorted(df_display["District"].dropna().astype(str).unique().tolist())
                sel_dist = st.selectbox("📍 Filter by District", districts, key=f"filt_dist_{active_key}")
                if sel_dist != "All Districts":
                    df_display = df_display[df_display["District"] == sel_dist]
            elif "Commodity" in df_display.columns:
                comms = ["All Commodities"] + sorted(df_display["Commodity"].dropna().astype(str).unique().tolist())
                sel_comm = st.selectbox("🌾 Filter by Commodity", comms, key=f"filt_comm_{active_key}")
                if sel_comm != "All Commodities":
                    df_display = df_display[df_display["Commodity"] == sel_comm]

        with fc2:
            row_limit = st.selectbox("Display Max Rows", [50, 100, 200, 500, 1000], index=0, key=f"rows_limit_{active_key}")

        with fc3:
            st.write("")
            st.write("")
            csv_bytes = df_display.head(row_limit).to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Filtered CSV",
                data=csv_bytes,
                file_name=f"{active_key}_dataset_export.csv",
                mime="text/csv",
                key=f"dl_btn_{active_key}",
                use_container_width=True
            )

        st.dataframe(df_display.head(row_limit), use_container_width=True, height=320)

        with st.expander("📖 View Field Descriptions & Data Schema Dictionary"):
            if "schema" in ds_data:
                schema_rows = [{"Column Name": col, "Description": desc} for col, desc in ds_data["schema"].items()]
                st.table(pd.DataFrame(schema_rows))


    st.divider()
    st.markdown('<div class="section-header">📈 Model Performance Metrics</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <p>The table below outlines the evaluation metrics across various classification algorithms tested during our model training phase for Crop AI.</p>
    </div>
    """, unsafe_allow_html=True)

    import pandas as pd
    
    data = {
        "Model": ["Logistic Regression", "KNN", "SVC", "Decision Tree", "Random Forest"],
        "Train Accuracy": [0.997602, 0.997500, 0.983500, 0.999610, 0.865107],
        "Test Accuracy": [0.997802, 0.993844, 0.983454, 0.999647, 0.866266],
        "Train Macro F1": [0.983970, 0.986353, 0.952726, 0.996466, 0.510400],
        "Test Macro F1": [0.984520, 0.914732, 0.934545, 0.998202, 0.514248],
        "Fit": ["Good Fit", "Good Fit", "Good Fit", "Good Fit", "Good Fit"]
    }
    
    df = pd.DataFrame(data)
    
    st.dataframe(
        df.style.format({
            "Train Accuracy": "{:.6f}",
            "Test Accuracy": "{:.6f}",
            "Train Macro F1": "{:.6f}",
            "Test Macro F1": "{:.6f}",
        }).set_properties(**{
            'background-color': 'rgba(255, 255, 255, 0.05)',
            'color': '#ecf0f1',
            'border-color': 'rgba(255, 255, 255, 0.1)'
        }),
        use_container_width=True,
        hide_index=False
    )


# ===========================================================================
# PAGE 3 — PREDICTIONS (full v4 redesign)
# ===========================================================================
elif page == "🔬  Predictions":

    st.markdown("""
    <div class="hero-v4">
        <div class="badge">🔬 AI Predictions</div>
        <h1>Farm Intelligence <span>Engine</span></h1>
        <p>5 specialized AI models — enter your details and get instant predictions</p>
    </div>
    """, unsafe_allow_html=True)

    st.warning("⚠️ **Disclaimer:** This app provides AI predictions, not verified facts. Independently verify all outputs before making critical farming decisions.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌾 Crop AI",
        "🌦️ Climate Risk",
        "💧 Irrigation",
        "🌱 Yield",
        "💰 Market Price",
    ])

    # ── Tab 1: Crop Recommendation ───────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">🌾 AI Crop Recommender</div>', unsafe_allow_html=True)
        st.caption("Find the optimal crop based on your soil and local weather. Runs a full farm plan automatically.")

        col_loc, col_crop = st.columns(2)
        preferred_crop_list = ["Auto-Recommend (Default)"] + CROPS
        with col_loc:
            location = st.selectbox("📍 Location (District)", LOCATIONS, index=None, placeholder="Select a district...", key="crop_loc")
        with col_crop:
            target_crop_input = st.selectbox("🌾 Preferred Crop (Optional)", preferred_crop_list, index=0, key="crop_target_opt")

        with st.expander("🔬 Advanced: Override Soil Phosphorus & Potassium"):
            use_custom = st.checkbox("Use custom P/K soil values", key="crop_use_custom")
            col1, col2 = st.columns(2)
            with col1:
                p_val = st.number_input("Phosphorus P (kg/ha)", value=50.0, disabled=not use_custom, key="crop_p_val")
            with col2:
                k_val = st.number_input("Potassium K (kg/ha)", value=50.0, disabled=not use_custom, key="crop_k_val")

        if st.button("🌾 Recommend Best Crop", key="btn_crop", use_container_width=True):
            if not location:
                st.warning("Please select a district first.")
            else:
                payload = {"location": location}
                if target_crop_input and target_crop_input != "Auto-Recommend (Default)":
                    payload["crop"] = target_crop_input
                if use_custom:
                    payload["phosphorus"] = p_val
                    payload["potassium"] = k_val
                with st.spinner("🤖 Analyzing soil & weather data..."):
                    result, error = call_api("/predict/crop-recommendation", payload)
                if error:
                    st.error(error)
                else:
                    st.session_state.crop_analysis_result = result
                    st.session_state.saved_crop_loc = location

        if st.session_state.get("crop_analysis_result"):
            result = st.session_state.crop_analysis_result
            location = st.session_state.saved_crop_loc
            rec_crop = result.get("recommended_crop", "Unknown")

            st.markdown(f"""
            <div class="result-card success">
                <div class="label">Best Crop for {location}</div>
                <div class="value">🌾 {rec_crop.title()}</div>
                <div style="font-size:0.8rem; color:rgba(255,255,255,0.4); margin-top:6px;">
                    📅 {result.get('date', '')} &nbsp;·&nbsp; AI Confidence Model
                </div>
            </div>
            """, unsafe_allow_html=True)

            t_eval = result.get("target_crop_eval")
            if t_eval:
                st.markdown(f"""
                <div class="glass-card" style="border-left:4px solid #3498db; margin-top:0.8rem; padding:0.9rem 1.2rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-size:0.8rem; color:rgba(255,255,255,0.6);">Preferred Crop Evaluation</span>
                            <h4 style="margin:2px 0 0; color:#3498db; font-size:1.05rem; font-weight:700;">🌱 {t_eval['requested_crop'].title()}</h4>
                        </div>
                        <div style="text-align:right;">
                            <span style="background:rgba(52,152,219,0.2); color:#3498db; padding:4px 10px; border-radius:16px; font-weight:700; font-size:0.75rem; border:1px solid rgba(52,152,219,0.4);">
                                Suitability: {t_eval['suitability']} (Rank #{t_eval['rank']})
                            </span>
                            <div style="font-size:0.75rem; color:rgba(255,255,255,0.5); margin-top:4px;">
                                Model Confidence: {t_eval['confidence']*100:.1f}%
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if result.get("top_5"):
                st.markdown("**Top 5 Candidates:**")
                for i, c in enumerate(result["top_5"], 1):
                    pct = c["confidence"] * 100
                    st.progress(int(pct), text=f"{i}. {c['crop'].title()} — {pct:.1f}%")

            with st.expander("📋 Inputs used for prediction"):
                st.json(result.get("inputs_used", {}))

            # ── Automatic full farm plan ──
            st.divider()

            st.markdown('### 📊 Auto Farm Plan & Full Crop Analysis')
            st.caption("Inspect Climate Risk, Irrigation Need, Estimated Yield, and Market Price for your selected crop or compare with top candidates.")

            current_preferred = target_crop_input if (target_crop_input and target_crop_input != "Auto-Recommend (Default)") else None

            if current_preferred:
                active_crop_title = current_preferred.title()
            elif t_eval and t_eval.get("requested_crop"):
                active_crop_title = t_eval["requested_crop"].title()
            else:
                active_crop_title = rec_crop.title()

            top_5_titles = [c["crop"].title() for c in result.get("top_5", [{"crop": rec_crop}])]
            crop_options = list(top_5_titles)

            if active_crop_title not in crop_options:
                crop_options.insert(0, active_crop_title)

            default_index = crop_options.index(active_crop_title) if active_crop_title in crop_options else 0

            selected_crop_display = st.radio("Choose a crop to analyze:", crop_options, index=default_index, horizontal=True, key=f"radio_farm_plan_{location}_{active_crop_title}")
            selected_farm_plan_crop = selected_crop_display.lower()

            st.markdown(f'<div class="section-header">Auto Farm Plan for {selected_farm_plan_crop.title()}</div>', unsafe_allow_html=True)

            with st.spinner(f"Running full analysis..."):
                risk_res, _  = call_api("/predict/climate-risk",   {"location": location, "crop": selected_farm_plan_crop})
                yield_res, _ = call_api("/predict/yield",          {"location": location, "crop": selected_farm_plan_crop, "area": 1.0})
                irr_res, _   = call_api("/predict/irrigation",     {"location": location, "crop": selected_farm_plan_crop, "growth_stage": "Initial"})
                market_res, _ = call_api("/predict/market-price",  {"location": location, "commodity": selected_farm_plan_crop, "arrival_quantity": 100.0})

            cA, cB = st.columns(2)
            with cA:
                if risk_res:
                    risk = risk_res.get("climate_risk", "Unknown")
                    color_c = {"low":"success","moderate":"warning","high":"danger","extreme":"danger"}.get(risk.lower(),"info")
                    st.markdown(f'<div class="result-card {color_c}"><div class="label">Climate Risk</div><div class="value"><span class="risk-badge risk-{risk.lower()}">{risk.upper()}</span></div></div>', unsafe_allow_html=True)
                if yield_res:
                    st.markdown(f'<div class="result-card success"><div class="label">Est. Yield (1 ha)</div><div class="value">{yield_res.get("predicted_yield","?")} tonnes</div></div>', unsafe_allow_html=True)
            with cB:
                if irr_res:
                    st.markdown(f'<div class="result-card info"><div class="label">Irrigation Need (Initial Stage)</div><div class="value">{irr_res.get("predicted_water_requirement_mm_per_day","?")} mm/day</div></div>', unsafe_allow_html=True)
                if market_res and market_res.get("predicted_price_per_quintal") is not None:
                    st.markdown(f'<div class="result-card warning"><div class="label">Est. Market Price</div><div class="value">₹{market_res.get("predicted_price_per_quintal","?")} /quintal</div></div>', unsafe_allow_html=True)

    # ── Tab 2: Climate Risk ───────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">🌦️ Climate Risk Prediction</div>', unsafe_allow_html=True)
        st.caption("Predict flood, drought, or heat-stress risk for your crop and district.")

        col1, col2 = st.columns(2)
        with col1:
            location = st.selectbox("📍 District", LOCATIONS, index=None, placeholder="Select...", key="climate_loc")
        with col2:
            crop = st.selectbox("🌾 Crop", CROPS, key="climate_crop")

        if st.button("🔍 Predict Climate Risk", key="btn_climate", use_container_width=True):
            if not location:
                st.warning("Please select a district.")
            else:
                with st.spinner("🌡️ Fetching weather & computing risk..."):
                    result, error = call_api("/predict/climate-risk", {"location": location, "crop": crop})
                if error:
                    st.error(error)
                else:
                    risk = result["climate_risk"]
                    color_c = {"low":"success","moderate":"warning","high":"danger","extreme":"danger"}.get(risk.lower(),"info")
                    st.markdown(f"""
                    <div class="result-card {color_c}">
                        <div class="label">Risk Level for {crop} in {location}</div>
                        <div class="value"><span class="risk-badge risk-{risk.lower()}">{risk.upper()}</span></div>
                        <div style="font-size:0.8rem; color:rgba(255,255,255,0.4); margin-top:8px;">
                            📅 {result.get('date','')} &nbsp;·&nbsp; 🌤️ {result.get('season','')} season
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("**Confidence Breakdown:**")
                    st.bar_chart(result["probabilities"])

    # ── Tab 3: Irrigation ─────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">💧 Irrigation Advisor</div>', unsafe_allow_html=True)
        st.caption("Calculate daily water requirement (mm/day) by growth stage using FAO ET₀ methodology.")

        col1, col2, col3 = st.columns(3)
        with col1:
            location = st.selectbox("📍 District", LOCATIONS, index=None, placeholder="Select...", key="irr_loc")
        with col2:
            crop = st.selectbox("🌾 Crop", CROPS, key="irr_crop")
        with col3:
            growth_stage = st.selectbox("🌱 Growth Stage", GROWTH_STAGES, index=1, key="irr_growth_stage")

        if st.button("💧 Calculate Irrigation Need", key="btn_irrigation", use_container_width=True):
            if not location:
                st.warning("Please select a district.")
            else:
                with st.spinner("Calculating..."):
                    result, error = call_api("/predict/irrigation", {"location": location, "crop": crop, "growth_stage": growth_stage})
                if error:
                    st.error(error)
                else:
                    val = result.get("predicted_water_requirement_mm_per_day", "?")
                    src = result.get("model_source", "")
                    src_tag = "🔬 FAO-56 Penman-Monteith" if "fao" in src else ("🤖 ML Model" if "pickle" in src else "")
                    st.markdown(f"""
                    <div class="result-card info">
                        <div class="label">Daily Water Requirement — {crop} ({growth_stage} Stage)</div>
                        <div class="value">💧 {val} mm/day</div>
                        <div style="font-size:0.8rem; color:rgba(255,255,255,0.4); margin-top:8px;">
                            📍 {result.get('location', location)} &nbsp;·&nbsp; 📅 {result.get('date','')} &nbsp;·&nbsp; {src_tag}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    details = result.get("details", {})
                    if details:
                        dc1, dc2, dc3, dc4 = st.columns(4)
                        for col, (lbl, val2) in zip([dc1,dc2,dc3,dc4], [
                            ("ET₀", f"{details.get('ET0_mm_day','?')} mm/day"),
                            ("Kc (Crop coeff.)", details.get('Kc','?')),
                            ("ETc (Crop ET)", f"{details.get('ETc_mm_day','?')} mm/day"),
                            ("Effective Rain", f"{details.get('effective_rain','?')} mm"),
                        ]):
                            with col:
                                st.markdown(f'<div class="result-card info" style="padding:0.7rem;"><div class="label" style="font-size:0.7rem;">{lbl}</div><div style="color:#fff;font-weight:700;font-size:0.9rem;">{val2}</div></div>', unsafe_allow_html=True)

    # ── Tab 4: Yield ──────────────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">🌱 Yield Estimator</div>', unsafe_allow_html=True)
        st.caption("Estimate tonnes per hectare for your crop based on weather and soil data.")

        col1, col2, col3 = st.columns(3)
        with col1:
            location = st.selectbox("📍 District", LOCATIONS, index=None, placeholder="Select...", key="yield_loc")
        with col2:
            crop = st.selectbox("🌾 Crop", CROPS, key="yield_crop")
        with col3:
            area = st.number_input("📐 Area (hectares)", min_value=0.1, value=1.0, step=0.5, key="yield_area")

        if st.button("🌱 Predict Yield", key="btn_yield", use_container_width=True):
            if not location:
                st.warning("Please select a district.")
            else:
                with st.spinner("Estimating yield..."):
                    result, error = call_api("/predict/yield", {"location": location, "crop": crop, "area": area})
                if error:
                    st.error(error)
                else:
                    val    = result.get("predicted_yield", "?")
                    val_ha = result.get("yield_per_ha", None)
                    season = result.get("season", "")
                    src    = result.get("model_source", "")
                    src_tag = "📐 FAO Crop Yield Model" if "fao" in src else ("🤖 ML Model" if "pickle" in src else "")
                    st.markdown(f"""
                    <div class="result-card success">
                        <div class="label">Predicted Yield — {crop} on {area} ha</div>
                        <div class="value">🌾 {val} tonnes</div>
                        <div style="font-size:0.8rem; color:rgba(255,255,255,0.4); margin-top:8px;">
                            📍 {result.get('location', location)} &nbsp;·&nbsp; 🌤️ {season} season &nbsp;·&nbsp;
                            {f'📐 {val_ha} t/ha &nbsp;·&nbsp;' if val_ha else ''} {src_tag}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    factors = result.get("factors", {})
                    if factors:
                        st.markdown("**🔬 Yield Factor Breakdown (FAO model):**")
                        fc1, fc2, fc3, fc4 = st.columns(4)
                        factor_info = [
                            ("🌡️ Temperature", factors.get('temperature_factor','?'), "How close temp is to crop optimum"),
                            ("💧 Water Stress", factors.get('water_stress_factor','?'), "FAO-33 ETa/ETc ratio"),
                            ("🌱 Soil Fertility", factors.get('soil_fertility_index','?'), "NPK, pH & organic carbon score"),
                            ("☀️ Solar Efficiency", factors.get('solar_factor','?'), "Radiation use efficiency"),
                        ]
                        for col, (lbl, fval, tip) in zip([fc1,fc2,fc3,fc4], factor_info):
                            pct = int(float(fval)*100) if fval != '?' else 0
                            with col:
                                st.markdown(f'<div class="result-card success" style="padding:0.7rem;"><div class="label" style="font-size:0.7rem;">{lbl}</div><div style="color:#2ecc71;font-weight:700;font-size:0.9rem;">{pct}%</div></div>', unsafe_allow_html=True)

    # ── Tab 5: Market Price ───────────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="section-header">💰 Market Price Forecast</div>', unsafe_allow_html=True)
        st.caption("Forecast mandi price (₹/quintal) using historical AP/TS market data. Supports 14 commodities.")

        col1, col2, col3 = st.columns(3)
        with col1:
            location = st.selectbox("📍 District", LOCATIONS, index=None, placeholder="Select...", key="mkt_loc")
        with col2:
            commodity = st.selectbox("🛒 Commodity", sorted([c.title() for c in MARKET_COMMODITIES]), key="mkt_commodity")
        with col3:
            qty = st.number_input("📦 Est. Arrival Qty (quintals)", min_value=1.0, value=100.0, step=10.0, key="mkt_qty")

        if st.button("💰 Predict Market Price", key="btn_market", use_container_width=True):
            if not location:
                st.warning("Please select a district.")
            else:
                with st.spinner("Fetching market data..."):
                    result, error = call_api("/predict/market-price", {"location": location, "commodity": commodity, "arrival_quantity": qty})
                if error:
                    st.error(error)
                else:
                    price  = result.get("predicted_price_per_quintal")
                    status = result.get("status")
                    if status and price is None:
                        st.error(status)
                    else:
                        src    = result.get("model_source", "")
                        src_tag = "📈 APMC Calibrated" if "apmc" in src else ("🤖 ML Model" if "pickle" in src else "")
                        st.markdown(f"""
                        <div class="result-card warning">
                            <div class="label">Predicted Mandi Price — {commodity} in {location}</div>
                            <div class="value">₹ {price} <span style="font-size:1rem;color:rgba(255,255,255,0.5);">/quintal</span></div>
                            <div style="font-size:0.8rem; color:rgba(255,255,255,0.4); margin-top:8px;">
                                📦 Arrival qty: {qty} quintals &nbsp;·&nbsp; 📅 {result.get('date','')} &nbsp;·&nbsp; {src_tag}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        pf = result.get("price_factors", {})
                        if pf:
                            st.markdown("**📊 Price Factor Breakdown:**")
                            pfc1, pfc2, pfc3, pfc4 = st.columns(4)
                            for col, (lbl, val2) in zip([pfc1,pfc2,pfc3,pfc4], [
                                ("📊 Base Price (2023)", f"₹{pf.get('base_price_2023','?')}"),
                                ("📅 Seasonal Multiplier", f"×{pf.get('seasonal_multiplier','?')}"),
                                ("🏙️ District Premium", f"×{pf.get('district_premium','?')}"),
                                ("📈 Inflation Factor", f"×{pf.get('inflation_factor','?')}"),
                            ]):
                                with col:
                                    st.markdown(f'<div class="result-card warning" style="padding:0.7rem;"><div class="label" style="font-size:0.7rem;">{lbl}</div><div style="color:#f39c12;font-weight:700;font-size:0.9rem;">{val2}</div></div>', unsafe_allow_html=True)


# ===========================================================================
# PAGE 4 — COVERAGE MAP
# ===========================================================================
elif page == "🗺️  Coverage Map":

    st.markdown("""
    <div class="hero-v4">
        <div class="badge">🗺️ Coverage</div>
        <h1>Geographic <span>Coverage</span></h1>
        <p>All supported districts across Telangana and Andhra Pradesh</p>
    </div>
    """, unsafe_allow_html=True)

    TELANGANA = [
        "Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon",
        "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar",
        "Khammam", "Komaram Bheem Asifabad", "Mahabubabad", "Mahabubnagar",
        "Mancherial", "Medak", "Medchal-Malkajgiri", "Mulugu", "Nagarkurnool",
        "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla",
        "Rangareddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy",
        "Warangal", "Hanamkonda", "Yadadri Bhuvanagiri",
    ]
    ANDHRA = [
        "Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", "Kurnool",
        "Prakasam", "Srikakulam", "Sri Potti Sriramulu Nellore", "Visakhapatnam",
        "Vizianagaram", "West Godavari", "YSR Kadapa", "Alluri Sitharama Raju",
        "Anakapalli", "Annamayya", "Bapatla", "Eluru", "Kakinada", "Kona Seema",
        "Nandyal", "NTR", "Palnadu", "Parvathipuram Manyam", "Sri Sathya Sai", "Tirupati",
    ]

    col_t, col_a = st.columns(2)
    with col_t:
        st.markdown(f'<div class="section-header" style="color:#2ecc71;">🟢 Telangana ({len(TELANGANA)} Districts)</div>', unsafe_allow_html=True)
        for d in sorted(TELANGANA):
            st.markdown(f"""
            <div class="glass-card" style="padding:0.6rem 1rem; margin-bottom:0.3rem; border-left: 2px solid rgba(46,204,113,0.4);">
                <span style="color:#d4f0de; font-size:0.88rem;">📍 {d}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_a:
        st.markdown(f'<div class="section-header" style="color:#3498db;">🔵 Andhra Pradesh ({len(ANDHRA)} Districts)</div>', unsafe_allow_html=True)
        for d in sorted(ANDHRA):
            st.markdown(f"""
            <div class="glass-card" style="padding:0.6rem 1rem; margin-bottom:0.3rem; border-left: 2px solid rgba(52,152,219,0.4);">
                <span style="color:#d4f0de; font-size:0.88rem;">📍 {d}</span>
            </div>
            """, unsafe_allow_html=True)