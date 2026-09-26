"""
VoltRelay Energy - Data Loader & Memory-Mapped Caching
Provides ultra-fast, sub-second cached data access from parquet analytical marts.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CACHE_DIR = os.path.join(DATA_DIR, "cache")

@st.cache_data(show_spinner=False)
def load_stations():
    fpath = os.path.join(CACHE_DIR, "stations_clean.parquet")
    if os.path.exists(fpath):
        return pd.read_parquet(fpath)
    return pd.read_csv(os.path.join(DATA_DIR, "stations.csv"))

@st.cache_data(show_spinner=False)
def load_fleet_partners():
    fpath = os.path.join(CACHE_DIR, "fleet_partners_clean.parquet")
    if os.path.exists(fpath):
        return pd.read_parquet(fpath)
    return pd.read_csv(os.path.join(DATA_DIR, "fleet_partners.csv"))

@st.cache_data(show_spinner=False)
def load_city_context():
    fpath = os.path.join(CACHE_DIR, "city_daily_context_clean.parquet")
    if os.path.exists(fpath):
        return pd.read_parquet(fpath)
    return pd.read_csv(os.path.join(DATA_DIR, "city_daily_context.csv"))

@st.cache_data(show_spinner=False)
def load_batteries():
    fpath = os.path.join(CACHE_DIR, "batteries_clean.parquet")
    if os.path.exists(fpath):
        return pd.read_parquet(fpath)
    return pd.read_csv(os.path.join(DATA_DIR, "batteries.csv"))

@st.cache_data(show_spinner=False)
def load_riders():
    fpath = os.path.join(CACHE_DIR, "riders_clean.parquet")
    if os.path.exists(fpath):
        return pd.read_parquet(fpath)
    return pd.read_csv(os.path.join(DATA_DIR, "riders.csv"))

@st.cache_data(show_spinner=False)
def load_support_tickets():
    fpath = os.path.join(CACHE_DIR, "support_tickets_clean.parquet")
    if os.path.exists(fpath):
        return pd.read_parquet(fpath)
    return pd.read_csv(os.path.join(DATA_DIR, "support_tickets.csv"))

@st.cache_data(show_spinner=False)
def load_swaps_daily_station():
    fpath = os.path.join(CACHE_DIR, "swaps_daily_station.parquet")
    return pd.read_parquet(fpath)

@st.cache_data(show_spinner=False)
def load_swaps_hourly_heatmap():
    fpath = os.path.join(CACHE_DIR, "swaps_hourly_heatmap.parquet")
    return pd.read_parquet(fpath)

@st.cache_data(show_spinner=False)
def load_swaps_monthly_network():
    fpath = os.path.join(CACHE_DIR, "swaps_monthly_network.parquet")
    return pd.read_parquet(fpath)

@st.cache_data(show_spinner=False)
def load_rider_mart():
    fpath = os.path.join(CACHE_DIR, "rider_analytics_mart.parquet")
    return pd.read_parquet(fpath)

@st.cache_data(show_spinner=False)
def load_battery_mart():
    fpath = os.path.join(CACHE_DIR, "battery_analytics_mart.parquet")
    return pd.read_parquet(fpath)

@st.cache_data(show_spinner=False)
def load_station_mart():
    fpath = os.path.join(CACHE_DIR, "station_analytics_mart.parquet")
    return pd.read_parquet(fpath)

@st.cache_data(show_spinner=False)
def load_telemetry_daily():
    fpath = os.path.join(CACHE_DIR, "station_daily_telemetry.parquet")
    if os.path.exists(fpath):
        return pd.read_parquet(fpath)
    return None

def filter_daily_swaps(df_daily, selected_cities, selected_waves, date_range):
    df = df_daily.copy()
    if selected_cities and len(selected_cities) > 0:
        df = df[df['city'].isin(selected_cities)]
    if selected_waves and len(selected_waves) > 0:
        df = df[df['expansion_wave'].isin(selected_waves)]
    if date_range and len(date_range) == 2:
        df = df[(df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))]
    return df
