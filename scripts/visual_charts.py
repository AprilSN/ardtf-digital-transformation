# =============================================================================
# 02_analysis_charts.py
# =============================================================================

from pathlib import Path
import pandas as pd
import warnings
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
from dataset_loader import load_all_data

# -----------------------------------------------------------------------------
# Output directory
# -----------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent # Resolve current script location
OUT_DIR = SCRIPT_DIR.parent / "charts" # create /chart folder if not already exist
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Colour palette (for consistency)
# -----------------------------------------------------------------------------

NAVY = "#1C2333"
MUTED = "#64748B"
GRID = "#E2E8F0"
PANEL_BG = "#F8F9FA"
TEXT = "#1B2231"

ACCENT = "#4A7FA5"
AMBER = "#E07B39"
GREEN = "#16A34A"
RED = "#DC2626"
PURPLE = "#7C3AED"

PETROL_C = "#3B5BDB"
DIESEL_C = "#8C4A2F"
HYBRID_C = "#3FAF62"
PHEV_C = "#E18B49"
BEV_C = "#1696B5"

# -----------------------------------------------------------------------------
# Matplotlib defaults (Standardizing)
# -----------------------------------------------------------------------------

plt.rcParams.update({
    "figure.facecolor":   "white",
    "axes.facecolor":     PANEL_BG,
    "axes.edgecolor":     "#CBD5E1",
    "axes.labelcolor":    MUTED,
    "axes.labelsize":     10,
    "axes.titlesize":     11,
    "axes.titleweight":   "bold",
    "axes.titlecolor":    NAVY,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          False,
    "axes.prop_cycle":    plt.cycler(color=[
        ACCENT, AMBER, RED, GREEN, PURPLE, DIESEL_C, BEV_C, PETROL_C
    ]),
    "axes.titlepad": 12,
    "axes.labelpad": 8,
    "grid.color":         GRID,
    "grid.linewidth":     0.6,
    "grid.alpha":         0.8,
    "xtick.color":        MUTED,
    "ytick.color":        MUTED,
    "xtick.labelsize":    8.5,
    "ytick.labelsize":    8.5,
    "text.color":         TEXT,
    "legend.facecolor":   "white",
    "legend.edgecolor":   "#CBD5E1",
    "legend.fontsize":    9,
    "legend.framealpha":  0.95,
    "legend.borderpad": 0.6,
    "legend.handlelength": 1.5,
    "figure.dpi":         140,
    "savefig.dpi":        240,
    "savefig.facecolor":  "white",
    "font.family":        "sans-serif",
    "font.sans-serif":    ["DejaVu Sans", "Arial", "Helvetica"],
})

# -----------------------------------------------------------------------------
# Shared helper function across charts
# -----------------------------------------------------------------------------
def save_fig(fig, file_name):
    """Save figure to OUT_DIR and close."""
    fig.tight_layout()
    path = OUT_DIR / file_name
    fig.savefig(path, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  ✓ {file_name}")

def suptitle(fig, text):
    """Left-aligned NAVY bold suptitle matching document heading style."""
    fig.suptitle(text, fontsize=13, fontweight="bold", color=NAVY,
                 x=0.02, y=1.03, ha="left")

def style_ax(ax, title="", xlabel="", ylabel="", grid_axis="y", baseline=False):
    """Apply consistent figure styling: axes, panel BG, spines, grid, labels."""
    ax.set_facecolor(PANEL_BG)
    # Clean spine
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.tick_params(colors=MUTED, labelsize=9)
    
    # Reset and apply only the desired grid axis
    ax.grid(False)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.6, alpha=0.8, zorder=0)

    if baseline:
        ax.axhline(0, linewidth=0.9, color="#CBD5E1", zorder=1)

    if title:
        ax.set_title(title, loc="left", pad=10, color=NAVY, fontsize=11, fontweight="bold")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9, color=MUTED)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9, color=MUTED)
    # Margins
    ax.margins(x=0.02, y=0.08)
        
def add_source(ax, text):
    """Add right-aligned muted italic source citation note beneath chart."""
    ax.annotate(
        f"Source: {text}",
        xy=(1, -0.15),
        xycoords="axes fraction",
        ha="right",
        fontsize=7,
        color=MUTED,
        style="italic"
    )

def apply_format(ax, ytype="thousands"):
    """Apply Y-axis number formatting."""
    if ytype == "thousands":
        ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
        )
    elif ytype == "percent":
        ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{x:.0f}%")
        )
    elif ytype == "millions":
        ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{x:.0f}M")
        )

def prepare_year(df):
    """
    Ensure time-series consistency:
    - Sort by year
    - Convert year to string for plotting
    """
    df = df.copy().sort_values("year")
    df["year"] = df["year"].astype(str)
    return df

def normalize_to_100(series):
    """Min-max normalise a numeric series to 0–100."""
    series = pd.to_numeric(series, errors="coerce")
    if series.max() == series.min():
        return pd.Series([50] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min()) * 100


def annotate_corr(ax, r, x=0.03, y=0.93):
    """Add correlation annotation box."""
    ax.text(
        x, y,
        f"Pearson r = {r:.2f}",
        transform=ax.transAxes,
        fontsize=8.5,
        color=NAVY,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#CBD5E1")
    )


def add_trendline(ax, x, y, color=RED, linewidth=2.0):
    """Add simple linear trendline to scatter plot."""
    x_num = pd.to_numeric(x, errors="coerce")
    y_num = pd.to_numeric(y, errors="coerce")
    mask = x_num.notna() & y_num.notna()
    x_num = x_num[mask]
    y_num = y_num[mask]

# -----------------------------------------------------------------------------
# Chart functions
# -----------------------------------------------------------------------------
# Fig A — UK New Car Registrations by Fuel Type, 2020–2025
def fig_a_smmt_fuel(df):
    df = prepare_year(df)

    fig, ax = plt.subplots(figsize=(13, 6))
    x = np.arange(len(df))
    width = 0.6

    bottom = np.zeros(len(df))
    series = [
        ("petrol", PETROL_C, "Petrol"),
        ("diesel", DIESEL_C, "Diesel"),
        ("hybrid", HYBRID_C, "Hybrid"),
        ("phev", PHEV_C, "PHEV"),
        ("bev", BEV_C, "BEV"),
    ]

    for col, color, label in series:
        vals = df[col].values
        ax.bar(
            x, vals, width=width, bottom=bottom,
            color=color, label=label, alpha=0.9,
            edgecolor="white", linewidth=0.6, zorder=3
        )
        bottom += vals

    # BEV unit labels above total registrations
    offset = df["total"].max() * 0.025
    for i, val in enumerate(df["bev"]):
        ax.text(
            i, df["total"].iloc[i] + offset, f"BEV\n{val:.1f}K",
            ha="center", va="bottom", fontsize=8.5,
            color=BEV_C, fontweight="bold"
        )

    ax.set_xticks(x)
    ax.set_xticklabels(df["year"])
    
    style_ax(
        ax,
        title="Fig A — UK New Car Registrations by Fuel Type, 2020–2025",
        xlabel="Year",
        ylabel="Registrations (Thousands)",
        grid_axis="y"
    )
    apply_format(ax, "thousands")
    ax.legend(ncol=3, loc="upper left", frameon=False)
    add_source(ax, "SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx — 2.CarRegsByFuelType")
    save_fig(fig, "Fig_A_fuel_type_registrations.png")

