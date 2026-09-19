# =============================================================================
# pages/4_Digital_Maturity.py — Digital Maturity
# ARDTF Pillar 3: IT Governance
# =============================================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from style import apply_style
from config import df_digital
from charts import digital_gap

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Digital Maturity | COMP6013",
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
    <span class="ph-pill">Pillar 3 — IT Governance</span>
    <h2>Digital Maturity</h2>
    <p>Capability gap · governance readiness · UK vs Myanmar comparison</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# KPI row
# -----------------------------------------------------------------------------
uk_avg = round(df_digital["UK"].mean(), 2)
mm_avg = round(df_digital["Myanmar"].mean(), 2)
gap_avg = round(uk_avg - mm_avg, 2)

weakest_mm = df_digital.loc[df_digital["Myanmar"].idxmin(), "dimension"]
strongest_uk = df_digital.loc[df_digital["UK"].idxmax(), "dimension"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("UK Average Score", f"{uk_avg:.2f}/10", "Advanced profile")
c2.metric("Myanmar Average Score", f"{mm_avg:.2f}/10", "Early-stage profile")
c3.metric("Average Capability Gap", f"{gap_avg:.2f} pts", "UK advantage")
c4.metric("Weakest Myanmar Area", weakest_mm, "Highest priority")

st.divider()

# =============================================================================
# SECTION 1 — Digital Capability Gap
# =============================================================================
st.markdown("### Digital Capability Gap")
st.caption("Capability comparison across the six dimensions of the digital maturity assessment.")

st.plotly_chart(
    digital_gap(df_digital),
    use_container_width=True
)

st.markdown(
    '<p class="source-note">Source: digital_maturity self-assessment framework</p>',
    unsafe_allow_html=True
)

st.divider()

# =============================================================================
# SECTION 2 — Capability Summary Table
# =============================================================================
st.markdown("### Capability Summary")
summary_df = df_digital.copy()
summary_df["gap"] = (summary_df["UK"] - summary_df["Myanmar"]).round(1)

st.dataframe(summary_df, use_container_width=True)

st.divider()

# =============================================================================
# DATA VIEW
# =============================================================================
with st.expander("📋 View raw dataset"):
    st.dataframe(df_digital, use_container_width=True)

# =============================================================================
# KEY FINDINGS
# =============================================================================
st.markdown("### Key Findings")

st.markdown(f"""
<div class="findings-box"><p>
• The UK demonstrates a consistently stronger digital profile, with an <strong>average score of {uk_avg:.2f}/10</strong> compared with {mm_avg:.2f}/10 for Myanmar.<br>
• The widest maturity gaps are concentrated in <strong>data, governance, and system integration capabilities</strong>, indicating that the transformation challenge is structural rather than isolated.<br>
• <strong>{weakest_mm}</strong> is the weakest area for Myanmar, highlighting it as the most urgent priority for digital capability development.<br>
• The UK’s strongest area is <strong>{strongest_uk}</strong>, reflecting a more developed operating environment for analytics-led and platform-enabled retail activity.<br>
• Overall, the evidence suggests that digital transformation depends not only on technology investment, but also on <strong>governance discipline, capability balance, and organisational readiness</strong>.
</p></div>
""", unsafe_allow_html=True)