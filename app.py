"""
app.py  –  E-Commerce Sales & Customer Analytics Dashboard
Run with:  streamlit run ecommerce_project/app.py
"""

import sys
import os

# Allow imports from the project folder regardless of launch directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_loader import get_clean_data
from analysis import (
    overall_kpis,
    sales_by_category,
    sales_by_product,
    sales_by_city,
    customer_type_summary,
    top_customers,
    monthly_trend,
    quarterly_trend,
    payment_analysis,
    order_status_summary,
    discount_impact,
    generate_insights,
)

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Main background */
    .main { background-color: #f8f9fb; }

    /* KPI cards */
    .kpi-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 18px 22px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        text-align: center;
        border-top: 4px solid #3b82f6;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #1e293b;
        margin: 4px 0;
    }
    .kpi-label {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Section headers */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e293b;
        border-left: 4px solid #3b82f6;
        padding-left: 10px;
        margin: 20px 0 10px 0;
    }

    /* Insight cards */
    .insight-card {
        background: #eff6ff;
        border-left: 5px solid #3b82f6;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 0.93rem;
        color: #1e293b;
        line-height: 1.6;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1e293b;
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* Tables */
    .dataframe th {
        background-color: #3b82f6 !important;
        color: white !important;
        font-weight: 600 !important;
    }

    div[data-testid="metric-container"] {
        background: #fff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Colour palette ──────────────────────────────────────────────────────────
COLORS = px.colors.qualitative.Bold
CATEGORY_COLORS = {
    "Electronics": "#3b82f6",
    "Fashion": "#f59e0b",
    "Sports": "#10b981",
    "Beauty": "#ec4899",
    "Home & Kitchen": "#8b5cf6",
}

# ─── Data loading (cached) ───────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading and cleaning dataset…")
def load_data():
    return get_clean_data()


df_full, quality_report = load_data()

# ─── Sidebar filters ─────────────────────────────────────────────────────────
st.sidebar.image(
    "https://img.icons8.com/fluency/96/shopping-cart.png", width=60
)
st.sidebar.markdown("## 🛒 E-Commerce Analytics")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🔍 Filters")

all_categories = sorted(df_full["Category"].unique().tolist())
sel_categories = st.sidebar.multiselect(
    "Category", all_categories, default=all_categories
)

all_cities = sorted(df_full["City"].unique().tolist())
sel_cities = st.sidebar.multiselect("City", all_cities, default=all_cities)

all_ctypes = sorted(df_full["Customer_Type"].unique().tolist())
sel_ctypes = st.sidebar.multiselect(
    "Customer Type", all_ctypes, default=all_ctypes
)

all_statuses = sorted(df_full["Order_Status"].unique().tolist())
sel_statuses = st.sidebar.multiselect(
    "Order Status", all_statuses, default=all_statuses
)

min_date = df_full["Order_Date"].min().date()
max_date = df_full["Order_Date"].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small style='color:#94a3b8'>Data: 1 000 orders · 2025</small>",
    unsafe_allow_html=True,
)

# ─── Apply filters ───────────────────────────────────────────────────────────
df = df_full.copy()
if sel_categories:
    df = df[df["Category"].isin(sel_categories)]
if sel_cities:
    df = df[df["City"].isin(sel_cities)]
if sel_ctypes:
    df = df[df["Customer_Type"].isin(sel_ctypes)]
if sel_statuses:
    df = df[df["Order_Status"].isin(sel_statuses)]
if isinstance(date_range, tuple) and len(date_range) == 2:
    df = df[
        (df["Order_Date"].dt.date >= date_range[0])
        & (df["Order_Date"].dt.date <= date_range[1])
    ]

if df.empty:
    st.warning("No data matches the selected filters. Please adjust the sidebar.")
    st.stop()

kpis = overall_kpis(df)

# ─── Title ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='background:linear-gradient(90deg,#1e3a5f,#3b82f6);
                padding:28px 32px;border-radius:12px;margin-bottom:24px;'>
        <h1 style='color:white;margin:0;font-size:2rem;'>
            🛒 E-Commerce Sales & Customer Analysis
        </h1>
        <p style='color:#bfdbfe;margin:6px 0 0 0;font-size:1rem;'>
            Comprehensive analytics dashboard — 2025 dataset
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Navigation tabs ─────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 Overview",
    "📦 Products & Categories",
    "🏙️ Locations",
    "👥 Customers",
    "📅 Time Trends",
    "💳 Payments & Discounts",
    "🔍 Data Quality",
    "💡 Insights",
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("### 📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🛍️ Total Orders",    f"{kpis['Total Orders']:,}")
    col2.metric("💰 Total Sales",     f"₹{kpis['Total Sales (₹)']:,.0f}")
    col3.metric("📈 Total Profit",    f"₹{kpis['Total Profit (₹)']:,.0f}")
    col4.metric("📉 Profit Margin",   f"{kpis['Overall Profit Margin (%)']:.2f}%")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("👤 Customers",       f"{kpis['Total Customers']:,}")
    col6.metric("🏷️ Products",        f"{kpis['Total Products']:,}")
    col7.metric("💵 Avg Order Value", f"₹{kpis['Avg Order Value (₹)']:,.2f}")
    col8.metric("✅ Delivery Rate",   f"{kpis['Delivery Rate (%)']:.1f}%")

    st.markdown("---")

    # Order status donut + Sales vs Profit bar side by side
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">Order Status Distribution</div>',
                    unsafe_allow_html=True)
        os_df = order_status_summary(df)
        fig_os = px.pie(
            os_df,
            names="Order_Status",
            values="Total_Orders",
            hole=0.55,
            color="Order_Status",
            color_discrete_map={
                "Delivered": "#10b981",
                "Cancelled": "#ef4444",
                "Returned": "#f59e0b",
            },
        )
        fig_os.update_traces(textposition="outside", textinfo="percent+label")
        fig_os.update_layout(
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20),
            height=340,
        )
        st.plotly_chart(fig_os, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Sales vs Profit by Category</div>',
                    unsafe_allow_html=True)
        cat_df = sales_by_category(df)
        fig_cat = go.Figure()
        fig_cat.add_trace(go.Bar(
            name="Sales",
            x=cat_df["Category"],
            y=cat_df["Total_Sales"],
            marker_color="#3b82f6",
            text=cat_df["Total_Sales"].apply(lambda x: f"₹{x/1e5:.1f}L"),
            textposition="outside",
        ))
        fig_cat.add_trace(go.Bar(
            name="Profit",
            x=cat_df["Category"],
            y=cat_df["Total_Profit"],
            marker_color="#10b981",
            text=cat_df["Total_Profit"].apply(lambda x: f"₹{x/1e5:.1f}L"),
            textposition="outside",
        ))
        fig_cat.update_layout(
            barmode="group",
            height=340,
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            yaxis_title="Amount (₹)",
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # Revenue Bucket distribution
    st.markdown('<div class="section-header">Revenue Bucket Distribution</div>',
                unsafe_allow_html=True)
    bucket_df = (
        df.groupby("Revenue_Bucket", observed=True)
        .agg(Orders=("Order_ID", "count"), Sales=("Calculated_Sales", "sum"))
        .reset_index()
    )
    fig_bucket = px.bar(
        bucket_df,
        x="Revenue_Bucket",
        y="Orders",
        color="Revenue_Bucket",
        color_discrete_map={"Low": "#f87171", "Medium": "#fbbf24", "High": "#34d399"},
        text="Orders",
        labels={"Revenue_Bucket": "Revenue Bucket", "Orders": "Number of Orders"},
    )
    fig_bucket.update_traces(textposition="outside")
    fig_bucket.update_layout(
        showlegend=False, height=300, margin=dict(t=10, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_bucket, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — PRODUCTS & CATEGORIES
# ════════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("### 📦 Products & Categories")

    # Category summary table
    st.markdown('<div class="section-header">Category Performance Summary</div>',
                unsafe_allow_html=True)
    cat_df = sales_by_category(df)
    cat_display = cat_df.copy()
    cat_display["Total_Sales"] = cat_display["Total_Sales"].apply(lambda x: f"₹{x:,.2f}")
    cat_display["Total_Profit"] = cat_display["Total_Profit"].apply(lambda x: f"₹{x:,.2f}")
    cat_display["Avg_Order_Value"] = cat_display["Avg_Order_Value"].apply(lambda x: f"₹{x:,.2f}")
    cat_display["Profit_Margin_%"] = cat_display["Profit_Margin_%"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(cat_display, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Sales Share by Category</div>',
                    unsafe_allow_html=True)
        fig_pie = px.pie(
            sales_by_category(df),
            names="Category",
            values="Total_Sales",
            color="Category",
            color_discrete_map=CATEGORY_COLORS,
            hole=0.4,
        )
        fig_pie.update_traces(textposition="outside", textinfo="percent+label")
        fig_pie.update_layout(height=350, margin=dict(t=10, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Profit Margin by Category</div>',
                    unsafe_allow_html=True)
        fig_margin = px.bar(
            sales_by_category(df).sort_values("Profit_Margin_%"),
            x="Profit_Margin_%",
            y="Category",
            orientation="h",
            color="Profit_Margin_%",
            color_continuous_scale="RdYlGn",
            text="Profit_Margin_%",
        )
        fig_margin.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig_margin.update_layout(
            height=350,
            margin=dict(t=10, b=10),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_margin, use_container_width=True)

    # Top 10 products
    st.markdown('<div class="section-header">Top 10 Products by Sales</div>',
                unsafe_allow_html=True)
    prod_df = sales_by_product(df, top_n=10)
    fig_prod = px.bar(
        prod_df.sort_values("Total_Sales"),
        x="Total_Sales",
        y="Product",
        color="Category",
        orientation="h",
        color_discrete_map=CATEGORY_COLORS,
        text=prod_df.sort_values("Total_Sales")["Total_Sales"].apply(
            lambda x: f"₹{x/1e5:.1f}L"
        ),
        labels={"Total_Sales": "Total Sales (₹)", "Product": ""},
    )
    fig_prod.update_traces(textposition="outside")
    fig_prod.update_layout(height=420, margin=dict(t=10, b=10, l=10, r=80))
    st.plotly_chart(fig_prod, use_container_width=True)

    # Product detail table
    st.markdown('<div class="section-header">Top 10 Products — Detail Table</div>',
                unsafe_allow_html=True)
    prod_display = prod_df.copy()
    prod_display["Total_Sales"] = prod_display["Total_Sales"].apply(lambda x: f"₹{x:,.2f}")
    prod_display["Total_Profit"] = prod_display["Total_Profit"].apply(lambda x: f"₹{x:,.2f}")
    prod_display["Profit_Margin_%"] = prod_display["Profit_Margin_%"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(prod_display, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — LOCATIONS
# ════════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("### 🏙️ City-wise Sales Performance")

    city_df = sales_by_city(df)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Total Sales by City</div>',
                    unsafe_allow_html=True)
        fig_city = px.bar(
            city_df.sort_values("Total_Sales"),
            x="Total_Sales",
            y="City",
            orientation="h",
            color="Total_Sales",
            color_continuous_scale="Blues",
            text=city_df.sort_values("Total_Sales")["Total_Sales"].apply(
                lambda x: f"₹{x/1e5:.1f}L"
            ),
            labels={"Total_Sales": "Total Sales (₹)", "City": ""},
        )
        fig_city.update_traces(textposition="outside")
        fig_city.update_layout(
            height=400,
            margin=dict(t=10, b=10),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_city, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Profit Margin by City</div>',
                    unsafe_allow_html=True)
        fig_city_margin = px.bar(
            city_df.sort_values("Profit_Margin_%"),
            x="Profit_Margin_%",
            y="City",
            orientation="h",
            color="Profit_Margin_%",
            color_continuous_scale="RdYlGn",
            text="Profit_Margin_%",
        )
        fig_city_margin.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig_city_margin.update_layout(
            height=400,
            margin=dict(t=10, b=10),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_city_margin, use_container_width=True)

    # City × Category heatmap
    st.markdown('<div class="section-header">City × Category Sales Heatmap</div>',
                unsafe_allow_html=True)
    heat_df = (
        df.groupby(["City", "Category"])["Calculated_Sales"]
        .sum()
        .reset_index()
        .pivot(index="City", columns="Category", values="Calculated_Sales")
        .fillna(0)
    )
    fig_heat = px.imshow(
        heat_df,
        color_continuous_scale="Blues",
        aspect="auto",
        text_auto=".2s",
        labels=dict(color="Sales (₹)"),
    )
    fig_heat.update_layout(height=380, margin=dict(t=10, b=10))
    st.plotly_chart(fig_heat, use_container_width=True)

    # City table
    st.markdown('<div class="section-header">City Performance Table</div>',
                unsafe_allow_html=True)
    city_display = city_df.copy()
    city_display["Total_Sales"] = city_display["Total_Sales"].apply(lambda x: f"₹{x:,.2f}")
    city_display["Total_Profit"] = city_display["Total_Profit"].apply(lambda x: f"₹{x:,.2f}")
    city_display["Avg_Order_Value"] = city_display["Avg_Order_Value"].apply(lambda x: f"₹{x:,.2f}")
    city_display["Profit_Margin_%"] = city_display["Profit_Margin_%"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(city_display, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — CUSTOMERS
# ════════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("### 👥 Customer Analysis")

    ct_df = customer_type_summary(df)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Sales by Customer Type</div>',
                    unsafe_allow_html=True)
        fig_ct = px.pie(
            ct_df,
            names="Customer_Type",
            values="Total_Sales",
            hole=0.45,
            color_discrete_sequence=COLORS,
        )
        fig_ct.update_traces(textposition="outside", textinfo="percent+label")
        fig_ct.update_layout(height=350, margin=dict(t=10, b=10))
        st.plotly_chart(fig_ct, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Avg Order Value by Customer Type</div>',
                    unsafe_allow_html=True)
        fig_ct_aov = px.bar(
            ct_df,
            x="Customer_Type",
            y="Avg_Order_Value",
            color="Customer_Type",
            color_discrete_sequence=COLORS,
            text="Avg_Order_Value",
            labels={"Avg_Order_Value": "Avg Order Value (₹)"},
        )
        fig_ct_aov.update_traces(
            texttemplate="₹%{text:,.0f}", textposition="outside"
        )
        fig_ct_aov.update_layout(
            showlegend=False, height=350, margin=dict(t=10, b=10)
        )
        st.plotly_chart(fig_ct_aov, use_container_width=True)

    # Customer type detail table
    st.markdown('<div class="section-header">Customer Type Summary</div>',
                unsafe_allow_html=True)
    ct_display = ct_df.copy()
    ct_display["Total_Sales"] = ct_display["Total_Sales"].apply(lambda x: f"₹{x:,.2f}")
    ct_display["Total_Profit"] = ct_display["Total_Profit"].apply(lambda x: f"₹{x:,.2f}")
    ct_display["Avg_Order_Value"] = ct_display["Avg_Order_Value"].apply(lambda x: f"₹{x:,.2f}")
    ct_display["Profit_Margin_%"] = ct_display["Profit_Margin_%"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(ct_display, use_container_width=True, hide_index=True)

    # Top customers
    st.markdown('<div class="section-header">Top 10 Customers by Revenue</div>',
                unsafe_allow_html=True)
    top_cust = top_customers(df, top_n=10)
    fig_top_cust = px.bar(
        top_cust.sort_values("Total_Sales"),
        x="Total_Sales",
        y="Customer_ID",
        orientation="h",
        color="Total_Sales",
        color_continuous_scale="Purples",
        text=top_cust.sort_values("Total_Sales")["Total_Sales"].apply(
            lambda x: f"₹{x/1e5:.1f}L"
        ),
        labels={"Total_Sales": "Total Sales (₹)", "Customer_ID": "Customer"},
    )
    fig_top_cust.update_traces(textposition="outside")
    fig_top_cust.update_layout(
        height=400,
        margin=dict(t=10, b=10),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_top_cust, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — TIME TRENDS
# ════════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("### 📅 Sales & Profit Trends Over Time")

    monthly = monthly_trend(df)
    quarterly = quarterly_trend(df)

    # Monthly line chart
    st.markdown('<div class="section-header">Monthly Sales & Profit</div>',
                unsafe_allow_html=True)
    fig_monthly = make_subplots(specs=[[{"secondary_y": True}]])
    fig_monthly.add_trace(
        go.Scatter(
            x=monthly["Month_Name"],
            y=monthly["Total_Sales"],
            name="Total Sales",
            mode="lines+markers",
            line=dict(color="#3b82f6", width=3),
            marker=dict(size=8),
        ),
        secondary_y=False,
    )
    fig_monthly.add_trace(
        go.Scatter(
            x=monthly["Month_Name"],
            y=monthly["Total_Profit"],
            name="Total Profit",
            mode="lines+markers",
            line=dict(color="#10b981", width=3, dash="dash"),
            marker=dict(size=8),
        ),
        secondary_y=False,
    )
    fig_monthly.add_trace(
        go.Bar(
            x=monthly["Month_Name"],
            y=monthly["Total_Orders"],
            name="Orders",
            opacity=0.25,
            marker_color="#94a3b8",
        ),
        secondary_y=True,
    )
    fig_monthly.update_layout(
        height=400,
        margin=dict(t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        hovermode="x unified",
    )
    fig_monthly.update_yaxes(title_text="Amount (₹)", secondary_y=False)
    fig_monthly.update_yaxes(title_text="Orders", secondary_y=True)
    st.plotly_chart(fig_monthly, use_container_width=True)

    # MoM growth
    st.markdown('<div class="section-header">Month-over-Month Sales Growth (%)</div>',
                unsafe_allow_html=True)
    mom = monthly.dropna(subset=["MoM_Sales_Growth_%"])
    fig_mom = px.bar(
        mom,
        x="Month_Name",
        y="MoM_Sales_Growth_%",
        color="MoM_Sales_Growth_%",
        color_continuous_scale="RdYlGn",
        text="MoM_Sales_Growth_%",
        labels={"MoM_Sales_Growth_%": "MoM Growth (%)", "Month_Name": "Month"},
    )
    fig_mom.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_mom.update_layout(
        height=320,
        margin=dict(t=10, b=10),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_mom, use_container_width=True)

    # Quarterly comparison
    st.markdown('<div class="section-header">Quarterly Sales vs Profit</div>',
                unsafe_allow_html=True)
    fig_q = go.Figure()
    fig_q.add_trace(go.Bar(
        name="Sales",
        x=quarterly["Quarter"],
        y=quarterly["Total_Sales"],
        marker_color="#3b82f6",
        text=quarterly["Total_Sales"].apply(lambda x: f"₹{x/1e5:.1f}L"),
        textposition="outside",
    ))
    fig_q.add_trace(go.Bar(
        name="Profit",
        x=quarterly["Quarter"],
        y=quarterly["Total_Profit"],
        marker_color="#10b981",
        text=quarterly["Total_Profit"].apply(lambda x: f"₹{x/1e5:.1f}L"),
        textposition="outside",
    ))
    fig_q.update_layout(
        barmode="group",
        height=340,
        margin=dict(t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis_title="Quarter",
        yaxis_title="Amount (₹)",
    )
    st.plotly_chart(fig_q, use_container_width=True)

    # Monthly table
    with st.expander("📋 Monthly Trend Table"):
        monthly_display = monthly.copy()
        monthly_display["Total_Sales"] = monthly_display["Total_Sales"].apply(lambda x: f"₹{x:,.2f}")
        monthly_display["Total_Profit"] = monthly_display["Total_Profit"].apply(lambda x: f"₹{x:,.2f}")
        monthly_display["MoM_Sales_Growth_%"] = monthly_display["MoM_Sales_Growth_%"].apply(
            lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A"
        )
        st.dataframe(monthly_display, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 6 — PAYMENTS & DISCOUNTS
# ════════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("### 💳 Payment Methods & Discount Analysis")

    pay_df = payment_analysis(df)
    disc_df = discount_impact(df)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Payment Method Distribution</div>',
                    unsafe_allow_html=True)
        fig_pay = px.pie(
            pay_df,
            names="Payment_Method",
            values="Total_Orders",
            hole=0.45,
            color_discrete_sequence=COLORS,
        )
        fig_pay.update_traces(textposition="outside", textinfo="percent+label")
        fig_pay.update_layout(height=350, margin=dict(t=10, b=10))
        st.plotly_chart(fig_pay, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Avg Order Value by Payment Method</div>',
                    unsafe_allow_html=True)
        fig_pay_aov = px.bar(
            pay_df.sort_values("Avg_Order_Value"),
            x="Avg_Order_Value",
            y="Payment_Method",
            orientation="h",
            color="Avg_Order_Value",
            color_continuous_scale="Blues",
            text="Avg_Order_Value",
            labels={"Avg_Order_Value": "Avg Order Value (₹)", "Payment_Method": ""},
        )
        fig_pay_aov.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig_pay_aov.update_layout(
            height=350,
            margin=dict(t=10, b=10),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_pay_aov, use_container_width=True)

    # Discount impact
    st.markdown('<div class="section-header">Discount Impact on Profit Margin</div>',
                unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        fig_disc_orders = px.bar(
            disc_df,
            x="Discount_Band",
            y="Total_Orders",
            color="Discount_Band",
            color_discrete_sequence=COLORS,
            text="Total_Orders",
            title="Orders per Discount Band",
            labels={"Total_Orders": "Orders", "Discount_Band": "Discount Band"},
        )
        fig_disc_orders.update_traces(textposition="outside")
        fig_disc_orders.update_layout(
            showlegend=False, height=320, margin=dict(t=30, b=10)
        )
        st.plotly_chart(fig_disc_orders, use_container_width=True)

    with c4:
        fig_disc_margin = px.bar(
            disc_df,
            x="Discount_Band",
            y="Avg_Profit_Margin",
            color="Avg_Profit_Margin",
            color_continuous_scale="RdYlGn",
            text="Avg_Profit_Margin",
            title="Avg Profit Margin per Discount Band",
            labels={"Avg_Profit_Margin": "Avg Profit Margin (%)", "Discount_Band": "Discount Band"},
        )
        fig_disc_margin.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig_disc_margin.update_layout(
            coloraxis_showscale=False, height=320, margin=dict(t=30, b=10)
        )
        st.plotly_chart(fig_disc_margin, use_container_width=True)

    # Payment table
    with st.expander("📋 Payment Method Detail Table"):
        pay_display = pay_df.copy()
        pay_display["Total_Sales"] = pay_display["Total_Sales"].apply(lambda x: f"₹{x:,.2f}")
        pay_display["Avg_Order_Value"] = pay_display["Avg_Order_Value"].apply(lambda x: f"₹{x:,.2f}")
        pay_display["Share_%"] = pay_display["Share_%"].apply(lambda x: f"{x:.2f}%")
        st.dataframe(pay_display, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 7 — DATA QUALITY
# ════════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("### 🔍 Data Quality Report")

    qr = quality_report
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Rows", f"{qr['total_rows']:,}")
    c2.metric("Total Columns", qr["total_columns"])
    c3.metric("Duplicate Rows", qr["duplicate_rows"])
    c4.metric("Missing Values", sum(qr["missing_values"].values()))

    st.markdown("---")

    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="section-header">Missing Values per Column</div>',
                    unsafe_allow_html=True)
        miss_df = pd.DataFrame.from_dict(
            qr["missing_values"], orient="index", columns=["Missing Count"]
        ).reset_index().rename(columns={"index": "Column"})
        fig_miss = px.bar(
            miss_df,
            x="Missing Count",
            y="Column",
            orientation="h",
            color="Missing Count",
            color_continuous_scale="Reds",
            text="Missing Count",
        )
        fig_miss.update_traces(textposition="outside")
        fig_miss.update_layout(
            height=420, margin=dict(t=10, b=10), coloraxis_showscale=False
        )
        st.plotly_chart(fig_miss, use_container_width=True)

    with c6:
        st.markdown('<div class="section-header">Data Integrity Checks</div>',
                    unsafe_allow_html=True)
        checks = {
            "Duplicate Rows": qr["duplicate_rows"],
            "Negative Quantities": qr["negative_quantity"],
            "Negative Unit Prices": qr["negative_unit_price"],
            "Invalid Discounts": qr["invalid_discount"],
        }
        check_df = pd.DataFrame(
            [{"Check": k, "Issues Found": v, "Status": "✅ OK" if v == 0 else "⚠️ Issues"}
             for k, v in checks.items()]
        )
        st.dataframe(check_df, use_container_width=True, hide_index=True)

        st.markdown("##### Columns with No Missing Values")
        clean_cols = [col for col, v in qr["missing_values"].items() if v == 0]
        st.success(f"All {len(clean_cols)} columns are complete — no missing values detected.")

    # Raw sample
    st.markdown('<div class="section-header">Raw Dataset Sample (first 20 rows)</div>',
                unsafe_allow_html=True)
    st.dataframe(df.head(20), use_container_width=True, hide_index=True)

    # Download cleaned data
    st.markdown('<div class="section-header">⬇️ Download Cleaned Dataset</div>',
                unsafe_allow_html=True)
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Cleaned CSV",
        data=csv_data,
        file_name="ecommerce_cleaned.csv",
        mime="text/csv",
    )


# ════════════════════════════════════════════════════════════════════════════════
# TAB 8 — INSIGHTS
# ════════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown("### 💡 Business Insights & Recommendations")

    insights = generate_insights(df, kpis)

    for insight in insights:
        st.markdown(
            f'<div class="insight-card">{insight}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### 📌 Strategic Recommendations")

    recommendations = [
        {
            "icon": "🎯",
            "title": "Double Down on Top Categories",
            "detail": "Allocate more marketing budget and inventory to the highest-revenue category. "
                      "Cross-sell within the segment to increase basket size.",
        },
        {
            "icon": "💸",
            "title": "Tighten Discount Policy",
            "detail": "High discounts (20%+) are eroding margins. Introduce loyalty-based discounts "
                      "for returning/premium customers rather than blanket cuts.",
        },
        {
            "icon": "📍",
            "title": "Geo-Targeted Campaigns",
            "detail": "Focus ad spend on top-performing cities while running targeted promotions "
                      "in lower-performing cities to grow market share.",
        },
        {
            "icon": "🔄",
            "title": "Reduce Return & Cancellation Rates",
            "detail": "Audit product descriptions, images, and fulfilment SLAs for the products "
                      "with the highest return rates to improve customer satisfaction.",
        },
        {
            "icon": "👑",
            "title": "VIP Customer Programme",
            "detail": "Top 10 customers drive disproportionate revenue. Introduce a VIP tier with "
                      "exclusive offers, early access, and dedicated support.",
        },
        {
            "icon": "📅",
            "title": "Seasonal Inventory Planning",
            "detail": "Use monthly trend data to pre-stock high-demand products before peak months "
                      "and avoid overstock during slow periods.",
        },
    ]

    cols = st.columns(2)
    for i, rec in enumerate(recommendations):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div style='background:#fff;border-radius:10px;padding:16px 20px;
                            box-shadow:0 2px 8px rgba(0,0,0,0.07);margin-bottom:14px;
                            border-top:4px solid #3b82f6;'>
                    <div style='font-size:1.3rem;margin-bottom:6px;'>{rec['icon']} <strong>{rec['title']}</strong></div>
                    <div style='color:#475569;font-size:0.9rem;line-height:1.6;'>{rec['detail']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Summary statistics footer
    st.markdown("---")
    st.markdown("#### 📊 At-a-Glance Summary")
    summary_cols = st.columns(3)
    summary_cols[0].markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-value'>₹{kpis['Total Sales (₹)']/1e6:.2f}M</div>
            <div class='kpi-label'>Total Revenue</div>
        </div>
        """, unsafe_allow_html=True
    )
    summary_cols[1].markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-value'>₹{kpis['Total Profit (₹)']/1e6:.2f}M</div>
            <div class='kpi-label'>Total Profit</div>
        </div>
        """, unsafe_allow_html=True
    )
    summary_cols[2].markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{kpis['Overall Profit Margin (%)']:.2f}%</div>
            <div class='kpi-label'>Profit Margin</div>
        </div>
        """, unsafe_allow_html=True
    )

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#94a3b8;font-size:0.82rem;padding:10px 0;'>"
    "E-Commerce Sales & Customer Analysis Dashboard · Built with Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True,
)
