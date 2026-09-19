# =============================================================================
# dataset_loader.py
# =============================================================================

import os
from pathlib import Path
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# -----------------------------------------------------------------------------
# Data directory
# -----------------------------------------------------------------------------

DATA_DIR = Path("/Users/april/Documents/Project/data")

# =============================================================================

def file_path(file_name):
    """Full path for a dataset file inside the data folder, given its filename."""
    return DATA_DIR / file_name


def file_exists(file_name):
    """Check whether the loaded dataset file exists in the data folder or not."""
    return file_path(file_name).exists()


def log_source(df_name, loaded=True):
    """Simple message for dataset loading status."""
    tag = "[✓ Loaded]" if loaded else "[MISSING]"
    print(f"{tag} {df_name}")

# =============================================================================
# Individual dataset loaders
# =============================================================================
# 1. SMMT Sale Type (File Name: SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx)
def smmt_sale_type_dataset():
    """
    Load SMMT sale type dataset.
    Then, aggregate cleaned dataframe into annual totals.
    Returns columns:
    - year (string value)
    - total, cars, private, fleet, business, lcv (numeric values in thousands)
    - private_share,fleet_share (percentage values, rounded to 1 decimal place)
    """

    file_name = "SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="1.RegBySaleType", header=None)

    # Set correct column header row (Excel row 6 contains the real headers)
    HEADER_ROW = 5  # Excel row 6 (as 0-indexed in pandas)
    df.columns = df.iloc[HEADER_ROW].astype(str)
    df = df.iloc[HEADER_ROW + 1:].copy()
    df.columns = [str(col).strip() for col in df.columns]

    # Rename columns into standard names 
    col_rename = {}

    for col in df.columns:
        col_name = str(col).lower()
        
        if "month" in col_name:
            col_rename[col] = "date"
        
        elif "total cars and lcvs" in col_name and "nsa" in col_name:
            col_rename[col] = "total"
        
        elif "total cars" in col_name and "lcvs" not in col_name and "nsa" in col_name:
            col_rename[col] = "cars"
        
        elif "private cars" in col_name and "nsa" in col_name:
            col_rename[col] = "private"

        elif "fleet cars" in col_name and "nsa" in col_name:
            col_rename[col] = "fleet"
        
        elif "business cars" in col_name and "nsa" in col_name:
            col_rename[col] = "business"
        
        elif "lcvs" in col_name and "nsa" in col_name:
            col_rename[col] = "lcv"

    df = df.rename(columns=col_rename)

    # Keep only the columns that is needed for the analysis (if they exist in the dataset)
    wanted_cols = ["date", "total", "cars", "private", "fleet", "business", "lcv"]
    df = df[[col for col in wanted_cols if col in df.columns]].copy()
    
    # Basic datacleaning (fix date + drop invalid rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]) # drop rows with invalid NA date
    df["year"] = df["date"].dt.year

    value_cols = ["total", "cars", "private", "fleet", "business", "lcv"]
    value_cols = [col for col in value_cols if col in df.columns]
    for col in value_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0) # convert to numeric and fill missing values with 0 where annual totals are required

    # Aggregate to annual totals
    annual = df.groupby("year", as_index=False)[value_cols].sum()

    # Ensure available years
    annual = annual[annual["year"].between(2020, 2025)]
    annual = annual.sort_values("year")
    # Convert year to string
    annual["year"] = annual["year"].astype(str)
    # Convert volumes to thousands (assuming original data is in units, convert to thousands for better readability)
    annual[value_cols] = (annual[value_cols] / 1000).round(1)

    # Add fleet share
    if "private" in annual.columns and "cars" in annual.columns: # double check if both columns exist before calculating share
        annual["private_share"] = (annual["private"] / annual["cars"] * 100).round(1)

    if "fleet" in annual.columns and "cars" in annual.columns: # double check if both columns exist before calculating share
        annual["fleet_share"] = (annual["fleet"] / annual["cars"] * 100).round(1)
    
    # Final column order
    final_cols = [
        "year", "total", "cars", "private", "fleet", "business", "lcv", "private_share", "fleet_share"
    ]
    final_cols = [col for col in final_cols if col in annual.columns]

    log_source(file_name)
    return annual[final_cols].reset_index(drop=True)

