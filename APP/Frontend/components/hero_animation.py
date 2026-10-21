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
    Seed → Plant Growth → Sun → Clouds → Rain → Soil Moisture → AI Analysis → 5 AI Modules → Intelligence
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
            {"stage": "1. Soil & Seed", "plant_height": 0.5, "sun": 2, "rain": 0, "ai_intensity": 10, "desc": "🌱 Seed planted in nutrient-rich soil"},
            {"stage": "2. Sprout & Sunlight", "plant_height": 2.2, "sun": 8, "rain": 1, "ai_intensity": 30, "desc": "☀️ Solar radiation fuels photosynthesis"},
            {"stage": "3. Growth & Rainfall", "plant_height": 4.5, "sun": 6, "rain": 7, "ai_intensity": 50, "desc": "🌧️ Moisture & humidity optimize growth"},
            {"stage": "4. Mature Crop & AI", "plant_height": 7.0, "sun": 9, "rain": 3, "ai_intensity": 85, "desc": "🧠 AI model analyzes 93 climate & soil features"},
            {"stage": "5. Smart Farm Decision", "plant_height": 9.5, "sun": 10, "rain": 5, "ai_intensity": 100, "desc": "🚜 AI-Powered Agriculture Intelligence Active"},
        ]

        df_anim = pd.DataFrame(stages)

        fig = go.Figure()

        # Add trace for plant growth bar
        fig.add_trace(go.Bar(
            x=df_anim["stage"],
            y=df_anim["plant_height"],
            name="Plant Growth (m)",
            marker=dict(color=df_anim["plant_height"], colorscale="Greens", showscale=False)
        ))

        # Add line trace for AI Intelligence Index
        fig.add_trace(go.Scatter(
            x=df_anim["stage"],
            y=df_anim["ai_intensity"] / 10,
            mode="lines+markers+text",
            name="AI Intelligence Level",
            text=[f"{v}%" for v in df_anim["ai_intensity"]],
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
        st.markdown("""
        <div style="background: rgba(10,35,18,0.7); border: 1px solid rgba(46,204,113,0.3); border-radius: 18px; padding: 1.2rem 1.4rem; height: 320px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <span style="background: rgba(46,204,113,0.2); color: #2ecc71; font-size: 0.75rem; padding: 3px 10px; border-radius: 12px; font-weight: 700;">
                    LIVE ECOSYSTEM INTEGRATION
                </span>
                <h3 style="color: #fff; font-size: 1.25rem; font-weight: 700; margin: 8px 0 4px;">
                    From Soil + Climate → Better Farming
                </h3>
                <p style="font-size: 0.85rem; color: rgba(200,240,210,0.7); margin-bottom: 10px;">
                    Connecting 5 AI Prediction Engines into one seamless intelligence pipeline.
                </p>
            </div>
            <div>
                <div style="font-size: 0.8rem; line-height: 1.6; color: #d4f0de;">
                    🔹 <b>Climate Risk</b> → Flood & drought detection<br/>
                    🔹 <b>Crop Recommendation</b> → NPK & soil suitability<br/>
                    🔹 <b>Yield Prediction</b> → Tonnes/ha harvest forecast<br/>
                    🔹 <b>Irrigation Advisor</b> → FAO-56 mm/day water req<br/>
                    🔹 <b>Market Price</b> → Mandi price forecasting
                </div>
                <div style="margin-top: 12px; font-weight: 700; color: #2ecc71; font-size: 0.85rem;">
                    ✨ AI-Powered Agriculture Intelligence
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_ecosystem_animation():
    """
    Renders an interactive Sankey ecosystem diagram illustrating the connected architecture:
    Soil + Climate → AI Engine → 5 Decision Outputs
    """
    st.markdown('<div class="section-header">🌍 Agriculture Ecosystem Intelligence Flow</div>', unsafe_allow_html=True)
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