# Fig B — BEV Market Share of UK New Car Registrations, 2020–2025
def fig_b_bev_share(df):
    df = prepare_year(df)

    # Calculate YoY growth from BEV registrations
    bev = df["bev"].tolist()
    bev_share = df["bev_share"].tolist()
    years = df["year"].tolist()

    yoy_growth = [0.0]
    for i in range(1, len(bev)):
        prev = bev[i - 1]
        curr = bev[i]
        growth = ((curr - prev) / prev * 100) if prev != 0 else 0
        yoy_growth.append(growth)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor("white")

    # Left panel — BEV market share
    x = np.arange(len(df))

    ax1.plot(
        x, bev_share,
        color=BEV_C, linewidth=2.8, marker="o", markersize=7,
        solid_capstyle="round", zorder=4
    )
    ax1.fill_between(x, bev_share, alpha=0.15, color=BEV_C, zorder=1)
    
    for i, val in enumerate(bev_share):
        ax1.annotate(
            f"{val:.1f}%",
            xy=(i, val + 0.6),
            ha="center",
            fontsize=8.5,
            color=BEV_C,
            fontweight="bold"
        )
    # Benchmark line     
    ax1.axhline(22, color=MUTED, linestyle="--", linewidth=1.3, label="IEA World Average BEV-Share 22% (2024)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.set_ylim(0, max(bev_share) + 8)
    
    style_ax(
        ax1,
        title="BEV Market Share of New Cars (%)",
        xlabel="Year",
        ylabel="BEV Share (%)",
        grid_axis="y",
        baseline=True
    )
    apply_format(ax1, "percent")
    add_source(ax1, "SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx — 2.CarRegsByFuelType")
    
    # Right panel — YoY growth in BEV registrations
    bar_colors = [MUTED] + [GREEN if g >= 0 else RED for g in yoy_growth[1:]]

    ax2.bar(
        x, yoy_growth,
        color=bar_colors, alpha=0.85, width=0.6,
        edgecolor="white", linewidth=0.6, zorder=3
    )

    for i, g in enumerate(yoy_growth):
        if i == 0:
            continue
        offset = 2 if g >= 0 else -5
        ax2.annotate(
            f"{g:.0f}%",
            xy=(i, g + offset),
            ha="center",
            fontsize=8.5,
            color=NAVY,
            fontweight="bold"
        )

    ax2.set_xticks(x)
    ax2.set_xticklabels(years)

    style_ax(
        ax2,
        title="BEV Registrations YoY Growth (%)",
        xlabel="Year",
        ylabel="YoY Change (%)",
        grid_axis="y",
        baseline=True
    )
    apply_format(ax2, "percent")
    add_source(ax2, "SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx — 2.CarRegsByFuelType")

    # Keep room for the suptitle
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.suptitle(
        "Fig B — UK BEV Market Share & Year-on-Year Growth, 2020–2025",
        x=0.06, y=0.98, ha="left", fontsize=13, fontweight="bold", color=NAVY
    )
    save_fig(fig, "Fig_B_bev_share_growth.png")

# Zapmap_EV_Charging_Devices_February2026.xlsx — Refined_Data
def fig_c_ev_charging(df):
    df = df.copy()

    # Checking if required columns exist
    if "slow" not in df.columns:
        df["slow"] = df["total"] - df["rapid"]

    # Use date label if available, otherwise year
    if "date" in df.columns:
        labels = df["date"].astype(str).tolist()
    else:
        labels = df["year"].astype(str).tolist()

    fig, ax = plt.subplots(figsize=(13, 6))
    x = np.arange(len(df))
    fig.patch.set_facecolor("white")
    width = 0.62

    # Stacked bars
    ax.bar(
        x, df["slow"],
        width=width,
        color=ACCENT,
        alpha=0.82,
        edgecolor="white",
        linewidth=0.7,
        label="Slow Chargers",
        zorder=3
    )

    ax.bar(
        x, df["rapid"],
        width=width,
        bottom=df["slow"],
        color=AMBER,
        alpha=0.9,
        edgecolor="white",
        linewidth=0.7,
        label="Rapid Chargers",
        zorder=3
    )

    # Total line
    ax.plot(
        x, df["total"],
        color=GREEN,
        linewidth=2.3,
        marker="D",
        markersize=6.5,
        label="Total (line)",
        zorder=5
    )

    # Total labels
    for i, total in enumerate(df["total"]):
        ax.annotate(
            f"{int(round(total / 1000))}k",
            xy=(i, total),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
            color=NAVY,
            fontweight="bold"
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=25, ha="right")

    style_ax(
        ax,
        title="Fig C — UK Public EV Charging Devices",
        xlabel="Period",
        ylabel="Number of Charging Devices",
        grid_axis="y"
    )

    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda v, _: f"{int(v/1000)}k")
    )

    # Legend order: total first, then slow, then rapid
    handles, labels_legend = ax.get_legend_handles_labels()
    order = [2, 0, 1]
    ax.legend(
        [handles[i] for i in order],
        [labels_legend[i] for i in order],
        loc="upper left",
        frameon=False
    )

    add_source(ax, "Zapmap_EV_Charging_Devices_February2026.xlsx — Refined_Data")
    save_fig(fig, "Fig_C_ev_charging_infrastructure.png")

