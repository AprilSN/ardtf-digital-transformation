# =============================================================================
# charts.py — Interactive Plotly chart layer
# =============================================================================

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import CHART_LAYOUT, C


# -----------------------------------------------------------------------------
# Base helpers
# -----------------------------------------------------------------------------
def apply_layout(fig, title="", xtitle="", ytitle="", height=340):
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, x=0, font=dict(size=13, color=C["accent"])),
        xaxis_title=xtitle,
        yaxis_title=ytitle,
        height=height,
    )
    return fig


def _corr_text(a, b):
    r = pd.Series(a).corr(pd.Series(b))
    if pd.isna(r):
        return "No clear relationship"
    if r >= 0.7:
        return f"Strong positive relationship (r = {r:.2f})"
    if r >= 0.4:
        return f"Moderate positive relationship (r = {r:.2f})"
    if r > -0.4:
        return f"Weak relationship (r = {r:.2f})"
    if r > -0.7:
        return f"Moderate negative relationship (r = {r:.2f})"
    return f"Strong negative relationship (r = {r:.2f})"


def _add_corr_annotation(fig, x, y, text):
    fig.add_annotation(
        x=x,
        y=y,
        text=text,
        showarrow=False,
        font=dict(size=10, color=C["navy"]),
        bgcolor="rgba(255,255,255,0.88)",
        bordercolor=C["border"],
        borderwidth=1,
    )


# =============================================================================
# MARKET
# =============================================================================
def fuel_mix(df):
    fig = go.Figure()

    for key, name, color in [
        ("petrol", "Petrol", C["petrol"]),
        ("diesel", "Diesel", C["diesel"]),
        ("hybrid", "Hybrid", C["hybrid"]),
        ("phev", "PHEV", C["phev"]),
        ("bev", "BEV", C["bev"]),
    ]:
        fig.add_bar(
            x=df["year"],
            y=df[key],
            name=name,
            marker_color=color,
            hovertemplate=f"{name}: %{{y:.1f}}k<br>Year: %{{x}}<extra></extra>",
        )

    fig.update_layout(barmode="stack")
    return apply_layout(fig, "UK Car Registrations by Fuel Type", ytitle="Registrations (thousand)")


def bev_vs_diesel(df):
    fig = go.Figure()

    fig.add_scatter(
        x=df["year"],
        y=df["bev_share"],
        name="BEV share",
        mode="lines+markers",
        line=dict(color=C["bev"], width=3),
        hovertemplate="BEV: %{y:.1f}%<br>Year: %{x}<extra></extra>",
    )

    fig.add_scatter(
        x=df["year"],
        y=df["diesel_share"],
        name="Diesel share",
        mode="lines+markers",
        line=dict(color=C["diesel"], width=3),
        hovertemplate="Diesel: %{y:.1f}%<br>Year: %{x}<extra></extra>",
    )

    return apply_layout(fig, "BEV Growth vs Diesel Decline", ytitle="Share of new car market (%)")


def sale_type_stacked(df):
    fig = go.Figure()

    for key, name, color in [
        ("private", "Private", C["navy"]),
        ("fleet", "Fleet", C["green"]),
        ("business", "Business", C["amber"]),
    ]:
        fig.add_bar(
            x=df["year"],
            y=df[key],
            name=name,
            marker_color=color,
            hovertemplate=f"{name}: %{{y:.1f}}k<br>Year: %{{x}}<extra></extra>",
        )

    fig.update_layout(barmode="stack")
    return apply_layout(fig, "Sales Composition by Channel", ytitle="Registrations (thousand)")


def sale_share_line(df):
    fig = go.Figure()

    fig.add_scatter(
        x=df["year"],
        y=df["private_share"],
        name="Private share",
        mode="lines+markers",
        line=dict(color=C["navy"], width=3),
    )

    fig.add_scatter(
        x=df["year"],
        y=df["fleet_share"],
        name="Fleet share",
        mode="lines+markers",
        line=dict(color=C["green"], width=3),
    )

    return apply_layout(fig, "Private vs Fleet Share Shift", ytitle="Share (%)")


def vehicle_production(df):
    fig = go.Figure()

    fig.add_bar(
        x=df["year"], y=df["cars"],
        name="Cars produced",
        marker_color=C["navy"],
        hovertemplate="Cars: %{y:.1f}k<br>Year: %{x}<extra></extra>",
    )
    fig.add_bar(
        x=df["year"], y=df["cvs"],
        name="CVs produced",
        marker_color=C["amber"],
        hovertemplate="CVs: %{y:.1f}k<br>Year: %{x}<extra></extra>",
    )

    fig.update_layout(barmode="group")
    return apply_layout(fig, "UK Vehicle Production", ytitle="Units produced (thousand)")