# 2. SMMT Fuel Type (File Name: SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx)
def smmt_fuel_type_dataset():
    """
    Loading SMMT fuel type dataset.
    Then, aggregate cleaned SMMT dataframe into annual totals.
    Returns columns:
    - year (string value) 
    - petrol, diesel, hybrid, phev, bev, and total (numeric values in thousands)
    - bev_share, diesel_share (percentage values, rounded to 1 decimal place)
    """

    file_name = "SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="2.CarRegsByFuelType", header=None)

    # Set correct column header row (Excel row 6 contains the real headers)
    HEADER_ROW = 5  # Excel row 6 (as 0-indexed in pandas)
    df.columns = df.iloc[HEADER_ROW].astype(str)
    df = df.iloc[HEADER_ROW + 1:].copy()
    df.columns = [str(col).strip() for col in df.columns]

    # Rename columns into standard names 
    col_rename = {}

    for col in df.columns:
        col_name = str(col).lower()

        if "month" in col_name:
            col_rename[col] = "date"

        elif "petrol" in col_name and "nsa" in col_name:
            col_rename[col] = "petrol"

        elif "diesel" in col_name and "nsa" in col_name:
            col_rename[col] = "diesel"

        elif "bev" in col_name and "nsa" in col_name:
            col_rename[col] = "bev"

        elif "phev" in col_name and "nsa" in col_name:
            col_rename[col] = "phev"

        elif "hev" in col_name and "nsa" in col_name:
            col_rename[col] = "hybrid"

        elif "total cars" in col_name and "nsa" in col_name:
            col_rename[col] = "total"

    df = df.rename(columns=col_rename)

    # Keep only the columns that is needed for the analysis (if they exist in the dataset)
    wanted_cols = ["date", "petrol", "diesel", "hybrid", "phev", "bev", "total"]
    df = df[[col for col in wanted_cols if col in df.columns]].copy()
    
    # Basic datacleaning (fix date + drop invalid rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]) # drop rows with invalid NA date
    df["year"] = df["date"].dt.year

    value_cols = ["petrol", "diesel", "hybrid", "phev", "bev", "total"] 
    value_cols = [col for col in value_cols if col in df.columns]
    for col in value_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0) # convert to numeric and fill missing values with 0 where annual totals are required

    # Aggregate to annual totals
    annual = df.groupby("year", as_index=False)[value_cols].sum()

    # Ensure available years
    annual = annual[annual["year"].between(2020, 2025)]
    annual = annual.sort_values("year")
    # Convert year to string
    annual["year"] = annual["year"].astype(str)
    # Convert volumes to thousands (assuming original data is in units, convert to thousands for better readability)
    annual[value_cols] = (annual[value_cols] / 1000).round(1)
    
    # Add share metrics
    if "bev" in annual.columns and "total" in annual.columns: # double check if both columns exist before calculating share
        annual["bev_share"] = (annual["bev"] / annual["total"] * 100).round(1)

    if "diesel" in annual.columns and "total" in annual.columns: # double check if both columns exist before calculating share
        annual["diesel_share"] = (annual["diesel"] / annual["total"] * 100).round(1)

    # Final column order
    final_cols = [
        "year", "petrol", "diesel", "hybrid", "phev", "bev",
        "total", "bev_share", "diesel_share"
    ]
    final_cols = [col for col in final_cols if col in annual.columns]

    log_source(file_name)
    return annual[final_cols].reset_index(drop=True)

# 3. SMMT Vehicle Production (File Name: SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx)
def smmt_vehicle_production_dataset():
    """
    Loading SMMT vehicle production dataset.
    Then, aggregate cleaned dataframe into annual totals.
    Returns columns:
    - year (string value) 
    - total, cars, cvs (numetric values in thousands)
    - cars_exported, cars_domestic, cvs_exported, cvs_domestic (numetric values in thousands)
    - cars_export_share, cars_domestic_share (percentage values, rounded to 1 decimal place)
    """

    file_name = "SMMT_Vehicle_Reg_and_Prod_dataset_150126.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="3.VehicleProd", header=None)

    # Set correct column header row (Excel row 6 contains the real headers)
    HEADER_ROW = 5  # Excel row 6 (as 0-indexed in pandas)
    df.columns = df.iloc[HEADER_ROW].astype(str)
    df = df.iloc[HEADER_ROW + 1:].copy()
    df.columns = [str(col).strip() for col in df.columns]

    # Rename columns into standard names
    col_rename = {}

    for col in df.columns:
        col_name = str(col).lower()

        if "month" in col_name:
            col_rename[col] = "date"

        elif "all vehicles total" in col_name and "nsa" in col_name:
            col_rename[col] = "total"
            
        elif "cars total" in col_name and "nsa" in col_name:
            col_rename[col] = "cars"
            
        elif "cars exported" in col_name and "nsa" in col_name:
            col_rename[col] = "cars_exported"
            
        elif "cars domestic" in col_name and "nsa" in col_name:
            col_rename[col] = "cars_domestic"
            
        elif "cvs total" in col_name and "nsa" in col_name:
            col_rename[col] = "cvs"
            
        elif "cvs exported" in col_name and "nsa" in col_name:
            col_rename[col] = "cvs_exported"
            
        elif "cvs domestic" in col_name and "nsa" in col_name:
            col_rename[col] = "cvs_domestic"

    df = df.rename(columns=col_rename)

    # Keep only the columns that is needed for the analysis (if they exist in the dataset)
    wanted_cols = [
        "date", "total", "cars", "cars_exported", "cars_domestic",
        "cvs", "cvs_exported", "cvs_domestic"
    ]
    df = df[[col for col in wanted_cols if col in df.columns]].copy()
    
    # Basic datacleaning (fix date + drop invalid rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]) # drop rows with invalid NA date
    df["year"] = df["date"].dt.year

    value_cols = [
        "total", "cars", "cars_exported", "cars_domestic",
        "cvs", "cvs_exported", "cvs_domestic"
    ]
    value_cols = [col for col in value_cols if col in df.columns]
    for col in value_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0) # convert to numeric and fill missing values with 0 where annual totals are required

    # Aggregate to annual totals
    annual = df.groupby("year", as_index=False)[value_cols].sum()

    # Ensure available years
    annual = annual[annual["year"].between(2020, 2025)]
    annual = annual.sort_values("year")
    # Convert year to string
    annual["year"] = annual["year"].astype(str)
    # Convert volumes to thousands (assuming original data is in units, convert to thousands for better readability)
    annual[value_cols] = (annual[value_cols] / 1000).round(1)

    # shares calculation
    if "cars_exported" in annual.columns and "cars_domestic" in annual.columns and "cars" in annual.columns: # double check if all columns exist before calculating share
        annual["cars_export_share"] = (
            annual["cars_exported"] / annual["cars"] * 100
        ).round(1)

        annual["cars_domestic_share"] = (
            annual["cars_domestic"] / annual["cars"] * 100
        ).round(1)
    
    # Final column order
    final_cols = [
        "year", "total", "cars",
        "cars_exported", "cars_domestic",
        "cvs", "cvs_exported", "cvs_domestic",
        "cars_export_share", "cars_domestic_share"
    ]
    final_cols = [col for col in final_cols if col in annual.columns]

    log_source(file_name)
    return annual[final_cols].reset_index(drop=True)

