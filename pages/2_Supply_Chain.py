# =============================================================================
# pages/2_Supply_Chain.py — Supply Chain Stress Analysis
# ARDTF Pillar 2: Analytics & BI
# =============================================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from style import apply_style
from config import df_fuel_price, df_fuel, df_lpi
from charts import (
    fuel_vs_demand,          # Fig P
    lpi_compare,             # LPI comparison
    supply_chain_stress,     # Fig R
    supply_chain_stress_text
)

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Supply Chain | COMP6013",
    layout="wide",
    initial_sidebar_state="expanded",
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
    <span class="ph-pill">Pillar 2 — Analytics & BI</span>
    <h2>Supply Chain Stress Analysis</h2>
    <p>Fuel cost pressure · ICE demand sensitivity · logistics capability · supply-chain stress</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# KPI row
# -----------------------------------------------------------------------------
summary_text = supply_chain_stress_text(df_fuel_price, df_fuel, df_lpi)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Fuel Cost Lens", "Combined ICE", "Petrol + diesel")
c2.metric("Demand Lens", "ICE Demand", "Petrol + diesel")
c3.metric("Logistics Benchmark", "UK vs Myanmar", "World Bank LPI")
c4.metric("Stress Framework", "Composite Index", "Fuel + demand + logistics")

st.divider()

# =============================================================================
# SECTION 1 — Fuel Cost Pressure vs ICE Demand (Fig P)
# =============================================================================
st.markdown("### Fuel Cost Pressure and ICE Demand")
st.caption("Combined petrol and diesel pump prices are compared against combined petrol and diesel registration demand.")

st.plotly_chart(
    fuel_vs_demand(df_fuel_price, df_fuel),
    use_container_width=True
)

st.markdown(
    '<p class="source-note">Source: DESNZ_env0105_FuelPrice.xlsx + SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx</p>',
    unsafe_allow_html=True
)

st.divider()

# =============================================================================
# SECTION 2 — Logistics Capability Comparison
# =============================================================================
st.markdown("### Logistics Capability Comparison")
st.caption("World Bank LPI comparison across six supply-chain capability dimensions.")

col1, col2 = st.columns([1.1, 1])  # slight emphasis on chart

# -----------------------------------------------------------------------------
# LEFT — Chart
# -----------------------------------------------------------------------------
with col1:
    st.plotly_chart(
        lpi_compare(df_lpi),
        use_container_width=True
    )
    st.markdown(
        '<p class="source-note">Source: WorldBank_Int_LPI_from_2007_to_2023.xlsx</p>',
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# RIGHT — Textual Analysis
# -----------------------------------------------------------------------------
with col2:

    st.markdown("""
    <div class="findings-box" style="font-size:12px; line-height:1.6;"><p>
    <h2>(UK VS MYANMAR) Logistics Performance KPI</h2>
    • The UK shows a <strong>consistently stronger logistics capability</strong> than Myanmar across all LPI dimensions, indicating a more resilient supply-chain structure.<br>
    • In <strong>customs</strong> and <strong>international shipments</strong>, the UK achieves greater efficiency and reliability, reducing cross-border friction.<br>
    • The largest structural gap lies in <strong>infrastructure</strong>, where the UK benefits from more advanced transport and distribution systems.<br>
    • Higher performance in <strong>logistics quality</strong> and <strong>tracking</strong> reflects stronger operational control and real-time visibility.<br>
    • In <strong>timeliness</strong>, the UK maintains more predictable delivery performance, while Myanmar remains more exposed to delays.<br>
    • Overall, the gap highlights differences in <strong>infrastructure maturity, system integration, and logistics governance</strong>, directly affecting supply-chain resilience.
    </p></div>
    """, unsafe_allow_html=True)

st.divider()

# =============================================================================
# SECTION 3 — Composite Supply-Chain Stress
# =============================================================================
st.markdown("### Composite Supply-Chain Stress")
st.caption("A combined view of fuel cost pressure, ICE demand weakness, and logistics capability.")

st.plotly_chart(
    supply_chain_stress(df_fuel_price, df_fuel, df_lpi),
    use_container_width=True
)

st.markdown(
    '<p class="source-note">Source: DESNZ_env0105_FuelPrice.xlsx + SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx + WorldBank_Int_LPI_from_2007_to_2023.xlsx</p>',
    unsafe_allow_html=True
)

st.markdown("### Supply-Chain Interpretation")
st.markdown(f"""
<div class="findings-box"><p>
{summary_text}
</p></div>
""", unsafe_allow_html=True)

st.divider()

# =============================================================================
# DATA VIEW
# =============================================================================
with st.expander("📋 View raw datasets"):
    tab1, tab2, tab3 = st.tabs(["Fuel Price", "Fuel Registrations", "LPI"])
    with tab1:
        st.dataframe(df_fuel_price, use_container_width=True)
    with tab2:
        st.dataframe(df_fuel, use_container_width=True)
    with tab3:
        st.dataframe(df_lpi, use_container_width=True)

# =============================================================================
# KEY FINDINGS
# =============================================================================
st.markdown("### Key Findings")

st.markdown("""
<div class="findings-box"><p>
• Fuel price dynamics exhibit a <strong>consistent inverse relationship</strong> with automotive demand, indicating that rising operating costs directly suppress vehicle purchasing activity.<br>
• The most significant disruption occurred during the <strong>2022 energy crisis</strong>, where peak fuel prices coincided with a clear contraction in ICE registration demand.<br>
• The use of a <strong>combined fuel price indicator</strong> alongside ICE demand provides a more realistic view of cost pressure across the internal combustion vehicle market.<br>
• The UK demonstrates a <strong>structurally stronger logistics capability</strong> than Myanmar across all World Bank LPI dimensions, particularly in infrastructure, tracking, and timeliness.<br>
• Integrating fuel cost pressure, demand sensitivity, and logistics performance into a <strong>composite supply-chain stress framework</strong> supports stronger operational monitoring and earlier risk detection.<br>
• These results reinforce the importance of <strong>data-driven forecasting, scenario analysis, and resilience planning</strong> as core capabilities under ARDTF Pillar 2.
</p></div>
""", unsafe_allow_html=True)