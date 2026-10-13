"""Inventory Planning Desk: a beginner Streamlit project using a fictional teaching dataset."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Inventory Planning Desk", page_icon=":bar_chart:", layout="wide")
st.title("Inventory Planning Desk")
st.caption("Business Analytics Workshop | Fictional teaching data | Currency: INR")
st.write("Find products that may need replenishment and compare inventory value across warehouses. Change the safety buffer to explore a simple planning scenario.")

# 1. Load the CSV beside this script, regardless of the terminal's directory.
# Keeping this uncached lets students edit the CSV and immediately rerun the app.
DATA_FILE = Path(__file__).resolve().with_name("inventory.csv")
try:
    frame = pd.read_csv(DATA_FILE)
    # This dataset is a single snapshot, so it has no date filter.
    numeric_columns = ['stock_on_hand', 'daily_demand', 'lead_time_days', 'safety_stock', 'unit_cost']
    required_columns = ['sku', 'warehouse', 'category', 'stock_on_hand', 'daily_demand', 'lead_time_days', 'safety_stock', 'unit_cost']
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
selected_warehouse = st.sidebar.multiselect("Warehouses", sorted(frame["warehouse"].unique()), default=sorted(frame["warehouse"].unique()), key="04_inventory_planning_warehouse")
filtered = filtered[filtered["warehouse"].isin(selected_warehouse)]
selected_category = st.sidebar.multiselect("Categories", sorted(frame["category"].unique()), default=sorted(frame["category"].unique()), key="04_inventory_planning_category")
filtered = filtered[filtered["category"].isin(selected_category)]
st.sidebar.caption(f"Showing {len(filtered):,} of {len(frame):,} rows")
if filtered.empty:
    st.info("No rows match these filters. Select at least one value or widen the date range.")
    st.stop()

# 3. Derive business measures, then compare totals, distributions and segments.
buffer = st.sidebar.slider("Extra safety buffer (days)", 0, 14, 0, key="inventory_buffer")
filtered["reorder_point"] = filtered["daily_demand"]*(filtered["lead_time_days"]+buffer)+filtered["safety_stock"]
filtered["reorder_units"] = (filtered["reorder_point"]-filtered["stock_on_hand"]).clip(lower=0)
filtered["inventory_value"] = filtered["stock_on_hand"]*filtered["unit_cost"]
filtered["days_cover"] = filtered["stock_on_hand"].div(filtered["daily_demand"].replace(0,float("nan")))
filtered["needs_reorder"] = filtered["reorder_units"]>0
columns = st.columns(4)
columns[0].metric("Stock value (INR)", f"{filtered['inventory_value'].sum():,.0f}")
columns[1].metric("Locations needing reorder", f"{filtered['needs_reorder'].sum():,}")
columns[2].metric("Suggested units", f"{filtered['reorder_units'].sum():,.0f}")
columns[3].metric("Estimated purchase (INR)", f"{(filtered['reorder_units']*filtered['unit_cost']).sum():,.0f}")
st.caption("One row is one SKU at one warehouse. Reorder point = demand x (lead time + extra buffer) + safety stock. This simplified scenario ignores open purchase orders and demand variability.")
overview, explore, data_tab = st.tabs(["Inventory dashboard", "Explore the data", "Data and quality"])
with overview:
    grouped = filtered.groupby(["warehouse","category"], as_index=False)["inventory_value"].sum()
    st.plotly_chart(px.bar(grouped, x="warehouse", y="inventory_value", color="category", title="Inventory value by warehouse", labels={"inventory_value":"INR"}), use_container_width=True)
    st.plotly_chart(px.scatter(filtered, x="daily_demand", y="stock_on_hand", color="needs_reorder", size="unit_cost", hover_data=["sku","warehouse","reorder_point"], title="Demand versus stock"), use_container_width=True)
    st.subheader("Replenishment worklist")
    st.dataframe(filtered.loc[filtered["needs_reorder"], ["sku","warehouse","stock_on_hand","reorder_point","reorder_units"]].sort_values("reorder_units", ascending=False), hide_index=True, width="stretch")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["days_cover"].dropna(), bins=20, color="#059669", edgecolor="white")
    ax.set(title="Days of inventory cover", xlabel="Days (stock / daily demand)", ylabel="SKU locations")
    left.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="category", y="days_cover", ax=ax, color="#bbf7d0")
    ax.set_title("Coverage spread by category")
    right.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9,4))
    sns.heatmap(filtered.pivot_table(index="warehouse", columns="category", values="needs_reorder", aggfunc="mean")*100, annot=True, fmt=".1f", cmap="YlOrRd", vmin=0, vmax=100, ax=ax)
    ax.set_title("SKU locations needing reorder (%)")
    st.pyplot(fig); plt.close(fig)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Filtered records")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_inventory.csv", "text/csv")
    st.subheader("Numeric summary")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Increase the safety buffer and record the extra cash required.\n2. Identify stockouts and high-cover products.\n3. Explain why SKU-location counts differ from unique SKU counts.\n4. Add incoming purchase orders to improve the reorder formula.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")