# 4. Zapmap EV Charging (File Name: Zapmap_EV_Charging_Devices_February2026.xlsx)
def zapmap_ev_charging_dataset():
    """
    Loading Zapmap UK-based EV charging dataset.
    Returns columns:
    - quarter (string value, e.g. '2024 Q1')
    - date (string value, e.g. 'Mar 24')
    - total (integer value)
    - rapid (integer value, may contain NaN if unavailable)
    """

    file_name = "Zapmap_EV_Charging_Devices_February2026.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="Refined_Data", header=None)

    # Set correct column header row (Excel row 3 contains the real headers)
    HEADER_ROW = 2  # Excel row 3 (as 0-indexed in pandas)
    df.columns = df.iloc[HEADER_ROW].astype(str)
    df = df.iloc[HEADER_ROW + 1:].copy().reset_index(drop=True)
    df.columns = [str(col).strip() for col in df.columns]

    # Use positional access — col 0=Year, 1=Month, 2=Total, 3=Rapid
    df = df.rename(columns={
        df.columns[0]: "year",
        df.columns[1]: "month",
        df.columns[2]: "total",
        df.columns[3]: "rapid"
    })

    # Keep only the columns that is needed for the analysis (if they exist in the dataset)
    wanted_cols = ["year", "month", "total", "rapid"]
    df = df[[col for col in wanted_cols if col in df.columns]].copy()
    
    # Basic datacleaning (fix date + drop invalid rows)
    df["year"]  = pd.to_numeric(df["year"], errors="coerce")
    df["total"] = pd.to_numeric(df["total"], errors="coerce")
    df["rapid"] = pd.to_numeric(df["rapid"], errors="coerce")   

    df = df.dropna(subset=["year", "total"]) # Drop only critical missing values (keep rows with missing rapid)
    # Convert types
    df["year"] = df["year"].astype(int)
    df["total"] = df["total"].astype(int)

    # Convert month name to month number
    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    df["month"] = df["month"].astype(str).str.strip()
    df["month_num"] = df["month"].map(month_map)

    # Drop rows where month could not be parsed
    df = df.dropna(subset=["month_num"]).copy()
    df["month_num"] = df["month_num"].astype(int)

    # Build real dateframe 
    df["date_dt"] = pd.to_datetime(
        dict(year=df["year"], month=df["month_num"], day=1),
        errors="coerce"
    )
    # Sort properly by actual datetime
    df = df.dropna(subset=["date_dt"]).sort_values("date_dt")

    # Core Logic: Keep February only 
    df = df[df["month_num"] == 2].copy()

    # Final formatting 
    df["year"] = df["year"].astype(str)
    df["date"] = df["date_dt"].dt.strftime("%b %y")

    # Derived metric
    df["slow"] = df["total"] - df["rapid"]

    # reset index cleanly
    df = df.reset_index(drop=True)

    log_source(file_name)

    return df[["year", "date", "total", "rapid", "slow"]]

