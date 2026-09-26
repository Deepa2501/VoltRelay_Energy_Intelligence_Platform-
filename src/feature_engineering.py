"""
VoltRelay Energy - Feature Engineering & Unit Economics
"""

import pandas as pd
import numpy as np

def compute_station_features(df_stn_mart):
    df = df_stn_mart.copy()
    # Capacity pressure: swaps per slot per day
    df['total_slots'] = df['slots_2w'] + df['slots_3w']
    df['swaps_per_slot_day'] = df['total_swaps'] / (df['active_days'] * df['total_slots']).replace(0, np.nan)
    return df

def compute_rider_features(df_rider_mart):
    df = df_rider_mart.copy()
    # Early failure hazard
    df['early_failure_flag'] = (df['first_3_failures'] >= 1).astype(int)
    # Swap frequency (swaps per active tenure week)
    df['tenure_weeks'] = np.maximum(1.0, df['tenure_days'] / 7.0)
    df['swaps_per_week'] = df['total_swaps'] / df['tenure_weeks']
    return df

def compute_battery_lifecycle_features(df_bat_mart):
    df = df_bat_mart.copy()
    df['degradation_per_swap'] = (df['soh_degradation_pct'] / df['total_swaps_performed'].replace(0, np.nan)).fillna(0)
    df['is_premature_death'] = (df['is_retired'] & (df['current_soh_pct'] < 70.0)).astype(int)
    return df
