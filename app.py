"""
VoltRelay Energy - Network Intelligence & Decision System
Main Streamlit Application Entry Point.
"""

import os
import streamlit as st
import pandas as pd
from src.data_loader import (
    load_stations, load_fleet_partners, load_city_context, load_batteries,
    load_riders, load_support_tickets, load_swaps_daily_station, load_swaps_hourly_heatmap,
    load_swaps_monthly_network, load_rider_mart, load_battery_mart, load_station_mart,
    load_telemetry_daily, filter_daily_swaps
)
from src.preprocessing import get_data_quality_report
from views.executive import render_executive_page
from views.reliability import render_reliability_page
from views.customers import render_customers_page
from views.batteries import render_batteries_page
from views.profitability import render_profitability_page
from views.predictive import render_predictive_page

# Page Configuration
st.set_page_config(
    page_title="VoltRelay Energy | Network Intelligence & Decision System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Datasets (Sub-second cached from Parquet)
with st.spinner("Initializing VoltRelay Analytical Engine..."):
    df_stations = load_stations()
    df_partners = load_fleet_partners()
    df_city_ctx = load_city_context()
    df_batteries = load_batteries()
    df_riders = load_riders()
    df_tickets = load_support_tickets()
    df_daily_swaps = load_swaps_daily_station()
    df_hourly_heatmap = load_swaps_hourly_heatmap()
    df_monthly_net = load_swaps_monthly_network()
    df_rider_mart = load_rider_mart()
    df_bat_mart = load_battery_mart()
    df_stn_mart = load_station_mart()
    df_telemetry = load_telemetry_daily()

# Sidebar Header & Navigation
st.sidebar.markdown('''
<div style="text-align: left; padding: 10px 0 16px 0;">
    <div style="font-size: 20px; font-weight: 800; color: #38BDF8; letter-spacing: -0.5px;">⚡ VOLTRELAY ENERGY</div>
    <div style="font-size: 11.5px; color: #94A3B8;">NETWORK INTELLIGENCE & DECISION SYSTEM</div>
</div>
''', unsafe_allow_html=True)

page_selection = st.sidebar.radio(
    "Navigation Menu",
    [
        "1. Executive Decision Center",
        "2. Network & Service Reliability",
        "3. Customer & Rider Intelligence",
        "4. Battery Intelligence & Quality",
        "5. Profitability & Pricing Economics",
        "6. Predictive & Priority Actions"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Global Filter Matrix")

# Global Interactive Filters
all_cities = sorted(df_stations['city'].unique().tolist())
selected_cities = st.sidebar.multiselect("Metro Cities", options=all_cities, default=all_cities)

all_waves = sorted(df_stations['expansion_wave'].unique().tolist())
selected_waves = st.sidebar.multiselect("Expansion Waves", options=all_waves, default=all_waves)

# Date Range Filter
min_dt = df_daily_swaps['date'].min().date()
max_dt = df_daily_swaps['date'].max().date()
date_range = st.sidebar.date_input("Date Window", value=(min_dt, max_dt), min_value=min_dt, max_value=max_dt)

# Filter Data
filtered_daily_swaps = filter_daily_swaps(df_daily_swaps, selected_cities, selected_waves, date_range)
filtered_stn_mart = df_stn_mart[df_stn_mart['city'].isin(selected_cities) & df_stn_mart['expansion_wave'].isin(selected_waves)]

st.sidebar.markdown("---")
with st.sidebar.expander("📋 Data Quality Audit", expanded=False):
    st.write("Dataset Verification & Cleaning Summary:")
    dq_df = get_data_quality_report()
    st.dataframe(dq_df[['Dataset', 'Rows', 'Completeness']], hide_index=True)

st.sidebar.caption("VoltRelay OS v2.4 • 3.88M Records Processed")

# Route Page Rendering
if "1. Executive" in page_selection:
    render_executive_page(filtered_daily_swaps, df_rider_mart, filtered_stn_mart, df_bat_mart, df_partners, df_monthly_net)
elif "2. Network" in page_selection:
    render_reliability_page(filtered_daily_swaps, df_hourly_heatmap, filtered_stn_mart, df_telemetry)
elif "3. Customer" in page_selection:
    render_customers_page(df_rider_mart, df_tickets)
elif "4. Battery" in page_selection:
    render_batteries_page(df_bat_mart)
elif "5. Profitability" in page_selection:
    render_profitability_page(filtered_stn_mart, df_partners, df_rider_mart, df_monthly_net)
elif "6. Predictive" in page_selection:
    render_predictive_page(filtered_daily_swaps, df_hourly_heatmap)
