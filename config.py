# =============================================================================
# config.py — loading clean data and visual configuration for the dashboard
# =============================================================================

from __future__ import annotations

import os
import sys
from pathlib import Path
import pandas as pd

# -----------------------------------------------------------------------------
# Project paths
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHARTS_DIR = BASE_DIR / "charts"
PAGES_DIR = BASE_DIR / "pages"
SCRIPTS_DIR = BASE_DIR / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from dataset_loader import (
    smmt_sale_type_dataset,
    smmt_fuel_type_dataset,
    smmt_vehicle_production_dataset,
    zapmap_ev_charging_dataset,
    worldbank_lpi_dataset,
    spgm_global_lv_sales_dataset,
    iea_ev_dataset,
    ons_env_ghg_dataset,
    naei_env_emission_index_dataset,
    naei_env_nox_dataset,
    desnz_env_fuel_price_dataset,
    desnz_env_energy_consumption_dataset,
    mm23_cpih_dataset,
    ons_cpi_insurance_dataset,
    qna_gdp_dataset,
    dft_lv_stock_dataset,
    digital_maturity_dataset,
)

# -----------------------------------------------------------------------------
# Visual system
# -----------------------------------------------------------------------------

C = {
    "navy": "#1C2333",
    "dark_blue": "#0F172A",
    "blue": "#2D3A52",
    "sky": "#4A7FA5",
    "accent": "#1E3A5F",
    "panel": "#FFFFFF",
    "bg": "#EAF1FB",
    "border": "#D9E2EC",
    "text": "#1C1C2E",
    "muted": "#64748B",
    "green": "#2E8B57",
    "amber": "#D97706",
    "red": "#DC2626",
    "purple": "#7C3AED",
    "petrol": "#3B5BDB",
    "diesel": "#DD841E",
    "hybrid": "#8E4EC6",
    "phev": "#B45309",
    "bev": "#2196C4",
}

# ── Plotly base layout ─────────────────────────────────────────────────────

CHART_LAYOUT = dict(
    paper_bgcolor = C["panel"],
    plot_bgcolor  = C["panel"],
    font          = dict(family="DM Sans, Georgia, sans-serif", color=C["text"], size=12),
    margin        = dict(l=50, r=20, t=45, b=40),
    legend        = dict(
        bgcolor     = "rgba(255,255,255,0.95)",
        bordercolor = C["border"], borderwidth=1,
        font        = dict(size=11, color=C["muted"]),
    ),
    xaxis = dict(
        showgrid=False, linecolor=C["border"],
        tickfont=dict(color=C["muted"], size=11),
        title_font=dict(color=C["muted"], size=11),
    ),
    yaxis = dict(
        showgrid=True, gridcolor="#f1f5f9", linecolor=C["border"],
        tickfont=dict(color=C["muted"], size=11),
        title_font=dict(color=C["muted"], size=11),
    ),
    hoverlabel = dict(
        bgcolor=C["panel"], bordercolor=C["border"],
        font=dict(color=C["text"], size=12),
    ),
)

PAGE_TITLES = {
    "market": "Market Overview",
    "supply": "Supply Chain & Demand",
    "global": "Global Market Outlook",
    "digital": "Digital Maturity",
    "macro": "Macroeconomic Context",
    "environment": "Environmental Pressure",
}

# -----------------------------------------------------------------------------
# Helpers Funtions 
# -----------------------------------------------------------------------------
def copy_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.copy() if isinstance(df, pd.DataFrame) else pd.DataFrame()


def ensure_year_str(df: pd.DataFrame, col: str = "year") -> pd.DataFrame:
    df = copy_df(df)
    if col in df.columns:
        df[col] = df[col].astype(str)
    return df


def ensure_year_int(df: pd.DataFrame, col: str = "year") -> pd.DataFrame:
    df = copy_df(df)
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def sort_year(df: pd.DataFrame, col: str = "year") -> pd.DataFrame:
    df = copy_df(df)
    if col in df.columns:
        year_num = pd.to_numeric(df[col], errors="coerce")
        df = df.assign(_year_num=year_num).sort_values("_year_num").drop(columns="_year_num")
    return df.reset_index(drop=True)


def round_numeric(df: pd.DataFrame, decimals: int = 2, exclude: list[str] | None = None) -> pd.DataFrame:
    df = copy_df(df)
    exclude = exclude or []
    for col in df.columns:
        if col not in exclude and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].round(decimals)
    return df