# 5. WorldBank LPI (File Name: WorldBank_Int_LPI_from_2007_to_2023.xlsx)
def worldbank_lpi_dataset():
    """
    Loading World Bank LPI dataset.
    Use 2018 data for both UK and Myanmar to ensure comparability,
    as Myanmar is missing in 2023 dataset.
    
    Returns columns:
    - LPI Dimensions (string value) 
    - UK, Myanmar (float value)
    """

    file_name = "WorldBank_Int_LPI_from_2007_to_2023.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="2018")
    # clean column names
    df.columns = [str(col).strip() for col in df.columns]

    # Filter for UK and Myanmar (2018 dataset structure)
    df_2018 = df[
        df["Country"].isin(["United Kingdom", "Myanmar"])
    ].copy()

    if df_2018.empty:
        return pd.DataFrame()

    # Map dimensions (2018 column names)
    map_dimension = {
        "Customs score": "Customs",
        "Infrastructure score": "Infrastructure",
        "International shipments score": "International Shipments",
        "Logistics quality and competence score": "Logistics Quality",
        "Tracking and tracing score": "Tracking",
        "Timeliness score": "Timeliness",
    }
    
    dimensions, uk_values, mm_values = [], [], []

    uk_row = df_2018[df_2018["Country"] == "United Kingdom"]
    mm_row = df_2018[df_2018["Country"] == "Myanmar"]

    if not uk_row.empty and not mm_row.empty:
        for col, label in map_dimension.items():
            if col in df_2018.columns:
                dimensions.append(label)
                uk_values.append(round(float(uk_row[col].values[0]), 2))
                mm_values.append(round(float(mm_row[col].values[0]), 2))
    
    # Final output
    final_output = pd.DataFrame({
        "LPI Dimensions": dimensions,
        "UK": uk_values,
        "Myanmar": mm_values
    })
    
    log_source(file_name)
    return final_output.reset_index(drop=True)

# 6. SPGM Global LV Sales (File Name: SPGM_Global_Auto_LVSales.xlsx)
def spgm_global_lv_sales_dataset():
    """
    Load S&P Global light vehicle sales data by region.

    Returns column values:
    - region (string)
    - s2024 (float, million units)
    - s2025 (float, million units)
    - s2026 (float, million units)
    - s2027 (float, million units)
    - s2028 (float, million units)
    - s2029 (float, million units)
    - s2030 (float, million units)
    - s2031 (float, million units)
    - s2032 (float, million units)
    """

    file_name = "SPGM_Global_Auto_LVSales.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="Data", header=None)

    # Set correct column header row (Excel row 5 contains the real headers)
    HEADER_ROW = 4  # Excel row 5 (as 0-indexed in pandas)
    df.columns = df.iloc[HEADER_ROW].astype(str)
    df = df.iloc[HEADER_ROW + 1:].copy()
    df.columns = [str(col).strip() for col in df.columns]
    
    # Standardise year column names like 2024.0 -> 2024
    rename_cols = {}
    for col in df.columns:
        col_str = str(col).strip()
        try:
            year_val = int(float(col_str))
            if 2024 <= year_val <= 2032:
                rename_cols[col] = str(year_val)
        except (ValueError, TypeError):
            pass

    df = df.rename(columns=rename_cols)

    # Keep rows with region labels
    df = df.dropna(subset=["Sales Region"])
    df = df[~df["Sales Region"].str.contains(
        "Data compiled|Source|©", case=False, na=False
    )]
    df["Sales Region"] = df["Sales Region"].astype(str).str.strip()
    df = df[~df["Sales Region"].str.lower().eq("total")].copy()

    # Convert year columns to numeric
    year_cols = ["2024", "2025", "2026", "2027", "2028", "2029", "2030", "2031", "2032"]

    for col in year_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[f"s{col}"] = (df[col] / 1_000_000).round(1)

    df = df.rename(columns={"Sales Region": "region"})
    
    # Final output
    final_cols = ["region"] + [f"s{year}" for year in year_cols if f"s{year}" in df.columns]

    log_source(file_name)
    return df[final_cols].reset_index(drop=True)

# 7. IEA EV Data (File Name: IEA_EVData_Explorer_2025.xlsx)
def iea_ev_dataset():
    """
    Load IEA EV sales share dataset for selected countries.

    Returns column values:
    - year (string value)
    - USA, UK, China, Germany, Norway, World (percentage values, rounded to 1 decimal place)
    """

    file_name = "IEA_EVData_Explorer_2025.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="GEVO_EV_2025")
    df.columns = [str(col).lower().strip() for col in df.columns]

    # Filter required data
    df = df[
        (df["parameter"] == "EV sales share") &
        (df["mode"] == "Cars") &
        (df["category"] == "Historical") &
        (df["unit"] == "percent")
    ].copy()

    # Map country names
    country_map = {
        "USA": "USA",
        "United Kingdom": "UK",
        "China": "China",
        "Germany": "Germany",
        "Norway": "Norway",
        "World": "World",
    }

    df = df[df["region_country"].isin(country_map.keys())].copy()
    df["country"] = df["region_country"].map(country_map)

    # Aggregate BEV + PHEV share
    df = df.groupby(["year", "country"], as_index=False)["value"].sum()

    # Reshape to wide format
    df = df.pivot(index="year", columns="country", values="value").reset_index()
    # Convert year to string
    df["year"] = df["year"].astype(str)

    # Final column order
    final_cols = ["year", "USA", "UK", "China", "Germany", "Norway", "World"]
    final_cols = [col for col in final_cols if col in df.columns]

    log_source(file_name)
    return df[final_cols].reset_index(drop=True)

