"""Retail Sales Explorer: a beginner Streamlit project using a fictional teaching dataset."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Retail Sales Explorer", page_icon=":bar_chart:", layout="wide")
st.title("Retail Sales Explorer")
st.caption("Business Analytics Workshop | Fictional teaching data | Currency: INR")
st.write("Follow revenue from individual orders to regional performance. Compare sales volume, discounts and gross profit.")

# 1. Load the CSV beside this script, regardless of the terminal's directory.
# Keeping this uncached lets students edit the CSV and immediately rerun the app.
DATA_FILE = Path(__file__).resolve().with_name("retail_sales.csv")
try:
    frame = pd.read_csv(DATA_FILE)
    frame["order_date"] = pd.to_datetime(frame["order_date"], errors="raise")
    numeric_columns = ['units', 'unit_price', 'discount_pct', 'unit_cost']
    required_columns = ['order_id', 'order_date', 'region', 'category', 'channel', 'units', 'unit_price', 'discount_pct', 'unit_cost']
    if not set(required_columns).issubset(frame.columns):
        raise ValueError("The CSV is missing required columns.")
    if frame.empty:
        raise ValueError("The CSV contains no rows.")
    for column in numeric_columns:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    if frame[required_columns].isna().any().any():
        raise ValueError("Fill missing values in the required analysis columns first.")
except (OSError, ValueError, KeyError) as error:
    st.error(f"Could not load {DATA_FILE.name}: {error}")
    st.stop()

def ratio(numerator, denominator):
    """Return zero for an empty denominator so filters never divide by zero."""
    return numerator / denominator if denominator else 0.0

# 2. Apply sidebar filters before calculating any KPI or chart.
st.sidebar.header("Filter the data")
filtered = frame.copy()
selected_region = st.sidebar.multiselect("Regions", sorted(frame["region"].unique()), default=sorted(frame["region"].unique()), key="01_retail_sales_region")
filtered = filtered[filtered["region"].isin(selected_region)]
selected_category = st.sidebar.multiselect("Categories", sorted(frame["category"].unique()), default=sorted(frame["category"].unique()), key="01_retail_sales_category")
filtered = filtered[filtered["category"].isin(selected_category)]
dates = st.sidebar.date_input("Date range", (frame["order_date"].min().date(), frame["order_date"].max().date()), min_value=frame["order_date"].min().date(), max_value=frame["order_date"].max().date(), key="01_retail_sales_dates")
if len(dates) != 2:
    st.info("Choose both a start and an end date.")
    st.stop()
filtered = filtered[filtered["order_date"].dt.date.between(dates[0], dates[1])]
st.sidebar.caption(f"Showing {len(filtered):,} of {len(frame):,} rows")
if filtered.empty:
    st.info("No rows match these filters. Select at least one value or widen the date range.")
    st.stop()

# 3. Derive business measures, then compare totals, distributions and segments.
filtered["revenue"] = filtered["units"] * filtered["unit_price"] * (1 - filtered["discount_pct"] / 100)
filtered["gross_profit"] = filtered["revenue"] - filtered["units"] * filtered["unit_cost"]
revenue = filtered["revenue"].sum()
profit = filtered["gross_profit"].sum()
columns = st.columns(4)
columns[0].metric("Net sales (INR)", f"{revenue:,.0f}")
columns[1].metric("Gross profit (INR)", f"{profit:,.0f}")
columns[2].metric("Gross margin", f"{ratio(profit, revenue):.1%}")
columns[3].metric("Average order (INR)", f"{filtered['revenue'].mean():,.0f}")
st.caption("One row is one order. Sales are after discounts; gross profit excludes operating expenses and tax.")
overview, explore, data_tab = st.tabs(["Sales dashboard", "Explore the data", "Data and quality"])
with overview:
    monthly = filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)[["revenue","gross_profit"]].sum()
    st.plotly_chart(px.line(monthly, x="month", y=["revenue","gross_profit"], markers=True, title="Monthly sales and gross profit", labels={"value":"INR","month":"Month"}), use_container_width=True)
    by_region = filtered.groupby(["region","category"], as_index=False)["revenue"].sum()
    st.plotly_chart(px.bar(by_region, x="region", y="revenue", color="category", title="Where do sales come from?", labels={"revenue":"Net sales (INR)"}), use_container_width=True)
    st.dataframe(filtered.groupby("category").agg(orders=("revenue","size"), units=("units","sum"), sales=("revenue","sum"), gross_profit=("gross_profit","sum")).round(2), width="stretch")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["revenue"], bins=20, color="#2563eb", edgecolor="white")
    ax.set(title="Order value distribution", xlabel="Net sales per order (INR)", ylabel="Orders")
    left.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="category", y="gross_profit", ax=ax, color="#a7f3d0")
    ax.set(title="Profit spread by category", xlabel="Category", ylabel="Gross profit (INR)")
    right.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,4))
    sns.heatmap(filtered[["units","discount_pct","revenue","gross_profit"]].corr(), annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Correlation: which measures move together?")
    st.pyplot(fig); plt.close(fig)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Filtered records")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_retail_sales.csv", "text/csv")
    st.subheader("Numeric summary")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Compare North and South with the same date range.\n2. Add a channel filter.\n3. Find categories with high revenue but low margin.\n4. Explain why correlation between sales and profit is partly built into the formulas.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")
