"""
AgriPredict AI — Irrigation Prediction Animation Component
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_irrigation_animation(water_req_mm: float, crop: str, stage: str, details: dict = None):
    """
    Renders smart irrigation animations:
    1. Water droplet requirement indicator (LOW 💧 / MODERATE 💧💧 / HIGH 💧💧💧)
    2. FAO-56 Evapotranspiration & Water Requirement Curve (ET₀ vs ETc)
    """
    st.subheader("💧 Smart Irrigation & Crop Water Requirements")

    col_req, col_fao = st.columns([1, 1])

    # Categorize water requirement state
    if water_req_mm < 3.0:
        water_state = "LOW WATER REQUIRED"
        water_icon = "💧"
        state_color = "#2ecc71"
    elif water_req_mm < 6.0:
        water_state = "MODERATE WATER REQUIRED"
        water_icon = "💧💧"
        state_color = "#f39c12"
    else:
        water_state = "HIGH WATER REQUIRED"
        water_icon = "💧💧💧"
        state_color = "#e74c3c"

    with col_req:
        st.info(f"### {water_icon} **{water_state}**")
        st.markdown(f"#### **Recommended Irrigation:** `{water_req_mm} mm/day` for **{crop.title()}** ({stage} stage)")

        # Animated water requirement gauge
        fig_water = go.Figure(go.Indicator(
            mode="gauge+number",
            value=water_req_mm,
            title={'text': "Daily Water Req (mm/day)", 'font': {'size': 16, 'color': state_color}},
            gauge={
                'axis': {'range': [0, 12], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': state_color},
                'bgcolor': "rgba(10,30,15,0.4)",
                'borderwidth': 2,
                'bordercolor': "rgba(52,152,219,0.3)",
                'steps': [
                    {'range': [0, 3.0], 'color': 'rgba(46, 204, 113, 0.2)'},
                    {'range': [3.0, 6.0], 'color': 'rgba(243, 156, 18, 0.2)'},
                    {'range': [6.0, 12.0], 'color': 'rgba(231, 76, 60, 0.2)'}
                ]
            }
        ))

        fig_water.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=240,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_water, use_container_width=True)

    with col_fao:
        st.markdown("### 📊 FAO-56 Water Balance Breakdown")

        et0 = float(details.get("ET0_mm_day", 5.0)) if details else 5.0
        kc = float(details.get("Kc", 1.05)) if details else 1.05
        etc = float(details.get("ETc_mm_day", water_req_mm)) if details else water_req_mm
        eff_rain = float(details.get("effective_rain", 0.0)) if details else 0.0

        metrics = ["Ref Evapotranspiration (ET₀)", "Crop Coeff (Kc × 10)", "Crop Water Requirement (ETc)", "Net Irrigation Needed"]
        vals = [et0, kc * 10, etc, water_req_mm]

        fig_fao = go.Figure(go.Bar(
            x=vals,
            y=metrics,
            orientation='h',
            text=[f"{v:.2f}" for v in vals],
            textposition='inside',
            marker=dict(
                color=["#3498db", "#2ecc71", "#e67e22", "#9b59b6"],
                showscale=False
            )
        ))

        fig_fao.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,30,15,0.4)",
            height=240,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(title="Water Quantity (mm/day / Index)"),
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_fao, use_container_width=True)
