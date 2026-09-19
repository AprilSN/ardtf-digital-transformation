import streamlit as st


def apply_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --bg: #EEF4FB;
        --panel: #FFFFFF;
        --sidebar-1: #203A43;
        --sidebar-2: #17303A;
        --sidebar-3: #0F2027;
        --text: #1C1C2E;
        --muted: #64748B;
        --border: #D9E2EC;
        --accent: #E07B39;
        --accent-soft: #FFF4EC;
        --shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        --radius: 10px;
        --radius-sm: 8px;
    }

    html, body, .stApp {
        background: var(--bg);
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .main .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1450px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--sidebar-1) 0%, var(--sidebar-2) 45%, var(--sidebar-3) 100%);
        min-width: 260px !important;
        max-width: 260px !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    [data-testid="stSidebar"] * {
        font-family: 'DM Sans', sans-serif !important;
        color: #E8EEF5 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.10) !important;
        margin: 0.8rem 0 !important;
    }

    [data-testid="stSidebarCollapseButton"],
    button[kind="header"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarHeader"],
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavSeparator"] {
        display: none !important;
        visibility: hidden !important;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 18px 16px 14px;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.10);
    }

    .sidebar-logo .logo-title {
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 700;
        margin: 0 0 3px;
        line-height: 1.2;
    }

    .sidebar-logo .logo-sub {
        color: rgba(255,255,255,0.50);
        font-size: 10px;
        margin: 0;
        line-height: 1.45;
    }

    .sidebar-section-label {
        color: rgba(255,255,255,0.42) !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.10em !important;
        margin: 0 !important;
        padding: 8px 0 6px !important;
    }

    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 999px;
        padding: 3px 8px;
        font-size: 10px;
        color: rgba(255,255,255,0.78);
        margin: 2px 4px 2px 0;
    }

    /* Sidebar links */
    [data-testid="stPageLink"] {
        margin-bottom: 2px !important;
    }

    [data-testid="stPageLink"] a {
        display: block;
        padding: 6px 8px !important;
        border-radius: 6px;
        text-decoration: none !important;
        color: rgba(255,255,255,0.84) !important;
        font-size: 11px !important;
        font-weight: 400 !important;
        line-height: 1.45 !important;
        transition: background 0.15s ease;
    }

    [data-testid="stPageLink"] a:hover {
        background: rgba(255,255,255,0.08) !important;
        color: #FFFFFF !important;
    }

    [data-testid="stPageLink"] svg {
        display: none !important;
    }

    /* Headings */
    h1 {
        color: var(--text) !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }

    h2 {
        color: var(--text) !important;
        font-size: 20px !important;
        font-weight: 650 !important;
    }

    h3 {
        color: var(--text) !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    h4 {
        color: var(--text) !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    hr {
        border-color: #E7EDF5 !important;
        margin: 1.2rem 0 !important;
    }

    /* Hero */
    .hero-banner {
        background: linear-gradient(135deg, #203A43 0%, #17303A 52%, #0F2027 100%);
        border-left: 4px solid var(--accent);
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 22px;
        box-shadow: var(--shadow);
    }

    .hero-banner .hero-label {
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: rgba(255,255,255,0.56);
        margin: 0 0 10px;
    }

    .hero-banner h1 {
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: 650 !important;
        line-height: 1.35;
        margin: 0 0 8px;
    }

    .hero-banner .hero-sub {
        font-size: 12px;
        color: rgba(255,255,255,0.64);
        margin: 8px 0 0;
        line-height: 1.5;
    }
    
    .hero-banner .hero-subtitle {
        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.12em;
        color: rgba(255,255,255,0.56);
        margin: 0 0 10px;
    }                

    /* Page header */
    .page-header {
        background: var(--panel);
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 0 var(--radius) var(--radius) 0;
        box-shadow: var(--shadow);
        padding: 14px 18px;
        margin-bottom: 18px;
    }

    .page-header h2 {
        margin: 0 0 4px !important;
        font-size: 18px !important;
    }

    .page-header p {
        color: var(--muted);
        font-size: 11px;
        line-height: 1.55;
        margin: 0;
    }

    .ph-pill {
        display: inline-block;
        font-size: 9px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        background: var(--accent-soft);
        color: var(--accent);
        border: 1px solid #F4D0B7;
        border-radius: 999px;
        padding: 3px 9px;
        margin-bottom: 6px;
    }

    /* Cards */
    .card,
    .pillar-card,
    .event-panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
    }

    .card {
        padding: 16px 18px;
        margin-bottom: 14px;
        border-top: 3px solid var(--accent);
    }

    .card h3 {
        margin: 0 0 8px !important;
        font-size: 15px !important;
    }

    .card p {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.65;
        margin: 0;
    }

    .pillar-card {
        padding: 18px 16px;
        text-align: center;
    }

    .pillar-card .pillar-num {
        font-size: 24px;
        font-weight: 700;
        margin: 0 0 5px;
    }

    .pillar-card .pillar-title {
        color: var(--text);
        font-size: 12px;
        font-weight: 600;
        margin: 0 0 6px;
    }

    .pillar-card .pillar-desc {
        color: var(--muted);
        font-size: 11px;
        line-height: 1.55;
        margin: 0;
    }

    .event-panel {
        padding: 14px 16px;
        margin-bottom: 10px;
        border-left: 4px solid var(--accent);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    }

    .event-panel .ep-period {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 0 0 4px;
    }

    .event-panel .ep-headline {
        color: var(--text);
        font-size: 13px;
        font-weight: 600;
        margin: 0 0 5px;
    }

    .event-panel .ep-detail {
        color: var(--muted);
        font-size: 11px;
        line-height: 1.6;
        margin: 0;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--border);
        border-top: 3px solid var(--accent);
        border-radius: var(--radius);
        padding: 14px 16px;
        box-shadow: var(--shadow);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }

    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 11px !important;
    }

    /* Chart and notes */
    .source-note {
        color: #8A98AA;
        font-size: 10px;
        font-style: italic;
        margin: 3px 0 14px;
        padding-left: 2px;
    }

    .findings-box {
        background: #FFF9F4;
        border: 1px solid #F5D8BE;
        border-left: 4px solid var(--accent);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        padding: 14px 18px;
        margin-top: 8px;
    }

    .findings-box p {
        color: #394150;
        font-size: 12px;
        line-height: 1.75;
        margin: 0;
    }

    .dashboard-pages {
        background: #F7FAFE;
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        padding: 14px 18px;
        margin-top: 8px;
    }

    .dashboard-pages p,
    .dashboard-pages ul {
        color: #394150;
        font-size: 12px;
        line-height: 1.7;
        margin: 0;
    }

    /* Tables / expander / tabs */
    [data-testid="stDataFrame"] {
        background: var(--panel);
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm);
        overflow: hidden;
    }

    [data-testid="stExpander"] {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
    }

    [data-testid="stExpander"] summary {
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    [data-testid="stExpander"] summary svg {
        margin-right: 6px !important;
    }

    [data-baseweb="tab-list"] {
        gap: 4px;
    }

    button[role="tab"] {
        border-radius: 8px 8px 0 0 !important;
        background: #F5F8FC !important;
        border: 1px solid var(--border) !important;
        color: var(--muted) !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 8px 14px !important;
    }

    button[role="tab"][aria-selected="true"] {
        background: var(--panel) !important;
        color: var(--text) !important;
        border-bottom: 1px solid var(--panel) !important;
    }

    .stCaption, [data-testid="stCaptionContainer"] {
        color: #7A8798 !important;
        font-size: 11px !important;
    }

    .footer {
        text-align: center;
        font-size: 10px;
        color: #94A3B8;
        padding: 16px 0 4px;
    }

    @media (max-width: 900px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        [data-testid="stSidebar"] {
            min-width: 220px !important;
            max-width: 220px !important;
        }

        .hero-banner {
            padding: 22px 24px;
        }
    }
    </style>
    """, unsafe_allow_html=True)