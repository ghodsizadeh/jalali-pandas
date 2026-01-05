"""Real-world use case: Sales and financial report with Jalali dates.

This module demonstrates a practical scenario of creating a comprehensive
sales and financial report using Jalali calendar for an Iranian business.
"""

import numpy as np
import pandas as pd

# =============================================================================
# Scenario: Iranian Retail Business Sales Report
# =============================================================================

print("=" * 70)
print("Real-World Use Case: Iranian Retail Business Sales Report")
print("=" * 70)

np.random.seed(42)

# =============================================================================
# Step 1: Generate Sample Sales Data
# =============================================================================

print("\nStep 1: Generate Sample Sales Data")
print("-" * 70)

# Generate daily sales data for one Jalali year (1402)
# Jalali year 1402 starts on March 21, 2023
start_date = pd.Timestamp("2023-03-21")
end_date = pd.Timestamp("2024-03-19")  # End of 1402

# Create date range
dates = pd.date_range(start_date, end_date, freq="D")
n_days = len(dates)

# Generate realistic sales data with seasonality
base_sales = 100 + 50 * np.sin(2 * np.pi * np.arange(n_days) / 365)
seasonal_boost = 30 * np.sin(4 * np.pi * np.arange(n_days) / 365)  # Quarterly peaks
random_noise = np.random.normal(0, 20, n_days)

# Weekend boost (Friday is weekend in Iran)
weekday_boost = np.zeros(n_days)
for i, date in enumerate(dates):
    if date.weekday() == 4:  # Friday
        weekday_boost[i] = 40

sales = base_sales + seasonal_boost + random_noise + weekday_boost
sales = np.maximum(sales, 10)  # Minimum sales

# Generate other metrics
transactions = np.random.poisson(20, n_days) + np.random.randint(5, 15, n_days)
returns = np.random.poisson(2, n_days)
discounts = np.random.uniform(0, 0.15, n_days) * sales

# Create DataFrame
df = pd.DataFrame(
    {
        "date": dates,
        "sales": sales,
        "transactions": transactions,
        "returns": returns,
        "discounts": discounts,
        "net_sales": sales - discounts,
        "profit": sales * 0.3 - discounts * 0.5,  # 30% margin, discounts cost 50%
    }
)

# Add Jalali date column
df["jalali_date"] = df["date"].jalali.to_jalali()

print(f"Generated {len(df)} days of sales data")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Jalali range: {df['jalali_date'].min()} to {df['jalali_date'].max()}")
print("\nSample data (first 5 days):")
print(df.head())

# =============================================================================
# Step 2: Extract Jalali Date Components
# =============================================================================

print("\nStep 2: Extract Jalali Date Components")
print("-" * 70)

df["jyear"] = df["jalali_date"].jalali.year
df["jmonth"] = df["jalali_date"].jalali.month
df["jday"] = df["jalali_date"].jalali.day
df["jweekday"] = df["jalali_date"].jalali.weekday
df["jmonth_name"] = df["jalali_date"].jalali.month_name(locale="en")

print("Added Jalali date components:")
print(
    df[
        ["date", "jalali_date", "jyear", "jmonth", "jday", "jweekday", "jmonth_name"]
    ].head()
)

# =============================================================================
# Step 3: Monthly Performance Report (Jalali Calendar)
# =============================================================================

print("\nStep 3: Monthly Performance Report (Jalali Calendar)")
print("-" * 70)

# Group by Jalali month
monthly_report = df.jalali.groupby("month").agg(
    {
        "sales": ["sum", "mean", "std"],
        "transactions": ["sum", "mean"],
        "returns": ["sum"],
        "discounts": ["sum"],
        "net_sales": ["sum"],
        "profit": ["sum"],
    }
)

# Flatten column names
monthly_report.columns = [
    "_".join(col).strip() for col in monthly_report.columns.values
]

# Calculate additional metrics
monthly_report["avg_transaction_value"] = (
    monthly_report["sales_sum"] / monthly_report["transactions_sum"]
)
monthly_report["return_rate"] = (
    monthly_report["returns_sum"] / monthly_report["transactions_sum"] * 100
)
monthly_report["discount_rate"] = (
    monthly_report["discounts_sum"] / monthly_report["sales_sum"] * 100
)
monthly_report["profit_margin"] = (
    monthly_report["profit_sum"] / monthly_report["net_sales_sum"] * 100
)

# Add month names
month_names = [
    "Farvardin",
    "Ordibehesht",
    "Khordad",
    "Tir",
    "Mordad",
    "Shahrivar",
    "Mehr",
    "Aban",
    "Azar",
    "Dey",
    "Bahman",
    "Esfand",
]
monthly_report["month_name"] = month_names

# Reorder columns
monthly_report = monthly_report[
    [
        "month_name",
        "sales_sum",
        "sales_mean",
        "transactions_sum",
        "avg_transaction_value",
        "net_sales_sum",
        "profit_sum",
        "profit_margin",
        "return_rate",
        "discount_rate",
    ]
]

print("Monthly Performance Report:")
print(monthly_report.round(2))

# =============================================================================
# Step 4: Quarterly Performance Report
# =============================================================================

print("\nStep 4: Quarterly Performance Report")
print("-" * 70)

quarterly_report = df.jalali.groupby("quarter").agg(
    {
        "sales": ["sum", "mean"],
        "transactions": ["sum"],
        "net_sales": ["sum"],
        "profit": ["sum"],
    }
)

quarterly_report.columns = [
    "_".join(col).strip() for col in quarterly_report.columns.values
]
quarterly_report["profit_margin"] = (
    quarterly_report["profit_sum"] / quarterly_report["net_sales_sum"] * 100
)

