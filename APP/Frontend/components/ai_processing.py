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
        ("📥 Step 1/5", "Collecting agricultural & environmental inputs..."),
        ("🔍 Step 2/5", "Validating district climate & soil profile data..."),
        ("⚙️ Step 3/5", "Engineering model feature vectors & FAO constants..."),
        ("🧠 Step 4/5", "Running AI model prediction inference..."),
        ("✨ Step 5/5", f"Generating smart farming insights for {module_name}..."),
    ]

    status_container = st.empty()
    progress_bar = st.progress(0)

    delay = 0.05 if fast_mode else 0.15

    for idx, (label, text) in enumerate(steps, 1):
        pct = int((idx / len(steps)) * 100)
        progress_bar.progress(pct)
        status_container.markdown(f"""
        <div style="background: rgba(46, 204, 113, 0.1); border: 1px solid rgba(46, 204, 113, 0.3); border-radius: 12px; padding: 0.8rem 1.2rem; margin: 0.8rem 0; font-weight: 600; color: #a8e063; display: flex; align-items: center; justify-content: space-between;">
            <div><span style="color: #2ecc71; margin-right: 8px;">{label}</span> {text}</div>
            <div style="font-size: 0.85rem; color: #2ecc71;">{pct}%</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(delay)

    # Brief hold on 100% then clear progress bar
    time.sleep(0.1)
    progress_bar.empty()
    status_container.empty()