# Fig D — UK New Car Registrations by Sale Type
def fig_d_sale_type(df):
    df = prepare_year(df).copy()
    df = df[df["year"].astype(int).between(2020, 2025)].copy()
    df["year"] = df["year"].astype(int)

    years = df["year"].values
    x = np.arange(len(df))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("white")

    fig.suptitle(
        "UK New Car Registrations by Sale Type (2020–2025)\n"
        "Source: SMMT — Private vs Fleet vs Business vs LCV",
        fontsize=15,
        fontweight="bold",
        color=NAVY,
        y=0.98
    )

    # -------------------------------------------------------------------------
    # Left panel — stacked total comparison
    # -------------------------------------------------------------------------
    private = df["private"].values
    fleet = df["fleet"].values
    business = df["business"].values
    lcv = df["lcv"].values
    total = df["total"].values

    w = 0.58

    ax1.bar(
        x, private, width=w,
        color=ACCENT, alpha=0.86,
        label="Private", zorder=3
    )
    ax1.bar(
        x, fleet, width=w, bottom=private,
        color=GREEN, alpha=0.82,
        label="Fleet", zorder=3
    )
    ax1.bar(
        x, business, width=w, bottom=private + fleet,
        color=AMBER, alpha=0.88,
        label="Business", zorder=3
    )
    ax1.bar(
        x, lcv, width=w, bottom=private + fleet + business,
        color=PURPLE, alpha=0.80,
        label="LCV", zorder=3
    )

    # Total labels on top
    for i, t in enumerate(total):
        ax1.annotate(
            f"{t:,.1f}",
            xy=(i, t),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=8.3,
            color=NAVY,
            fontweight="bold"
        )

    ax1.set_xticks(x)
    ax1.set_xticklabels(years)

    style_ax(
        ax1,
        title="Stacked Total Market Composition",
        xlabel="Year",
        ylabel="Registrations (Thousands)",
        grid_axis="y",
        baseline=False
    )
    apply_format(ax1, "thousands")
    ax1.legend(frameon=False, loc="upper left", fontsize=8.8)

    # -------------------------------------------------------------------------
    # Right panel — private vs fleet share progress
    # -------------------------------------------------------------------------
    private_share = df["private_share"].values
    fleet_share = df["fleet_share"].values

    ax2.fill_between(years, private_share, color=ACCENT, alpha=0.10, zorder=1)
    ax2.plot(
        years, private_share,
        color=ACCENT, linewidth=2.6,
        marker="o", markersize=8,
        label="Private Share %",
        zorder=4
    )

    ax2.fill_between(years, fleet_share, color=GREEN, alpha=0.10, zorder=1)
    ax2.plot(
        years, fleet_share,
        color=GREEN, linewidth=2.6,
        marker="o", markersize=8,
        label="Fleet Share %",
        zorder=4
    )

    # crossover / divergence emphasis
    ax2.axvspan(2022.5, 2023.5, color=AMBER, alpha=0.07, zorder=0)
    ax2.text(
        2023.0, 60,
        "Fleet overtakes\nprivate share",
        ha="center", va="center",
        fontsize=8,
        color=GREEN,
        fontstyle="italic"
    )

    # Point labels
    for yr, val in zip(years, private_share):
        ax2.annotate(
            f"{val:.1f}%",
            xy=(yr, val),
            xytext=(0, -16),
            textcoords="offset points",
            ha="center",
            fontsize=8.4,
            color=ACCENT,
            fontweight="bold"
        )

    for yr, val in zip(years, fleet_share):
        ax2.annotate(
            f"{val:.1f}%",
            xy=(yr, val),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=8.4,
            color=GREEN,
            fontweight="bold"
        )

    style_ax(
        ax2,
        title="Private vs Fleet Share Progress (%)",
        xlabel="Year",
        ylabel="Share of Total Registrations (%)",
        grid_axis="y",
        baseline=False
    )
    apply_format(ax2, "percent")
    ax2.set_xticks(years)
    ax2.set_ylim(35, 65)
    ax2.legend(frameon=False, loc="upper left", fontsize=9)

    # -------------------------------------------------------------------------
    # Sources
    # -------------------------------------------------------------------------
    ax1.text(
        0.00, -0.10,
        "Source: SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx \n — 1.RegBySaleType",
        transform=ax1.transAxes,
        fontsize=7.5, color=MUTED, style="italic"
    )
    ax2.text(
        0.00, -0.10,
        "Source: SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx \n — 1.RegBySaleType",
        transform=ax2.transAxes,
        fontsize=7, color=MUTED, style="italic"
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_fig(fig, "Fig_D_sale_type_registrations.png")

# Fig E — UK Car & CVs Production: Export vs Domestic, 2020–2025 
def fig_e_vehicle_production(df):
    df = prepare_year(df)

    fig, ax = plt.subplots(figsize=(13, 6))
    ax.fill_between(df["year"], df["cars_exported"], color=AMBER, alpha=0.18, zorder=1)
    ax.plot(
        df["year"], df["cars_exported"], color=AMBER, marker="o",
        linewidth=2.4, solid_capstyle="round", label="Cars Exported", zorder=3
    )
    ax.fill_between(df["year"], df["cars_domestic"], color=GREEN, alpha=0.18, zorder=1)
    ax.plot(
        df["year"], df["cars_domestic"], color=GREEN, marker="o",
        linewidth=2.4, linestyle="--", solid_capstyle="round", label="Cars Domestic", zorder=3
    )
    ax.fill_between(df["year"], df["cvs_exported"], color=RED, alpha=0.18, zorder=1)
    ax.plot(
        df["year"], df["cvs_exported"], color=RED, marker="o",
        linewidth=2.4, solid_capstyle="round", label="CVs Exported", zorder=3
    )
    ax.fill_between(df["year"], df["cvs_domestic"], color=PURPLE, alpha=0.18, zorder=1)
    ax.plot(
        df["year"], df["cvs_domestic"], color=PURPLE, marker="o",
        linewidth=2.4, linestyle="--", solid_capstyle="round", label="CVs Domestic", zorder=3
    )
    
    style_ax(
        ax,
        title="Fig E — UK Car & CVs Production: Export vs Domestic, 2020–2025",
        xlabel="Year",
        ylabel="Vehicles (Thousands)",
        grid_axis="y",
        baseline=True
    )
    apply_format(ax, "thousands")
    ax.legend(
        loc="upper right",
        frameon=False,
        fontsize=9
    )
    add_source(ax, "SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx — 3.VehicleProd")
    save_fig(fig, "Fig_E_vehicle_production.png")

# Fig F — Global Light Vehicle Sales by Region
def fig_f_global_sales(df):
    df = df.copy()

    # Keep expected year columns only if they exist
    year_cols = [f"s{y}" for y in range(2024, 2033) if f"s{y}" in df.columns]
    if len(year_cols) < 2:
        return

    # Sort regions by latest year for stronger reading order
    df = df.sort_values(year_cols[-1], ascending=False).reset_index(drop=True)

    years = [int(col.replace("s", "")) for col in year_cols]
    regions = df["region"].tolist()

    # Matrix for stackplot
    values = [df[col].values for col in year_cols]

    # Region colors
    region_colors = [ACCENT, PURPLE, RED, AMBER, GREEN, "#6D90A8", "#8FB996", "#E07A5F", "#7A9E9F", "#9C89B8", "#C8553D"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    fig.patch.set_facecolor("white")

    fig.suptitle(
        "Fig F — Global Light Vehicle Sales by Region, 2024–2032",
        x=0.06, y=0.98, ha="left",
        fontsize=14, fontweight="bold", color=NAVY
    )

    # -------------------------------------------------------------------------
    # Left panel — stacked area trend
    # -------------------------------------------------------------------------
    stack_series = [df.loc[i, year_cols].values.astype(float) for i in range(len(df))]

    ax1.stackplot(
        years,
        stack_series,
        labels=regions,
        colors=region_colors[:len(regions)],
        alpha=0.72,
        zorder=2
    )

    style_ax(
        ax1,
        title="Regional Sales Trend (Million Units)",
        xlabel="Year",
        ylabel="Units (millions)",
        grid_axis="y"
    )
    apply_format(ax1, "millions")
    ax1.legend(
        fontsize=7.5,
        loc="upper left",
        ncol=4,
        frameon=False
    )

    # -------------------------------------------------------------------------
    # Right panel — current vs projected year comparison
    # -------------------------------------------------------------------------
    first_col = year_cols[2]   # usually s2026
    last_col = year_cols[-1]   # usually s2032

    compare_df = df.sort_values(last_col, ascending=True).reset_index(drop=True)

    x = np.arange(len(compare_df))
    w = 0.36

    ax2.bar(
        x - w/2,
        compare_df[first_col],
        w,
        label=first_col.replace("s", ""),
        color=NAVY,
        alpha=0.84,
        zorder=3
    )
    ax2.bar(
        x + w/2,
        compare_df[last_col],
        w,
        label=last_col.replace("s", ""),
        color=ACCENT,
        alpha=0.72,
        zorder=3
    )

    # Growth labels
    for i, (_, row) in enumerate(compare_df.iterrows()):
        start = row[first_col]
        end = row[last_col]
        if pd.notna(start) and start != 0:
            pct = (end - start) / start * 100
            col = GREEN if pct > 0 else RED
            ax2.text(
                i,
                max(start, end) + 0.35,
                f"{pct:+.0f}%",
                ha="center",
                fontsize=8.5,
                color=col,
                fontweight="bold"
            )

    ax2.set_xticks(x)
    ax2.set_xticklabels(compare_df["region"], rotation=20, ha="right")

    style_ax(
        ax2,
        title=f"{first_col.replace('s','')} vs {last_col.replace('s','')} Comparison by Region",
        xlabel="Region",
        ylabel="Units (millions)",
        grid_axis="y"
    )
    apply_format(ax2, "millions")
    ax2.legend(frameon=False, fontsize=9, loc="upper left")

    add_source(ax2, "SPGM_Global_Auto_LVSales.xlsx — Data")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save_fig(fig, "Fig_F_global_lv_sales.png")

# Fig G — World Bank LPI Comparison: UK vs Myanmar (2018)
def fig_g_lpi(df):
    df = df.copy()

    fig, ax = plt.subplots(figsize=(13, 6))
    x = np.arange(len(df))
    width = 0.3

    ax.bar(x - width/2, df["UK"], width=width, label="UK", color=ACCENT)
    ax.bar(x + width/2, df["Myanmar"], width=width, label="Myanmar", color=AMBER)

    for i, v in enumerate(df["UK"]):
        ax.text(i - width / 2, v + 0.05, f"{v:.1f}", ha="center", fontsize=8)
    for i, v in enumerate(df["Myanmar"]):
        ax.text(i + width / 2, v + 0.05, f"{v:.1f}", ha="center", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(df["LPI Dimensions"], rotation=0, ha="right")

    style_ax(
        ax,
        title="Fig G — World Bank LPI Comparison: UK vs Myanmar (2018)",
        xlabel="",
        ylabel="Score",
        grid_axis="y"
    )
    ax.legend(frameon=False, loc="upper left")    
    add_source(ax, "WorldBank_Int_LPI_from_2007_to_2023.xlsx — 2018")
    save_fig(fig, "Fig_G_worldbank_lpi.png")

# Fig H — EV Sales Share by Selected Markets
def fig_h_iea_ev(df):
    df = prepare_year(df)

    fig, ax = plt.subplots(figsize=(13, 6))

    series = [
        ("USA", PURPLE, 2.0, 0.9),
        ("UK", ACCENT, 2.0, 0.95),
        ("China", RED, 2.6, 1.0),
        ("Germany", AMBER, 2.0, 0.9),
        ("Norway", GREEN, 2.8, 1.0),
        ("World", MUTED, 2.0, 0.9),
    ]
    
    for col, color, lw, alpha in series:
        if col in df.columns:
            ax.plot(
                df["year"], df[col],
                marker="o", linewidth=lw, alpha=alpha,
                label=col, color=color, solid_capstyle="round"
            )

    style_ax(
        ax,
        title="Fig H — EV Sales Share by Selected Markets",
        xlabel="Year",
        ylabel="EV Sales Share (%)",
        grid_axis="y",
        baseline=True
    )
    apply_format(ax, "percent")
    ax.legend(ncol=2, frameon=False, loc="upper left")
    add_source(ax, "IEA_EVData_Explorer_2025.xlsx — GEVO_EV_2025")
    save_fig(fig, "Fig_H_iea_ev_share.png")

# Fig I — UK Road Transport NOx Emissions, 2006–2025
def fig_i_nox_emissions(df):
    df = prepare_year(df)
    recent = df[df["year"].astype(int).between(2006, 2023)].copy()

    recent["year"] = recent["year"].astype(int)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor("white")
    fig.suptitle(
        "Fig I — UK Road Transport NOx Emissions, 2006–2023",
        x=0.06, y=0.98, ha="left",
        fontsize=13, fontweight="bold", color=NAVY
    )

    # ---------------------------------------------------------------------
    # Left panel — NOx emissions by vehicle type
    # ---------------------------------------------------------------------
    ax1.fill_between(recent["year"], recent["cars"], color=ACCENT, alpha=0.18, zorder=1)
    ax1.plot(recent["year"], recent["cars"], marker="o", linewidth=2.5, label="Cars", color=ACCENT, zorder=3)

    ax1.fill_between(recent["year"], recent["vans"], color=AMBER, alpha=0.18, zorder=1)
    ax1.plot(recent["year"], recent["vans"], marker="o", linewidth=2.5, label="Vans", color=AMBER, zorder=3)

    ax1.fill_between(recent["year"], recent["hgv"], color=RED, alpha=0.18, zorder=1)
    ax1.plot(recent["year"], recent["hgv"], marker="o", linewidth=2.5, label="HGV", color=RED, zorder=3)

    ax1.fill_between(recent["year"], recent["buses"], color=GREEN, alpha=0.18, zorder=1)
    ax1.plot(recent["year"], recent["buses"], marker="o", linewidth=2.5, label="Buses", color=GREEN, zorder=3)

    # show fewer x labels
    year_ticks = recent["year"].tolist()
    year_labels = [
        str(y) if (i % 5 == 0 or i >= len(year_ticks) - 4) else ""
        for i, y in enumerate(year_ticks)
    ]
    ax1.set_xticks(year_ticks)
    ax1.set_xticklabels(year_labels, rotation=0, ha="center", fontsize=8)

    style_ax(
        ax1,
        title="UK Road Transport NOx Emissions by Vehicle Type, 2006–2023",
        xlabel="Year",
        ylabel="ktNOx",
        grid_axis="y",
        baseline=True
    )
    ax1.set_ylim(bottom=0)
    ax1.legend(loc="upper right", frameon=False, fontsize=9)
    add_source(ax1, "NAEI_env0301_NOX.xlsx — ENV0301c_NOx")

    # ---------------------------------------------------------------------
    # Right panel — NOx Index Bar Chart (2006 = 100)
    # ---------------------------------------------------------------------
    recent["total_nox"] = recent["cars"] + recent["vans"] + recent["hgv"] + recent["buses"]

    if 2006 in recent["year"].values:
        base_2006 = recent.loc[recent["year"] == 2006, "total_nox"].iloc[0]
        recent["nox_index"] = recent["total_nox"] / base_2006 * 100
    else:
        recent["nox_index"] = np.nan

    # color bands by period
    bar_colors = []
    for yr in recent["year"]:
        if yr <= 2008:
            bar_colors.append("#D76655")
        elif yr <= 2012:
            bar_colors.append("#E59A3A")
        else:
            bar_colors.append("#4FA36C")

    ax2.bar(
        recent["year"].astype(str),
        recent["nox_index"],
        color=bar_colors,
        width=0.6,
        edgecolor="white",
        linewidth=0.6,
        zorder=3
    )
    ax2.axhline(100, color=MUTED, linestyle="--", linewidth=1.0, alpha=0.9)

    latest_idx = recent["nox_index"].iloc[-1]
    reduction = 100 - latest_idx

    style_ax(
        ax2,
        title=f"Road NOx Index (2006 = 100) — {reduction:.0f}% Reduction",
        xlabel="Year",
        ylabel="Index (2006 = 100)",
        grid_axis="y",
        baseline=True
    )

    ax2.set_xticks(np.arange(len(recent)))
    ax2.set_xticklabels(year_labels, rotation=0, ha="center", fontsize=8)

    add_source(ax2, "NAEI_env0301_NOX.xlsx — ENV0301c_NOx")

    # Keep room for the suptitle
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save_fig(fig, "Fig_I_nox_index.png")

# Fig J — UK Transport Environmental Pressure & Fuel-Consumption Relationship
def fig_j_environmental_impact(env_ghg_df, fuel_df, energy_df):
    # -------------------------------------------------------------------------
    # Prepare data
    # -------------------------------------------------------------------------
    ghg = prepare_year(env_ghg_df).copy()
    fuel = prepare_year(fuel_df).copy()
    energy = prepare_year(energy_df).copy()

    ghg["year"] = ghg["year"].astype(int)
    fuel["year"] = fuel["year"].astype(int)
    energy["year"] = energy["year"].astype(int)

    # -------------------------------------------------------------------------
    # Figure layout
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor("white")

    fig.suptitle(
        "UK Transport Environmental Pressure — GHG Emissions, Fuel Prices & Fuel Consumption",
        fontsize=15,
        fontweight="bold",
        color=NAVY,
        y=0.98
    )

    # =========================================================================
    # GHG Emissions
    # =========================================================================
    ax = axes[0, 0]

    ghg_recent = ghg[ghg["year"].between(2006, 2023)].copy()

    ax.fill_between(ghg_recent["year"], ghg_recent["vans"], color=ACCENT, alpha=0.18, zorder=1)
    ax.plot(ghg_recent["year"], ghg_recent["vans"], color=ACCENT, linewidth=2.0, label="Vans", zorder=3)

    ax.fill_between(ghg_recent["year"], ghg_recent["hgv"], color=AMBER, alpha=0.18, zorder=1)
    ax.plot(ghg_recent["year"], ghg_recent["hgv"], color=AMBER, linewidth=2.0, label="HGV", zorder=3)

    ax.fill_between(ghg_recent["year"], ghg_recent["buses"], color=GREEN, alpha=0.18, zorder=1)
    ax.plot(ghg_recent["year"], ghg_recent["buses"], color=GREEN, linewidth=2.0, label="Buses", zorder=3)

    ax.fill_between(ghg_recent["year"], ghg_recent["cars"], color=RED, alpha=0.16, zorder=1)
    ax.plot(ghg_recent["year"], ghg_recent["cars"], color=RED, linewidth=2.2, label="Cars", zorder=4)

    if 2020 in ghg_recent["year"].values:
        ax.axvline(2020, color=MUTED, linestyle="--", linewidth=1.0, alpha=0.8)
        covid_val = ghg_recent.loc[ghg_recent["year"] == 2020, "cars"].iloc[0]
        ax.annotate(
            "COVID\nshock",
            xy=(2020, covid_val),
            xytext=(2020.2, covid_val + 8),
            fontsize=8,
            color=MUTED,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8)
        )

    style_ax(
        ax,
        title="Road Transport GHG (MtCO2e), 2006–2023",
        xlabel="Year",
        ylabel="MtCO2e",
        grid_axis="y"
    )
    ax.legend(frameon=False, loc="upper right", fontsize=8)

    # =========================================================================
    # Petrol & Diesel Pump Prices
    # =========================================================================
    ax = axes[0, 1]

    fuel_recent = fuel[fuel["year"].between(2006, 2024)].copy()

    ax.plot(fuel_recent["year"], fuel_recent["petrol"], color=ACCENT, linewidth=2.5, label="Petrol (p/L)")
    ax.plot(fuel_recent["year"], fuel_recent["diesel"], color=AMBER, linewidth=2.5, label="Diesel (p/L)")

    ax.fill_between(
        fuel_recent["year"],
        fuel_recent["petrol"],
        fuel_recent["diesel"],
        where=(fuel_recent["diesel"] >= fuel_recent["petrol"]),
        color=RED,
        alpha=0.08,
        label="Diesel premium"
    )

    peak_year = fuel_recent.loc[fuel_recent["diesel"].idxmax(), "year"]
    peak_val = fuel_recent["diesel"].max()

    ax.axvline(peak_year, color=RED, linestyle=":", linewidth=1.2, alpha=0.7)
    ax.annotate(
        "Energy\ncrisis",
        xy=(peak_year, peak_val),
        xytext=(peak_year + 0.2, peak_val - 5),
        fontsize=8,
        color=RED,
        fontweight="bold"
    )

    style_ax(
        ax,
        title="Petrol & Diesel Pump Prices (p/L), 2006–2024",
        xlabel="Year",
        ylabel="Pence per Litre",
        grid_axis="y"
    )
    ax.legend(frameon=False, loc="upper left", fontsize=8)

    # =========================================================================
    # Car Fuel Consumption
    # =========================================================================
    ax = axes[1, 0]

    cons = energy[["year", "petrol_cars", "diesel_cars"]].copy()
    cons = cons[cons["year"].between(2006, 2022)].copy()

    ax.fill_between(cons["year"], cons["petrol_cars"], color=ACCENT, alpha=0.12, zorder=1)
    ax.plot(
        cons["year"], cons["petrol_cars"],
        color=ACCENT, linewidth=2.5, label="Petrol Cars", zorder=3
    )

    ax.fill_between(cons["year"], cons["diesel_cars"], color=AMBER, alpha=0.14, zorder=1)
    ax.plot(
        cons["year"], cons["diesel_cars"],
        color=AMBER, linewidth=2.5, label="Diesel Cars", zorder=3
    )

    # Annotate diesel peak
    d_peak_year = cons.loc[cons["diesel_cars"].idxmax(), "year"]
    d_peak_val = cons["diesel_cars"].max()
    ax.axvline(d_peak_year, color=MUTED, linestyle="--", linewidth=1.0, alpha=0.8)
    ax.annotate(
        f"Diesel-car peak\n{d_peak_year}",
        xy=(d_peak_year, d_peak_val),
        xytext=(d_peak_year + 0.3, d_peak_val + 0.8),
        fontsize=8,
        color=AMBER,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=AMBER, lw=0.8)
    )

    style_ax(
        ax,
        title="Car Fuel Consumption: Petrol vs Diesel (Mt), 2006–2022",
        xlabel="Year",
        ylabel="Million Tonnes",
        grid_axis="y"
    )
    ax.legend(frameon=False, loc="upper right", fontsize=8)

    # =========================================================================
    # Petrol Price vs Petrol Consumption Relationship
    # =========================================================================
    ax = axes[1, 1]

    rel = pd.merge(
        energy[["year", "petrol_cars"]],
        fuel[["year", "petrol"]],
        on="year",
        how="inner"
    ).copy()

    rel = rel[rel["year"].between(2006, 2022)].copy()
    rel["year_num"] = rel["year"].astype(int)

    base = rel["petrol_cars"].iloc[0]
    rel["consumption_index"] = rel["petrol_cars"] / base * 100

    r = rel["petrol"].corr(rel["consumption_index"])

    ax.plot(
        rel["year_num"], rel["petrol"],
        color=AMBER, linewidth=2.6, marker="o",
        label="Petrol Price (p/L)", zorder=4
    )
    ax.fill_between(rel["year_num"], rel["petrol"], color=AMBER, alpha=0.10, zorder=1)
    ax.set_ylabel("Petrol Price (Pence/Litre)", fontsize=10, color=AMBER, labelpad=8)
    ax.tick_params(axis="y", colors=AMBER)

    ax2 = ax.twinx()
    ax2.plot(
        rel["year_num"], rel["consumption_index"],
        color=GREEN, linewidth=2.6, marker="o", linestyle="--",
        label="Petrol Consumption Index", zorder=4
    )
    ax2.fill_between(rel["year_num"], rel["consumption_index"], color=GREEN, alpha=0.10, zorder=1)
    ax2.set_ylabel("Consumption Index (Base Year = 100)", fontsize=10, color=GREEN, labelpad=8)
    ax2.tick_params(axis="y", colors=GREEN)

    style_ax(
        ax,
        title=f"Petrol Price vs Petrol Consumption Index\nCorrelation r = {r:.2f}",
        xlabel="Year",
        ylabel="",
        grid_axis="y"
    )

    xticks = rel["year_num"][::2]
    ax.set_xticks(xticks)
    ax.set_xticklabels(rel.loc[rel.index[::2], "year"])

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper right", fontsize=8)

    # -------------------------------------------------------------------------
    # Panel-level source notes
    # -------------------------------------------------------------------------
    axes[0, 0].text(
        0.00, -0.10, "Source: ONS_env0201_GHG.xlsx",
        transform=axes[0, 0].transAxes,
        fontsize=7.5, color=MUTED, style="italic"
    )
    axes[0, 1].text(
        0.00, -0.10, "Source: DESNZ_env0105_FuelPrice.xlsx",
        transform=axes[0, 1].transAxes,
        fontsize=7.5, color=MUTED, style="italic"
    )
    axes[1, 0].text(
        0.00, -0.10, "Source: DESNZ_env0101_Energy_Consumption.xlsx",
        transform=axes[1, 0].transAxes,
        fontsize=7.5, color=MUTED, style="italic"
    )
    axes[1, 1].text(
        0.00, -0.10, "Source: DESNZ_env0105_FuelPrice.xlsx \n + DESNZ_env0101_Energy_Consumption.xlsx",
        transform=axes[1, 1].transAxes,
        fontsize=7.5, color=MUTED, style="italic"
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_fig(fig, "Fig_J_environmental_impact.png")

# Fig K — Diesel Decline vs BEV Rise
def fig_k_diesel_bev_crossover(df):
    df = prepare_year(df).copy()
    df = df[df["year"].astype(int).between(2020, 2025)].copy()

    years = df["year"].astype(int).values
    bev_share = df["bev_share"].values
    diesel_share = df["diesel_share"].values

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("white")

    # Soft fills
    ax.fill_between(years, bev_share, color=ACCENT, alpha=0.12, zorder=1)
    ax.fill_between(years, diesel_share, color=RED, alpha=0.10, zorder=1)

    # Main lines
    ax.plot(
        years, diesel_share,
        color=RED, linewidth=2.6,
        marker="o", markersize=8,
        label="Diesel Share %",
        zorder=4
    )
    ax.plot(
        years, bev_share,
        color=ACCENT, linewidth=2.6,
        marker="o", markersize=8,
        label="BEV Share %",
        zorder=4
    )

    # Highlight crossover zone
    ax.axvspan(2022.3, 2023.3, color=AMBER, alpha=0.08, label="Crossover zone (2022–23)", zorder=0)
    ax.text(
        2022.65, 14.3,
        "Crossover\nzone",
        color=AMBER,
        fontsize=9,
        fontstyle="italic",
        ha="center",
        va="center"
    )

    # Point labels
    for x, y in zip(years, diesel_share):
        ax.annotate(
            f"{y:.1f}%",
            xy=(x, y),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
            color=RED,
            fontweight="bold"
        )

    for x, y in zip(years, bev_share):
        ax.annotate(
            f"{y:.1f}%",
            xy=(x, y),
            xytext=(0, -16),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
            color=ACCENT,
            fontweight="bold"
        )

    style_ax(
        ax,
        title="Fig K — The Great Crossover: Diesel Decline vs BEV Rise\nUK New Car Market Share %, 2020–2025",
        xlabel="Year",
        ylabel="Market Share (%)",
        grid_axis="y",
        baseline=False
    )

    apply_format(ax, "percent")
    ax.set_xticks(years)
    ax.set_ylim(0, max(bev_share.max(), diesel_share.max()) + 5)

    ax.legend(loc="upper right", frameon=False, fontsize=9)
    add_source(ax, "SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx — 2.CarRegsByFuelType")
    save_fig(fig, "Fig_K_diesel_bev_crossover.png")    

# Fig L — UK CPIH Annual Inflation Rate
def fig_l_cpih(df):
    df = prepare_year(df).copy()
    recent = df[df["year"].astype(int).between(2016, 2024)].copy()
    recent["year"] = recent["year"].astype(int)

    years = recent["year"].values
    cpih = recent["cpih"].values

    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    fig.patch.set_facecolor("white")

    # Main line + soft fill
    ax.fill_between(years, cpih, color=AMBER, alpha=0.14, zorder=1)
    ax.plot(
        years, cpih,
        color=AMBER, linewidth=2.8,
        marker="o", markersize=8,
        zorder=4
    )

    # Bank of England target
    ax.axhline(
        2,
        color=GREEN,
        linestyle="--",
        linewidth=1.6,
        alpha=0.95,
        label="Bank of England 2% target"
    )

    # COVID band
    ax.axvspan(2019.7, 2020.5, color=ACCENT, alpha=0.08, label="COVID")

    # Energy crisis band
    ax.axvspan(2021.7, 2022.5, color=RED, alpha=0.06, label="Energy crisis")

    # Point labels
    for yr, val in zip(years, cpih):
        ax.annotate(
            f"{val:.1f}%",
            xy=(yr, val),
            xytext=(0, 10 if yr != 2022 else -20),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
            color=AMBER,
            fontweight="bold"
        )

    # Peak annotation
    peak_idx = int(np.argmax(cpih))
    peak_year = years[peak_idx]
    peak_val = cpih[peak_idx]
    ax.annotate(
        f"Energy crisis\npeak: {peak_val:.1f}%",
        xy=(peak_year, peak_val),
        xytext=(peak_year - 0.2, peak_val + 0.3),
        fontsize=8.5,
        color=RED,
        fontstyle="italic",
        arrowprops=dict(arrowstyle="->", color=RED, lw=0.9)
    )

    # COVID annotation
    if 2020 in years:
        covid_val = recent.loc[recent["year"] == 2020, "cpih"].iloc[0]
        ax.annotate(
            f"COVID\n{covid_val:.1f}%",
            xy=(2020, covid_val),
            xytext=(2019.8, covid_val + 0.7),
            fontsize=8.5,
            color=ACCENT,
            fontstyle="italic"
        )

    style_ax(
        ax,
        title="Fig L — UK CPIH Annual Inflation Rate (2016–2024)",
        xlabel="Year",
        ylabel="CPIH Annual Rate (%)",
        grid_axis="y",
        baseline=False
    )

    apply_format(ax, "percent")
    ax.set_xticks(years)
    ax.set_ylim(-0.5, max(cpih) + 2)

    ax.legend(loc="upper left", frameon=False, fontsize=9)
    add_source(ax, "MM23_CPIH.xlsx — Annual")
    save_fig(fig, "Fig_L_cpih_inflation.png")

# Fig M: UK CPI Car Insurance Index, 2000–2018
def fig_m_insurance(df):
    df = prepare_year(df)
    recent = df[df["year"].astype(int).between(2000, 2018)].copy()

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor("white")

    years = recent["year"].astype(int).values
    values = recent["annual_avg"].values

    # Main area + line
    ax.fill_between(years, values, alpha=0.12, color=RED, zorder=1)
    ax.plot(
        years, values,
        color=RED, linewidth=2.6,
        marker="o", markersize=5.8,
        solid_capstyle="round",
        zorder=4
    )

    # Base year reference line
    ax.axhline(
        100,
        color=MUTED,
        linestyle="--",
        linewidth=1.3,
        alpha=0.9,
        label="Base year 2015 = 100"
    )

    # Only shade recent inflationary period if data actually exists
    if years.max() >= 2015:
        ax.axvspan(
            2015, min(2026, years.max()),
            alpha=0.06,
            color=AMBER,
            label="Recent inflationary pressure"
        )

    # Peak annotation
    peak_idx = int(np.argmax(values))
    peak_year = years[peak_idx]
    peak_val = values[peak_idx]

    start_val = values[0]
    change_pct = ((peak_val - start_val) / start_val * 100) if start_val != 0 else 0

    ax.annotate(
        f"Peak: {peak_val:.1f} ({peak_year})\n+{change_pct:.0f}% since {years[0]}",
        xy=(peak_year, peak_val),
        xytext=(peak_year - 4.2, peak_val + 8),
        fontsize=8.5,
        color=RED,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.0)
    )

    # Base year annotation
    if 2015 in years:
        base_val = recent.loc[recent["year"].astype(int) == 2015, "annual_avg"].iloc[0]
        ax.annotate(
            "Base year\n2015 = 100",
            xy=(2015, base_val),
            xytext=(2011.5, base_val + 8),
            fontsize=8,
            color=MUTED,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8)
        )

    # label for latest value
    latest_year = years[-1]
    latest_val = values[-1]
    ax.annotate(
        f"{latest_val:.1f}",
        xy=(latest_year, latest_val),
        xytext=(0, 7),
        textcoords="offset points",
        ha="center",
        fontsize=8.5,
        color=RED,
        fontweight="bold"
    )

    style_ax(
        ax,
        title="Fig M — UK CPI Car Insurance Index, 2000–2018",
        xlabel="Year",
        ylabel="CPI Index (2015 = 100)",
        grid_axis="y",
        baseline=False
    )

    ax.set_ylim(max(40, values.min() - 8), values.max() + 18)
    ax.set_xticks(years[::2])
    ax.set_xticklabels(years[::2])

    ax.legend(loc="upper left", frameon=False, fontsize=9)
    add_source(ax, "ONS_CPI_Insurance.xlsx — CPI Car Insurance")
    save_fig(fig, "Fig_M_cpi_insurance.png")

