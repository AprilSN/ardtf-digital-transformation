# =============================================================================
# pages/6_Environment.py — Environmental Pressure & Emissions
# ARDTF Pillar 4: Change Management
# =============================================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from style import apply_style
from config import df_ghg, df_nox, df_fuel_price, df_vehicle_stock
from charts import (
    ghg_trend,
    nox_emissions,
    fuel_prices,
    nox_vs_vehicles
)

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Environment | COMP6013",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_style()  # Apply custom CSS styles

# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <svg viewBox="0 0 48 48" width="42" height="42" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="sg" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#4a7fa5"/>
              <stop offset="100%" style="stop-color:#e07b39"/>
            </linearGradient>
          </defs>
          <!-- Shield -->
          <path d="M24 3 L42 10 L42 26 C42 35 33 43 24 46 C15 43 6 35 6 26 L6 10 Z"
                fill="url(#sg)" opacity="0.92"/>
          <!-- Car body -->
          <rect x="12" y="25" width="24" height="9" rx="2" fill="#ffffff" opacity="0.95"/>
          <rect x="16" y="20" width="16" height="7" rx="2" fill="#ffffff" opacity="0.85"/>
          <!-- Wheels -->
          <circle cx="16" cy="34" r="3" fill="#1c2333"/>
          <circle cx="32" cy="34" r="3" fill="#1c2333"/>
          <!-- Chart bars -->
          <rect x="26" y="13" width="3" height="6" rx="1" fill="#ffffff" opacity="0.9"/>
          <rect x="31" y="10" width="3" height="9" rx="1" fill="#ffffff" opacity="0.9"/>
          <rect x="36" y="12" width="3" height="7" rx="1" fill="#ffffff" opacity="0.9"/>
          <!-- Chart line -->
          <polyline points="26,16 31,12 36,14" stroke="#e07b39" stroke-width="1.5"
                    fill="none" stroke-linecap="round"/>
        </svg>
        <div>
            <p class="logo-title">Automotive BI Dashboard</p>
            <p class="logo-sub">COMP6013 · Oxford Brookes University<br>April Soe Naing · 19384274</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p class='sidebar-section-label'>Navigation</p>", unsafe_allow_html=True)
    st.page_link("app.py", label="Home")
    st.page_link("pages/1_Market_Overview.py", label="Market Overview & EV Trends")
    st.page_link("pages/2_Supply_Chain.py", label="Supply Chain Stress Analysis")
    st.page_link("pages/3_Global_Markets.py", label="Global Market Comparisons")
    st.page_link("pages/4_Digital_Maturity.py", label="Digital Maturity")
    st.page_link("pages/5_Macroeconomic.py", label="Macroeconomic Context")
    st.page_link("pages/6_Environment.py", label="Environment & Emissions")
    st.divider()

    st.markdown("""
    <p class='sidebar-section-label'>Data Sources</p>
    """, unsafe_allow_html=True)
    for src in ["SMMT","Zapmap","DESNZ","Gov.UK: OZEV","QNA","ONS","S&P Global","World Bank","IEA","DfT", "NAEI"]:
        st.markdown(f'<span class="badge">{src}</span>', unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <p style="color:rgba(255,255,255,0.25); font-size:10px; text-align:center; margin:0;">
    Supervisor: Peter Marshall · 2026
    </p>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown("""
<div class="page-header">
    <span class="ph-pill">Pillar 4 — Change Management</span>
    <h2>Environment & Emissions</h2>
    <p>Transport emissions, fuel price pressure, and the relationship between pollution and vehicle growth</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# KPI row
# -----------------------------------------------------------------------------
ghg_latest = (df_ghg.iloc[-1][["cars", "vans", "hgv", "buses"]].sum())
nox_latest = (df_nox.iloc[-1][["cars", "vans", "hgv", "buses"]].sum())
nox_start = (df_nox.iloc[0][["cars", "vans", "hgv", "buses"]].sum())
nox_reduction = ((nox_latest - nox_start) / nox_start) * 100
vehicle_latest = df_vehicle_stock.iloc[-1]["total"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Latest Road GHG", f"{ghg_latest:.2f}", "MtCO2e")
c2.metric("Latest Road NOx", f"{nox_latest:.2f}", "ktNOx")
c3.metric("NOx Change", f"{nox_reduction:.0f}%", "From earliest year")
c4.metric("Vehicle Stock", f"{vehicle_latest:,.0f}", "Latest total")

st.divider()

# =============================================================================
# SECTION 1 — GHG and NOx
# =============================================================================
st.markdown("### Emissions by Vehicle Type")
st.caption("Greenhouse gas and NOx trends highlight the environmental burden of different transport segments.")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        ghg_trend(df_ghg),
        use_container_width=True
    )
    st.markdown(
        '<p class="source-note">Source: ONS_env0201_GHG.xlsx</p>',
        unsafe_allow_html=True
    )

with col2:
    st.plotly_chart(
        nox_emissions(df_nox),
        use_container_width=True
    )
    st.markdown(
        '<p class="source-note">Source: NAEI_env0301_NOX.xlsx</p>',
        unsafe_allow_html=True
    )

st.divider()

# =============================================================================
# SECTION 2 — Fuel Prices and Vehicle Stock Relationship
# =============================================================================
st.markdown("### Fuel Prices and NOx vs Vehicle Stock")
st.caption("Fuel cost pressure and the long-run divergence between emissions reduction and fleet growth.")

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        fuel_prices(df_fuel_price),
        use_container_width=True
    )
    st.markdown(
        '<p class="source-note">Source: DESNZ_env0105_FuelPrice.xlsx</p>',
        unsafe_allow_html=True
    )

with col4:
    st.plotly_chart(
        nox_vs_vehicles(df_nox, df_vehicle_stock),
        use_container_width=True
    )
    st.markdown(
        '<p class="source-note">Source: NAEI_env0301_NOX.xlsx + Dft_veh0101_LicensedStock.xlsx</p>',
        unsafe_allow_html=True
    )

st.divider()

# =============================================================================
# DATA VIEW
# =============================================================================
with st.expander("📋 View raw datasets"):
    tab1, tab2, tab3, tab4 = st.tabs(["GHG", "NOx", "Fuel Prices", "Vehicle Stock"])
    with tab1:
        st.dataframe(df_ghg, use_container_width=True)
    with tab2:
        st.dataframe(df_nox, use_container_width=True)
    with tab3:
        st.dataframe(df_fuel_price, use_container_width=True)
    with tab4:
        st.dataframe(df_vehicle_stock, use_container_width=True)

# =============================================================================
# KEY FINDINGS
# =============================================================================
st.markdown("### Key Findings")

st.markdown(f"""
<div class="findings-box"><p>
• Environmental pressure in road transport remains significant, with latest total GHG emissions at <strong>{ghg_latest:.2f} MtCO2e</strong> across cars, vans, HGVs, and buses.<br>
• Latest road NOx emissions stand at <strong>{nox_latest:.2f} ktNOx</strong>, but the longer-term trend shows a substantial reduction relative to the earliest observation period.<br>
• Total NOx has changed by <strong>{nox_reduction:.0f}%</strong> over the series, indicating that emissions performance and vehicle growth have not moved in the same direction.<br>
• The latest licensed vehicle stock remains high at <strong>{vehicle_latest:,.0f}</strong>, showing that environmental improvement has depended more on efficiency and regulatory change than on fleet contraction.<br>
• Fuel prices remain an important contextual pressure, reinforcing the case for transition toward cleaner technologies and more sustainable transport system design.
</p></div>
""", unsafe_allow_html=True)