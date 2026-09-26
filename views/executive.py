"""
Page 1: Executive Decision Center
Provides leadership with a 30-second comprehensive diagnostic of network growth, reliability, retention, and economics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.analytics import compute_network_kpis, compute_period_comparison, compute_monthly_network_trends, compute_top_business_issues

def render_executive_page(df_daily_swaps, df_rider_mart, df_stn_mart, df_bat_mart, df_partners, df_monthly_net):
    st.markdown('''
    <div style="margin-bottom: 20px;">
        <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 4px;">⚡ Executive Decision Center</h2>
        <p style="color: #94A3B8; font-size: 14px;">Real-time network diagnostic across 3.88M swap events, 152 stations, and 6,500 battery assets (Jan 2024 – Jun 2025).</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Calculate KPIs
    kpis = compute_network_kpis(df_daily_swaps, df_rider_mart, df_stn_mart)
    
    # Row 1: KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Total Swap Volume</div>
            <div class="metric-value">{kpis['total_swaps']:,}</div>
            <div class="metric-sub"><span style="color:#10B981;">▲ 204%</span> vs Jan 2024 baseline</div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
        <div class="metric-card" style="border-color: rgba(239, 68, 68, 0.4);">
            <div class="metric-label">Service Failure Rate</div>
            <div class="metric-value" style="color:#EF4444;">{kpis['failure_rate']:.2f}%</div>
            <div class="metric-sub"><span style="color:#EF4444;">▲ +3.1 pts</span> peak failure rate</div>
        </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Gross Net Revenue</div>
            <div class="metric-value">₹{kpis['total_revenue']/1e7:.2f} Cr</div>
            <div class="metric-sub">Avg ₹{kpis['rev_per_swap']:.2f} / completed swap</div>
        </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Active / Churned Riders</div>
            <div class="metric-value">{kpis['active_riders']:,} <span style="font-size:14px;color:#94A3B8;">/ {kpis['total_riders'] - kpis['active_riders']:,}</span></div>
            <div class="metric-sub">Network Churn: <span style="color:#F59E0B;">{kpis['churn_rate']:.1f}%</span></div>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 30-Second Executive Summary Alert Banner
    st.markdown('''
    <div style="background: linear-gradient(90deg, rgba(239, 68, 68, 0.12) 0%, rgba(245, 158, 11, 0.08) 100%); border-left: 5px solid #EF4444; border-radius: 8px; padding: 16px 20px; margin-bottom: 24px;">
        <div style="font-weight: 700; font-size: 15px; color: #FCA5A5; margin-bottom: 6px;">
            ⚠️ EXECUTIVE SUMMARY: THE GROWTH-QUALITY PARADOX
        </div>
        <div style="color: #E2E8F0; font-size: 13.5px; line-height: 1.6;">
            While VoltRelay expanded swap volume by <b>3.0x</b> (from 110k to 336k swaps/month), per-swap profitability and reliability have deteriorated simultaneously due to three compounding operational shocks:
            <ul style="margin-top: 6px; margin-bottom: 0; padding-left: 20px;">
                <li><b>Battery Quality Collapse:</b> 87.8% (1,438 units) of Kyron battery packs commissioned in 2024H2 suffered premature catastrophic degradation (SOH 63.7%), causing 134k+ battery-unavailable failures.</li>
                <li><b>Fleet Contract Dilution:</b> FP-03 (ZipDrop) discount renegotiation (12% → 28% with peak surcharge waiver) caused net revenue/swap to drop from ₹57.1 to ₹43.3–₹46.7 (-24%).</li>
                <li><b>Station Bottlenecks:</b> Jaipur (7.16%) & Delhi NCR (6.83%) Launch stations bear excessive evening peak demand with queue times up to 32 minutes.</li>
            </ul>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 4-Pillar Network Health Matrix
    st.subheader("🎯 4-Pillar Network Health Diagnostic")
    h1, h2, h3, h4 = st.columns(4)
    with h1:
        st.markdown('''
        <div style="background:#111827; border: 1px solid #10B981; border-radius:8px; padding:14px;">
            <div style="font-size:12px; color:#10B981; font-weight:700;">1. GROWTH</div>
            <div style="font-size:18px; font-weight:800; color:#F8FAFC; margin:4px 0;">EXPANDING</div>
            <div style="font-size:12px; color:#94A3B8;">Swaps +204%, Stations 92 → 152. Strong top-line demand across all 6 metros.</div>
        </div>
        ''', unsafe_allow_html=True)
    with h2:
        st.markdown('''
        <div style="background:#111827; border: 1px solid #EF4444; border-radius:8px; padding:14px;">
            <div style="font-size:12px; color:#EF4444; font-weight:700;">2. RELIABILITY</div>
            <div style="font-size:18px; font-weight:800; color:#EF4444; margin:4px 0;">CRITICAL STRAIN</div>
            <div style="font-size:12px; color:#94A3B8;">Failure rate rose to ~9.0% peak. Average queue time tripled to >8 minutes in bottleneck hubs.</div>
        </div>
        ''', unsafe_allow_html=True)
    with h3:
        st.markdown('''
        <div style="background:#111827; border: 1px solid #F59E0B; border-radius:8px; padding:14px;">
            <div style="font-size:12px; color:#F59E0B; font-weight:700;">3. RETENTION</div>
            <div style="font-size:18px; font-weight:800; color:#F59E0B; margin:4px 0;">WEAKENING</div>
            <div style="font-size:12px; color:#94A3B8;">Cohort 30-day retention declined from 84% to 68% driven by early onboarding failure exposure.</div>
        </div>
        ''', unsafe_allow_html=True)
    with h4:
        st.markdown('''
        <div style="background:#111827; border: 1px solid #F59E0B; border-radius:8px; padding:14px;">
            <div style="font-size:12px; color:#F59E0B; font-weight:700;">4. UNIT ECONOMICS</div>
            <div style="font-size:18px; font-weight:800; color:#F59E0B; margin:4px 0;">COMPRESSION</div>
            <div style="font-size:12px; color:#94A3B8;">Effective discount rate expanded to 28% for largest partner; battery write-offs erode contribution.</div>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Monthly Trends Chart
    st.subheader("📈 Monthly Performance & Growth Trajectory (Jan 2024 – Jun 2025)")
    df_trends = compute_monthly_network_trends(df_monthly_net)
    
    fig = go.Figure()
    # Volume bars
    fig.add_trace(go.Bar(
        x=df_trends['month'],
        y=df_trends['completed_swaps'],
        name='Completed Swaps',
        marker_color='#38BDF8',
        opacity=0.85,
        yaxis='y'
    ))
    fig.add_trace(go.Bar(
        x=df_trends['month'],
        y=df_trends['failed_swaps'],
        name='Failed / Aborted Swaps',
        marker_color='#EF4444',
        opacity=0.85,
        yaxis='y'
    ))
    # Failure rate line
    fig.add_trace(go.Scatter(
        x=df_trends['month'],
        y=df_trends['failure_rate_pct'],
        name='Failure Rate %',
        mode='lines+markers',
        line=dict(color='#F59E0B', width=3),
        marker=dict(size=7),
        yaxis='y2'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0F172A',
        plot_bgcolor='#0F172A',
        height=380,
        margin=dict(l=40, r=40, t=30, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title='Swap Events', gridcolor='#1E293B'),
        yaxis2=dict(title='Failure Rate %', overlaying='y', side='right', range=[0, 12], gridcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Period-over-Period Performance Table
    st.subheader("📊 Network Evolution by Operational Era")
    df_era = compute_period_comparison(df_daily_swaps)
    st.dataframe(
        df_era[['period', 'total_swaps', 'completed_swaps', 'failed_swaps', 'failure_rate_pct', 'total_revenue', 'rev_per_completed_swap', 'avg_queue_sec', 'active_stations']],
        column_config={
            'period': 'Operational Era',
            'total_swaps': st.column_config.NumberColumn('Total Swaps', format="%d"),
            'completed_swaps': st.column_config.NumberColumn('Completed', format="%d"),
            'failed_swaps': st.column_config.NumberColumn('Failed', format="%d"),
            'failure_rate_pct': st.column_config.NumberColumn('Failure Rate %', format="%.2f%%"),
            'total_revenue': st.column_config.NumberColumn('Revenue (INR)', format="₹%d"),
            'rev_per_completed_swap': st.column_config.NumberColumn('Rev / Swap', format="₹%.2f"),
            'avg_queue_sec': st.column_config.NumberColumn('Avg Queue (sec)', format="%d s"),
            'active_stations': 'Stations'
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Top Business Issues Section
    st.subheader("🔍 Top 5 Quantified Business Issues")
    issues = compute_top_business_issues(df_bat_mart, df_rider_mart, df_stn_mart, df_partners)
    
    for idx, iss in enumerate(issues, 1):
        color_badge = "badge-critical" if "CRITICAL" in iss['Severity'] else ("badge-warning" if "HIGH" in iss['Severity'] else "badge-info")
        st.markdown(f'''
        <div style="background:#111827; border: 1px solid #1E293B; border-radius:10px; padding:16px 20px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div style="font-size:15px; font-weight:700; color:#F8FAFC;">#{idx}. {iss['Issue']}</div>
                <span class="{color_badge}">{iss['Severity']}</span>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:13px; color:#94A3B8;">
                <div><b>📍 Where:</b> {iss['Where']}</div>
                <div><b>⏱ When:</b> {iss['When']}</div>
                <div><b>📉 Magnitude:</b> <span style="color:#F1F5F9;">{iss['Magnitude']}</span></div>
                <div><b>💰 Financial Impact:</b> <span style="color:#38BDF8;">{iss['Financial Impact']}</span></div>
            </div>
            <div style="margin-top:8px; font-size:12.5px; color:#CBD5E1; background:rgba(15,23,42,0.6); padding:8px 12px; border-radius:6px;">
                <b>🔬 Evidence-Supported Driver:</b> {iss['Drivers']}
            </div>
        </div>
        ''', unsafe_allow_html=True)
