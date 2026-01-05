"""Formatting with Persian locale and RTL support examples.

This module demonstrates how to format Jalali dates with Persian locale
and handle right-to-left (RTL) text rendering for Persian/Farsi output.
"""

import pandas as pd

from jalali_pandas import JalaliTimestamp

# =============================================================================
# Basic Formatting with English Locale
# =============================================================================

print("=" * 60)
print("Basic Formatting with English Locale")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15, 14, 30, 45)

print(f"\nTimestamp: {ts}")
print(f"ISO format: {ts.isoformat()}")
print(f"Default str: {str(ts)}")

# Various format strings
formats = [
    ("%Y-%m-%d", "ISO date"),
    ("%Y/%m/%d", "Slash separator"),
    ("%d-%m-%Y", "Day first"),
    ("%Y-%m-%d %H:%M:%S", "With time"),
    ("%A, %d %B %Y", "Full weekday and month"),
    ("%a, %d %b %Y", "Short weekday and month"),
]

for fmt, description in formats:
    formatted = ts.strftime(fmt)
    print(f"{description:25s}: {formatted}")

# =============================================================================
# Month Names in English
# =============================================================================

print("\n" + "=" * 60)
print("Month Names in English")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15)

print(f"\nFull month name: {ts.strftime('%B')}")
print(f"Short month name: {ts.strftime('%b')}")

# All month names
print("\nAll Jalali months:")
for month in range(1, 13):
    ts_month = JalaliTimestamp(1402, month, 1)
    full_name = ts_month.strftime("%B")
    short_name = ts_month.strftime("%b")
    print(f"  Month {month:2d}: {full_name:12s} ({short_name})")

# =============================================================================
# Day Names in English
# =============================================================================

print("\n" + "=" * 60)
print("Day Names in English")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15)

print(f"\nFull day name: {ts.strftime('%A')}")
print(f"Short day name: {ts.strftime('%a')}")

# All day names (Jalali week starts on Saturday)
print("\nAll Jalali weekdays:")
for day in range(7):
    ts_day = JalaliTimestamp(1402, 6, 10 + day)  # Starting from Saturday
    full_name = ts_day.strftime("%A")
    short_name = ts_day.strftime("%a")
    print(f"  Day {day} ({'Sat' if day == 0 else ''}): {full_name:12s} ({short_name})")

# =============================================================================
# Month Names with Persian Locale
# =============================================================================

print("\n" + "=" * 60)
print("Month Names with Persian Locale")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15)

# Note: month_name() and day_name() methods support locale parameter
try:
    persian_month = ts.strftime("%B", locale="fa")
    print(f"\nPersian month name: {persian_month}")
except Exception as e:
    print("\nNote: Persian locale may require jdatetime locale support")
    print(f"Error: {e}")

# Alternative: Manual mapping
persian_months = {
    1: "فروردین",
    2: "اردیبهشت",
    3: "خرداد",
    4: "تیر",
    5: "مرداد",
    6: "شهریور",
    7: "مهر",
    8: "آبان",
    9: "آذر",
    10: "دی",
    11: "بهمن",
    12: "اسفند",
}

print("\nAll Jalali months in Persian:")
for month, name in persian_months.items():
    print(f"  Month {month:2d}: {name}")

# =============================================================================
# Day Names in Persian
# =============================================================================

print("\n" + "=" * 60)
print("Day Names in Persian")
print("=" * 60)

persian_days = {
    0: "شنبه",  # Saturday
    1: "یک‌شنبه",  # Sunday
    2: "دوشنبه",  # Monday
    3: "سه‌شنبه",  # Tuesday
    4: "چهارشنبه",  # Wednesday
    5: "پنج‌شنبه",  # Thursday
    6: "جمعه",  # Friday
}

print("All Jalali weekdays in Persian:")
for day, name in persian_days.items():
    print(f"  Day {day}: {name}")

# =============================================================================
# Persian Numerals Conversion
# =============================================================================

