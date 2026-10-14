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

# This case study explains both the business question and how to read the evidence.
CASE = ('A fictional operations team must balance stock availability with cash tied up in products. Total '
 'stock can look healthy even when individual SKU locations are close to stockout.')
DECISION = ('Create a transparent replenishment review list and examine how an extra safety buffer changes the '
 'proposed units and purchase cost.')
DATA_CONTEXT = ('One row is one SKU at one warehouse. The 180 fictional rows cover 60 SKUs across Delhi, Mumbai and '
 'Bengaluru. Repeated SKU codes across warehouses are valid, not duplicate errors. Demand is an assumed '
 'average, not a forecast fitted by this app.')
FORMULAS = [('Stock value',
  'Sum of stock on hand x unit cost',
  'Cost value of current stock, not selling value or realizable cash.'),
 ('Reorder point',
  'Daily demand x (lead time days + extra buffer days) + safety stock',
  'A simple deterministic threshold in units.'),
 ('Suggested units',
  'Maximum of reorder point - stock on hand and zero',
  'A proposed top-up to the threshold, ignoring existing purchase orders.'),
 ('Days cover',
  'Stock on hand / daily demand',
  'How many days stock would last if assumed demand stayed constant.'),
 ('Estimated purchase',
  'Sum of suggested units x unit cost',
  'An approximate acquisition cost, excluding shipping, discounts and minimum order quantities.')]
VISUAL_GUIDE = [('Inventory value by warehouse',
  'Show where inventory cost is concentrated.',
  'The bar height is stock at cost in INR. Each bar is a warehouse, and stacked colors represent '
  'categories.',
  'Which warehouse and category hold the most inventory value?',
  'High value alone is not excess stock: demand, lead time and service requirements matter.'),
 ('Demand versus stock',
  'Compare stock levels with assumed demand for individual SKU locations.',
  'Each bubble is a SKU/warehouse pair. X is daily demand, y is stock on hand, color flags a positive '
  'reorder suggestion, and bubble size reflects unit cost. Hover shows SKU, warehouse and threshold.',
  'Which locations combine high demand with insufficient stock under this scenario?',
  'The true/false flag depends on the chosen buffer. This is not a probabilistic stockout forecast.'),
 ('Days of cover distribution',
  'Identify short-cover and long-cover SKU locations.',
  'The histogram counts SKU locations in ranges of days cover. Days cover is stock divided by assumed '
  'daily demand.',
  'Is inventory unevenly distributed relative to demand?',
  'Cover assumes demand stays constant. Locations with zero demand would have undefined cover and are '
  'omitted from this histogram.'),
 ('Coverage spread by category',
  'Compare the typical cover and variability across product categories.',
  'The center line is median days cover; the box spans the middle 50%; whiskers use 1.5 interquartile '
  'ranges. Individual points beyond them are possible outliers.',
  'Which categories have very different stock coverage across locations?',
  'A single policy may not suit all categories. Longer lead times can justify greater cover.'),
 ('Share of locations needing reorder',
  'Summarize the breadth of replenishment needs by warehouse and category.',
  'Each heatmap cell is the percentage of SKU locations in that warehouse/category with suggested units '
  'above zero. Colors use a fixed 0-100 scale.',
  'Is the reorder workload concentrated in a particular warehouse/category?',
  'It counts locations equally. It does not show units, purchase cost, urgency or customer impact; use '
  'the worklist and cost KPIs alongside it.')]
RECOMMENDATIONS = ['Review zero-stock locations and the largest proposed replenishments against customer commitments and '
 'stock already on order.',
 'Compare buffer scenarios and their incremental cash requirement before adopting a company-wide rule.',
 'Add demand variability, service targets, minimum order quantities, supplier calendars and incoming '
 'purchase orders before using the calculation operationally.']
LIMITATIONS = ('The model assumes constant daily demand and fixed lead time. It ignores seasonality, open purchase '
 'orders, supplier capacity, order multiples, expiry and transfer options. No purchase is placed by '
 'this dashboard.')

