# =============================================================================
# pages/1_Market_Overview.py — Auto Market Overview & EV Trends
# ARDTF Pillar 1: Operational Foundation
# =============================================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from style import apply_style
from config import df_fuel, df_sale, df_charging, df_prod
from charts import (
    fuel_mix,                 # Fig A
    bev_vs_diesel,            # Fig K
    sale_type_stacked,        # Fig D (stacked)
    sale_share_line,          # Fig D (share)
    charging_growth,          # Fig C
    vehicle_production        # Fig E
)

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Market Overview | COMP6013", 
    layout="wide", 
    initial_sidebar_state="expanded"
)
apply_style()  # Apply custom CSS styles

# -----------------------------------------------------------------------------
# Sidebar (Home Page design)
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
    <span class="ph-pill">Pillar 1 — Operational Foundation</span>
    <h2>Auto Market Overview & EV Trends</h2>
    <p>UK registrations · fuel transition · EV adoption · production & infrastructure</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# SECTION 1 — Fuel Transition (Fig A + K)
# =============================================================================
st.markdown("### Fuel Type Transition & Electrification Shift")
st.caption("Stacked composition and structural crossover from ICE to BEV.")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fuel_mix(df_fuel),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        bev_vs_diesel(df_fuel),
        use_container_width=True
    )

st.divider()

# =============================================================================
# SECTION 2 — Sales Structure (Fig D)
# =============================================================================
st.markdown("### Sales Channel Transformation")
st.caption("Shift from private demand to fleet-driven electrification.")

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        sale_type_stacked(df_sale),
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        sale_share_line(df_sale),
        use_container_width=True
    )

st.divider()

# =============================================================================
# SECTION 3 — Infrastructure + Production (Fig C + E)
# =============================================================================
st.markdown("### Infrastructure Growth & Industrial Output")
st.caption("Charging expansion supports EV adoption; production reflects structural adjustment.")

col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(
        charging_growth(df_charging),
        use_container_width=True
    )

with col6:
    st.plotly_chart(
        vehicle_production(df_prod),
        use_container_width=True
    )

st.divider()

# =============================================================================
# DATA VIEW
# =============================================================================
with st.expander("📋 View raw datasets"):
    tab1, tab2 = st.tabs(["Fuel Data", "Sales Data"])
    with tab1:
        st.dataframe(df_fuel, use_container_width=True)
    with tab2:
        st.dataframe(df_sale, use_container_width=True)

# =============================================================================
# KEY INSIGHTS (High-quality academic tone)
# =============================================================================
st.markdown("### Key Findings")

st.markdown("""
<div class="findings-box"><p>
• The UK automotive market is undergoing a <strong>structural transition from internal combustion (ICE) to electrification</strong>, reshaping both demand composition and industry dynamics.<br>
• BEV market share increased significantly from <strong>6.6% in 2020 to 23.4% in 2025</strong>, overtaking diesel (5.1%) and confirming a decisive shift in fuel preference.<br>
• The <strong>diesel-to-BEV crossover</strong> marks a critical inflection point, indicating the irreversible decline of traditional fuel dominance in the UK market.<br>
• <strong>Fleet registrations surged by 41%</strong>, establishing fleet demand as the primary driver of new vehicle registrations, largely due to regulatory compliance and corporate electrification strategies.<br>
• This transition is strongly influenced by the <strong>UK Zero Emission Vehicle (ZEV) mandate</strong>, which is accelerating adoption through policy-driven market transformation.<br>
• Public EV charging infrastructure expanded rapidly, with growth exceeding <strong>200% between 2022 and 2026</strong>, supporting increased BEV adoption.<br>
• <strong>Rapid chargers (≥50kW)</strong> now account for approximately 20% of the network, reducing range anxiety and improving usability for long-distance travel.<br>
• Domestic vehicle production remains volatile, reflecting <strong>post-Brexit supply chain disruptions, global demand shifts, and industrial restructuring</strong> within the UK automotive sector.
</p></div>
""", unsafe_allow_html=True)