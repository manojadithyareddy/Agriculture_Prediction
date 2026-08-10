"""
AgriPredict AI — Central AI Engine Processing Component
"""
import time
import streamlit as st

def render_ai_processing_animation(module_name: str = "AgriPredict AI", fast_mode: bool = False):
    """
    Renders the unified 6-step AI Engine processing sequence across all prediction modules.
    Communicates: INPUT DATA → ⚙️ AI ENGINE → PREDICTION → RECOMMENDATION
    """
    steps = [
        ("📥 Step 1/6", "Collecting Inputs..."),
        ("🔍 Step 2/6", "Validating Data & District Profile..."),
        ("⚙️ Step 3/6", "Preparing Features & FAO Constants..."),
        ("🧠 Step 4/6", "Running ML Model Inference..."),
        ("📊 Step 5/6", "Generating Prediction..."),
        ("✨ Step 6/6", f"Preparing Recommendation for {module_name}..."),
    ]

    status_container = st.empty()
    progress_bar = st.progress(0)

    delay = 0.04 if fast_mode else 0.12

    for idx, (label, text) in enumerate(steps, 1):
        pct = int((idx / len(steps)) * 100)
        progress_bar.progress(pct)
        status_container.info(f"**{label}** · {text}")
        time.sleep(delay)

    time.sleep(0.1)
    progress_bar.empty()
    status_container.empty()