with st.expander("Business problem and context", expanded=True):
    st.markdown("**The problem:** " + CASE)
    st.markdown("**Decision this dashboard supports:** " + DECISION)
    st.markdown("**What one row means:** " + DATA_CONTEXT)
    st.info("This is a fictional teaching case. Every finding below is calculated from the selected CSV rows, not a claim about a real business.")
    st.write("Start with the KPI cards, read the explanation under each visual, inspect the source data, then open Full report for the complete analysis and a downloadable copy. Filters recalculate the findings and report.")


FIELD_GUIDE = {'sku': 'Stock keeping unit; the same SKU can appear in different warehouses.',
 'warehouse': 'Stock location; SKU plus warehouse identifies the row.',
 'category': 'Product category.',
 'stock_on_hand': 'Units currently held at this location.',
 'daily_demand': 'Assumed demand in units per day; not a forecast fitted by this dashboard.',
 'lead_time_days': 'Assumed replenishment lead time in days.',
 'safety_stock': 'Baseline safety inventory in units.',
 'unit_cost': 'Purchase cost per unit in INR.'}

def explain_visual(index, container=st):
    title, purpose, reading, question, caution = VISUAL_GUIDE[index]
    container.markdown(f"**{title}: what this visual explains**")
    container.write(purpose)
    container.markdown("**How to read it:** " + reading)
    container.markdown("**Question it answers:** " + question)
    container.caption("Interpretation limit: " + caution)

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
value_by_warehouse = filtered.groupby("warehouse")["inventory_value"].sum()
top_warehouse = value_by_warehouse.idxmax()
stockouts = int((filtered["stock_on_hand"]==0).sum())
base_reorder = (filtered["daily_demand"]*filtered["lead_time_days"]+filtered["safety_stock"]-filtered["stock_on_hand"]).clip(lower=0)
base_purchase = (base_reorder*filtered["unit_cost"]).sum()
purchase = (filtered["reorder_units"]*filtered["unit_cost"]).sum()
largest = filtered.sort_values("reorder_units",ascending=False).iloc[0]
insights = [
 ("What does the selected stock represent?", f"{len(filtered)} SKU locations representing {filtered['sku'].nunique()} distinct SKUs hold INR {filtered['inventory_value'].sum():,.2f} of stock at cost. One SKU can appear at several locations."),
 ("Where is the most inventory value?", f"{top_warehouse} holds INR {value_by_warehouse[top_warehouse]:,.2f}, or {ratio(value_by_warehouse[top_warehouse],filtered['inventory_value'].sum()):.1%} of selected stock value."),
 ("How many locations need attention?", f"{int(filtered['needs_reorder'].sum())} of {len(filtered)} locations need a top-up under the current rule. {stockouts} currently have zero stock. These are different conditions."),
 ("What would the proposed top-up cost?", f"The rule suggests {filtered['reorder_units'].sum():,.0f} units at an estimated INR {purchase:,.2f}. This is a planning calculation, not an order placed with a supplier."),
 ("What changes when the buffer changes?", f"With {buffer} extra safety days, purchase cost is INR {purchase-base_purchase:,.2f} above the zero-extra-buffer scenario for the same selected records."),
 ("Which record has the largest suggested quantity?", f"{largest['sku']} at {largest['warehouse']}: {largest['reorder_units']:,.0f} units, from stock {largest['stock_on_hand']:,.0f} toward threshold {largest['reorder_point']:,.0f}." if largest['reorder_units']>0 else "No selected location has a positive reorder suggestion."),
]
kpi_values=[("Stock value (INR)",f"{filtered['inventory_value'].sum():,.2f}"),("Locations needing reorder",str(int(filtered['needs_reorder'].sum()))),("Suggested units",f"{filtered['reorder_units'].sum():,.0f}"),("Estimated purchase (INR)",f"{purchase:,.2f}"),("Extra safety buffer (days)",str(buffer))]

