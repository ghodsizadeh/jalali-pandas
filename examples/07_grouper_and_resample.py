"""JalaliGrouper and resample_jalali API examples.

This module demonstrates the advanced grouping and resampling functionality
using JalaliGrouper and resample_jalali for time series analysis with
Jalali calendar boundaries.
"""

import numpy as np
import pandas as pd

from jalali_pandas.api import JalaliGrouper, jalali_groupby, resample_jalali

# =============================================================================
# Setup: Create Sample Data
# =============================================================================

print("=" * 60)
print("JalaliGrouper and resample_jalali Examples")
print("=" * 60)

np.random.seed(42)

# Create a DataFrame with Gregorian dates spanning a Jalali year
df = pd.DataFrame(
    {
        "date": pd.date_range("2023-03-21", periods=365, freq="D"),
        "sales": np.random.randint(100, 500, size=365),
        "visitors": np.random.randint(50, 200, size=365),
        "category": np.random.choice(["A", "B", "C"], size=365),
    }
)

print("\nSample DataFrame (first 10 rows):")
print(df.head(10))

# =============================================================================
# JalaliGrouper: Group by Jalali Month End
# =============================================================================

print("\n" + "=" * 60)
print("JalaliGrouper: Group by Jalali Month End (JME)")
print("=" * 60)

# Create a grouper for Jalali month end
grouper = JalaliGrouper(key="date", freq="JME")
result = df.groupby(grouper.get_grouper(df)).sum(numeric_only=True)

print("\nMonthly totals (grouped by Jalali month end):")
print(result.head())

# =============================================================================
# JalaliGrouper: Group by Jalali Quarter End
# =============================================================================

print("\n" + "=" * 60)
print("JalaliGrouper: Group by Jalali Quarter End (JQE)")
print("=" * 60)

grouper_q = JalaliGrouper(key="date", freq="JQE")
result_q = df.groupby(grouper_q.get_grouper(df)).sum(numeric_only=True)

print("\nQuarterly totals (grouped by Jalali quarter end):")
print(result_q)

# =============================================================================
# JalaliGrouper: Group by Jalali Year End
# =============================================================================

print("\n" + "=" * 60)
print("JalaliGrouper: Group by Jalali Year End (JYE)")
print("=" * 60)

grouper_y = JalaliGrouper(key="date", freq="JYE")
result_y = df.groupby(grouper_y.get_grouper(df)).sum(numeric_only=True)

print("\nYearly totals (grouped by Jalali year end):")
print(result_y)

# =============================================================================
# JalaliGrouper: Multiple Aggregations
# =============================================================================

print("\n" + "=" * 60)
print("JalaliGrouper: Multiple Aggregations")
print("=" * 60)

grouper = JalaliGrouper(key="date", freq="JME")
result_agg = df.groupby(grouper.get_grouper(df)).agg(
    {
        "sales": ["sum", "mean", "std"],
        "visitors": ["sum", "mean"],
    }
)

print("\nMonthly statistics:")
print(result_agg.head())

# =============================================================================
# jalali_groupby: Convenience Function
# =============================================================================

print("\n" + "=" * 60)
print("jalali_groupby: Convenience Function")
print("=" * 60)

# Using the convenience function
result_conv = jalali_groupby(df, "date", "JME").sum(numeric_only=True)

print("\nMonthly totals using jalali_groupby:")
print(result_conv.head())

# =============================================================================
# resample_jalali: Resample Series
# =============================================================================

print("\n" + "=" * 60)
print("resample_jalali: Resample Series")
print("=" * 60)

# Create a Series with DatetimeIndex
series = pd.Series(df["sales"].values, index=pd.DatetimeIndex(df["date"]), name="sales")

# Resample by Jalali month
resampled_monthly = resample_jalali(series, "JME").sum()

print("\nMonthly sales (resampled by Jalali month end):")
print(resampled_monthly.head())

# Resample by Jalali quarter
resampled_quarterly = resample_jalali(series, "JQE").sum()

print("\nQuarterly sales (resampled by Jalali quarter end):")
print(resampled_quarterly)

# =============================================================================
# resample_jalali: Multiple Aggregations
# =============================================================================

print("\n" + "=" * 60)
print("resample_jalali: Multiple Aggregations")
print("=" * 60)

