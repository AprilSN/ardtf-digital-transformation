# =============================================================================
# app.py — Main page (Home) for Dashboard

# Run:   pip3 install -r requirements.txt
#        cd path/to/project
#        streamlit run app.py
# =============================================================================

import streamlit as st
from style import apply_style
from config import (
    df_fuel,
    df_charging,
    df_lpi,
    df_nox,
    df_global,
)
from pathlib import Path

# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
icon_path = BASE_DIR / "images" / "icon.png"
st.set_page_config(
    page_title="Automotive Intelligence Dashboard",
    page_icon=str(icon_path),
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_style()  # Apply custom CSS styles

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def safe_last(df, col):
    try:
        return df.iloc[-1][col]
    except Exception:
        return None


def safe_prev(df, col):
    try:
        return df.iloc[-2][col]
    except Exception:
        return None
    
# -----------------------------------------------------------------------------
# KPI values
# -----------------------------------------------------------------------------

bev_2025 = safe_last(df_fuel, "bev_share")
bev_2024 = safe_prev(df_fuel, "bev_share")
bev_delta = bev_2025 - bev_2024 if bev_2025 is not None and bev_2024 is not None else None

charger_total = safe_last(df_charging, "total")
charger_date = safe_last(df_charging, "date")

uk_lpi = None
if df_lpi is not None and not df_lpi.empty and "UK" in df_lpi.columns:
    uk_lpi = round(df_lpi["UK"].mean(), 2)

nox_reduction = None
if df_nox is not None and not df_nox.empty:
    df_nox_tmp = df_nox.copy()
    df_nox_tmp["total_nox"] = df_nox_tmp[["cars", "vans", "hgv", "buses"]].sum(axis=1)
    nox_start = df_nox_tmp.iloc[0]["total_nox"]
    nox_end = df_nox_tmp.iloc[-1]["total_nox"]
    if nox_start:
        nox_reduction = ((nox_end - nox_start) / nox_start) * 100

global_2025 = None
if df_global is not None and not df_global.empty and "s2025" in df_global.columns:
    global_2025 = round(df_global["s2025"].sum(), 1)

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
            <p class="logo-sub">COMP6013: Computing Project<br>Oxford Brookes University</p>
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
# Hero
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <p class="hero-label">COMP6013: Computing Project &nbsp;·&nbsp; Oxford Brookes University</p>
    <h1>Automotive Industry BI Dashboard<br>
    <span style="font-weight:normal; font-size:0.85em;">
    Data-Driven Digital Transformation for Automotive Retailers</span></h1>
    <p class="hero-subtitle">A data-driven analytical platform exploring structural transformation 
    in the automotive sector across market dynamics, supply chain resilience, 
    digital maturity, and macroeconomic pressures.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# Project overview
# -----------------------------------------------------------------------------
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("""
    <div style="padding:8px 0; font-size:16px; color:#fffff; line-height:1.8;">
        <h1>Project Overview</h1>
        <p style="text-align:justify;">
        This dashboard prototype demonstrates how business intelligence can support
        strategic decision-making in the automotive retail sector, particularly in the context of digital transformation and sustainability transition.
        </p>
        <p style="text-align:justify;">
        It brings together six analytical domains: market trends, supply chain pressure,
        global market dynamics, digital maturity (UK VS Myanmar Market), macroeconomic conditions, and environmental
        impact — structured around the <strong>ARDTF four-pillar framework</strong>.
        </p>
        <p style="text-align:justify;">
        The dashboard was developed in Python using Streamlit and Plotly, leveraging publicly available 
        automotive and macroeconomic datasets from sources including SMMT, ONS, Gov.UK, World Bank, IEA, S&P Global, and DfT/NAEI.        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("#### Dashboard at a Glance")

    c1, c2 = st.columns(2)
    c1.metric(
        "BEV Share",
        f"{bev_2025:.1f}%" if bev_2025 is not None else "–",
        f"{bev_delta:+.1f}pp YoY" if bev_delta is not None else None,
    )
    c2.metric(
        "EV Chargers",
        f"{charger_total:,.0f}" if charger_total is not None else "–",
        charger_date if charger_date is not None else None,
    )

    c3, c4 = st.columns(2)
    c3.metric(
        "UK LPI Score",
        f"{uk_lpi:.2f}/5" if uk_lpi is not None else "–",
        "Logistics benchmark",
    )
    c4.metric(
        "Road NOx Change",
        f"{nox_reduction:.0f}%" if nox_reduction is not None else "–",
        "1990 → latest",
    )

    c5, c6 = st.columns(2)
    c5.metric(
        "Global LV Sales",
        f"{global_2025:.1f}M" if global_2025 is not None else "–",
        "2025 outlook",
    )
    c6.metric(
        "Market Shift",
        "Fleet-led",
        "Demand structure",
    )

st.divider()

# -----------------------------------------------------------------------------
# Key Insights Section
# -----------------------------------------------------------------------------
st.markdown("## Key Insights")

st.markdown(
    """
    - **Electrification is accelerating**: BEV adoption continues to expand rapidly, 
      reshaping the composition of the UK automotive market.

    - **Fleet dominance is increasing**: Corporate and fleet purchases now drive 
      the majority of new registrations, indicating structural demand shifts.

    - **Supply chain pressure remains elevated**: Fuel volatility and logistics 
      inefficiencies continue to impact operational performance.

    - **Digital capability gap persists**: Emerging markets lag significantly 
      behind the UK in data-driven transformation readiness.
    """
)

# -----------------------------------------------------------------------------
# Analytical domains
# -----------------------------------------------------------------------------
st.markdown("## Analytical Domains")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>Market Overview</h3>
        <p>Track vehicle sales trends, EV adoption, and changes in fuel mix. This section also highlights shifts in demand structure and charging infrastructure growth.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>Supply Chain</h3>
        <p>Examine supply-chain pressure through fuel cost volatility, demand sensitivity, logistics performance, and broader operational stress indicators.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>Global Markets</h3>
        <p>Compare regional vehicle demand, global market outlook, and international EV adoption patterns to place the UK transition in a wider context.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>Digital Maturity</h3>
        <p>Assess how far automotive retailers have progressed in data, governance, system integration, and digital service capability across the UK and Myanmar.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>Macroeconomic</h3>
        <p>Explore GDP trends, inflation pressure, insurance costs, and other macro conditions that shape demand, affordability, and investment decisions.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>Environment</h3>
        <p>Analyse long-term changes in GHG and NOx emissions, fuel consumption, and the environmental pressures driving transport sector transformation.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# ARDTF framework
# -----------------------------------------------------------------------------
st.markdown("## ARDTF — Four-Pillar Framework")
st.markdown(
    "<p style='color:#6b7280; font-size:12px; margin-bottom:16px;'>"
    "The Automotive Retail Digital Transformation Framework (ARDTF) provides the analytical foundation for all six dashboard sections."
    "</p>",
    unsafe_allow_html=True,
)

p1, p2, p3, p4 = st.columns(4)

pillar_data = [
    (
        p1, "01", "Operational Foundation",
        "Market demand, registrations, sales structure, and operational pressure form the base layer of transformation.",
        "#1f4e79", "📊 Market Overview"
    ),
    (
        p2, "02", "Analytics & BI",
        "Forecasting, correlation analysis, infrastructure growth, and international benchmarking support decision-making.",
        "#16a34a", "🔗 Supply Chain · 🌍 Global"
    ),
    (
        p3, "03", "IT Governance",
        "Governance, KPI discipline, and digital maturity benchmarking help organisations scale transformation reliably.",
        "#d97706", "💻 Digital Maturity"
    ),
    (
        p4, "04", "Change Management",
        "Macroeconomic pressure and environmental transition reinforce the need for organisational readiness and adaptation.",
        "#dc2626", "📈 Macro · 🌿 Environment"
    ),
]

for col, num, title, desc, color, pages in pillar_data:
    col.markdown(f"""
    <div class="pillar-card" style="border-top:3px solid {color};">
        <p class="pillar-num" style="color:{color};">{num}</p>
        <p class="pillar-title">{title}</p>
        <p class="pillar-desc">{desc}</p>
        <p style="font-size:10px; color:#9ca3af; margin:8px 0 0;">→ {pages}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# Dashboard navigation note
# -----------------------------------------------------------------------------

st.markdown("## Dashboard Pages")
st.markdown("""
<div class="dashboard-pages">
<p>
Use the sidebar to move through each analytical module:
</p>
<ul>
• Market Overview & EV Trends<br>
• Supply Chain Stress Analysis<br>
• Global Market Comparisons<br>
• Digital Maturity<br>
• Macroeconomic Context<br>
• Environment & Emissions<br>
</ul>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("""
<div class="footer">
    Built with Python and Streamlit using published automotive, macroeconomic, and environmental datasets<br>
    Oxford Brookes University — COMP6013 Computing Project · April Soe Naing (19384274)
</div>
""", unsafe_allow_html=True)