# Fig N: Digital Maturity Comparison: UK vs Myanmar
def fig_n_digital_maturity(df):
    df = df.copy()

    categories = df["Dimension"].tolist()
    uk = df["UK"].tolist()
    mm = df["Myanmar"].tolist()

    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    uk += uk[:1]
    mm += mm[:1]

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
    ax.plot(angles, uk, color=ACCENT, linewidth=2.2, label="UK")
    ax.fill(angles, uk, color=ACCENT, alpha=0.22)
    ax.plot(angles, mm, color=AMBER, linewidth=2.2, label="Myanmar")
    ax.fill(angles, mm, color=AMBER, alpha=0.22)

    ax.grid(color=GRID, alpha=0.35)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9, color=MUTED)
    ax.set_ylim(0, 10)
    ax.set_title(
        "Fig N — Digital Maturity Comparison: UK vs Myanmar",
        loc="left", pad=20, color=NAVY, fontsize=11, fontweight="bold"
    )
    ax.legend(loc="upper right", bbox_to_anchor=(1.18, 1.12), frameon=False)
    fig.text(
        0.99, 0.02,
        "Source: Author-created digital maturity assessment",
        ha="right", fontsize=7, color=MUTED, style="italic"
    )
    save_fig(fig, "Fig_N_digital_maturity_radar.png")