# Data Validation Layer
def validate_df(df, name):
    if df.empty:
        print(f"[WARNING] {name} is empty")
        return

    if "year" in df.columns:
        if df["year"].isnull().any():
            print(f"[WARNING] {name} has missing year values")

        if df["year"].duplicated().any():
            print(f"[WARNING] {name} has duplicate years")

        try:
            year_check = pd.to_numeric(df["year"], errors="coerce")
            if not year_check.is_monotonic_increasing:
                print(f"[WARNING] {name} is not sorted by year")
        except:
            pass

# Data parsing function
def parse_wide(file_name, sheet_name):
    """
    Read wide ONS/ DfT / DESNZ / NAEI style tables where:
    - Excel row 6 : headers
    - data starts from Excel row 7
    Returns:
    - df
    - year_cols
    - year_labels
    """
    df = pd.read_excel(file_path(file_name), sheet_name=sheet_name, header=None)

    HEADER_ROW = 5
    df.columns = df.iloc[HEADER_ROW].astype(str)
    df = df.iloc[HEADER_ROW + 1:].copy()
    df.columns = [str(col).strip() for col in df.columns]
    df = df.dropna(how="all")

    year_cols = []
    year_labels = []

    for col in df.columns:
        parts = str(col).split(" ")
        for part in parts:
            part = part.strip().strip("(").strip(")")
            if part.isdigit() and 1988 <= int(part) <= 2035:
                year_cols.append(col)
                year_labels.append(part)
                break

    # REMOVE non-absolute rows 
    df = df[~df.iloc[:, 0].astype(str).str.contains(
        "percentage|change|index", case=False, na=False
    )]
    return df, year_cols, year_labels


# 8. ONS Env-Data GHG (File Name: ONS_env0201_GHG.xlsx)
def ons_env_ghg_dataset():
    """
    Load UK road transport GHG emissions by vehicle type.

    Returns column values:
    - year (string)
    - cars, vans, hgv, buses (MtCO2e)
    """

    file_name = "ONS_env0201_GHG.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # call parse function
    df, year_cols, year_labels = parse_wide(file_name, "ENV0201a_source")
    
    
    mode_col = "Transport type and mode"
    df[mode_col] = df[mode_col].astype(str).str.strip()
    
    row_map = {
        "cars": "Cars and taxis",
        "vans": "Light vans",
        "hgv": "Heavy goods vehicles",
        "buses": "Buses and coaches",
    }

    result = {"year": year_labels}

    for new_name, source_name in row_map.items():
        row = df[df[mode_col].str.contains(source_name, case=False, na=False)]
        if not row.empty:
            values = []
            for col in year_cols:
                try:
                    values.append(round(float(row[col].values[0]), 2))
                except:
                    values.append(None)
            result[new_name] = values

    # Final output
    final_output = pd.DataFrame(result).dropna()
    final_output = final_output.groupby("year", as_index=False).mean()
    final_output = final_output.sort_values("year")
    
    log_source(file_name)
    return final_output.reset_index(drop=True)

