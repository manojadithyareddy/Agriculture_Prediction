"""
AgriPredict AI — Crop Yield Prediction Animation Component
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_yield_animation(predicted_yield: float, crop: str, area: float, factors: dict = None):
    """
    Renders crop yield prediction animations:
    1. Lifecycle yield accumulation curve (Seed → Plant → Growth → Harvest)
    2. Environmental Factor Breakdown Gauge (Temperature, Water Stress, Soil Fertility, Solar Efficiency)
    """
    st.subheader("🌱 Yield Potential & Environmental Factors")

    col_curve, col_factors = st.columns([1, 1])

    yield_per_ha = round(predicted_yield / max(0.1, area), 2)

    with col_curve:
        st.success(f"🌾 **Predicted Yield:** {predicted_yield} tonnes total ({yield_per_ha} tonnes/ha over {area} ha)")

        stages = ["Seed", "Vegetative", "Flowering", "Harvest"]
        # Cumulative yield potential accumulation over 100 days
        days = [0, 30, 65, 100]
        yield_acc = [0.0, round(yield_per_ha * 0.25, 2), round(yield_per_ha * 0.75, 2), yield_per_ha]

        fig_curve = go.Figure()
        fig_curve.add_trace(go.Scatter(
            x=days,
            y=yield_acc,
            mode="lines+markers+text",
            text=[f"{v} t/ha" for v in yield_acc],
            textposition="top left",
            line=dict(color="#2ecc71", width=3, shape="spline"),
            marker=dict(size=8, color="#a8e063"),
            fill="tozeroy",
            fillcolor="rgba(46, 204, 113, 0.15)"
        ))

        fig_curve.update_layout(
            title=f"📈 {crop.title()} Biomass & Yield Curve (1 ha)",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,30,15,0.4)",
            height=260,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(title="Days from Sowing", tickvals=days, ticktext=stages),
            yaxis=dict(title="Yield (Tonnes / ha)")
        )
        st.plotly_chart(fig_curve, use_container_width=True)

    with col_factors:
        st.markdown("### 🔬 Environmental Factor Analysis")

        if factors:
            temp_f = round(float(factors.get("temperature_factor", 0.9)) * 100, 1)
            water_f = round(float(factors.get("water_stress_factor", 0.85)) * 100, 1)
            soil_f = round(float(factors.get("soil_fertility_index", 0.92)) * 100, 1)
            solar_f = round(float(factors.get("solar_factor", 0.88)) * 100, 1)
        else:
            temp_f, water_f, soil_f, solar_f = 90.0, 85.0, 92.0, 88.0

        factor_names = ["🌡️ Temp Suitability", "💧 Water Availability", "🌱 Soil Fertility Index", "☀️ Solar Radiation Efficiency"]
        factor_scores = [temp_f, water_f, soil_f, solar_f]

        fig_factors = go.Figure(go.Bar(
            x=factor_scores,
            y=factor_names,
            orientation='h',
            text=[f"{s}%" for s in factor_scores],
            textposition='inside',
            marker=dict(
                color=factor_scores,
                colorscale="Greens",
                showscale=False
            )
        ))

        fig_factors.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,30,15,0.4)",
            height=260,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(title="Factor Efficiency (%)", range=[0, 110]),
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_factors, use_container_width=True)
