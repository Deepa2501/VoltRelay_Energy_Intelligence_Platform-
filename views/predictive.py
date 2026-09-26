"""
Page 6: Predictive Intelligence & Recommendation Center
Demand forecasting, proactive risk scoring, and evidence-backed priority action plans.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.forecasting import forecast_network_demand, compute_peak_hour_distribution
from src.recommendations import get_actionable_recommendations

def render_predictive_page(df_daily_swaps, df_hourly_heatmap):
    st.markdown('''
    <div style="margin-bottom: 20px;">
        <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 4px;">⚡ Predictive Intelligence & Recommendation Center</h2>
        <p style="color: #94A3B8; font-size: 14px;">30-day network demand forecasts, peak load simulations, and prioritized executive action plans.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 30-Day Demand Forecast
    st.subheader("📈 30-Day Network Swap Demand Forecast (July 2025)")
    
    daily_hist, df_fc = forecast_network_demand(df_daily_swaps, horizon_days=30)
    
    fig_fc = go.Figure()
    # Historical
    fig_fc.add_trace(go.Scatter(
        x=daily_hist['date'].tail(90),
        y=daily_hist['total_swaps'].tail(90),
        name='Historical Daily Swaps (Last 90d)',
        line=dict(color='#38BDF8', width=2)
    ))
    # Forecast
    fig_fc.add_trace(go.Scatter(
        x=df_fc['date'],
        y=df_fc['forecast_swaps'],
        name='Forecasted Swaps',
        line=dict(color='#10B981', width=2.5, dash='dash')
    ))
    # Upper CI
    fig_fc.add_trace(go.Scatter(
        x=df_fc['date'],
        y=df_fc['upper_ci_95'],
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    # Lower CI
    fig_fc.add_trace(go.Scatter(
        x=df_fc['date'],
        y=df_fc['lower_ci_95'],
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(16, 185, 129, 0.15)',
        name='95% Confidence Interval'
    ))
    
    fig_fc.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0F172A',
        plot_bgcolor='#0F172A',
        height=360,
        margin=dict(l=30,r=30,t=20,b=20),
        yaxis=dict(title='Daily Swaps', gridcolor='#1E293B'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_fc, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Prioritized Actions Engine
    st.subheader("🎯 Executive Priority Action Plan (Evidence-Backed)")
    st.write("Concrete, quantified management interventions to resolve reliability, retention, and economics:")
    
    recs = get_actionable_recommendations()
    for r in recs:
        badge_cls = "badge-critical" if "P0" in r['Priority'] else ("badge-warning" if "P1" in r['Priority'] else "badge-info")
        with st.expander(f"{r['Priority']} | {r['Title']}", expanded=True if "P0" in r['Priority'] else False):
            st.markdown(f'''
            <div style="font-size:13.5px; line-height:1.6; color:#E2E8F0;">
                <p><b>🚨 Business Problem:</b> {r['Problem']}</p>
                <p><b>🔬 Empirical Data Evidence:</b> {r['Evidence']}</p>
                <p><b>🎯 Target Segment:</b> {r['Target Segment']}</p>
                <p><b>🛠️ Prescribed Action:</b> <span style="color:#38BDF8;">{r['Recommended Action']}</span></p>
                <div style="background:rgba(16, 185, 129, 0.1); border-left:4px solid #10B981; padding:10px 14px; border-radius:6px; margin-top:8px;">
                    <b>💰 Expected Business Impact:</b> <span style="color:#10B981; font-weight:700;">{r['Expected Impact']}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