# Fig O — Licensed Vehicle Stock (Q4 Snapshot), 2006–2024
def fig_o_vehicle_stock(df):
    df = prepare_year(df)
    recent = df[df["year"].astype(int).between(2006, 2024)].copy()
    
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(recent["year"], recent["cars"],  marker="o", linewidth=2.6, alpha=0.8, label="Cars",  color=ACCENT, zorder=3)
    ax.plot(recent["year"], recent["total"], marker="o", linewidth=2.6, alpha=0.8, label="Total", color=GREEN, zorder=3)
    ax.fill_between(recent["year"], recent["cars"], color=ACCENT, alpha=0.12, zorder=1)
    ax.fill_between(recent["year"], recent["total"], color=RED, alpha=0.12, zorder=1)

    style_ax(
        ax,
        title="Fig O — Licensed Vehicle Stock (Q4 Snapshot), 2006–2024",
        xlabel="Year",
        ylabel="Vehicle Stock (Thousands)",
        grid_axis="y",
        baseline=True
    )
    apply_format(ax, "thousands")
    ax.legend(ncol=2, frameon=False, loc="upper left")
    add_source(ax, "Dft_veh0101_LicensedStock.xlsx — VEH0101a_Lic")
    save_fig(fig, "Fig_O_vehicle_stock.png")