# Build one report from the same filtered dataframe used by the charts.
scope_parts = []
for column in frame.select_dtypes(include="object").columns:
    if frame[column].nunique() <= 12:
        scope_parts.append(column.replace("_", " ") + ": " + ", ".join(map(str, sorted(filtered[column].unique()))))
for column in frame.select_dtypes(include="datetime").columns:
    scope_parts.append(f"{column}: observed records {filtered[column].min():%Y-%m-%d} to {filtered[column].max():%Y-%m-%d}")
scope = "; ".join(scope_parts)
scope += f"; extra safety buffer: {buffer} days"

with st.expander("KPI definitions and calculation rules"):
    st.dataframe(pd.DataFrame(FORMULAS, columns=["Measure", "Calculation", "Business meaning"]), hide_index=True, width="stretch")
    st.caption("All cards, charts and findings use the same selected rows. Ratios use summed numerators and denominators where stated. A zero denominator makes the corresponding rate undefined; use the underlying counts before interpreting a displayed fallback zero.")

st.subheader("What the selected data answers")
for question, answer in insights[:3]:
    st.markdown(f"**{question}** {answer}")
st.caption(f"Analysis scope: {len(filtered):,} of {len(frame):,} source rows. " + scope)

report_parts = [
    "# " + '04 Inventory Planning' + " - full analytical report",
    "## 1. Business problem\n" + CASE,
    "## 2. Context and decision\n" + DECISION + "\n\n" + DATA_CONTEXT,
    "## 3. Data and analysis scope\n" + f"Dataset: `{DATA_FILE.name}`. Selected rows: {len(filtered):,} of {len(frame):,}.\n\n" + scope + "\n\nAll data is fictional teaching data; monetary figures are INR. This report is recalculated for the current selections. It is descriptive, not a forecast or causal study.",
    "## 4. Executive summary\n" + "\n\n".join(answer for _,answer in insights[:3]),
    "## 5. KPI results\n| Measure | Selected result |\n| --- | --- |\n" + "\n".join(f"| {name} | {value} |" for name,value in kpi_values),
    "## 6. Definitions and methods\n| Measure | Calculation | Interpretation |\n| --- | --- | --- |\n" + "\n".join(f"| {name} | {formula} | {meaning} |" for name,formula,meaning in FORMULAS),
    "## 7. Questions answered by the data\n" + "\n\n".join(f"### {question}\n{answer}" for question,answer in insights),
    "## 8. Every visual explained\n" + "\n\n".join(f"### {title}\n**Purpose:** {purpose}\n\n**How to read:** {reading}\n\n**Question answered:** {question}\n\n**Caution:** {caution}" for title,purpose,reading,question,caution in VISUAL_GUIDE),
    "## 9. Data quality and aggregation\n" + f"Source rows: {len(frame):,}; exact duplicate rows: {frame.duplicated().sum():,}; missing cells: {frame.isna().sum().sum():,}. The data tab shows each field's type and missing count. Required numeric fields are parsed explicitly; missing required values stop analysis instead of silently dropping rows. No outliers are automatically removed. These checks do not establish that values are accurate or that the sample represents a real population.",
    "## 10. Suggested next steps\n" + "\n".join(f"{i}. {text}" for i,text in enumerate(RECOMMENDATIONS,1)) + "\n\nTreat these as investigation steps, not decisions already proved by the data.",
    "## 11. What this analysis cannot answer\n" + LIMITATIONS + "\n\nTies in automatically named leaders are resolved by the dataframe's sorted group order; inspect the tables for other tied groups. No confidence intervals or significance tests are calculated. Single-row or constant data cannot support correlation estimates.",
    "## 12. Reproduce and extend the analysis\nOpen the CSV beside app.py, restore the filter selections listed above, and compare a small sample with the documented formulas. The data tab contains a filtered CSV download, descriptive statistics and a source-quality table. Use Plotly hover to inspect values, zoom to investigate a period, and double-click to reset axes. Matplotlib and Seaborn images can be enlarged with their fullscreen controls. Add an extra variable or a controlled experiment to investigate an unanswered question.",
]
report_parts[5] += "\n\n### Source field dictionary\n| Field | Meaning and units |\n| --- | --- |\n" + "\n".join(f"| `{name}` | {meaning} |" for name, meaning in FIELD_GUIDE.items())
full_report = "\n\n".join(report_parts)