def vehicle_export_mix(df):
    fig = go.Figure()

    fig.add_scatter(
        x=df["year"], y=df["cars_export_share"],
        name="Cars exported",
        mode="lines+markers",
        line=dict(color=C["green"], width=3),
        hovertemplate="Export share: %{y:.1f}%<br>Year: %{x}<extra></extra>",
    )
    fig.add_scatter(
        x=df["year"], y=df["cars_domestic_share"],
        name="Cars domestic",
        mode="lines+markers",
        line=dict(color=C["amber"], width=3),
        hovertemplate="Domestic share: %{y:.1f}%<br>Year: %{x}<extra></extra>",
    )

    return apply_layout(fig, "Vehicle Production Split: Export vs Domestic", ytitle="Share (%)")


# =============================================================================
# INFRASTRUCTURE / SUPPLY
# =============================================================================
def charging_growth(df):
    fig = go.Figure()

    fig.add_bar(
        x=df["year"], y=df["slow"],
        name="Slow",
        marker_color=C["bev"],
        hovertemplate="Slow: %{y:,.0f}<br>Year: %{x}<extra></extra>",
    )
    fig.add_bar(
        x=df["year"], y=df["rapid"],
        name="Rapid",
        marker_color=C["amber"],
        hovertemplate="Rapid: %{y:,.0f}<br>Year: %{x}<extra></extra>",
    )
    fig.add_scatter(
        x=df["year"], y=df["total"],
        name="Total",
        mode="lines+markers",
        line=dict(color=C["green"], width=3),
        hovertemplate="Total: %{y:,.0f}<br>Year: %{x}<extra></extra>",
    )

    fig.update_layout(barmode="stack")
    return apply_layout(fig, "EV Charging Infrastructure Growth", ytitle="Charging devices")


def lpi_compare(df):
    fig = go.Figure()

    fig.add_bar(
        y=df["dimension"],
        x=df["UK"],
        name="UK",
        orientation="h",
        marker_color=C["navy"],
        hovertemplate="UK<br>%{y}: %{x:.2f}<extra></extra>",
    )

    fig.add_bar(
        y=df["dimension"],
        x=df["Myanmar"],
        name="Myanmar",
        orientation="h",
        marker_color=C["amber"],
        hovertemplate="Myanmar<br>%{y}: %{x:.2f}<extra></extra>",
    )

    fig.update_layout(barmode="group")
    return apply_layout(fig, "World Bank LPI Comparison: UK vs Myanmar", xtitle="Score (0–5)", ytitle="")


def fuel_vs_demand(df_fuel_price, df_fuel):
    fuel_price = df_fuel_price.copy()
    fuel = df_fuel.copy()

    fuel_price["year"] = fuel_price["year"].astype(int)
    fuel["year"] = fuel["year"].astype(int)

    merged = pd.merge(
        fuel_price[["year", "petrol", "diesel"]],
        fuel[["year", "petrol", "diesel"]],
        on="year",
        how="inner",
        suffixes=("_price", "_regs")
    ).copy()

    merged = merged[merged["year"].between(2020, 2025)].copy()
    merged = merged.sort_values("year").reset_index(drop=True)

    merged["fuel_price_avg"] = (merged["petrol_price"] + merged["diesel_price"]) / 2
    merged["ice_regs"] = merged["petrol_regs"] + merged["diesel_regs"]

    base = merged["ice_regs"].iloc[0]
    merged["demand_index"] = merged["ice_regs"] / base * 100

    r = merged["fuel_price_avg"].corr(merged["demand_index"])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_scatter(
        x=merged["year"].astype(str),
        y=merged["fuel_price_avg"],
        name="Average fuel price (p/L)",
        mode="lines+markers",
        line=dict(color=C["amber"], width=3),
        fill="tozeroy",
        fillcolor="rgba(217,119,6,0.08)",
        hovertemplate="Fuel price<br>Year: %{x}<br>%{y:.1f} p/L<extra></extra>",
        secondary_y=False,
    )

    fig.add_scatter(
        x=merged["year"].astype(str),
        y=merged["demand_index"],
        name="ICE demand index (2020 = 100)",
        mode="lines+markers",
        line=dict(color=C["sky"], width=3, dash="dash"),
        fill="tozeroy",
        fillcolor="rgba(74,127,165,0.08)",
        hovertemplate="ICE demand<br>Year: %{x}<br>%{y:.1f}<extra></extra>",
        secondary_y=True,
    )

    peak_row = merged.loc[merged["fuel_price_avg"].idxmax()]
    low_row = merged.loc[merged["demand_index"].idxmin()]

    fig.add_annotation(
        x=str(int(peak_row["year"])),
        y=peak_row["fuel_price_avg"],
        text=f"Fuel price peak: {peak_row['fuel_price_avg']:.1f}p",
        showarrow=True,
        arrowhead=2,
        ax=-70,
        ay=-25,
        font=dict(size=10, color=C["amber"]),
        arrowcolor=C["amber"],
        yref="y"
    )

    fig.add_annotation(
        x=str(int(low_row["year"])),
        y=low_row["demand_index"],
        text=f"ICE demand low: {low_row['demand_index']:.1f}",
        showarrow=True,
        arrowhead=2,
        ax=70,
        ay=25,
        font=dict(size=10, color=C["sky"]),
        arrowcolor=C["sky"],
        yref="y2"
    )

    fig.update_yaxes(title_text="Average Fuel Price (Pence/Litre)", secondary_y=False)
    fig.update_yaxes(title_text="ICE Demand Index (2020 = 100)", secondary_y=True)

    fig = apply_layout(
        fig,
        f"Combined Fuel Price vs ICE Registration Demand<br><span style='font-size:12px;'>Correlation r = {r:.2f}</span>",
        xtitle="Year",
        height=380
    )

    return fig


