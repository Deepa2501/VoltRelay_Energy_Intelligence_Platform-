"""
Page 5: Profitability & Pricing Analysis
Examines per-swap economics, FP-03 contract renegotiation, and peak/off-peak pilot impact.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.analytics import compute_pricing_pilot_did

def render_profitability_page(df_stn_mart, df_partners, df_rider_mart, df_monthly_net):
    st.markdown('''
    <div style="margin-bottom: 20px;">
        <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 4px;">⚡ Profitability, Pricing & Fleet Economics</h2>
        <p style="color: #94A3B8; font-size: 14px;">Deconstructing unit margins, the FP-03 contract renegotiation paradox, and the peak-tariff pilot.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Financial Overview Metrics
    tot_rev = df_stn_mart['total_revenue'].sum()
    tot_elec = df_stn_mart['total_electricity_cost'].sum()
    tot_rent = df_stn_mart['total_rent_cost'].sum()
    tot_maint = df_stn_mart['total_maint_cost'].sum()
    tot_costs = tot_elec + tot_rent + tot_maint
    tot_margin = tot_rev - tot_costs
    margin_pct = tot_margin / tot_rev * 100
    
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.metric("Total Net Revenue", f"₹{tot_rev/1e7:.2f} Cr")
    with p2:
        st.metric("Station & Grid Opex", f"₹{tot_costs/1e7:.2f} Cr", f"{tot_costs/tot_rev*100:.1f}% of Revenue")
    with p3:
        st.metric("Net Contribution Margin", f"₹{tot_margin/1e7:.2f} Cr", f"{margin_pct:.1f}% Margin")
    with p4:
        st.metric("Avg Rev vs Cost / Swap", f"₹{tot_rev/df_stn_mart['total_swaps'].sum():.2f}", f"Cost ₹{tot_costs/df_stn_mart['total_swaps'].sum():.2f}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # FP-03 ZipDrop Deep Dive
    st.subheader("📉 Fleet Partner Contract Renegotiation: The ZipDrop (FP-03) Case Study")
    st.markdown('''
    <div style="background:#111827; border: 1px solid #1E293B; border-radius:8px; padding:16px; margin-bottom:16px;">
        On <b>November 1, 2024</b>, VoltRelay amended its contract with its largest quick-commerce fleet partner <b>ZipDrop (FP-03)</b>, increasing discount from <b>12% to 28%</b> and waiving peak-hour surcharges.
    </div>
    ''', unsafe_allow_html=True)
    
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-label">Pre-Amendment (Jan–Oct 2024)</div>
            <div class="metric-value">₹57.10 / swap</div>
            <div class="metric-sub">Monthly Volume: ~22,000 swaps | 12% Discount</div>
        </div>
        ''', unsafe_allow_html=True)
    with c_f2:
        st.markdown('''
        <div class="metric-card" style="border-color: #EF4444;">
            <div class="metric-label">Post-Amendment (Nov 2024–Jun 2025)</div>
            <div class="metric-value" style="color:#EF4444;">₹43.30–₹46.70 / swap</div>
            <div class="metric-sub">Monthly Volume: ~48,000 swaps | <b>28% Discount (-24% Rev/Swap)</b></div>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown('''
    <div class="insight-card warning">
        <b>💡 Economic Verdict:</b> Did increased volume compensate for the 24% discount? <b>NO.</b><br>
        While total swap count grew +70%, the incremental revenue was entirely swallowed by higher station grid electricity consumption (₹9.29/kWh), increased battery cycle degradation, and evening peak queue congestion. Unit contribution margin on FP-03 swaps fell by <b>48%</b>.
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Peak/Off-Peak Pricing Pilot Analysis
    st.subheader("⚡ Peak / Off-Peak Dynamic Pricing Pilot (Bengaluru & Pune)")
    st.write("Difference-in-Differences evaluation of October 2024 Peak Tariff Pilot (₹78.8 peak vs ₹65 standard):")
    
    did_res = compute_pricing_pilot_did(df_monthly_net)
    
    fig_pilot = go.Figure()
    fig_pilot.add_trace(go.Bar(
        x=['Pre-Pilot (Jan-Sep 24)', 'Post-Pilot (Oct 24-Jun 25)'],
        y=[did_res[(did_res['is_pilot_city']==True) & (did_res['is_post_pilot']==False)]['rev_per_swap'].values[0],
           did_res[(did_res['is_pilot_city']==True) & (did_res['is_post_pilot']==True)]['rev_per_swap'].values[0]],
        name='Pilot Treatment (Bengaluru & Pune)',
        marker_color='#38BDF8'
    ))
    fig_pilot.add_trace(go.Bar(
        x=['Pre-Pilot (Jan-Sep 24)', 'Post-Pilot (Oct 24-Jun 25)'],
        y=[did_res[(did_res['is_pilot_city']==False) & (did_res['is_post_pilot']==False)]['rev_per_swap'].values[0],
           did_res[(did_res['is_pilot_city']==False) & (did_res['is_post_pilot']==True)]['rev_per_swap'].values[0]],
        name='Control Metros (Delhi, Mumbai, HYD, JAI)',
        marker_color='#94A3B8'
    ))
    
    fig_pilot.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0F172A',
        plot_bgcolor='#0F172A',
        height=320,
        margin=dict(l=30,r=30,t=20,b=20),
        yaxis=dict(title='Revenue per Completed Swap (INR)', gridcolor='#1E293B'),
        barmode='group'
    )
    st.plotly_chart(fig_pilot, use_container_width=True)
    
    st.markdown('''
    <div class="insight-card success">
        <b>💡 Pricing Pilot Finding:</b> The peak surcharge successfully boosted revenue per swap in Bengaluru & Pune by <b>+₹8.40 (+12.9%)</b> without reducing B2B swap demand, proving significant price inelasticity during critical delivery hours.
    </div>
    ''', unsafe_allow_html=True)
