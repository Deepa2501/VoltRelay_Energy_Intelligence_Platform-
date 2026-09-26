"""
Page 2: Network & Service Reliability Analysis
Deep dive into failure modes, hourly heatmaps, station risk scoring, and root causes.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_reliability_page(df_daily_swaps, df_hourly_heatmap, df_stn_mart, df_telemetry):
    st.markdown('''
    <div style="margin-bottom: 20px;">
        <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 4px;">⚡ Network & Service Reliability</h2>
        <p style="color: #94A3B8; font-size: 14px;">Granular investigation of failure mechanisms, congestion bottlenecks, and station operational health.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Failure Mode Breakdown
    st.subheader("📊 Network Failure Mode Distribution (3.88M Swaps)")
    
    f1, f2, f3, f4, f5 = st.columns(5)
    total_swaps = df_daily_swaps['total_swaps'].sum()
    completed = df_daily_swaps['completed_swaps'].sum()
    no_bat = df_daily_swaps['failed_no_bat'].sum()
    abandoned = df_daily_swaps['abandoned_queue'].sum()
    cancelled = df_daily_swaps['cancelled_by_rider'].sum()
    sys_err = df_daily_swaps['failed_sys_error'].sum()
    
    with f1:
        st.metric("Completed Swaps", f"{completed:,}", f"{completed/total_swaps*100:.1f}%")
    with f2:
        st.metric("No Charged Battery", f"{no_bat:,}", f"{no_bat/total_swaps*100:.2f}% of total", delta_color="inverse")
    with f3:
        st.metric("Queue Abandoned", f"{abandoned:,}", f"{abandoned/total_swaps*100:.2f}%", delta_color="inverse")
    with f4:
        st.metric("Cancelled by Rider", f"{cancelled:,}", f"{cancelled/total_swaps*100:.2f}%", delta_color="inverse")
    with f5:
        st.metric("System / Tech Errors", f"{sys_err:,}", f"{sys_err/total_swaps*100:.2f}%", delta_color="inverse")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        st.subheader("🗺️ City-Level Failure Rate & Queue Time")
        city_perf = df_daily_swaps.groupby('city').agg(
            total_swaps=('total_swaps', 'sum'),
            failed_swaps=('failed_swaps', 'sum'),
            avg_queue=('sum_queue_wait_sec', lambda s: s.sum() / df_daily_swaps.loc[s.index, 'total_swaps'].sum())
        ).reset_index()
        city_perf['failure_rate_pct'] = (city_perf['failed_swaps'] / city_perf['total_swaps'] * 100).round(2)
        
        fig_city = px.bar(
            city_perf.sort_values(by='failure_rate_pct', ascending=True),
            x='failure_rate_pct',
            y='city',
            orientation='h',
            color='failure_rate_pct',
            color_continuous_scale=['#10B981', '#F59E0B', '#EF4444'],
            labels={'failure_rate_pct': 'Failure Rate %', 'city': 'Metro Market'},
            template='plotly_dark'
        )
        fig_city.update_layout(paper_bgcolor='#0F172A', plot_bgcolor='#0F172A', height=320, margin=dict(l=20,r=20,t=10,b=10))
        st.plotly_chart(fig_city, use_container_width=True)
        
    with col_r:
        st.subheader("🏢 Expansion Wave Comparison")
        wave_perf = df_stn_mart.groupby('expansion_wave').agg(
            stations=('station_id', 'count'),
            total_swaps=('total_swaps', 'sum'),
            failed_swaps=('failed_swaps', 'sum'),
            avg_queue=('avg_queue_sec', 'mean')
        ).reset_index()
        wave_perf['failure_rate'] = (wave_perf['failed_swaps'] / wave_perf['total_swaps'] * 100).round(2)
        
        fig_wave = px.pie(
            wave_perf,
            names='expansion_wave',
            values='total_swaps',
            color='expansion_wave',
            color_discrete_map={'Launch': '#38BDF8', 'Wave1_2024H2': '#818CF8', 'Wave2_2025H1': '#34D399'},
            hole=0.45,
            template='plotly_dark'
        )
        fig_wave.update_layout(paper_bgcolor='#0F172A', height=320, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_wave, use_container_width=True)

    # Hourly Heatmap
    st.subheader("🔥 24-Hour Network Failure Heatmap (Hour of Day vs Day of Week)")
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heat_pivot = df_hourly_heatmap.pivot_table(
        index='day_of_week', columns='hour', values='failure_rate_pct', aggfunc='mean'
    ).reindex(days_order)
    
    fig_heat = px.imshow(
        heat_pivot,
        color_continuous_scale='Inferno',
        labels=dict(x="Hour of Day (00:00 – 23:00)", y="Day of Week", color="Failure %"),
        template='plotly_dark'
    )
    fig_heat.update_layout(paper_bgcolor='#0F172A', plot_bgcolor='#0F172A', height=340, margin=dict(l=30,r=30,t=20,b=20))
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown('''
    <div class="insight-card danger">
        <b>💡 Operational Root Cause Insight:</b> Failure rates peak sharply between <b>17:00 and 21:00</b> across all weekdays (exceeding 8.5%), directly driven by delivery rider shift overlaps coinciding with empty battery replenishment lag.
    </div>
    ''', unsafe_allow_html=True)
    
    # Station Risk Table
    st.subheader("🚨 Station Operational Risk Table (152 Stations)")
    st.write("Stations categorized by composite operational risk (Failure Rate, Queue Congestion, Outages):")
    
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        tier_filter = st.multiselect("Filter Risk Tier", options=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'], default=['CRITICAL', 'HIGH'])
    with col_f2:
        search_stn = st.text_input("Search Station ID or City", "")
        
    filtered_stn = df_stn_mart.copy()
    if tier_filter:
        filtered_stn = filtered_stn[filtered_stn['risk_tier'].isin(tier_filter)]
    if search_stn:
        filtered_stn = filtered_stn[
            filtered_stn['station_id'].str.contains(search_stn, case=False) | 
            filtered_stn['city'].str.contains(search_stn, case=False)
        ]
        
    st.dataframe(
        filtered_stn[['station_id', 'city', 'expansion_wave', 'charger_generation', 'total_swaps', 'failure_rate_pct', 'avg_queue_sec', 'total_revenue', 'margin_pct', 'risk_tier']].sort_values(by='failure_rate_pct', ascending=False),
        column_config={
            'station_id': 'Station ID',
            'city': 'Metro City',
            'expansion_wave': 'Expansion Wave',
            'charger_generation': 'Charger Gen',
            'total_swaps': st.column_config.NumberColumn('Total Swaps', format="%d"),
            'failure_rate_pct': st.column_config.NumberColumn('Failure Rate', format="%.2f%%"),
            'avg_queue_sec': st.column_config.NumberColumn('Avg Queue', format="%d s"),
            'total_revenue': st.column_config.NumberColumn('Revenue (INR)', format="₹%d"),
            'margin_pct': st.column_config.NumberColumn('Margin %', format="%.1f%%"),
            'risk_tier': 'Risk Tier'
        },
        hide_index=True,
        use_container_width=True
    )
