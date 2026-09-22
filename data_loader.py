"""
data_loader.py
--------------
Handles loading, validating, cleaning, and feature engineering
for the E-Commerce Sales & Customer Analysis dataset.
"""

import os
import pandas as pd
import numpy as np


# ─── Path resolution ──────────────────────────────────────────────────────────
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_CSV = os.path.join(_THIS_DIR, "..", "ecommerce_sales_customer_analysis_dataset.csv")


def load_raw(filepath: str = _DEFAULT_CSV) -> pd.DataFrame:
    """Read the CSV and return a raw DataFrame."""
    df = pd.read_csv(filepath, parse_dates=["Order_Date"])
    return df


def validate(df: pd.DataFrame) -> dict:
    """
    Inspect the raw DataFrame and return a quality-report dict:
      - total_rows
      - missing_values  (per column)
      - duplicate_rows
      - negative_quantity
      - negative_unit_price
    """
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "negative_quantity": int((df["Quantity"] < 0).sum()),
        "negative_unit_price": int((df["Unit_Price"] < 0).sum()),
        "invalid_discount": int(((df["Discount"] < 0) | (df["Discount"] > 1)).sum()),
    }
    return report


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare the dataset:
    1. Drop exact duplicate rows.
    2. Drop rows where critical fields are null.
    3. Convert Order_Date to datetime (if not already).
    4. Strip whitespace from string columns.
    5. Clip Discount to [0, 1].
    6. Remove rows with Quantity <= 0 or Unit_Price <= 0.
    """
    df = df.copy()

    # 1. Remove duplicates
    df.drop_duplicates(inplace=True)

    # 2. Drop rows missing critical fields
    critical = ["Order_ID", "Order_Date", "Customer_ID", "Product",
                "Category", "City", "Quantity", "Unit_Price", "Discount"]
    df.dropna(subset=critical, inplace=True)

    # 3. Ensure datetime
    if not pd.api.types.is_datetime64_any_dtype(df["Order_Date"]):
        df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df.dropna(subset=["Order_Date"], inplace=True)

    # 4. Strip whitespace from object columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # 5. Clip discount
    df["Discount"] = df["Discount"].clip(0, 1)

    # 6. Remove non-positive numeric rows
    df = df[(df["Quantity"] > 0) & (df["Unit_Price"] > 0)]

    df.reset_index(drop=True, inplace=True)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived columns:
    - Calculated_Sales  = Quantity × Unit_Price × (1 − Discount)
    - Profit_Margin_%   = (Profit / Calculated_Sales) × 100
    - Month             = month number of Order_Date
    - Month_Name        = abbreviated month name
    - Quarter           = calendar quarter
    - Year              = year
    - Revenue_Bucket    = Low / Medium / High based on Calculated_Sales
    """
    df = df.copy()

    # Step 4 requirement: recalculate sales
    df["Calculated_Sales"] = (
        df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"])
    ).round(2)

    # Profit margin
    df["Profit_Margin_%"] = np.where(
        df["Calculated_Sales"] > 0,
        (df["Profit"] / df["Calculated_Sales"] * 100).round(2),
        0.0,
    )

    # Time-based features
    df["Year"]       = df["Order_Date"].dt.year
    df["Month"]      = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Quarter"]    = df["Order_Date"].dt.quarter.apply(lambda q: f"Q{q}")

    # Revenue bucket
    q33 = df["Calculated_Sales"].quantile(0.33)
    q66 = df["Calculated_Sales"].quantile(0.66)
    df["Revenue_Bucket"] = pd.cut(
        df["Calculated_Sales"],
        bins=[-np.inf, q33, q66, np.inf],
        labels=["Low", "Medium", "High"],
    )

    return df


def get_clean_data(filepath: str = _DEFAULT_CSV) -> tuple[pd.DataFrame, dict]:
    """
    Full pipeline: load → validate → clean → feature-engineer.
    Returns (processed_df, quality_report).
    """
    raw = load_raw(filepath)
    report = validate(raw)
    cleaned = clean(raw)
    final = engineer_features(cleaned)
    return final, report