# Fig P — UK Combined Fuel Price vs ICE Registration Demand Index, 2020–2025
def fig_p_fuel_price_vs_demand(fuel_price_df, fuel_type_df):
    fuel_price_df = prepare_year(fuel_price_df)
    fuel_type_df = prepare_year(fuel_type_df)

    # Merge annual fuel prices with annual fuel-type registrations
    df = pd.merge(
        fuel_price_df[["year", "petrol", "diesel"]],
        fuel_type_df[["year", "petrol", "diesel"]],
        on="year",
        how="inner",
        suffixes=("_price", "_regs")
    ).copy()

    df = df[df["year"].astype(int).between(2020, 2025)].copy()
    df["year_num"] = df["year"].astype(int)

    # Combined fuel price = average petrol + diesel price
    df["fuel_price_avg"] = (df["petrol_price"] + df["diesel_price"]) / 2

    # Combined ICE demand = petrol + diesel registrations
    df["ice_regs"] = df["petrol_regs"] + df["diesel_regs"]

    # Demand index (base year = 2020)
    base = df["ice_regs"].iloc[0]
    df["demand_index"] = df["ice_regs"] / base * 100

    # Correlation
    r = df["fuel_price_avg"].corr(df["demand_index"])

    fig, ax1 = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("white")

    # ------------------------------------------------------------------
    # Left axis — combined fuel price
    # ------------------------------------------------------------------
    ax1.plot(
        df["year_num"], df["fuel_price_avg"],
        color=AMBER, linewidth=2.8, marker="o",
        label="Average Fuel Price (p/L)", zorder=4
    )
    ax1.fill_between(
        df["year_num"], df["fuel_price_avg"],
        color=AMBER, alpha=0.10, zorder=1
    )
    ax1.set_ylabel("Average Fuel Price (Pence/Litre)", fontsize=10, color=AMBER, labelpad=8)
    ax1.tick_params(axis="y", colors=AMBER)

    # ------------------------------------------------------------------
    # Right axis — ICE demand index
    # ------------------------------------------------------------------
    ax2 = ax1.twinx()
    ax2.plot(
        df["year_num"], df["demand_index"],
        color=ACCENT, linewidth=2.8, marker="o", linestyle="--",
        label="ICE Demand Index (2020 = 100)", zorder=4
    )
    ax2.fill_between(
        df["year_num"], df["demand_index"],
        color=ACCENT, alpha=0.10, zorder=1
    )
    ax2.set_ylabel("ICE Demand Index (2020 = 100)", fontsize=10, color=ACCENT, labelpad=8)
    ax2.tick_params(axis="y", colors=ACCENT)

    # ------------------------------------------------------------------
    # Peak annotation
    # ------------------------------------------------------------------
    peak_idx = df["fuel_price_avg"].idxmax()
    ax1.annotate(
        f"Fuel price peak: {df.loc[peak_idx, 'fuel_price_avg']:.1f}p",
        xy=(df.loc[peak_idx, "year_num"], df.loc[peak_idx, "fuel_price_avg"]),
        xytext=(df.loc[peak_idx, "year_num"] - 0.9, df.loc[peak_idx, "fuel_price_avg"] + 8),
        fontsize=8.5,
        color=AMBER,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.0)
    )

    # Optional demand low annotation
    low_idx = df["demand_index"].idxmin()
    ax2.annotate(
        f"ICE demand low: {df.loc[low_idx, 'demand_index']:.1f}",
        xy=(df.loc[low_idx, "year_num"], df.loc[low_idx, "demand_index"]),
        xytext=(df.loc[low_idx, "year_num"] + 0.15, df.loc[low_idx, "demand_index"] - 6),
        fontsize=8.5,
        color=ACCENT,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.0)
    )

    # ------------------------------------------------------------------
    # Styling
    # ------------------------------------------------------------------
    style_ax(
        ax1,
        title=(
            "Fig P — UK Combined Fuel Price vs ICE Registration Demand Index, 2020–2025\n"
            f"Correlation r = {r:.2f}"
        ),
        xlabel="Year",
        ylabel="",
        grid_axis="y"
    )

    ax1.set_xticks(df["year_num"])
    ax1.set_xticklabels(df["year"])

    # Combined legend
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, frameon=False, loc="upper right")

    add_source(
        ax1,
        "DESNZ_env0105_FuelPrice.xlsx + SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx"
    )

    save_fig(fig, "Fig_P_fuel_price_vs_demand_index.png")

