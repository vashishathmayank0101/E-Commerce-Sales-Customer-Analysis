"""
analysis.py
-----------
All aggregation, KPI computation, and business-insight functions.
Each function accepts a clean DataFrame and returns a summary DataFrame or scalar.
"""

import pandas as pd
import numpy as np


# ─── 1. Overall KPIs ─────────────────────────────────────────────────────────

def overall_kpis(df: pd.DataFrame) -> dict:
    """Return top-level business KPIs."""
    delivered = df[df["Order_Status"] == "Delivered"]
    return {
        "Total Orders": len(df),
        "Total Customers": df["Customer_ID"].nunique(),
        "Total Products": df["Product"].nunique(),
        "Total Sales (₹)": round(df["Calculated_Sales"].sum(), 2),
        "Total Profit (₹)": round(df["Profit"].sum(), 2),
        "Avg Order Value (₹)": round(df["Calculated_Sales"].mean(), 2),
        "Overall Profit Margin (%)": round(
            df["Profit"].sum() / df["Calculated_Sales"].sum() * 100, 2
        ),
        "Delivered Orders": len(delivered),
        "Cancelled Orders": len(df[df["Order_Status"] == "Cancelled"]),
        "Returned Orders": len(df[df["Order_Status"] == "Returned"]),
        "Delivery Rate (%)": round(len(delivered) / len(df) * 100, 2),
    }


# ─── 2. Sales by Category ─────────────────────────────────────────────────────

