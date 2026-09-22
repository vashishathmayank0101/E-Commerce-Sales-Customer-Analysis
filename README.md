# 🛒 E-Commerce Sales & Customer Analysis

A complete Python data analytics project on e-commerce sales data, featuring an interactive Streamlit dashboard and a professionally generated PowerPoint presentation.

---

## 📁 Project Structure

```
ecommerce_project/
├── app.py                       # Streamlit dashboard (main entry point)
├── data_loader.py               # Data loading, cleaning & feature engineering
├── analysis.py                  # All KPI, aggregation & insight functions
├── generate_ppt.py              # PowerPoint presentation generator
├── ECommerce_Sales_Analysis.pptx  # Generated PPT (15 slides)
└── requirements.txt             # Python dependencies
ecommerce_sales_customer_analysis_dataset.csv   # Source dataset (1,000 orders)
```

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r ecommerce_project/requirements.txt
```

### 2. Run the Streamlit dashboard
```bash
streamlit run ecommerce_project/app.py
```

### 3. Regenerate the PowerPoint
```bash
python ecommerce_project/generate_ppt.py
```

---

## 📊 Dataset Overview

| Column | Description |
|---|---|
| Order_ID | Unique order identifier |
| Order_Date | Date of purchase |
| Customer_ID | Unique customer ID |
| Customer_Type | New / Returning / Premium |
| Product | Product name (25 SKUs) |
| Category | Electronics, Fashion, Sports, Beauty, Home & Kitchen |
| City | 8 Indian cities |
| Quantity | Units ordered |
| Unit_Price | Price per unit (INR) |
| Discount | Discount rate (0.0 – 1.0) |
| Payment_Method | UPI, Credit/Debit Card, Net Banking, COD |
| Sales | Original sales value |
| Profit | Profit amount |
| Order_Status | Delivered / Cancelled / Returned |

---

## 🔧 Analytics Pipeline (10 Steps)

| Step | Description |
|---|---|
| 1 | Collect and load the CSV dataset |
| 2 | Check for missing, duplicate, or incorrect values |
| 3 | Clean and prepare the dataset |
| 4 | Calculate Sales = Quantity × Unit Price − Discount |
| 5 | Calculate total sales and profit |
| 6 | Group and summarize using totals, counts, and averages |
| 7 | Analyze customers, products, categories, and locations |
| 8 | Create interactive charts to compare results |
| 9 | Identify business problems and trends |
| 10 | Derive actionable business decisions from data |

---

## 📱 Dashboard Tabs

| Tab | Content |
|---|---|
| 📊 Overview | KPI cards, order status, revenue bucket distribution |
| 📦 Products & Categories | Category/product tables, pie charts, bar charts |
| 🏙️ Locations | City rankings, heatmap, profit margin by city |
| 👥 Customers | Customer type analysis, top customers |
| 📅 Time Trends | Monthly/quarterly charts, MoM growth |
| 💳 Payments & Discounts | Payment method pie, discount impact |
| 🔍 Data Quality | Quality report, raw data sample, CSV download |
| 💡 Insights | Auto-generated insights + strategic recommendations |

---

## 📑 PowerPoint Slides (15 slides)

1. Title Slide
2. Agenda
3. Project Overview & Tech Stack
4. Dataset Description & Data Quality
5. Data Cleaning & Feature Engineering
6. Key Performance Indicators
7. Sales by Category
8. Top Products
9. City Analysis
10. Customer Segmentation
11. Time Trends
12. Payments & Discounts
13. Business Insights
14. Strategic Recommendations
15. Thank You / Conclusion

---

## 🛠️ Technology Stack

- **Python 3.11+** – Core language
- **pandas / NumPy** – Data manipulation
- **Streamlit** – Interactive web dashboard
- **Plotly Express** – Charts & visualizations
- **python-pptx** – Automated PPT generation