# Fig Q — UK Vehicle Stock Index vs Car NOX Emissions Index
def fig_q_nox_emission_vs_vehicle_stock(nox_df, stock_df):
    nox_df = prepare_year(nox_df)
    stock_df = prepare_year(stock_df)

    df = pd.merge(
        nox_df[["year", "cars"]],
        stock_df[["year", "cars"]],
        on="year",
        how="inner",
        suffixes=("_emissions", "_stock")
    ).copy()

    df = df[df["year"].astype(int).between(2006, 2024)].copy()
    df["year_num"] = df["year"].astype(int)

    base_stock = df["cars_stock"].iloc[0]
    base_em = df["cars_emissions"].iloc[0]

    df["stock_index"] = df["cars_stock"] / base_stock * 100
    df["emissions_index"] = df["cars_emissions"] / base_em * 100

    r = df["stock_index"].corr(df["emissions_index"])

    fig, ax1 = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("white")

    ax1.plot(
        df["year_num"], df["stock_index"],
        color=ACCENT, linewidth=2.6, marker="o",
        label="Licensed Cars Stock Index", zorder=4
    )
    ax1.fill_between(df["year_num"], df["stock_index"], color=ACCENT, alpha=0.10, zorder=1)
    ax1.set_ylabel("Vehicle Stock Index (Base Year = 100)", fontsize=10, color=ACCENT, labelpad=8)
    ax1.tick_params(axis="y", colors=ACCENT)

    ax2 = ax1.twinx()
    ax2.plot(
        df["year_num"], df["emissions_index"],
        color=RED, linewidth=2.6, marker="o", linestyle="--",
        label="Car Emissions Index", zorder=4
    )
    ax2.fill_between(df["year_num"], df["emissions_index"], color=RED, alpha=0.08, zorder=1)
    ax2.set_ylabel("Emissions Index (Base Year = 100)", fontsize=10, color=RED, labelpad=8)
    ax2.tick_params(axis="y", colors=RED)

    style_ax(
        ax1,
        title=f"Fig Q — UK Licensed Vehicle Stock vs Car NOX Emissions Index\nCorrelation r = {r:.2f}",
        xlabel="Year",
        ylabel="",
        grid_axis="y"
    )

    xticks = df["year_num"][::2]
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(df.loc[df.index[::2], "year"])

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(
        h1 + h2, l1 + l2,
        loc="lower right",
        frameon=False,
        fontsize=9
    )

    add_source(ax1, "NAEI_env0301_NOX.xlsx + Dft_veh0101_LicensedStock.xlsx")
    save_fig(fig, "Fig_Q_nox_emission_vs_vehicle_stock_index.png")

