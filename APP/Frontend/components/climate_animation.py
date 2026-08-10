"""
AgriPredict AI — Climate Risk Animation Component
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_climate_animation(risk_level: str, weather_details: dict = None, risk_score: float = None, probabilities: dict = None):
    """
    Renders animated climate risk visualizations:
    1. Dynamic Risk Gauge Indicator (Score 0-100 & LOW / MODERATE / HIGH / EXTREME)
    2. Environmental Parameter Radar (Temp, Humidity, Rain, Wind, Cloud Cover, Solar Radiation)
    3. Weather Trend Timeline
    """
    st.subheader("🌦️ Environmental & Weather Intelligence")

    col_gauge, col_radar = st.columns([1, 1])

    risk_clean = (risk_level or "Low").lower()

    if risk_score is not None:
        gauge_score = float(risk_score)
    elif probabilities:
        low_p = float(probabilities.get("low", 0.7))
        mod_p = float(probabilities.get("moderate", 0.2))
        high_p = float(probabilities.get("high", 0.05))
        ext_p = float(probabilities.get("extreme", 0.05))
        gauge_score = round(low_p * 18.0 + mod_p * 48.0 + high_p * 76.0 + ext_p * 95.0, 1)
    else:
        risk_val_map = {"low": 22.5, "moderate": 52.0, "high": 76.5, "extreme": 92.0}
        gauge_score = risk_val_map.get(risk_clean, 25.0)

    risk_colors = {
        "low": "#2ecc71",
        "moderate": "#f39c12",
        "high": "#e74c3c",
        "extreme": "#c0392b"
    }
    active_color = risk_colors.get(risk_clean, "#2ecc71")

    with col_gauge:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gauge_score,
            number={'suffix': "/100", 'font': {'size': 26, 'color': active_color}},
            title={'text': f"Climate Risk: {risk_level.upper()}", 'font': {'size': 18, 'color': active_color}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': active_color},
                'bgcolor': "rgba(10,30,15,0.4)",
                'borderwidth': 2,
                'bordercolor': "rgba(46,204,113,0.3)",
                'steps': [
                    {'range': [0, 32], 'color': 'rgba(46, 204, 113, 0.2)'},
                    {'range': [32, 62], 'color': 'rgba(243, 156, 18, 0.2)'},
                    {'range': [62, 82], 'color': 'rgba(231, 76, 60, 0.2)'},
                    {'range': [82, 100], 'color': 'rgba(192, 57, 43, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': gauge_score
                }
            }
        ))

        fig_gauge.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=260,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_radar:
        categories = ['☀️ Temp (°C)', '💧 Humidity (%)', '🌧️ Rain (mm)', '💨 Wind (km/h)', '☁️ Cloud (%)', '☀️ Solar (MJ)']
        
        temp = float(weather_details.get("temperature", 30)) if weather_details else 30.0
        rh = float(weather_details.get("humidity", 65)) if weather_details else 65.0
        rain = float(weather_details.get("rainfall", 5)) if weather_details else 5.0
        wind = float(weather_details.get("wind_speed", 12)) if weather_details else 12.0
        cloud = float(weather_details.get("cloud_cover", 40)) if weather_details else 40.0
        solar = float(weather_details.get("solar_rad", 18)) if weather_details else 18.0

        norm_values = [
            min(100, (temp / 45) * 100),
            rh,
            min(100, (rain / 20) * 100),
            min(100, (wind / 40) * 100),
            cloud,
            min(100, (solar / 25) * 100)
        ]
        norm_values.append(norm_values[0])
        categories_radar = categories + [categories[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=norm_values,
            theta=categories_radar,
            fill='toself',
            name='Environmental Features',
            fillcolor='rgba(46, 204, 113, 0.25)',
            line=dict(color='#2ecc71', width=2)
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color="#a8e063"),
                bgcolor="rgba(10,30,15,0.4)"
            ),
            showlegend=False,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            height=260,
            margin=dict(l=30, r=30, t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.caption("📈 Weather Parameter Trend entering AI Model")
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
    df_trend = pd.DataFrame({
        "Day": days,
        "Temperature (°C)": [temp - 1.5, temp - 0.5, temp, temp + 1.0, temp + 0.5],
        "Rainfall (mm)": [rain * 0.8, rain * 1.2, rain, rain * 0.5, rain * 0.2],
        "Humidity (%)": [rh - 5, rh - 2, rh, rh + 3, rh + 1]
    })

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=df_trend["Day"], y=df_trend["Temperature (°C)"], name="☀️ Temp (°C)", line=dict(color="#f39c12", width=2)))
    fig_line.add_trace(go.Scatter(x=df_trend["Day"], y=df_trend["Rainfall (mm)"], name="🌧️ Rain (mm)", line=dict(color="#3498db", width=2)))
    fig_line.add_trace(go.Scatter(x=df_trend["Day"], y=df_trend["Humidity (%)"], name="💧 Humidity (%)", line=dict(color="#2ecc71", width=2)))

    fig_line.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,30,15,0.4)",
        height=220,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", y=1.1, x=0)
    )
    st.plotly_chart(fig_line, use_container_width=True)