# 9. NAEI Env_Data Emission Index (File Name: NAEI_env0302_Emission.xlsx)
def naei_env_emission_index_dataset():
    """
    Load hot-exhaust emission index table.
    """
    file_name = "NAEI_env0302_Emission.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="ENV0302a_emissions", header=None)

    # Set correct column header row (Excel row 5 contains the real headers)
    HEADER_ROW = 4
    df.columns = df.iloc[HEADER_ROW].astype(str)
    df = df.iloc[HEADER_ROW + 1:].copy()
    df.columns = [str(col).strip() for col in df.columns]

    # Rename columns into standard names 
    col_rename = {}

    for col in df.columns:
        col_name = str(col).lower()
        if "fuel and transport" in col_name:
            col_rename[col] = "fuel_type"
        elif "description" in col_name:
            col_rename[col] = "description"
        elif "regulation class" in col_name:
            col_rename[col] = "euro_class"
        elif "time period" in col_name:
            col_rename[col] = "period"
        elif "carbon monoxide" in col_name:
            col_rename[col] = "CO"
        elif "hydrocarbon" in col_name:
            col_rename[col] = "NMVOCs"
        elif "nitrogen oxide" in col_name:
            col_rename[col] = "NOx"
        elif "particulate" in col_name:
            col_rename[col] = "PM"
            
    df = df.rename(columns=col_rename)

    # Keep only the columns that is needed for the analysis (if they exist in the dataset)
    wanted_cols = ["fuel_type", "description", "euro_class", "period", "CO", "NMVOCs", "NOx", "PM"]
    df = df[[col for col in wanted_cols if col in df.columns]].copy()
    
    # Final column order
    for col in ["CO", "NMVOCs", "NOx", "PM"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

    log_source(file_name)
    return df.reset_index(drop=True)

# 10. NAEI Env_Data NOX Emission (File Name: NAEI_env0301_NOX.xlsx)
def naei_env_nox_dataset():
    """
    Load road transport NOx data.

    Returns:
    - year
    - cars, vans, hgv, buses
    """

    file_name = "NAEI_env0301_NOX.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    df, year_cols, year_labels = parse_wide(file_name, "ENV0301c_NOx")

    mode_col = "Transport type and mode"
    df[mode_col] = df[mode_col].astype(str).str.strip()

    row_map = {
        "cars": "Cars and taxis",
        "vans": "Light vans",
        "hgv": "Heavy goods vehicles",
        "buses": "Buses and coaches",
    }

    result = {"year": year_labels}

    for new_name, source_name in row_map.items():
        row = df[df[mode_col].str.contains(source_name, case=False, na=False)]
        if not row.empty:
            values = []
            for col in year_cols:
                try:
                    values.append(round(float(row[col].values[0]), 2))
                except:
                    values.append(None)
            result[new_name] = values

    # Final output
    final_output = pd.DataFrame(result).dropna()
    final_output = final_output.groupby("year", as_index=False).mean()
    final_output = final_output.sort_values("year")

    log_source(file_name)
    return final_output.reset_index(drop=True)

# 11. DESNZ Env_Data Fuel Price (File Name: DESNZ_env0105_FuelPrice.xlsx)
def desnz_env_fuel_price_dataset():
    """
    Load petrol and diesel pump prices.

    Returns:
    - year
    - petrol
    - diesel
    """
    file_name = "DESNZ_env0105_FuelPrice.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    df, year_cols, year_labels = parse_wide(file_name, "ENV0105a_fuel_prices")

    fuel_col = "Fuel and tax type"
    df[fuel_col] = df[fuel_col].astype(str).str.strip()

    petrol_row = df[df[fuel_col].str.contains("Petrol.*Total price|Petrol, Total", case=False, na=False)]
    diesel_row = df[df[fuel_col].str.contains("Diesel.*Total price|Diesel, Total", case=False, na=False)]

    years = []
    petrol_vals = []
    diesel_vals = []

    for col, year in zip(year_cols, year_labels):
        try:
            petrol_vals.append(round(float(petrol_row[col].values[0]), 1))
            diesel_vals.append(round(float(diesel_row[col].values[0]), 1))
            years.append(year)
        except:
            pass

    # Final output
    final_output = pd.DataFrame({
        "year": years,
        "petrol": petrol_vals,
        "diesel": diesel_vals
    }).dropna()
    final_output = final_output.groupby("year", as_index=False).mean()
    final_output = final_output.sort_values("year")

    log_source(file_name)
    return final_output.reset_index(drop=True)

# 12. DESNZ Env_Data Energy Consumption (File Name: DESNZ_env0101_Energy_Consumption.xlsx)
def desnz_env_energy_consumption_dataset():
    """
    Load road transport petroleum consumption data.
    """
    file_name = "DESNZ_env0101_Energy_Consumption.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    df, year_cols, year_labels = parse_wide(file_name, "ENV0101a_road_transport")

    fuel_col = "Fuel type and road transport type"
    df[fuel_col] = df[fuel_col].astype(str).str.strip()

    row_map = {
        "petrol_cars": "Petrol, Cars and taxis",
        "diesel_cars": "Diesel, Cars and taxis",
        "total_petrol": "Total petrol consumption",
        "total_diesel": "Total diesel consumption",
    }

    result = {"year": year_labels}

    for new_name, source_name in row_map.items():
        row = df[df[fuel_col].str.contains(source_name, case=False, na=False)]
        if not row.empty:
            values = []
            for col in year_cols:
                try:
                    values.append(round(float(row[col].values[0]), 3))
                except:
                    values.append(None)
            result[new_name] = values

    # Final output
    final_output = pd.DataFrame(result).dropna()
    final_output = final_output.groupby("year", as_index=False).mean()
    final_output = final_output.sort_values("year")

    log_source(file_name)
    return final_output.reset_index(drop=True)

# 13. MM23 CPIH Data (File Name: MM23_CPIH.xlsx)
def mm23_cpih_dataset():
    """
    Load annual CPIH data.
    """
    file_name = "MM23_CPIH.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    df = pd.read_excel(file_path(file_name), sheet_name="Annual")
    df.columns = [str(col).strip() for col in df.columns]

    rename = {}
    for col in df.columns:
        col_name = str(col).lower()
        if "year" in col_name:
            rename[col] = "year"
        elif "cpih" in col_name or "value" in col_name:
            rename[col] = "cpih"

    df = df.rename(columns=rename)

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["cpih"] = pd.to_numeric(df["cpih"], errors="coerce")
    df = df.dropna(subset=["year", "cpih"])
    df["year"] = df["year"].astype(int).astype(str)
    df = df.sort_values("year")
    df["cpih"] = df["cpih"].round(1)

    log_source(file_name)
    return df[["year", "cpih"]].reset_index(drop=True)

# 14. ONS CPI Insurance (File Name: ONS_CPI_Insurance.xlsx)
def ons_cpi_insurance_dataset():
    """
    Load annual car insurance CPI index.
    """
    file_name = "ONS_CPI_Insurance.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()
    
    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="CPI Car Insurance", header=None)
    # Set correct column header row (Excel row 5 contains the real headers)
    HEADER_ROW = 4
    df.columns = df.iloc[HEADER_ROW].astype(str)
    df = df.iloc[HEADER_ROW + 1:].copy()
    df.columns = [str(col).strip() for col in df.columns]

    rename = {}
    for col in df.columns:
        col_name = str(col).lower()
        if "year" in col_name:
            rename[col] = "year"
        elif "annual" in col_name or "average" in col_name:
            rename[col] = "annual_avg"

    df = df.rename(columns=rename)

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["annual_avg"] = pd.to_numeric(df["annual_avg"], errors="coerce")
    df = df.dropna(subset=["year", "annual_avg"])
    df["year"] = df["year"].astype(int).astype(str)
    df = df.sort_values("year")
    df["annual_avg"] = df["annual_avg"].round(1)

    log_source(file_name)
    return df[["year", "annual_avg"]].reset_index(drop=True)