def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Category")
        .agg(
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Orders=("Order_ID", "count"),
            Avg_Order_Value=("Calculated_Sales", "mean"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    grp["Profit_Margin_%"] = (grp["Total_Profit"] / grp["Total_Sales"] * 100).round(2)
    grp["Total_Sales"] = grp["Total_Sales"].round(2)
    grp["Total_Profit"] = grp["Total_Profit"].round(2)
    grp["Avg_Order_Value"] = grp["Avg_Order_Value"].round(2)
    return grp


# ─── 3. Sales by Product ──────────────────────────────────────────────────────

def sales_by_product(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    grp = (
        df.groupby(["Product", "Category"])
        .agg(
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Quantity=("Quantity", "sum"),
            Total_Orders=("Order_ID", "count"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(top_n)
    )
    grp["Profit_Margin_%"] = (grp["Total_Profit"] / grp["Total_Sales"] * 100).round(2)
    return grp.round(2)


# ─── 4. Sales by City ─────────────────────────────────────────────────────────

def sales_by_city(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("City")
        .agg(
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Orders=("Order_ID", "count"),
            Avg_Order_Value=("Calculated_Sales", "mean"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    grp["Profit_Margin_%"] = (grp["Total_Profit"] / grp["Total_Sales"] * 100).round(2)
    return grp.round(2)


# ─── 5. Customer Analysis ─────────────────────────────────────────────────────

def customer_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Customer_Type")
        .agg(
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Orders=("Order_ID", "count"),
            Unique_Customers=("Customer_ID", "nunique"),
            Avg_Order_Value=("Calculated_Sales", "mean"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    grp["Profit_Margin_%"] = (grp["Total_Profit"] / grp["Total_Sales"] * 100).round(2)
    return grp.round(2)


def top_customers(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    grp = (
        df.groupby("Customer_ID")
        .agg(
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Orders=("Order_ID", "count"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(top_n)
    )
    return grp.round(2)


# ─── 6. Monthly / Quarterly Trends ───────────────────────────────────────────

def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby(["Year", "Month", "Month_Name"])
        .agg(
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Orders=("Order_ID", "count"),
        )
        .reset_index()
        .sort_values(["Year", "Month"])
    )
    grp["MoM_Sales_Growth_%"] = grp["Total_Sales"].pct_change().mul(100).round(2)
    return grp.round(2)


def quarterly_trend(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby(["Year", "Quarter"])
        .agg(
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Orders=("Order_ID", "count"),
        )
        .reset_index()
        .sort_values(["Year", "Quarter"])
    )
    return grp.round(2)


# ─── 7. Payment Method Analysis ──────────────────────────────────────────────

def payment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Payment_Method")
        .agg(
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Orders=("Order_ID", "count"),
            Avg_Order_Value=("Calculated_Sales", "mean"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    grp["Share_%"] = (grp["Total_Orders"] / grp["Total_Orders"].sum() * 100).round(2)
    return grp.round(2)


# ─── 8. Order Status Analysis ────────────────────────────────────────────────

def order_status_summary(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Order_Status")
        .agg(
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Orders=("Order_ID", "count"),
            Total_Profit=("Profit", "sum"),
        )
        .reset_index()
    )
    grp["Share_%"] = (grp["Total_Orders"] / grp["Total_Orders"].sum() * 100).round(2)
    return grp.round(2)


# ─── 9. Discount Impact ──────────────────────────────────────────────────────

def discount_impact(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bucket orders by discount band and compare avg profit margin.
    """
    bins   = [-0.001, 0.0, 0.10, 0.20, 1.0]
    labels = ["No Discount", "1–10%", "11–20%", "21%+"]
    df = df.copy()
    df["Discount_Band"] = pd.cut(df["Discount"], bins=bins, labels=labels)
    grp = (
        df.groupby("Discount_Band", observed=True)
        .agg(
            Total_Orders=("Order_ID", "count"),
            Total_Sales=("Calculated_Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Avg_Profit_Margin=("Profit_Margin_%", "mean"),
        )
        .reset_index()
    )
    return grp.round(2)


# ─── 10. Business Insights ───────────────────────────────────────────────────

def generate_insights(df: pd.DataFrame, kpis: dict) -> list[str]:
    """
    Derive plain-English actionable business insights.
    Returns a list of insight strings.
    """
    insights = []

    # Best category
    cat = sales_by_category(df).iloc[0]
    insights.append(
        f"🏆 **Top Category:** {cat['Category']} leads with ₹{cat['Total_Sales']:,.2f} in sales "
        f"({cat['Profit_Margin_%']:.1f}% margin)."
    )

    # Worst category by margin
    cat_margin = sales_by_category(df).sort_values("Profit_Margin_%")
    worst = cat_margin.iloc[0]
    insights.append(
        f"⚠️ **Low-Margin Category:** {worst['Category']} has the lowest profit margin "
        f"({worst['Profit_Margin_%']:.1f}%). Review pricing or cost structure."
    )

    # Best city
    city = sales_by_city(df).iloc[0]
    insights.append(
        f"📍 **Top City:** {city['City']} generates ₹{city['Total_Sales']:,.2f} in revenue — "
        f"a key market to prioritise."
    )

    # Customer type best performer
    ct = customer_type_summary(df).iloc[0]
    insights.append(
        f"👥 **Best Customer Segment:** {ct['Customer_Type']} customers account for "
        f"₹{ct['Total_Sales']:,.2f} in sales. Focus retention efforts here."
    )

    # Cancellation / return alert
    cancel_rate = kpis["Cancelled Orders"] / kpis["Total Orders"] * 100
    return_rate = kpis["Returned Orders"] / kpis["Total Orders"] * 100
    if cancel_rate > 5:
        insights.append(
            f"🚨 **Cancellation Alert:** {cancel_rate:.1f}% of orders are cancelled. "
            f"Investigate fulfilment bottlenecks."
        )
    if return_rate > 5:
        insights.append(
            f"🔄 **Return Alert:** {return_rate:.1f}% of orders are returned. "
            f"Review product quality or description accuracy."
        )

    # Discount insight
    di = discount_impact(df)
    no_disc = di[di["Discount_Band"] == "No Discount"]["Avg_Profit_Margin"].values
    high_disc = di[di["Discount_Band"] == "21%+"]["Avg_Profit_Margin"].values
    if len(no_disc) and len(high_disc):
        insights.append(
            f"💸 **Discount Impact:** Orders with no discount average "
            f"{no_disc[0]:.1f}% margin vs {high_disc[0]:.1f}% for 21%+ discounts. "
            f"Tighten discount strategy."
        )

    # Top product
    prod = sales_by_product(df, top_n=1).iloc[0]
    insights.append(
        f"📦 **Best-Selling Product:** {prod['Product']} with ₹{prod['Total_Sales']:,.2f} in sales "
        f"({prod['Total_Quantity']} units sold)."
    )

    # Overall margin
    insights.append(
        f"📊 **Overall Profit Margin:** {kpis['Overall Profit Margin (%)']:.2f}%. "
        f"{'Healthy margin — sustain current pricing.' if kpis['Overall Profit Margin (%)'] > 20 else 'Below 20% — consider cost optimisation.'}"
    )

    return insights
