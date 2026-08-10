"""
AgriPredict AI — Crop Recommendation Animation Component
"""
import time
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_crop_animation(recommended_crop: str, top_5_list: list = None):
    """
    Renders crop recommendation animation sequence:
    1. Input Flow: SOIL + WEATHER + SEASON → AI ANALYSIS → RECOMMENDED CROP
    2. Crop Growth Stages: Seed 🌱 → Sprout 🌿 → Plant 🪴 → Mature Crop 🌾
    3. Top Candidate Crop Compatibility bars
    """
    st.subheader("🌾 Crop Growth & AI Compatibility Sequence")

    col_growth, col_chart = st.columns([1, 1])

    with col_growth:
        st.markdown(f"### 🌾 Recommended Crop: **{recommended_crop.title()}**")

        # 4 Growth Stages visual representation
        stages = [
            ("1. Seed", "🌱", "Seed selected for soil profile", 25),
            ("2. Sprout", "🌿", "Germination & seedling stage", 50),
            ("3. Plant", "🪴", "Vegetative & flowering stage", 75),
            ("4. Mature Crop", "🌾", "Harvest-ready yield potential", 100)
        ]

        df_growth = pd.DataFrame(stages, columns=["Stage", "Icon", "Description", "Growth %"])

        fig_growth = go.Figure(go.Bar(
            x=[f"{s[1]} {s[0]}" for s in stages],
            y=[s[3] for s in stages],
            text=[s[2] for s in stages],
            textposition="auto",
            marker=dict(
                color=[s[3] for s in stages],
                colorscale="Greens",
                showscale=False
            )
        ))

        fig_growth.update_layout(
            title=f"🌱 {recommended_crop.title()} Growth Journey",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,30,15,0.4)",
            height=260,
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis=dict(title="Growth Stage Completion %", range=[0, 115])
        )
        st.plotly_chart(fig_growth, use_container_width=True)

    with col_chart:
        st.markdown("### 📊 Top 5 AI Crop Compatibility Scores")

        if top_5_list and len(top_5_list) > 0:
            crops = [item.get("crop", "").title() for item in top_5_list]
            confidences = [round(item.get("confidence", 0.0) * 100, 1) for item in top_5_list]

            # Horizontal bar chart for Top 5 crops
            fig_top5 = go.Figure(go.Bar(
                x=confidences,
                y=crops,
                orientation='h',
                text=[f"{c}%" for c in confidences],
                textposition='inside',
                marker=dict(
                    color=confidences,
                    colorscale="Viridis",
                    showscale=False
                )
            ))

            fig_top5.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(10,30,15,0.4)",
                height=260,
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis=dict(title="Compatibility Index (%)", range=[0, 105]),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_top5, use_container_width=True)
        else:
            st.info(f"Recommended Crop: **{recommended_crop.title()}** based on optimal NPK, pH, and climate metrics.")