# 15. QNA GDP Data (File Name: QNA_GDP.xlsx)
def qna_gdp_dataset():
    """
    Load UK annual average GDP quarter-on-quarter growth.

    Returns columns:
    - year (string)
    - gdp_qoq_avg (float)
    """

    file_name = "QNA_GDP.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="data", header=None)
    # Set correct column header row (Excel row 9 contains the real headers)
    HEADER_ROW = 8
    df.columns = df.iloc[HEADER_ROW].astype(str)
    df = df.iloc[HEADER_ROW + 1:].copy()
    df.columns = [str(col).strip() for col in df.columns]

    rename = {}
    for col in df.columns:
        col_name = str(col).lower()
        if "date" in col_name:
            rename[col] = "quarter"
        elif "value" in col_name:
            rename[col] = "gdp_qoq"

    df = df.rename(columns=rename)

    # Clean values
    df["quarter"] = df["quarter"].astype(str).str.strip()
    df["gdp_qoq"] = pd.to_numeric(df["gdp_qoq"], errors="coerce")
    df = df.dropna(subset=["quarter", "gdp_qoq"]).copy()

    # Extract year and quarter
    df["year"] = df["quarter"].str.extract(r"(\d{4})")
    df["qtr"] = df["quarter"].str.extract(r"(Q[1-4])")

    # Keep valid rows only
    df = df.dropna(subset=["year", "qtr"]).copy()
    df["year"] = df["year"].astype(int)

    # Aggregate to annual average
    annual = (
        df.groupby("year", as_index=False)["gdp_qoq"]
        .mean()
        .rename(columns={"gdp_qoq": "gdp_qoq_avg"})
    )

    # Round values
    annual["gdp_qoq_avg"] = annual["gdp_qoq_avg"].round(2)

    # Convert year to string for chart consistency
    annual["year"] = annual["year"].astype(str)

    log_source(file_name)
    return annual[["year", "gdp_qoq_avg"]].reset_index(drop=True)

