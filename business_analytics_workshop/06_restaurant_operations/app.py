"""Restaurant Operations Dashboard: a beginner Streamlit project using a fictional teaching dataset."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Restaurant Operations Dashboard", page_icon=":bar_chart:", layout="wide")
st.title("Restaurant Operations Dashboard")
st.caption("Business Analytics Workshop | Fictional teaching data | Currency: INR")
st.write("Connect order value, service time and customer ratings. Compare branches and meal periods to identify operational questions.")

# 1. Load the CSV beside this script, regardless of the terminal's directory.
# Keeping this uncached lets students edit the CSV and immediately rerun the app.
DATA_FILE = Path(__file__).resolve().with_name("restaurant_orders.csv")
try:
    frame = pd.read_csv(DATA_FILE)
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    numeric_columns = ['guests', 'bill_amount', 'food_cost', 'wait_minutes', 'rating']
    required_columns = ['order_id', 'date', 'branch', 'meal_period', 'channel', 'guests', 'bill_amount', 'food_cost', 'wait_minutes', 'rating']
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
selected_branch = st.sidebar.multiselect("Branches", sorted(frame["branch"].unique()), default=sorted(frame["branch"].unique()), key="06_restaurant_operations_branch")
filtered = filtered[filtered["branch"].isin(selected_branch)]
selected_meal_period = st.sidebar.multiselect("Meal periods", sorted(frame["meal_period"].unique()), default=sorted(frame["meal_period"].unique()), key="06_restaurant_operations_meal_period")
filtered = filtered[filtered["meal_period"].isin(selected_meal_period)]
dates = st.sidebar.date_input("Date range", (frame["date"].min().date(), frame["date"].max().date()), min_value=frame["date"].min().date(), max_value=frame["date"].max().date(), key="06_restaurant_operations_dates")
if len(dates) != 2:
    st.info("Choose both a start and an end date.")
    st.stop()
filtered = filtered[filtered["date"].dt.date.between(dates[0], dates[1])]
st.sidebar.caption(f"Showing {len(filtered):,} of {len(frame):,} rows")
if filtered.empty:
    st.info("No rows match these filters. Select at least one value or widen the date range.")
    st.stop()

# 3. Derive business measures, then compare totals, distributions and segments.
filtered["contribution"] = filtered["bill_amount"]-filtered["food_cost"]
sales = filtered["bill_amount"].sum()
columns = st.columns(4)
columns[0].metric("Sales (INR)", f"{sales:,.0f}")
columns[1].metric("Average bill (INR)", f"{filtered['bill_amount'].mean():,.0f}")
columns[2].metric("Average wait", f"{filtered['wait_minutes'].mean():.1f} min")
columns[3].metric("Average rating", f"{filtered['rating'].mean():.2f} / 5")
st.caption("One row is one order. Contribution = bill - food cost, before staffing, rent, delivery fees and tax. Ratings are observations, not proof that wait time causes a particular rating.")
overview, explore, data_tab = st.tabs(["Operations dashboard", "Explore the data", "Data and quality"])
with overview:
    daily = filtered.groupby(["date","branch"], as_index=False)["bill_amount"].sum()
    st.plotly_chart(px.line(daily, x="date", y="bill_amount", color="branch", title="Daily sales by branch", labels={"bill_amount":"Sales (INR)"}), use_container_width=True)
    st.plotly_chart(px.scatter(filtered, x="wait_minutes", y="rating", color="channel", size="guests", hover_data=["order_id","branch","bill_amount"], opacity=.6, title="Wait time and rating"), use_container_width=True)
    st.dataframe(filtered.groupby("branch").agg(orders=("order_id","size"), sales=("bill_amount","sum"), contribution=("contribution","sum"), average_wait=("wait_minutes","mean"), rating=("rating","mean")).round(2), width="stretch")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["bill_amount"], bins=20, color="#e11d48", edgecolor="white")
    ax.set(title="Order value distribution", xlabel="Bill amount (INR)", ylabel="Orders")
    left.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="meal_period", y="wait_minutes", ax=ax, color="#fecdd3")
    ax.set_title("Service time by meal period")
    right.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9,4))
    sns.heatmap(filtered.pivot_table(index="branch", columns="meal_period", values="rating", aggfunc="mean"), annot=True, fmt=".2f", vmin=1, vmax=5, cmap="YlGnBu", ax=ax)
    ax.set_title("Average rating by branch and meal period")
    st.pyplot(fig); plt.close(fig)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Filtered records")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_restaurant_orders.csv", "text/csv")
    st.subheader("Numeric summary")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Find the branch with the longest average wait.\n2. Add a channel filter and compare delivery with dine in.\n3. Calculate sales per guest using totals.\n4. Compare group sizes before recommending a staffing change.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")