overview, explore, data_tab, report_tab = st.tabs(["Inventory dashboard", "Explore the data", "Data and quality", "Full report"])
with overview:
    grouped = filtered.groupby(["warehouse","category"], as_index=False)["inventory_value"].sum()
    st.plotly_chart(px.bar(grouped, x="warehouse", y="inventory_value", color="category", title="Inventory value by warehouse", labels={"inventory_value":"INR"}), use_container_width=True)
    explain_visual(0, st)
    st.plotly_chart(px.scatter(filtered, x="daily_demand", y="stock_on_hand", color="needs_reorder", size="unit_cost", hover_data=["sku","warehouse","reorder_point"], title="Demand versus stock"), use_container_width=True)
    explain_visual(1, st)
    st.subheader("Replenishment worklist")
    st.write("Only locations with a positive suggested top-up appear here, largest suggested quantity first. Stock is current units; reorder point is the scenario threshold; reorder units is the positive gap. This is a review list, not a purchase order.")
    st.dataframe(filtered.loc[filtered["needs_reorder"], ["sku","warehouse","stock_on_hand","reorder_point","reorder_units"]].sort_values("reorder_units", ascending=False), hide_index=True, width="stretch")
    st.caption("The table above gives exact grouped values behind the dashboard. Group sizes matter: compare counts alongside totals or rates, and use the data tab to inspect individual observations.")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["days_cover"].dropna(), bins=20, color="#059669", edgecolor="white")
    ax.set(title="Days of inventory cover", xlabel="Days (stock / daily demand)", ylabel="SKU locations")
    left.pyplot(fig); plt.close(fig)
    explain_visual(2, left)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="category", y="days_cover", ax=ax, color="#bbf7d0")
    ax.set_title("Coverage spread by category")
    right.pyplot(fig); plt.close(fig)
    explain_visual(3, right)
    fig, ax = plt.subplots(figsize=(9,4))
    sns.heatmap(filtered.pivot_table(index="warehouse", columns="category", values="needs_reorder", aggfunc="mean")*100, annot=True, fmt=".1f", cmap="YlOrRd", vmin=0, vmax=100, ax=ax)
    ax.set_title("SKU locations needing reorder (%)")
    st.pyplot(fig); plt.close(fig)
    explain_visual(4, st)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Source field dictionary")
    st.dataframe(pd.DataFrame(FIELD_GUIDE.items(), columns=["Field", "Meaning and units"]), hide_index=True, width="stretch")
    st.subheader("Filtered records")
    st.write("These are the exact selected observations used for the KPIs and charts, including any derived columns. Sorting this table does not change the analytical filters. Compare a few rows with the formulas before relying on an aggregate.")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_inventory.csv", "text/csv")
    st.subheader("Numeric summary")
    st.write("Count is the number of available values; mean is the arithmetic average; std measures spread; min/max are extremes; 25%, 50% and 75% are quartiles. The 50% value is the median. Identifier-like numeric columns and derived measures require business context before interpretation.")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Increase the safety buffer and record the extra cash required.\n2. Identify stockouts and high-cover products.\n3. Explain why SKU-location counts differ from unique SKU counts.\n4. Add incoming purchase orders to improve the reorder formula.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")

with report_tab:
    st.download_button("Download full report (Markdown)", full_report, "04_inventory_planning_report.md", "text/markdown")
    st.markdown(full_report)