print("Quarterly Performance Report:")
print(quarterly_report.round(2))

# =============================================================================
# Step 5: Weekly Analysis (Friday as Weekend)
# =============================================================================

print("\nStep 5: Weekly Analysis (Friday as Weekend)")
print("-" * 70)

# Filter Fridays (weekday 0 in Jalali)
friday_sales = df[df["jweekday"] == 0]
weekday_sales = df[df["jweekday"] != 0]

friday_avg = friday_sales["sales"].mean()
weekday_avg = weekday_sales["sales"].mean()

print(f"Friday average sales: {friday_avg:.2f}")
print(f"Weekday average sales: {weekday_avg:.2f}")
print(f"Friday premium: {((friday_avg / weekday_avg - 1) * 100):.1f}%")

# =============================================================================
# Step 6: Best and Worst Performing Days
# =============================================================================

print("\nStep 6: Best and Worst Performing Days")
print("-" * 70)

# Top 5 days
top_days = df.nlargest(5, "sales")[["jalali_date", "sales", "transactions"]]
print("Top 5 sales days:")
for _, row in top_days.iterrows():
    print(
        f"  {row['jalali_date'].strftime('%Y-%m-%d (%A)')}: "
        f"{row['sales']:.0f} sales, {row['transactions']} transactions"
    )

# Bottom 5 days
bottom_days = df.nsmallest(5, "sales")[["jalali_date", "sales", "transactions"]]
print("\nBottom 5 sales days:")
for _, row in bottom_days.iterrows():
    print(
        f"  {row['jalali_date'].strftime('%Y-%m-%d (%A)')}: "
        f"{row['sales']:.0f} sales, {row['transactions']} transactions"
    )

# =============================================================================
# Step 7: Year-to-Date Analysis
# =============================================================================

print("\nStep 7: Year-to-Date Analysis")
print("-" * 70)

total_sales = df["sales"].sum()
total_profit = df["profit"].sum()
total_transactions = df["transactions"].sum()
total_returns = df["returns"].sum()

print(f"Total Sales: {total_sales:,.0f}")
print(f"Total Net Sales: {df['net_sales'].sum():,.0f}")
print(f"Total Profit: {total_profit:,.0f}")
print(f"Total Transactions: {total_transactions:,}")
print(f"Total Returns: {total_returns:,}")
print(f"Average Daily Sales: {df['sales'].mean():.0f}")
print(f"Average Transaction Value: {(total_sales / total_transactions):.2f}")
print(f"Return Rate: {(total_returns / total_transactions * 100):.2f}%")
print(f"Profit Margin: {(total_profit / df['net_sales'].sum() * 100):.2f}%")

# =============================================================================
# Step 8: Month-over-Month Growth
# =============================================================================

print("\nStep 8: Month-over-Month Growth")
print("-" * 70)

monthly_sales = df.jalali.groupby("month").sum()["sales"]
mom_growth = monthly_sales.pct_change() * 100

print("Month-over-Month Sales Growth:")
for i, (month, growth) in enumerate(mom_growth.items(), 1):
    if pd.notna(growth):
        print(f"  Month {i} -> {i + 1}: {growth:+.1f}%")

# =============================================================================
# Step 9: Create Executive Summary
# =============================================================================

print("\n" + "=" * 70)
print("EXECUTIVE SUMMARY - Jalali Year 1402")
print("=" * 70)

best_month = monthly_report.loc[monthly_report["sales_sum"].idxmax()]
worst_month = monthly_report.loc[monthly_report["sales_sum"].idxmin()]

print(f"\nBest Performing Month: {best_month['month_name']}")
print(f"  Sales: {best_month['sales_sum']:,.0f}")
print(f"  Profit: {best_month['profit_sum']:,.0f}")
print(f"  Profit Margin: {best_month['profit_margin']:.1f}%")

print(f"\nWorst Performing Month: {worst_month['month_name']}")
print(f"  Sales: {worst_month['sales_sum']:,.0f}")
print(f"  Profit: {worst_month['profit_sum']:,.0f}")
print(f"  Profit Margin: {worst_month['profit_margin']:.1f}%")

print("\nYearly Performance:")
print(f"  Total Revenue: {total_sales:,.0f} Toman")
print(f"  Total Profit: {total_profit:,.0f} Toman")
print(f"  Total Transactions: {total_transactions:,}")
print(f"  Average Daily Revenue: {df['sales'].mean():,.0f} Toman")

# =============================================================================
# Step 10: Export Report to CSV
# =============================================================================

print("\nStep 10: Export Report to CSV")
print("-" * 70)

# Prepare export data
export_data = monthly_report.copy()
export_data["jalali_month"] = range(1, 13)
export_data = export_data[
    [
        "jalali_month",
        "month_name",
        "sales_sum",
        "sales_mean",
        "transactions_sum",
        "avg_transaction_value",
        "net_sales_sum",
        "profit_sum",
        "profit_margin",
        "return_rate",
        "discount_rate",
    ]
]
export_data.columns = [
    "Jalali Month",
    "Month Name",
    "Total Sales",
    "Average Sales",
    "Total Transactions",
    "Avg Transaction Value",
    "Net Sales",
    "Total Profit",
    "Profit Margin (%)",
    "Return Rate (%)",
    "Discount Rate (%)",
]

print("Monthly report ready for export:")
print(export_data.head())
print("\nTo export, use: export_data.to_csv('monthly_report_1402.csv', index=False)")

print("\n" + "=" * 70)
print("Report generation completed successfully!")
print("=" * 70)