def supply_chain_stress(df_fuel_price, df_fuel, df_lpi):
    fuel_price = df_fuel_price.copy()
    fuel = df_fuel.copy()
    lpi = df_lpi.copy()

    fuel_price["year"] = pd.to_numeric(fuel_price["year"], errors="coerce")
    fuel["year"] = pd.to_numeric(fuel["year"], errors="coerce")

    merged = pd.merge(
        fuel_price[["year", "petrol", "diesel"]],
        fuel[["year", "petrol", "diesel"]],
        on="year",
        how="inner",
        suffixes=("_price", "_regs")
    ).dropna().copy()

    merged["year"] = merged["year"].astype(int)
    merged = (
        merged[merged["year"].between(2020, 2025)]
        .sort_values("year")
        .reset_index(drop=True)
    )

    if merged.empty:
        return apply_layout(go.Figure(), "Supply-Chain Stress Index", ytitle="Index (0–100)")

    merged["fuel_price_avg"] = (merged["petrol_price"] + merged["diesel_price"]) / 2
    merged["ice_regs"] = merged["petrol_regs"] + merged["diesel_regs"]

    def minmax_100(series):
        s_min, s_max = series.min(), series.max()
        if s_max == s_min:
            return pd.Series([50.0] * len(series), index=series.index)
        return (series - s_min) / (s_max - s_min) * 100

    merged["fuel_component"] = minmax_100(merged["fuel_price_avg"])
    merged["demand_component"] = 100 - minmax_100(merged["ice_regs"])

    uk_lpi_mean = pd.to_numeric(lpi["UK"], errors="coerce").mean()
    logistics_component = 100 - (uk_lpi_mean / 5 * 100)
    merged["logistics_component"] = logistics_component

    merged["stress_index"] = (
        0.45 * merged["fuel_component"] +
        0.35 * merged["demand_component"] +
        0.20 * merged["logistics_component"]
    ).round(1)

    fig = go.Figure()

    fig.add_scatter(
        x=merged["year"],
        y=merged["stress_index"],
        name="Composite stress index",
        mode="lines+markers",
        line=dict(color=C["red"], width=3),
        fill="tozeroy",
        fillcolor="rgba(220,38,38,0.10)",
        hovertemplate="Stress index<br>Year: %{x}<br>%{y:.1f}<extra></extra>",
    )

    fig.add_scatter(
        x=merged["year"],
        y=merged["fuel_component"],
        name="Fuel cost component",
        mode="lines+markers",
        line=dict(color=C["amber"], width=2.4, dash="dash"),
        hovertemplate="Fuel cost<br>Year: %{x}<br>%{y:.1f}<extra></extra>",
    )

    fig.add_scatter(
        x=merged["year"],
        y=merged["demand_component"],
        name="Demand weakness component",
        mode="lines+markers",
        line=dict(color=C["purple"], width=2.4, dash="dot"),
        hovertemplate="Demand weakness<br>Year: %{x}<br>%{y:.1f}<extra></extra>",
    )

    fig.add_hline(y=70, line_dash="dash", line_color=C["amber"])
    fig.add_hline(y=40, line_dash="dot", line_color=C["muted"])

    peak_row = merged.loc[merged["stress_index"].idxmax()]
    latest_row = merged.iloc[-1]

    fig.add_annotation(
        x=int(peak_row["year"]),
        y=peak_row["stress_index"],
        text="Peak stress",
        showarrow=True,
        arrowhead=2,
        ax=-40,
        ay=-25,
        font=dict(size=10, color=C["red"]),
        arrowcolor=C["red"]
    )

    fig.add_annotation(
        x=int(latest_row["year"]),
        y=latest_row["stress_index"],
        text=f"Latest: {latest_row['stress_index']:.1f}",
        showarrow=True,
        arrowhead=2,
        ax=45,
        ay=-25,
        font=dict(size=10, color=C["navy"]),
        arrowcolor=C["navy"]
    )

    fig = apply_layout(fig, "Supply-Chain Stress Index", ytitle="Index (0–100)")

    fig.update_xaxes(
        tickmode="linear",
        dtick=1,
        tickformat="d"
    )

    fig.update_yaxes(range=[0, 100])

    return fig