print("\n" + "=" * 60)
print("Persian Numerals Conversion")
print("=" * 60)


def to_persian_numerals(text):
    """Convert Arabic numerals to Persian numerals."""
    arabic_nums = "0123456789"
    persian_nums = "۰۱۲۳۴۵۶۷۸۹"
    translation_table = str.maketrans(arabic_nums, persian_nums)
    return text.translate(translation_table)


# Format date with Persian numerals
ts = JalaliTimestamp(1402, 6, 15)
date_str = ts.strftime("%Y/%m/%d")
date_persian = to_persian_numerals(date_str)

print(f"\nArabic numerals: {date_str}")
print(f"Persian numerals: {date_persian}")

# =============================================================================
# RTL Formatting for DataFrame Display
# =============================================================================

print("\n" + "=" * 60)
print("RTL Formatting for DataFrame Display")
print("=" * 60)

# Create DataFrame with Jalali dates
df = pd.DataFrame(
    {
        "jalali_date": [
            JalaliTimestamp(1402, 1, 1),
            JalaliTimestamp(1402, 6, 15),
            JalaliTimestamp(1402, 12, 29),
        ],
        "event": ["Nowruz", "Mid-year review", "Year-end"],
        "value": [100, 200, 300],
    }
)

# Add Persian formatted columns
df["date_persian"] = df["jalali_date"].apply(
    lambda x: to_persian_numerals(x.strftime("%Y/%m/%d"))
)
df["month_persian"] = df["jalali_date"].apply(lambda x: persian_months[x.month])
df["day_persian"] = df["jalali_date"].apply(lambda x: persian_days[x.dayofweek])

print("\nDataFrame with Persian formatting:")
print(df[["date_persian", "month_persian", "day_persian", "event", "value"]])

# =============================================================================
# Creating RTL-Ready Reports
# =============================================================================

print("\n" + "=" * 60)
print("Creating RTL-Ready Reports")
print("=" * 60)


def format_jalali_date_persian(ts):
    """Format Jalali date with Persian numerals and month name."""
    year = to_persian_numerals(str(ts.year))
    month = persian_months[ts.month]
    day = to_persian_numerals(str(ts.day).zfill(2))
    return f"{day} {month} {year}"


# Sample dates
dates = [
    JalaliTimestamp(1402, 1, 1),
    JalaliTimestamp(1402, 6, 15),
    JalaliTimestamp(1402, 12, 29),
]

print("\nDates in Persian format:")
for ts in dates:
    persian_date = format_jalali_date_persian(ts)
    print(f"  {persian_date}")

# =============================================================================
# Full Date-Time Formatting in Persian
# =============================================================================

print("\n" + "=" * 60)
print("Full Date-Time Formatting in Persian")
print("=" * 60)


def format_datetime_persian(ts):
    """Format full datetime with Persian numerals."""
    year = to_persian_numerals(str(ts.year))
    month = persian_months[ts.month]
    day = to_persian_numerals(str(ts.day).zfill(2))
    hour = to_persian_numerals(str(ts.hour).zfill(2))
    minute = to_persian_numerals(str(ts.minute).zfill(2))
    second = to_persian_numerals(str(ts.second).zfill(2))
    weekday = persian_days[ts.dayofweek]

    return f"{weekday}، {day} {month} {year} - ساعت {hour}:{minute}:{second}"


ts = JalaliTimestamp(1402, 6, 15, 14, 30, 45)
persian_datetime = format_datetime_persian(ts)

print(f"\nEnglish: {ts.strftime('%A, %B %d, %Y - %H:%M:%S')}")
print(f"Persian: {persian_datetime}")

# =============================================================================
# Series Formatting with Persian Locale
# =============================================================================

print("\n" + "=" * 60)
print("Series Formatting with Persian Locale")
print("=" * 60)

