"""
AgriPredict AI — Hero Landing Animation & Agriculture Ecosystem Visualization
"""
import time
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_hero_animation():
    """
    Renders a 3-6 second agriculture animation sequence communicating:
    🌱 Seed → ☀️ Sun → ☁️ Clouds → 🌧️ Rain → 💧 Soil Moisture → 🧠 AI Analysis → 5 AI Modules → 🚜 Smart Decision
    """
    if "hero_anim_played" not in st.session_state:
        st.session_state["hero_anim_played"] = True
        is_first_load = True
    else:
        is_first_load = False

    col_anim, col_info = st.columns([3, 2])

    with col_anim:
        # Create an animated Plotly figure representing the farm growth & AI sequence
        stages = [
            {"stage": "1. Seed & Soil", "height": 0.8, "sun": 2, "rain": 0, "ai": 10, "desc": "🌱 Seed planted in nutrient soil"},
            {"stage": "2. Sprout & Sun", "height": 2.5, "sun": 8, "rain": 1, "ai": 30, "desc": "☀️ Solar radiation fuels growth"},
            {"stage": "3. Clouds & Rain", "height": 4.8, "sun": 6, "rain": 8, "ai": 50, "desc": "🌧️ Rainfall & moisture absorption"},
            {"stage": "4. Soil & Moisture", "height": 7.2, "sun": 7, "rain": 4, "ai": 75, "desc": "💧 Moisture & nutrient integration"},
            {"stage": "5. AI Intelligence", "height": 9.8, "sun": 10, "rain": 5, "ai": 100, "desc": "🧠 AI Model active on 5 Modules"},
        ]

        df_anim = pd.DataFrame(stages)

        fig = go.Figure()

        # Add trace for plant growth bar
        fig.add_trace(go.Bar(
            x=df_anim["stage"],
            y=df_anim["height"],
            name="Crop Growth (m)",
            marker=dict(color=df_anim["height"], colorscale="Greens", showscale=False)
        ))

        # Add line trace for AI Intelligence Index
        fig.add_trace(go.Scatter(
            x=df_anim["stage"],
            y=df_anim["ai"] / 10,
            mode="lines+markers+text",
            name="AI Intelligence Level",
            text=[f"{v}%" for v in df_anim["ai"]],
            textposition="top center",
            line=dict(color="#2ecc71", width=3, dash="dot"),
            marker=dict(size=10, color="#a8e063")
        ))

        fig.update_layout(
            title="🌾 Agricultural Growth & AI Intelligence Flow",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,30,15,0.4)",
            height=320,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", y=1.1, x=0),
            yaxis=dict(title="Growth Index / AI Score", range=[0, 12]),
            xaxis=dict(tickangle=-15)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.subheader("🌾 AI-Powered Agriculture Intelligence")
        st.caption("Connecting 5 AI Prediction Engines into one seamless farming intelligence pipeline.")
        
        st.markdown("""
        * **🌦️ Climate Risk** — Flood, drought & heat stress detection
        * **🌾 Crop Recommendation** — NPK & soil suitability analysis
        * **🌱 Yield Forecast** — Tonnes per hectare harvest estimation
        * **💧 Irrigation Advisor** — FAO-56 daily water requirement
        * **💰 Market Price** — Mandi commodity price forecasting
        """)
        st.success("✨ **From Soil + Climate + Intelligence → Better Agricultural Decisions**")


def render_ecosystem_animation():
    """
    Renders an interactive Sankey ecosystem diagram illustrating the connected architecture:
    🌱 SOIL → 🌦️ CLIMATE → 🧠 AGRI AI → 🌾 CROP / 💧 WATER / 🌱 YIELD / 💰 MARKET → 🚜 BETTER FARMING
    """
    st.subheader("🌍 Agriculture Ecosystem Intelligence Flow")
    st.caption("Visualizing how soil, climate, and real-time parameters flow through the central AI engine into 5 agricultural decisions.")

    nodes = [
        "🌱 Soil Properties (NPK, pH)", "🌦️ Climate Data (Temp, Rain, ET₀)", "📍 Regional Location (AP & TS)",  # 0, 1, 2
        "🧠 AGRI-PREDICT AI ENGINE",                                                                               # 3
        "🌾 Crop Recommendation", "🌦️ Climate Risk Level", "🌱 Yield Forecast", "💧 Irrigation Requirement", "💰 Market Price Forecast", # 4, 5, 6, 7, 8
        "🚜 Better Farming Decisions"                                                                             # 9
    ]

    source = [0, 1, 2, 3, 3, 3, 3, 3, 4, 5, 6, 7, 8]
    target = [3, 3, 3, 4, 5, 6, 7, 8, 9, 9, 9, 9, 9]
    value  = [3, 4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

    node_colors = [
        "#27ae60", "#3498db", "#f39c12",
        "#2ecc71",
        "#a8e063", "#e74c3c", "#2ecc71", "#3498db", "#e67e22",
        "#2ecc71"
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="rgba(0,0,0,0.5)", width=0.5),
            label=nodes,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color="rgba(46, 204, 113, 0.25)"
        )
    )])

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,30,15,0.4)",
        height=340,
        margin=dict(l=15, r=15, t=20, b=20),
        font=dict(size=12, color="#d4f0de")
    )

    st.plotly_chart(fig, use_container_width=True)