# -----------------------------------------------------------------------------
# Dataset preparation
# -----------------------------------------------------------------------------
def prepare_smmt_sale_type() -> pd.DataFrame:
    df = smmt_sale_type_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 1, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_smmt_fuel_type() -> pd.DataFrame:
    df = smmt_fuel_type_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 1, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_smmt_vehicle_production() -> pd.DataFrame:
    df = smmt_vehicle_production_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 1, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_charging() -> pd.DataFrame:
    df = zapmap_ev_charging_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 1, exclude=["year", "date"])
    df = ensure_year_str(df)
    return df


def prepare_lpi() -> pd.DataFrame:
    df = worldbank_lpi_dataset()
    df = df.rename(columns={"LPI Dimensions": "dimension"})
    return round_numeric(df, 2, exclude=["dimension"])


def prepare_global_sales() -> pd.DataFrame:
    df = spgm_global_lv_sales_dataset()
    return round_numeric(df, 1, exclude=["region"])


def prepare_iea_ev() -> pd.DataFrame:
    df = iea_ev_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 2, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_ghg() -> pd.DataFrame:
    df = ons_env_ghg_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 2, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_emission_index() -> pd.DataFrame:
    df = naei_env_emission_index_dataset()
    return round_numeric(df, 2, exclude=["fuel_type", "description", "euro_class", "period"])


def prepare_nox() -> pd.DataFrame:
    df = naei_env_nox_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 2, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_fuel_price() -> pd.DataFrame:
    df = desnz_env_fuel_price_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 1, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_energy_consumption() -> pd.DataFrame:
    df = desnz_env_energy_consumption_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 3, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_cpih() -> pd.DataFrame:
    df = mm23_cpih_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 1, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_insurance() -> pd.DataFrame:
    df = ons_cpi_insurance_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 1, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_gdp() -> pd.DataFrame:
    df = qna_gdp_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 2, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_vehicle_stock() -> pd.DataFrame:
    df = dft_lv_stock_dataset()
    df = ensure_year_int(df)
    df = sort_year(df)
    df = round_numeric(df, 2, exclude=["year"])
    df = ensure_year_str(df)
    return df


def prepare_digital_maturity() -> pd.DataFrame:
    df = digital_maturity_dataset()
    df = df.rename(columns={"Dimension": "dimension"})
    return round_numeric(df, 1, exclude=["dimension"])


# -----------------------------------------------------------------------------
# Load all datasets once
# -----------------------------------------------------------------------------
def load_data() -> dict[str, pd.DataFrame]:
    return {
        "smmt_sale_type": prepare_smmt_sale_type(),
        "smmt_fuel_type": prepare_smmt_fuel_type(),
        "smmt_vehicle_production": prepare_smmt_vehicle_production(),
        "zapmap_ev_charging": prepare_charging(),
        "worldbank_lpi": prepare_lpi(),
        "spgm_global_lv_sales": prepare_global_sales(),
        "iea_ev": prepare_iea_ev(),
        "ons_env_ghg": prepare_ghg(),
        "naei_env_emission_index": prepare_emission_index(),
        "naei_env_nox": prepare_nox(),
        "desnz_env_fuel_price": prepare_fuel_price(),
        "desnz_env_energy_consumption": prepare_energy_consumption(),
        "mm23_cpih": prepare_cpih(),
        "ons_cpi_insurance": prepare_insurance(),
        "qna_gdp": prepare_gdp(),
        "dft_lv_stock": prepare_vehicle_stock(),
        "digital_maturity": prepare_digital_maturity(),
    }


DATA = load_data()

# Convenient aliases for pages / charts
df_sale = DATA["smmt_sale_type"]
df_fuel = DATA["smmt_fuel_type"]
df_prod = DATA["smmt_vehicle_production"]
df_charging = DATA["zapmap_ev_charging"]
df_lpi = DATA["worldbank_lpi"]
df_global = DATA["spgm_global_lv_sales"]
df_iea = DATA["iea_ev"]
df_ghg = DATA["ons_env_ghg"]
df_emission_index = DATA["naei_env_emission_index"]
df_nox = DATA["naei_env_nox"]
df_fuel_price = DATA["desnz_env_fuel_price"]
df_energy = DATA["desnz_env_energy_consumption"]
df_cpih = DATA["mm23_cpih"]
df_insurance = DATA["ons_cpi_insurance"]
df_gdp = DATA["qna_gdp"]
df_vehicle_stock = DATA["dft_lv_stock"]
df_digital = DATA["digital_maturity"]

# -----------------------------------------------------------------------------
# Startup check
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "=" * 64)
    print("Dashboard config — dataset status")
    print("=" * 64)
    for name, df in DATA.items():
        print(f"{name:<28} {df.shape}")
    print("=" * 64 + "\n")
