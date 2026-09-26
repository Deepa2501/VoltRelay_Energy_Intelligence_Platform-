"""
Page 4: Battery Intelligence & Supplier Governance
Deconstructs battery lifecycle, SOH degradation, Kyron vendor failure, and asset risk.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_batteries_page(df_bat_mart):
    st.markdown('''
    <div style="margin-bottom: 20px;">
        <h2 style="font-weight: 800; color: #F8FAFC; margin-bottom: 4px;">⚡ Battery Intelligence & Supplier Governance</h2>
        <p style="color: #94A3B8; font-size: 14px;">Fleet-wide asset lifecycle analysis, SOH degradation curves, and supplier quality audits across 6,500 battery packs.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    total_packs = len(df_bat_mart)
    retired_packs = int(df_bat_mart['is_retired'].sum())
    active_packs = total_packs - retired_packs
    mean_soh = df_bat_mart['current_soh_pct'].mean()
    
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.metric("Total Battery Fleet", f"{total_packs:,}")
    with b2:
        st.metric("Active Packs in Field", f"{active_packs:,}", f"{active_packs/total_packs*100:.1f}% Healthy")
    with b3:
        st.metric("Premature Retirements", f"{retired_packs:,}", f"{retired_packs/total_packs*100:.1f}% Fleet Loss", delta_color="inverse")
    with b4:
        st.metric("Fleet Average SOH", f"{mean_soh:.1f}%", "-18.2% vs initial")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Supplier Comparison Deep-Dive
    st.subheader("🔬 Supplier Performance Audit: Cellora vs Amptek vs Kyron")
    
    sup_summary = df_bat_mart.groupby('supplier').agg(
        total_packs=('battery_id', 'count'),
        retired_packs=('is_retired', 'sum'),
        mean_initial_soh=('initial_soh_pct', 'mean'),
        mean_current_soh=('current_soh_pct', 'mean'),
        min_current_soh=('current_soh_pct', 'min'),
        total_swaps=('total_swaps_performed', 'sum'),
        total_capex=('purchase_cost_inr', 'sum')
    ).reset_index()
    
    sup_summary['retirement_rate_pct'] = (sup_summary['retired_packs'] / sup_summary['total_packs'] * 100).round(1)
    sup_summary['soh_loss_pct'] = (sup_summary['mean_initial_soh'] - sup_summary['mean_current_soh']).round(1)
    
    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        fig_soh = px.box(
            df_bat_mart,
            x='supplier',
            y='current_soh_pct',
            color='supplier',
            color_discrete_map={'Cellora': '#38BDF8', 'Amptek': '#10B981', 'Kyron': '#EF4444'},
            labels={'current_soh_pct': 'Current SOH %', 'supplier': 'Supplier'},
            template='plotly_dark'
        )
        fig_soh.update_layout(paper_bgcolor='#0F172A', plot_bgcolor='#0F172A', height=340, margin=dict(l=20,r=20,t=10,b=10), showlegend=False)
        st.plotly_chart(fig_soh, use_container_width=True)
        
    with col_r:
        st.markdown('''
        <div style="background:#111827; border: 1px solid #EF4444; border-radius:10px; padding:18px; height:340px;">
            <div style="font-size:15px; font-weight:700; color:#EF4444; margin-bottom:8px;">⚠️ THE KYRON DEFECT SMOKING GUN</div>
            <div style="font-size:13px; color:#E2E8F0; line-height:1.6;">
                • <b>Kyron (1,638 packs):</b> 1,438 packs (<b>87.8%</b>) prematurely degraded and retired within 9 months. Average SOH collapsed to <b>63.7%</b>.<br><br>
                • <b>Cellora (3,555 packs):</b> <b>0</b> retirements, mean SOH <b>80.9%</b> across 24+ months of field operation.<br><br>
                • <b>Amptek (1,307 packs):</b> <b>0</b> retirements, mean SOH <b>81.0%</b>.<br><br>
                • <b>Root Cause:</b> Defective thermal dissipation and substandard cell balancing in Kyron lots CE-25xx causing rapid capacity fade under high ambient Indian summer charging.
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    # Supplier Scorecard Table
    st.subheader("📋 Supplier Fleet Scorecard")
    st.dataframe(
        sup_summary[['supplier', 'total_packs', 'retired_packs', 'retirement_rate_pct', 'mean_initial_soh', 'mean_current_soh', 'soh_loss_pct', 'total_capex']],
        column_config={
            'supplier': 'Supplier Name',
            'total_packs': st.column_config.NumberColumn('Total Fleet', format="%d"),
            'retired_packs': st.column_config.NumberColumn('Retired Packs', format="%d"),
            'retirement_rate_pct': st.column_config.NumberColumn('Retirement Rate', format="%.1f%%"),
            'mean_initial_soh': st.column_config.NumberColumn('Initial SOH', format="%.1f%%"),
            'mean_current_soh': st.column_config.NumberColumn('Current SOH', format="%.1f%%"),
            'soh_loss_pct': st.column_config.NumberColumn('Degradation Delta', format="%.1f%%"),
            'total_capex': st.column_config.NumberColumn('Total Capex (INR)', format="₹%d")
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Battery Risk Table
    st.subheader("🚨 High-Risk Battery Packs (Active Packs with SOH < 75%)")
    st.write("Active packs requiring immediate station recall and thermal inspection:")
    
    at_risk_bats = df_bat_mart[(df_bat_mart['is_retired'] == False) & (df_bat_mart['current_soh_pct'] < 75.0)]
    st.dataframe(
        at_risk_bats[['battery_id', 'supplier', 'manufacturing_lot', 'pack_type', 'commission_date', 'current_soh_pct', 'soh_degradation_pct', 'total_swaps_performed', 'failed_swaps_associated']].sort_values(by='current_soh_pct', ascending=True),
        column_config={
            'battery_id': 'Battery ID',
            'supplier': 'Supplier',
            'manufacturing_lot': 'Lot Code',
            'pack_type': 'Pack Type',
            'commission_date': 'Commissioned',
            'current_soh_pct': st.column_config.NumberColumn('Current SOH', format="%.1f%%"),
            'soh_degradation_pct': st.column_config.NumberColumn('Degradation', format="%.1f%%"),
            'total_swaps_performed': 'Total Swaps',
            'failed_swaps_associated': 'Associated Failures'
        },
        hide_index=True,
        use_container_width=True
    )
