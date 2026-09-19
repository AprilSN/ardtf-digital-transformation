# =============================================================================
# pages/3_Global_Markets.py — Global Market Comparisons
# ARDTF Pillar 2: Analytics & BI
# =============================================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from style import apply_style
from config import df_global, df_iea
from charts import (
    global_sales,       # Global regional sales outlook
    ev_share_global     # EV adoption by country
)

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Global Markets | COMP6013",
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
    <span class="ph-pill">Pillar 2 — Analytics & BI</span>
    <h2>Global Market Comparisons</h2>
    <p>Regional sales outlook · EV adoption benchmarking · international market context</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# KPI row
# -----------------------------------------------------------------------------
global_2025 = round(df_global["s2025"].sum(), 1)

china_2025 = df_global.loc[df_global["region"] == "Greater China", "s2025"].iloc[0]
north_america_2025 = df_global.loc[df_global["region"] == "North America", "s2025"].iloc[0]
india_2032 = df_global.loc[df_global["region"] == "Indian Subcontinent", "s2032"].iloc[0]

iea_2024 = df_iea[df_iea["year"] == "2024"].iloc[0]
uk_2024 = iea_2024["UK"]
world_2024 = iea_2024["World"]
norway_2024 = iea_2024["Norway"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Global LV Sales 2025", f"{global_2025:.1f}M", "Forecast year total")
c2.metric("Greater China 2025", f"{china_2025:.1f}M", "Largest regional market")
c3.metric("UK EV Share 2024", f"{uk_2024:.1f}%", f"World: {world_2024:.1f}%")
c4.metric("Norway EV Share 2024", f"{norway_2024:.1f}%", "Global benchmark")

st.divider()

# =============================================================================
# SECTION 1 — Regional Sales Outlook
# =============================================================================
st.markdown("### Regional Light Vehicle Sales Outlook")
st.caption("Regional market size comparison across current and projected demand.")

st.plotly_chart(
    global_sales(df_global),
    use_container_width=True
)

st.markdown(
    '<p class="source-note">Source: SPGM_Global_Auto_LVSales.xlsx</p>',
    unsafe_allow_html=True
)

st.divider()

# =============================================================================
# SECTION 2 — Global EV Adoption Benchmark
# =============================================================================
st.markdown("### EV Adoption by Country")
st.caption("The UK is benchmarked against China, Germany, Norway, and the world average.")

display_cols = ["year", "UK", "China", "Germany", "Norway", "World"]
ev_df = df_iea[display_cols].copy()

st.plotly_chart(
    ev_share_global(ev_df),
    use_container_width=True
)

st.markdown(
    '<p class="source-note">Source: IEA_EVData_Explorer_2025.xlsx</p>',
    unsafe_allow_html=True
)

st.divider()

# =============================================================================
# DATA VIEW
# =============================================================================
with st.expander("📋 View raw datasets"):
    tab1, tab2 = st.tabs(["Global Sales", "IEA EV Share"])
    with tab1:
        st.dataframe(df_global, use_container_width=True)
    with tab2:
        st.dataframe(ev_df, use_container_width=True)

# =============================================================================
# KEY FINDINGS
# =============================================================================
st.markdown("### Key Findings")

st.markdown(f"""
<div class="findings-box"><p>
• The global automotive market remains highly concentrated, with <strong>Greater China accounting for {china_2025:.1f} million units in 2025</strong>, substantially ahead of North America at {north_america_2025:.1f} million.<br>
• Growth potential is unevenly distributed across regions, with the <strong>Indian Subcontinent projected to reach {india_2032:.1f} million units by 2032</strong>, indicating stronger medium-term expansion in emerging markets.<br>
• The UK’s EV share reached <strong>{uk_2024:.1f}% in 2024</strong>, above the world average of {world_2024:.1f}%, but still below leading electrification markets such as Norway.<br>
• <strong>Norway remains the strongest global benchmark</strong>, with EV penetration at {norway_2024:.1f}%, illustrating what sustained policy support and infrastructure readiness can achieve.<br>
• These patterns show that global automotive transformation is progressing at different speeds, shaped by <strong>market scale, policy consistency, and infrastructure maturity</strong>.
</p></div>
""", unsafe_allow_html=True)