def supply_chain_stress_text(df_fuel_price, df_fuel, df_lpi):
    fuel_price = df_fuel_price.copy()
    fuel = df_fuel.copy()
    lpi = df_lpi.copy()

    fuel_price["year"] = fuel_price["year"].astype(int)
    fuel["year"] = fuel["year"].astype(int)

    merged = pd.merge(
        fuel_price[["year", "petrol", "diesel"]],
        fuel[["year", "petrol", "diesel"]],
        on="year",
        how="inner",
        suffixes=("_price", "_regs")
    ).copy()

    merged = merged[merged["year"].between(2020, 2025)].copy()
    if merged.empty:
        return "Supply-chain pressure cannot be summarised because the merged time series is empty."

    merged["fuel_price_avg"] = (merged["petrol_price"] + merged["diesel_price"]) / 2
    merged["ice_regs"] = merged["petrol_regs"] + merged["diesel_regs"]

    peak_fuel_row = merged.loc[merged["fuel_price_avg"].idxmax()]
    low_demand_row = merged.loc[merged["ice_regs"].idxmin()]

    uk_lpi_mean = pd.to_numeric(lpi["UK"], errors="coerce").mean()
    mm_lpi_mean = pd.to_numeric(lpi["Myanmar"], errors="coerce").mean()
    logistics_gap = uk_lpi_mean - mm_lpi_mean

    return (
        f"Average ICE fuel prices peaked in {int(peak_fuel_row['year'])}, while combined petrol and diesel "
        f"registrations reached their weakest point in {int(low_demand_row['year'])}. "
        f"The UK–Myanmar logistics capability gap averages {logistics_gap:.2f} points on the World Bank LPI, "
        f"showing that supply-chain pressure is shaped not only by fuel-cost volatility, but also by structural "
        f"differences in infrastructure, tracking, and operational resilience."
    )

# =============================================================================
# GLOBAL
# =============================================================================
def global_sales(df):
    fig = go.Figure()

    year_cols = [c for c in df.columns if c.startswith("s20")]
    for col in year_cols:
        fig.add_bar(
            y=df["region"],
            x=df[col],
            name=col.replace("s", ""),
            orientation="h",
            hovertemplate=f"{col.replace('s', '')}: %{{x:.1f}}M<br>%{{y}}<extra></extra>",
        )

    fig.update_layout(barmode="group")
    return apply_layout(fig, "Global Vehicle Sales by Region", xtitle="Million units", height=420)


def ev_share_global(df):
    fig = go.Figure()

    palette = {
        "UK": C["navy"],
        "China": C["red"],
        "Germany": C["amber"],
        "Norway": C["green"],
        "World": C["muted"],
    }

    for col in df.columns:
        if col != "year":
            fig.add_scatter(
                x=df["year"],
                y=df[col],
                name=col,
                mode="lines+markers" if col == "UK" else "lines",
                line=dict(color=palette.get(col, C["sky"]), width=3 if col == "UK" else 2),
            )

    return apply_layout(fig, "EV Adoption by Country", ytitle="EV share of new car sales (%)")


