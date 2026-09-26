"""
VoltRelay Energy - Time-Series Demand & Peak Load Forecasting Engine
"""

import pandas as pd
import numpy as np

def forecast_network_demand(df_daily_swaps, horizon_days=30):
    """Generates a 30-day forecast of swap volume with confidence intervals."""
    daily_ts = df_daily_swaps.groupby('date')['total_swaps'].sum().reset_index()
    daily_ts['day_num'] = np.arange(len(daily_ts))
    
    # Fit linear trend + 7-day cyclical seasonality
    x = daily_ts['day_num'].values
    y = daily_ts['total_swaps'].values
    
    poly_fit = np.polyfit(x, y, deg=2)
    trend_fn = np.poly1d(poly_fit)
    
    # Day of week seasonal multipliers
    daily_ts['dow'] = daily_ts['date'].dt.dayofweek
    dow_multipliers = daily_ts.groupby('dow')['total_swaps'].mean() / daily_ts['total_swaps'].mean()
    
    last_date = daily_ts['date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon_days, freq='D')
    
    future_day_nums = np.arange(len(daily_ts), len(daily_ts) + horizon_days)
    base_trend = trend_fn(future_day_nums)
    future_dows = future_dates.dayofweek
    seasonality = [dow_multipliers.get(d, 1.0) for d in future_dows]
    
    forecast_vals = base_trend * np.array(seasonality)
    # Std error of residuals
    resids = y - trend_fn(x) * np.array([dow_multipliers.get(d, 1.0) for d in daily_ts['dow']])
    std_err = np.std(resids)
    
    df_forecast = pd.DataFrame({
        'date': future_dates,
        'forecast_swaps': np.round(forecast_vals).astype(int),
        'lower_ci_95': np.round(np.maximum(0, forecast_vals - 1.96 * std_err)).astype(int),
        'upper_ci_95': np.round(forecast_vals + 1.96 * std_err).astype(int)
    })
    
    return daily_ts, df_forecast

def compute_peak_hour_distribution(df_hourly_heatmap):
    """Calculates network hourly load and peak congestion curves."""
    hourly_agg = df_hourly_heatmap.groupby('hour').agg(
        total_swaps=('total_swaps', 'sum'),
        failed_swaps=('failed_swaps', 'sum'),
        avg_queue_sec=('avg_queue_sec', 'mean')
    ).reset_index()
    
    hourly_agg['failure_rate_pct'] = (hourly_agg['failed_swaps'] / hourly_agg['total_swaps'] * 100).round(2)
    hourly_agg['is_peak_window'] = hourly_agg['hour'].isin([8, 9, 10, 17, 18, 19, 20, 21])
    return hourly_agg
