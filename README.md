# 🛒 E-Commerce Sales & Customer Analysis

An end-to-end data analytics project on e-commerce order data: data loading, quality checks, cleaning, feature engineering, KPI analysis and an interactive Streamlit dashboard that turns the data into business insights and recommendations.

## 📌 Project Description

The project analyses 1,000 e-commerce orders (Jan–Dec 2025) to answer business questions such as:

- Which categories, products and cities drive the most sales and profit?
- Which customer segments (New / Returning / Premium) are the most valuable?
- How do sales and profit trend month by month and quarter by quarter?
- How do payment methods and discounts affect orders and profit margin?
- Where are the risks (cancellations, returns, low-margin categories) and what should management do?

## 📂 Dataset

- **Source:** Synthetic dataset generated with ChatGPT for this project (included in this repository as `ecommerce_sales_customer_analysis_dataset.csv`, so no external download link is needed)
- **Note:** Since the data is synthetic, the insights show the analysis approach and are not real-world business findings
- **File:** `ecommerce_sales_customer_analysis_dataset.csv` (1,000 rows × 14 columns)

| Column | Description |
|---|---|
| Order_ID | Unique order identifier |
| Order_Date | Date of purchase |
| Customer_ID | Unique customer ID (291 customers) |
| Customer_Type | New / Returning / Premium |
| Product | Product name (25 products) |
| Category | Electronics, Fashion, Sports, Beauty, Home & Kitchen |
| City | 8 Indian cities |
| Quantity | Units ordered |
| Unit_Price | Price per unit (INR) |
| Discount | Discount rate (0.0 – 1.0) |
| Payment_Method | UPI, Credit/Debit Card, Net Banking, COD |
| Sales | Original sales value |
| Profit | Profit amount |
| Order_Status | Delivered / Cancelled / Returned |

## 🔧 Analytics Pipeline

1. Load the CSV dataset
2. Check for missing, duplicate and incorrect values
3. Clean and prepare the data
4. Calculate sales as `Quantity × Unit_Price × (1 − Discount)`
5. Compute total sales, profit and profit margin
6. Group and summarise using totals, counts and averages
7. Analyse customers, products, categories and locations
8. Build interactive charts to compare results
9. Identify business problems and trends
10. Derive actionable business decisions

## 📊 Dashboard Tabs

| Tab | Content |
|---|---|
| Overview | KPI cards, order status, revenue bucket distribution |
| Products & Categories | Category/product tables and charts |
| Locations | City rankings, heatmap, profit margin by city |
| Customers | Customer-type analysis, top customers |
| Time Trends | Monthly/quarterly trends, MoM growth |
| Payments & Discounts | Payment method share, discount impact |
| Data Quality | Quality report, data sample, cleaned CSV download |
| Insights | Auto-generated insights and recommendations |

The sidebar filters (category, city, customer type, order status, date range) update every tab.

## 📈 Key Numbers

- Total sales: ₹1.63 crore | Total profit: ₹36.0 lakh | Overall margin: 22.07%
- 922 of 1,000 orders delivered (92.2%); 50 cancelled, 28 returned
- Electronics is the top category by sales; Bangalore and Mumbai are the top cities

## 🛠️ Technologies Used

- Python 3.10+
- pandas, NumPy: data cleaning and analysis
- Streamlit: interactive dashboard
- Plotly: charts

## 🚀 Setup & Run

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd <your-repo-folder>

# 2. (Optional) create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run MayankVashishath_E-Commerce_Sales_Customer_Analysis.py
```

Keep `ecommerce_sales_customer_analysis_dataset.csv` in the same folder as `MayankVashishath_E-Commerce_Sales_Customer_Analysis.py`. The dashboard opens at http://localhost:8501.

## 📁 Files

```
MayankVashishath_E-Commerce_Sales_Customer_Analysis.py                          # complete project code (loading, analysis, dashboard)
ecommerce_sales_customer_analysis_dataset.csv  # dataset
requirements.txt                               # dependencies
README.md                                      # this file
MayankVashishath_ProjectReport.docx                    # project report (submitted separately)
```