# Different aggregation functions
print("\nMonthly statistics:")
print(f"  Sum: {resample_jalali(series, 'JME').sum().head()}")
print(f"  Mean: {resample_jalali(series, 'JME').mean().head()}")
print(f"  Max: {resample_jalali(series, 'JME').max().head()}")
print(f"  Min: {resample_jalali(series, 'JME').min().head()}")
print(f"  Count: {resample_jalali(series, 'JME').count().head()}")

# =============================================================================
# resample_jalali: Resample DataFrame
# =============================================================================

print("\n" + "=" * 60)
print("resample_jalali: Resample DataFrame")
print("=" * 60)

# Create DataFrame with DatetimeIndex
df_indexed = df.set_index("date")

# Resample DataFrame
df_monthly = resample_jalali(df_indexed, "JME").sum(numeric_only=True)

print("\nMonthly DataFrame (resampled by Jalali month end):")
print(df_monthly.head())

# =============================================================================
# Advanced: Custom Aggregation with apply
# =============================================================================

print("\n" + "=" * 60)
print("Advanced: Custom Aggregation with apply")
print("=" * 60)


# Custom aggregation function
def custom_agg(group):
    """Calculate custom metrics for each group."""
    return pd.Series(
        {
            "total_sales": group["sales"].sum(),
            "avg_sales": group["sales"].mean(),
            "total_visitors": group["visitors"].sum(),
            "sales_per_visitor": group["sales"].sum() / group["visitors"].sum(),
        }
    )


grouper = JalaliGrouper(key="date", freq="JME")
result_custom = df.groupby(grouper.get_grouper(df)).apply(custom_agg)

print("\nCustom monthly metrics:")
print(result_custom.head())

# =============================================================================
# Advanced: Grouping with Multiple Keys
# =============================================================================

print("\n" + "=" * 60)
print("Advanced: Grouping with Multiple Keys")
print("=" * 60)

# Group by Jalali month and category
grouper = JalaliGrouper(key="date", freq="JME")
result_multi = df.groupby([grouper.get_grouper(df), "category"]).sum(numeric_only=True)

print("\nMonthly totals by category:")
print(result_multi.head(10))

# =============================================================================
# Advanced: Resampling with Different Frequencies
# =============================================================================

print("\n" + "=" * 60)
print("Advanced: Resampling with Different Frequencies")
print("=" * 60)

# Create hourly data
hourly_df = pd.DataFrame(
    {
        "date": pd.date_range("2023-03-21", periods=720, freq="H"),
        "value": np.random.randint(10, 100, size=720),
    }
)
hourly_series = pd.Series(
    hourly_df["value"].values,
    index=pd.DatetimeIndex(hourly_df["date"]),
    name="hourly_value",
)

# Resample to daily (day boundaries are same in both calendars)
daily_resampled = hourly_series.resample("D").sum()
print("\nHourly to daily:")
print(daily_resampled.head())

# Resample to weekly (Jalali week)
weekly_resampled = resample_jalali(hourly_series, "JW").sum()
print("\nHourly to weekly (Jalali week):")
print(weekly_resampled.head())

# =============================================================================
# Practical Use Case: Sales Report
# =============================================================================

print("\n" + "=" * 60)
print("Practical Use Case: Sales Report")
print("=" * 60)

# Generate a comprehensive sales report
print("\n=== Monthly Sales Report (Jalali Calendar) ===")

grouper = JalaliGrouper(key="date", freq="JME")
monthly_report = df.groupby(grouper.get_grouper(df)).agg(
    {
        "sales": ["sum", "mean", "count"],
        "visitors": ["sum", "mean"],
    }
)

# Flatten column names
monthly_report.columns = [
    "_".join(col).strip() for col in monthly_report.columns.values
]
monthly_report["avg_sale_per_visitor"] = (
    monthly_report["sales_sum"] / monthly_report["visitors_sum"]
)

print(monthly_report)

# =============================================================================
# Comparison: Gregorian vs Jalali Grouping
# =============================================================================

print("\n" + "=" * 60)
print("Comparison: Gregorian vs Jalali Grouping")
print("=" * 60)

# Gregorian monthly grouping
gregorian_monthly = df.set_index("date").resample("ME").sum(numeric_only=True)

# Jalali monthly grouping
jalali_monthly = resample_jalali(df.set_index("date"), "JME").sum(numeric_only=True)

print("\nGregorian monthly totals (first 3):")
print(gregorian_monthly.head(3))

print("\nJalali monthly totals (first 3):")
print(jalali_monthly.head(3))

print("\nNote: Notice how the boundaries differ between Gregorian and Jalali calendars")

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
