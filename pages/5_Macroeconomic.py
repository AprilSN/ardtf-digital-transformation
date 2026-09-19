# =============================================================================
# pages/5_Macroeconomic.py — Macroeconomic Context
# ARDTF Pillar 4: Change Management
# =============================================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from style import apply_style
from config import df_gdp, df_cpih, df_insurance
from charts import (
    gdp_growth,
    inflation,
    insurance_index
)

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Macroeconomic | COMP6013",
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
    <h2>Macroeconomic Context</h2>
    <p>Growth, inflation, and cost pressures shaping automotive affordability and demand</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# KPI row
# -----------------------------------------------------------------------------
latest_gdp = df_gdp.iloc[-1]["gdp_qoq_avg"] if not df_gdp.empty else None
latest_cpih = df_cpih.iloc[-1]["cpih"] if not df_cpih.empty else None
latest_insurance = df_insurance.iloc[-1]["annual_avg"] if not df_insurance.empty else None

peak_cpih = df_cpih["cpih"].max() if not df_cpih.empty else None
peak_cpih_year = df_cpih.loc[df_cpih["cpih"].idxmax(), "year"] if not df_cpih.empty else None

c1, c2, c3, c4 = st.columns(4)
c1.metric("Latest GDP Growth", f"{latest_gdp:.2f}%", "Average annual growth")
c2.metric("Latest CPIH", f"{latest_cpih:.1f}%", "Inflation rate")
c3.metric("Peak CPIH", f"{peak_cpih:.1f}%", str(peak_cpih_year))
c4.metric("Insurance Index", f"{latest_insurance:.1f}", "Latest annual average")

st.divider()

# =============================================================================
# SECTION 1 — GDP and Inflation
# =============================================================================
st.markdown("### Growth and Inflation")
st.caption("Macroeconomic stability and price pressure shape affordability, planning, and market confidence.")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        gdp_growth(df_gdp),
        use_container_width=True
    )
    st.markdown(
        '<p class="source-note">Source: QNA_GDP.xlsx</p>',
        unsafe_allow_html=True
    )

with col2:
    st.plotly_chart(
        inflation(df_cpih),
        use_container_width=True
    )
    st.markdown(
        '<p class="source-note">Source: MM23_CPIH.xlsx</p>',
        unsafe_allow_html=True
    )

st.divider()

# =============================================================================
# SECTION 2 — Insurance Cost Pressure
# =============================================================================
st.markdown("### Insurance Cost Pressure")
st.caption("Rising insurance costs add a secondary affordability burden to household vehicle ownership.")

st.plotly_chart(
    insurance_index(df_insurance),
    use_container_width=True
)

st.markdown(
    '<p class="source-note">Source: ONS_CPI_Insurance.xlsx</p>',
    unsafe_allow_html=True
)

st.divider()

# =============================================================================
# DATA VIEW
# =============================================================================
with st.expander("📋 View raw datasets"):
    tab1, tab2, tab3 = st.tabs(["GDP", "CPIH", "Insurance"])
    with tab1:
        st.dataframe(df_gdp, use_container_width=True)
    with tab2:
        st.dataframe(df_cpih, use_container_width=True)
    with tab3:
        st.dataframe(df_insurance, use_container_width=True)

# =============================================================================
# KEY FINDINGS
# =============================================================================
st.markdown("### Key Findings")

st.markdown(f"""
<div class="findings-box"><p>
• The macroeconomic environment remains an important determinant of automotive retail performance, with <strong>growth, inflation, and ownership costs</strong> directly affecting affordability and confidence.<br>
• Latest GDP growth stands at <strong>{latest_gdp:.2f}%</strong>, indicating a relatively modest growth environment rather than a high-expansion recovery phase.<br>
• CPIH inflation peaked at <strong>{peak_cpih:.1f}% in {peak_cpih_year}</strong>, highlighting the scale of price pressure experienced during the recent inflation cycle.<br>
• Although inflation has eased, the latest CPIH reading of <strong>{latest_cpih:.1f}%</strong> still signals continued cost sensitivity across households and businesses.<br>
• Insurance costs also remain elevated, with the latest annual index at <strong>{latest_insurance:.1f}</strong>, reinforcing that vehicle affordability is influenced by a broader cost structure than purchase price alone.
</p></div>
""", unsafe_allow_html=True)