# =============================================================================
# DIGITAL
# =============================================================================
def digital_gap(df):
    fig = go.Figure()

    fig.add_bar(
        y=df["dimension"],
        x=df["UK"],
        name="UK",
        orientation="h",
        marker_color=C["navy"],
    )
    fig.add_bar(
        y=df["dimension"],
        x=df["Myanmar"],
        name="Myanmar",
        orientation="h",
        marker_color=C["amber"],
    )

    fig.update_layout(barmode="group")
    return apply_layout(fig, "Digital Capability Gap", xtitle="Score", height=340)


# =============================================================================
# MACRO
# =============================================================================

def gdp_growth(df):
    colors = [C["red"] if v < 0 else C["navy"] for v in df["gdp_qoq_avg"]]

    fig = go.Figure(go.Bar(
        x=df["year"],
        y=df["gdp_qoq_avg"],
        marker_color=colors,
        marker_opacity=0.85,
        hovertemplate="Year: %{x}<br>GDP growth: %{y:.2f}%<extra></extra>",
    ))

    fig.add_hline(y=0, line_dash="dash", line_color=C["muted"], line_width=1)

    return apply_layout(
        fig,
        "UK GDP Growth",
        xtitle="Year",
        ytitle="Average Annual GDP Growth (%)",
        height=340
    )

def inflation(df):
    fig = go.Figure()

    fig.add_scatter(
        x=df["year"],
        y=df["cpih"],
        mode="lines+markers",
        line=dict(color=C["amber"], width=3),
        fill="tozeroy",
        fillcolor="rgba(217,119,6,0.08)",
        hovertemplate="CPIH: %{y:.1f}%<br>Year: %{x}<extra></extra>",
    )

    fig.add_hline(y=2, line_dash="dash", line_color=C["muted"])
    return apply_layout(fig, "CPIH Inflation", ytitle="Inflation (%)")


def insurance_index(df):
    fig = go.Figure()

    fig.add_scatter(
        x=df["year"],
        y=df["annual_avg"],
        mode="lines+markers",
        line=dict(color=C["red"], width=3),
        fill="tozeroy",
        fillcolor="rgba(220,38,38,0.08)",
        hovertemplate="Index: %{y:.1f}<br>Year: %{x}<extra></extra>",
    )

    return apply_layout(fig, "Car Insurance Price Index", ytitle="Index")


# =============================================================================
# ENVIRONMENT
# =============================================================================
def ghg_trend(df):
    fig = go.Figure()

    for key, name, color in [
        ("cars", "Cars", C["bev"]),
        ("vans", "Vans", C["amber"]),
        ("hgv", "HGV", C["red"]),
        ("buses", "Buses", C["purple"]),
    ]:
        fig.add_scatter(
            x=df["year"],
            y=df[key],
            stackgroup="one",
            name=name,
            line=dict(color=color),
            hovertemplate=f"{name}: %{{y:.2f}}<br>Year: %{{x}}<extra></extra>",
        )

    return apply_layout(fig, "Transport Emissions (GHG)", ytitle="MtCO2e")


def nox_emissions(df):
    fig = go.Figure()

    for key, name, color in [
        ("cars", "Cars", C["bev"]),
        ("vans", "Vans", C["amber"]),
        ("hgv", "HGV", C["red"]),
        ("buses", "Buses", C["purple"]),
    ]:
        fig.add_bar(
            x=df["year"],
            y=df[key],
            name=name,
            marker_color=color,
            hovertemplate=f"{name}: %{{y:.2f}}<br>Year: %{{x}}<extra></extra>",
        )

    fig.update_layout(barmode="stack")
    return apply_layout(fig, "NOx Emissions by Vehicle Type", ytitle="ktNOx")


def fuel_prices(df):
    fig = go.Figure()

    fig.add_scatter(
        x=df["year"],
        y=df["petrol"],
        name="Petrol",
        mode="lines+markers",
        line=dict(color=C["petrol"], width=3),
    )
    fig.add_scatter(
        x=df["year"],
        y=df["diesel"],
        name="Diesel",
        mode="lines+markers",
        line=dict(color=C["diesel"], width=3),
    )

    return apply_layout(fig, "Fuel Prices", ytitle="Pence per litre")