# 16. DfT Licensed Vehicle Stock Data (File Name: Dft_veh0101_LicensedStock.xlsx)
def dft_lv_stock_dataset():
    """
    Load licensed vehicle stock data.
    Returns columns:
    - year (integer)
    - cars, lgvs, hgvs, total (numeric values in thousands)
    - cars_share, lgv_share, hgv_share (percentage of total, rounded to 1 decimal place)
    """
    
    # Load file
    file_name = "Dft_veh0101_LicensedStock.xlsx"

    if not file_exists(file_name):
        log_source(file_name, loaded=False)
        return pd.DataFrame()

    # loading raw sheet
    df = pd.read_excel(file_path(file_name), sheet_name="VEH0101a_Lic")
    df.columns = [str(col).strip() for col in df.columns]

    # Keep only Great Britain and United Kingdom
    df = df[df["Geography"].isin(["Great Britain", "United Kingdom"])].copy()

    # Rename relevant columns
    df = df.rename(columns={
        "Geography": "geography",
        "Date": "date",
        "Cars": "cars",
        "Light goods vehicles": "lgvs",
        "Heavy goods vehicles": "hgvs",
        "Total": "total"
    })

    # Convert vehicle columns to numeric
    value_cols = ["cars", "lgvs", "hgvs", "total"]
    for col in value_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce") # Convert vehicle columns to numeric

    # Basic datacleaning (fix date + drop invalid rows)
    # Extract year and quarter
    df["year"] = df["date"].astype(str).str.extract(r"(\d{4})")
    df["quarter"] = df["date"].astype(str).str.extract(r"(Q[1-4])")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # Keep only required years and quarter
    df = df[df["year"].between(2000, 2025)]
    df = df[df["quarter"] == "Q4"].copy()
    # Drop Invalid Rows
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    df = df.sort_values(["year", "geography"])
    df = df.drop_duplicates(subset=["year"], keep="last")

    #Add Share Columns
    if "cars" in df.columns:
        df["cars_share"] = (df["cars"] / df["total"] * 100).round(1)
    if "lgvs" in df.columns:    
        df["lgv_share"]  = (df["lgvs"] / df["total"] * 100).round(1)
    if "hgvs" in df.columns:
        df["hgv_share"]  = (df["hgvs"] / df["total"] * 100).round(1)

    # Final output
    final_cols = [
        "year", "cars", "lgvs", "hgvs", "total",
        "cars_share", "lgv_share", "hgv_share"
    ]
    final_cols = [col for col in final_cols if col in df.columns]

    log_source(file_name)
    return df[final_cols].reset_index(drop=True)

# 17. Self-assessed Digital maturity of UK & Myanmar across 6 Dimensions
def digital_maturity_dataset():
    """
    Load self-created digital maturity comparison across 6 Dimensions.
    """

    self_assessed_data= pd.DataFrame({
        "Dimension": [
            "Data & Analytics",
            "IT Governance",
            "System Integration",
            "Change Management",
            "E-commerce",
            "After-Sales Digital"
        ],
        "UK": [7.9, 7.4, 7.8, 6.2, 7.8, 7.2],
        "Myanmar": [2.8, 2.1, 2.6, 3.5, 3.5, 1.9],
    })
    
    return self_assessed_data.reset_index(drop=True)

# =============================================================================
# MASTER LOADER
# =============================================================================

def load_all_data(verbose=True):
    """
    Load all datasets and return them.
    Each is a cleaned pandas DataFrame ready for analysis or charting.
    """

    if verbose:
        print("\n" + "=" * 60)
        print("Data Loader — COMP6013 Project")
        print(f"Data directory: {DATA_DIR}")
        print(f"Directory exists: {DATA_DIR.exists()}")
        print("=" * 60)

    data = {
        "smmt_sale_type": smmt_sale_type_dataset(),
        "smmt_fuel_type": smmt_fuel_type_dataset(),
        "smmt_vehicle_production": smmt_vehicle_production_dataset(),
        "zapmap_ev_charging": zapmap_ev_charging_dataset(),
        "worldbank_lpi": worldbank_lpi_dataset(),
        "spgm_global_lv_sales": spgm_global_lv_sales_dataset(),
        "iea_ev": iea_ev_dataset(),
        "ons_env_ghg": ons_env_ghg_dataset(),
        "naei_env_emission_index": naei_env_emission_index_dataset(),
        "naei_env_nox": naei_env_nox_dataset(),
        "desnz_env_fuel_price": desnz_env_fuel_price_dataset(),
        "desnz_env_energy_consumption": desnz_env_energy_consumption_dataset(),
        "mm23_cpih": mm23_cpih_dataset(),
        "ons_cpi_insurance": ons_cpi_insurance_dataset(),
        "qna_gdp": qna_gdp_dataset(),
        "dft_lv_stock": dft_lv_stock_dataset(),
        "digital_maturity": digital_maturity_dataset(),
    }

    for name, df in data.items():
        if isinstance(df, pd.DataFrame) and "year" in df.columns:
            validate_df(df, name)
    
    if verbose:
        print(f"\nLoaded {len(data)} datasets:\n")
        for name, df in data.items():
            print(f"{name:<30} {df.shape}")

    return data

# =============================================================================
# DATASETINSPECTOR
# =============================================================================

def inspect_data(data, rows=5):
    """Quick inspection of all datasets."""
    print("\n" + "=" * 60)
    print("DATA INSPECTION")
    print("=" * 60)

    for name, df in data.items():
        print(f"\n{name:<30} {df.shape}")
        if not df.empty:
            print(df.head(rows).to_string(index=False))
        else:
            print("⚠ EMPTY")

# =============================================================================
# STANDALONE RUN (+ BASIC DATA VALIDATION BY DEBUG PRINTS)
# =============================================================================

if __name__ == "__main__":
    all_data = load_all_data(verbose=True)
    inspect_data(all_data, rows=10)
    