# Create Series of Jalali dates
dates_series = pd.Series(
    [
        JalaliTimestamp(1402, 1, 1),
        JalaliTimestamp(1402, 2, 15),
        JalaliTimestamp(1402, 3, 21),
        JalaliTimestamp(1402, 6, 15),
        JalaliTimestamp(1402, 9, 23),
    ]
)

# Format with Persian
dates_series_persian = dates_series.apply(format_jalali_date_persian)

print("\nOriginal dates:")
print(dates_series)

print("\nPersian formatted:")
print(dates_series_persian)

# =============================================================================
# Custom Format Strings for Business Reports
# =============================================================================

print("\n" + "=" * 60)
print("Custom Format Strings for Business Reports")
print("=" * 60)

ts = JalaliTimestamp(1402, 6, 15)

business_formats = [
    (
        "Report header",
        lambda x: f"گزارش {persian_months[x.month]} {to_persian_numerals(str(x.year))}",
    ),
    ("Invoice date", lambda x: to_persian_numerals(x.strftime("%Y/%m/%d"))),
    (
        "Full formal",
        lambda x: f"{to_persian_numerals(str(x.day))} {persian_months[x.month]} سال {to_persian_numerals(str(x.year))}",
    ),
    (
        "Short",
        lambda x: f"{to_persian_numerals(str(x.day))}/{to_persian_numerals(str(x.month))}/{to_persian_numerals(str(x.year))}",
    ),
]

print("\nBusiness report formats:")
for name, formatter in business_formats:
    print(f"  {name:20s}: {formatter(ts)}")

# =============================================================================
# Handling RTL in Text Output
# =============================================================================

print("\n" + "=" * 60)
print("Handling RTL in Text Output")
print("=" * 60)

print("\nNote: In RTL contexts, text should be displayed right-to-left")
print("For proper RTL rendering, use HTML/CSS with dir='rtl' attribute")

# Example HTML output
html_template = """
<div dir="rtl" style="font-family: Tahoma, Arial; text-align: right;">
    <h2>گزارش فروش</h2>
    <p>تاریخ: {date}</p>
    <p>ماه: {month}</p>
</div>
"""

date_persian = format_jalali_date_persian(ts)
month_persian = persian_months[ts.month]

html_output = html_template.format(date=date_persian, month=month_persian)

print("\nExample HTML for RTL display:")
print(html_output)

# =============================================================================
# DataFrame Export with Persian Formatting
# =============================================================================

print("\n" + "=" * 60)
print("DataFrame Export with Persian Formatting")
print("=" * 60)

df = pd.DataFrame(
    {
        "تاریخ": dates_series.apply(format_jalali_date_persian),
        "ماه": dates_series.apply(lambda x: persian_months[x.month]),
        "روز": dates_series.apply(lambda x: persian_days[x.dayofweek]),
        "مقدار": [1000, 2000, 3000, 4000, 5000],
    }
)

print("\nDataFrame ready for RTL display:")
print(df)

print("\nNote: For proper CSV export with Persian text, use UTF-8 encoding:")
print("  df.to_csv('report.csv', index=False, encoding='utf-8-sig')")

# =============================================================================
# Practical Example: Invoice with Persian Dates
# =============================================================================

print("\n" + "=" * 60)
print("Practical Example: Invoice with Persian Dates")
print("=" * 60)


def generate_invoice_persian(invoice_date, customer, amount):
    """Generate invoice text with Persian formatting."""
    date_str = format_jalali_date_persian(invoice_date)
    amount_persian = to_persian_numerals(f"{amount:,}")

    invoice = f"""
{"=" * 50}
                    فاکتور فروش
{"=" * 50}

تاریخ فاکتور:          {date_str}
نام مشتری:             {customer}
مبلغ فاکتور:           {amount_persian} ریال

{"=" * 50}
"""
    return invoice


invoice = generate_invoice_persian(JalaliTimestamp(1402, 6, 15), "شرکت نمونه", 15000000)

print(invoice)

print("\n" + "=" * 60)
print("Examples completed successfully!")
print("=" * 60)