# Fig R — UK Automotive Supply-Chain Stress Index, 2020–2025
def fig_r_supply_chain_stress(fuel_price_df, fuel_type_df, lpi_df):
    fuel_price_df = prepare_year(fuel_price_df)
    fuel_type_df = prepare_year(fuel_type_df)

    df = pd.merge(
        fuel_price_df[["year", "petrol", "diesel"]],
        fuel_type_df[["year", "petrol", "diesel"]],
        on="year",
        how="inner",
        suffixes=("_price", "_regs")
    ).copy()

    df = df[df["year"].astype(int).between(2020, 2025)].copy()
    df["year_num"] = df["year"].astype(int)

    df["fuel_price_avg"] = (df["petrol_price"] + df["diesel_price"]) / 2
    df["ice_regs"] = df["petrol_regs"] + df["diesel_regs"]

    df["fuel_component"] = normalize_to_100(df["fuel_price_avg"])
    df["demand_component"] = 100 - normalize_to_100(df["ice_regs"])

    uk_lpi_mean = pd.to_numeric(lpi_df["UK"], errors="coerce").mean()
    logistics_scalar = 100 - (uk_lpi_mean / 5 * 100)
    df["logistics_component"] = logistics_scalar

    df["stress_index"] = (
        0.45 * df["fuel_component"] +
        0.35 * df["demand_component"] +
        0.20 * df["logistics_component"]
    )

    x = np.arange(len(df))
    years = df["year"].astype(str).tolist()

    fig, ax = plt.subplots(figsize=(13.2, 6.2))
    fig.patch.set_facecolor("white")

    # Main stress area and line
    ax.fill_between(
        x, df["stress_index"],
        alpha=0.09, color=RED, zorder=1
    )
    ax.plot(
        x, df["stress_index"],
        color=RED, linewidth=3.1,
        marker="o", markersize=8,
        markerfacecolor=RED,
        markeredgecolor="white",
        markeredgewidth=1.2,
        label="Composite Stress Index",
        zorder=5
    )

    # Secondary components — lighter visual weight
    ax.plot(
        x, df["fuel_component"],
        color=AMBER, linewidth=2.3,
        linestyle="--", alpha=0.82,
        label="Fuel Cost Component",
        zorder=3
    )

    ax.plot(
        x, df["demand_component"],
        color=PURPLE, linewidth=2.3,
        linestyle=":", alpha=0.82,
        label="ICE Demand Weakness Component",
        zorder=3
    )

    # Threshold line
    ax.axhline(
        70,
        color=RED, linestyle="--",
        linewidth=1.2, alpha=0.35,
        zorder=2
    )
    ax.text(
        x[-1] + 0.06, 72,
        "High-stress threshold",
        fontsize=8.5, color=RED, alpha=0.65,
        ha="left", va="bottom"
    )

    # Key annotations
    peak_pos = int(np.argmax(df["stress_index"].values))
    latest_pos = len(df) - 1

    # COVID / starting point
    ax.annotate(
        "COVID shock",
        xy=(0, df["stress_index"].iloc[0]),
        xytext=(0.3, df["stress_index"].iloc[0] + 2),
        fontsize=8.8,
        color=NAVY,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9)
    )

    # Peak
    ax.annotate(
        "Peak stress",
        xy=(peak_pos, df["stress_index"].iloc[peak_pos]),
        xytext=(peak_pos + 0.18, df["stress_index"].iloc[peak_pos] + 7),
        fontsize=8.8,
        color=NAVY,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9)
    )

    # Latest point
    ax.annotate(
        "Recent level",
        xy=(latest_pos, df["stress_index"].iloc[latest_pos]),
        xytext=(latest_pos + 0.18, df["stress_index"].iloc[latest_pos] +1),
        fontsize=8.8,
        color=NAVY,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9)
    )

    # Latest value
    ax.annotate(
        f"{df['stress_index'].iloc[-1]:.0f}",
        xy=(x[-1], df["stress_index"].iloc[-1]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9.5,
        color=RED,
        fontweight="bold"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(years, rotation=0)

    style_ax(
        ax,
        title="Fig R — UK Automotive Supply-Chain Stress Index, 2020–2025",
        xlabel="Year",
        ylabel="Stress Index (0–100)",
        grid_axis="y"
    )

    ax.set_ylim(0, 105)
    ax.set_xlim(-0.08, len(x) - 0.92)

    # Cleaner legend
    leg = ax.legend(
        loc="upper right",
        frameon=False,
        fontsize=9,
        handlelength=2.6
    )
    for line in leg.get_lines():
        line.set_linewidth(2.6)

    add_source(
        ax,
        "Derived from DESNZ fuel prices, SMMT fuel type registrations, and World Bank LPI"
    )

    save_fig(fig, "Fig_R_supply_chain_stress.png")

# Fig S — UK Annual Average GDP Growth
def fig_s_gdp_growth(df):
    df = prepare_year(df).copy()
    if df.empty:
        return

    recent = df[df["year"].astype(int).between(2000, 2025)].copy()
    recent["year"] = recent["year"].astype(int)

    years = recent["year"].values
    values = recent["gdp_qoq_avg"].values

    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    fig.patch.set_facecolor("white")

    # Positive / negative fill
    ax.fill_between(years, values, 0, where=(values >= 0), color=GREEN, alpha=0.12, zorder=1)
    ax.fill_between(years, values, 0, where=(values < 0), color=RED, alpha=0.10, zorder=1)

    # Main line
    ax.plot(
        years, values,
        color=NAVY, linewidth=2.5,
        marker="o", markersize=5.8,
        zorder=4
    )

    # Zero line
    ax.axhline(0, color=MUTED, linestyle="--", linewidth=1.2, alpha=0.8)

    # COVID shock annotation
    if 2020 in years:
        covid_val = recent.loc[recent["year"] == 2020, "gdp_qoq_avg"].iloc[0]
        ax.annotate(
            f"COVID shock\n{covid_val:.2f}%",
            xy=(2020, covid_val),
            xytext=(2021.2, covid_val - 1.5),
            fontsize=8.5,
            color=RED,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=0.9)
        )

    # Latest value label
    ax.annotate(
        f"{values[-1]:.2f}%",
        xy=(years[-1], values[-1]),
        xytext=(0, 8),
        textcoords="offset points",
        ha="center",
        fontsize=8.5,
        color=NAVY,
        fontweight="bold"
    )

    style_ax(
        ax,
        title=f"Fig S — UK Annual Average GDP Growth, {years.min()}–{years.max()}",
        xlabel="Year",
        ylabel="Average GDP QoQ Growth (%)",
        grid_axis="y",
        baseline=False
    )

    apply_format(ax, "percent")
    ax.set_xticks(years[::2])
    ax.set_xticklabels(years[::2], rotation=0)
    add_source(ax, "QNA_GDP.xlsx — data")
    save_fig(fig, "Fig_S_gdp_growth.png")

# Fig T — UK Vehicle Stock Index vs Car GHG Emissions Index
def fig_t_ghg_emission_vs_vehicle_stock(ghg_df, stock_df):
    ghg_df = prepare_year(ghg_df)
    stock_df = prepare_year(stock_df)

    df = pd.merge(
        ghg_df[["year", "cars"]],
        stock_df[["year", "cars"]],
        on="year",
        how="inner",
        suffixes=("_emissions", "_stock")
    ).copy()

    df = df[df["year"].astype(int).between(2006, 2024)].copy()
    df["year_num"] = df["year"].astype(int)

    base_stock = df["cars_stock"].iloc[0]
    base_em = df["cars_emissions"].iloc[0]

    df["stock_index"] = df["cars_stock"] / base_stock * 100
    df["emissions_index"] = df["cars_emissions"] / base_em * 100

    r = df["stock_index"].corr(df["emissions_index"])

    fig, ax1 = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("white")

    ax1.plot(
        df["year_num"], df["stock_index"],
        color=ACCENT, linewidth=2.6, marker="o",
        label="Licensed Cars Stock Index", zorder=4
    )
    ax1.fill_between(df["year_num"], df["stock_index"], color=ACCENT, alpha=0.10, zorder=1)
    ax1.set_ylabel("Vehicle Stock Index (Base Year = 100)", fontsize=10, color=ACCENT, labelpad=8)
    ax1.tick_params(axis="y", colors=ACCENT)

    ax2 = ax1.twinx()
    ax2.plot(
        df["year_num"], df["emissions_index"],
        color=RED, linewidth=2.6, marker="o", linestyle="--",
        label="Car Emissions Index", zorder=4
    )
    ax2.fill_between(df["year_num"], df["emissions_index"], color=RED, alpha=0.08, zorder=1)
    ax2.set_ylabel("Emissions Index (Base Year = 100)", fontsize=10, color=RED, labelpad=8)
    ax2.tick_params(axis="y", colors=RED)

    style_ax(
        ax1,
        title=f"Fig T — UK Licensed Vehicle Stock vs Car GHG Emissions Index\nCorrelation r = {r:.2f}",
        xlabel="Year",
        ylabel="",
        grid_axis="y"
    )

    xticks = df["year_num"][::2]
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(df.loc[df.index[::2], "year"])

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(
        h1 + h2, l1 + l2,
        loc="lower right",
        frameon=False,
        fontsize=9
    )

    add_source(ax1, "NAEI_env0301_NOX.xlsx + Dft_veh0101_LicensedStock.xlsx")
    save_fig(fig, "Fig_T_ghg_emission_vs_vehicle_stock_index.png")

# -----------------------------------------------------------------------------
# Main Function (Printing figure by linking to respective dataset)
# -----------------------------------------------------------------------------
def main():
    print("\n" + "=" * 60)
    print("Generating dissertation charts...")
    print("=" * 60)

    data = load_all_data(verbose=False)

    fig_a_smmt_fuel(data["smmt_fuel_type"])
    fig_b_bev_share(data["smmt_fuel_type"])
    fig_c_ev_charging(data["zapmap_ev_charging"])
    fig_d_sale_type(data["smmt_sale_type"])
    fig_e_vehicle_production(data["smmt_vehicle_production"])
    fig_f_global_sales(data["spgm_global_lv_sales"])
    fig_g_lpi(data["worldbank_lpi"])
    fig_h_iea_ev(data["iea_ev"])
    fig_i_nox_emissions(data["naei_env_nox"])
    fig_j_environmental_impact(
        data["ons_env_ghg"],
        data["desnz_env_fuel_price"],
        data["desnz_env_energy_consumption"]
    )
    fig_k_diesel_bev_crossover(data["smmt_fuel_type"])
    fig_l_cpih(data["mm23_cpih"])
    fig_m_insurance(data["ons_cpi_insurance"])
    fig_n_digital_maturity(data["digital_maturity"])
    fig_o_vehicle_stock(data["dft_lv_stock"])
    fig_p_fuel_price_vs_demand(
        data["desnz_env_fuel_price"],
        data["smmt_fuel_type"]
    )
    fig_q_nox_emission_vs_vehicle_stock(
        data["naei_env_nox"],
        data["dft_lv_stock"]
    )
    fig_r_supply_chain_stress(
        data["desnz_env_fuel_price"],
        data["smmt_fuel_type"],
        data["worldbank_lpi"]
    )
    fig_s_gdp_growth(data["qna_gdp"])
    fig_t_ghg_emission_vs_vehicle_stock(
        data["ons_env_ghg"],
        data["dft_lv_stock"]
    )

    print("\nAll charts generated successfully.")

if __name__ == "__main__":
    main()