def nox_vs_vehicles(df_nox, df_vehicle_stock):
    nox = df_nox.copy()
    stock = df_vehicle_stock.copy()

    nox["year"] = nox["year"].astype(int)
    stock["year"] = stock["year"].astype(int)

    nox["total_nox"] = nox[["cars", "vans", "hgv", "buses"]].sum(axis=1)

    merged = pd.merge(
        nox[["year", "total_nox"]],
        stock[["year", "total"]],
        on="year",
        how="inner"
    ).copy()

    corr = merged["total_nox"].corr(merged["total"])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_bar(
        x=merged["year"].astype(str),
        y=merged["total_nox"],
        name="Total NOx",
        marker_color=C["red"],
        opacity=0.75,
        hovertemplate="Year: %{x}<br>Total NOx: %{y:.1f} kt<extra></extra>",
        secondary_y=False
    )

    fig.add_scatter(
        x=merged["year"].astype(str),
        y=merged["total"],
        name="Licensed Vehicles",
        mode="lines+markers",
        line=dict(color=C["navy"], width=3),
        marker=dict(size=7),
        hovertemplate="Year: %{x}<br>Licensed vehicles: %{y:,.0f}<extra></extra>",
        secondary_y=True
    )

    fig.add_annotation(
        x=merged["year"].astype(str).iloc[len(merged) // 2],
        y=merged["total_nox"].max() * 0.85,
        text=f"**Correlation:** {corr:.2f}",
        showarrow=False,
        font=dict(size=10, color=C["navy"]),
        bgcolor="rgba(255,255,255,0.85)"
    )

    fig.update_yaxes(title_text="Total NOx (kt)", secondary_y=False)
    fig.update_yaxes(title_text="Licensed Vehicles", secondary_y=True)

    return apply_layout(
        fig,
        "Road NOx Emissions vs Licensed Vehicle Stock",
        xtitle="Year",
        height=360
    )

# =============================================================================
# CORRELATION / ANALYSIS
# =============================================================================
def fuel_price_vs_demand_scatter(df):
    fig = go.Figure()

    fig.add_scatter(
        x=df["price"],
        y=df["demand"],
        mode="markers+text",
        text=df["month"],
        textposition="top center",
        marker=dict(size=10, color=C["red"], opacity=0.75),
        hovertemplate="Price: %{x:.1f}<br>Demand: %{y:.1f}<br>%{text}<extra></extra>",
        name="Observed period",
    )

    text = _corr_text(df["price"], df["demand"])
    _add_corr_annotation(fig, df["price"].min(), df["demand"].max(), text)

    return apply_layout(fig, "Fuel Price vs Demand Correlation", "Fuel price index", "Demand index")


def emission_vs_vehicle_stock(df_ghg, df_stock):
    ghg = df_ghg.copy()
    ghg["total_ghg"] = ghg[["cars", "vans", "hgv", "buses"]].sum(axis=1)
    ghg["year"] = ghg["year"].astype(str)

    stock = df_stock.copy()
    stock["year"] = stock["year"].astype(str)

    merged = pd.merge(
        ghg[["year", "total_ghg"]],
        stock[["year", "total_vehicles"]],
        on="year",
        how="inner"
    ).copy()

    fig = go.Figure()

    fig.add_scatter(
        x=merged["total_vehicles"],
        y=merged["total_ghg"],
        mode="markers+text",
        text=merged["year"],
        textposition="top center",
        marker=dict(size=10, color=C["navy"], opacity=0.75),
        hovertemplate="Vehicles: %{x:.1f}<br>GHG: %{y:.2f}<br>Year: %{text}<extra></extra>",
    )

    text = _corr_text(merged["total_vehicles"], merged["total_ghg"])
    _add_corr_annotation(fig, merged["total_vehicles"].min(), merged["total_ghg"].max(), text)

    return apply_layout(fig, "Emissions vs Vehicle Stock", "Licensed vehicles", "Total road GHG")


def energy_vs_fuel_price(df_energy, df_fuel_price):
    energy = df_energy.copy()
    fuel = df_fuel_price.copy()

    energy["year"] = energy["year"].astype(str)
    fuel["year"] = fuel["year"].astype(str)

    merged = pd.merge(
        energy[["year", "total_petrol", "total_diesel"]],
        fuel[["year", "petrol", "diesel"]],
        on="year",
        how="inner"
    ).copy()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_scatter(
        x=merged["year"],
        y=merged["total_petrol"],
        name="Petrol consumption",
        line=dict(color=C["petrol"], width=3),
        secondary_y=False,
    )
    fig.add_scatter(
        x=merged["year"],
        y=merged["petrol"],
        name="Petrol price",
        line=dict(color=C["navy"], width=2, dash="dash"),
        secondary_y=True,
    )

    fig.update_yaxes(title_text="Consumption", secondary_y=False)
    fig.update_yaxes(title_text="Price (p/litre)", secondary_y=True)

    return apply_layout(fig, "Energy Use vs Fuel Price", height=360)