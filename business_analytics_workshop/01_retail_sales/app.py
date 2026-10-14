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

# This case study explains both the business question and how to read the evidence.
CASE = ('A fictional retail manager sees sales totals but cannot tell which regions and categories create '
 'profitable demand. More revenue can hide heavy discounts, costly products, or a small number of '
 'unusually large orders.')
DECISION = ('Decide which categories and regions deserve a closer pricing, merchandising or cost review before '
 'changing stock or promotions.')
DATA_CONTEXT = ('One row is one order with a single category, channel and region. The dataset contains 720 fictional '
 'orders over January to June 2025. It does not contain customer-level repeat purchases, refunds, '
 'operating expenses or taxes.')
FORMULAS = [('Net sales',
  'Sum of units x unit price x (1 - discount percentage / 100)',
  'Sales after the stated discount; not cash collected.'),
 ('Gross profit',
  'Net sales - sum of units x unit cost',
  'Contribution after product cost, before operating expenses and tax.'),
 ('Gross margin',
  'Total gross profit / total net sales x 100',
  'A weighted total margin, not the average of each order margin.'),
 ('Average order',
  'Total net sales / number of selected orders',
  'Compare with the median because large orders can move the mean.')]
VISUAL_GUIDE = [('Monthly sales and gross profit',
  'Identify when selected sales and product-level profit are strongest.',
  'The horizontal axis is calendar month. The vertical axis is INR. Each line sums one measure across '
  'selected orders in that month. Hover shows values; the legend can hide a line.',
  'Which month contributed the most sales, and did product profit move in the same direction?',
  'Boundary months may contain fewer selected days. A larger total is not necessarily a higher daily '
  'growth rate. No prior-year comparison is available.'),
 ('Regional category mix',
  'Separate the size of a region from the categories contributing to it.',
  'Each stacked bar is a region. Its total height is regional net sales in INR; colors split that total '
  'by category. Hover identifies each segment.',
  'Where are selected sales concentrated, and which products explain that concentration?',
  'This chart measures totals, not margin, population-adjusted demand, customer loyalty or causal '
  'effects of location.'),
 ('Order value distribution',
  'Show whether a typical order is small or whether large orders drive the average.',
  'Matplotlib groups order values into 20 intervals. The x-axis is net sales per order in INR; the '
  'y-axis counts orders in each interval. A long right tail signals some high-value orders.',
  'How representative is the average order value of an ordinary order?',
  'Bin choices change the appearance. A high-value order is not automatically a data error.'),
 ('Profit spread by category',
  'Compare typical profit and variability, not just totals.',
  'The middle line of each Seaborn box is the median. The box covers the middle 50% of order profits. '
  'Whiskers extend to observations within 1.5 interquartile ranges; separate points are possible '
  'outliers.',
  'Which categories have consistently profitable orders or wide variation?',
  'Categories can have unequal sample sizes. Points outside the whiskers are observations to '
  'investigate, not records to delete automatically.'),
 ('Correlation between measures',
  'Explore linear relationships among quantity, discounts, sales and profit.',
  'Cells show Pearson correlation from -1 to +1. Positive values mean measures tend to increase '
  'together; negative values mean they tend to move in opposite directions. Diagonal values are 1.',
  'Which measures move together within the selected orders?',
  'Sales and profit share mathematical inputs. Correlation is partly mechanical and does not prove that '
  'discounting causes a profit change. Blank cells mean a relationship cannot be estimated from '
  'constant or insufficient data.')]
RECOMMENDATIONS = ['Review the sales-leading category alongside the margin-leading category; investigate cost and '
 'discount differences before changing prices.',
 'Inspect unusually large or negative-profit orders in the data table and confirm they are valid '
 'business transactions.',
 'Compare equal-length periods and add refunds, operating costs and customer counts before making a '
 'profitability or growth decision.']
LIMITATIONS = ('No customer acquisition costs, returns, store sizes or repeat-customer identifiers are included. '
 'Gross profit is not net profit. This descriptive dashboard cannot estimate the causal impact of a '
 'discount or forecast demand.')

with st.expander("Business problem and context", expanded=True):
    st.markdown("**The problem:** " + CASE)
    st.markdown("**Decision this dashboard supports:** " + DECISION)
    st.markdown("**What one row means:** " + DATA_CONTEXT)
    st.info("This is a fictional teaching case. Every finding below is calculated from the selected CSV rows, not a claim about a real business.")
    st.write("Start with the KPI cards, read the explanation under each visual, inspect the source data, then open Full report for the complete analysis and a downloadable copy. Filters recalculate the findings and report.")


FIELD_GUIDE = {'order_id': 'Synthetic order identifier; one row per order.',
 'order_date': 'Order date; filters are inclusive.',
 'region': 'Sales region used to group orders.',
 'category': 'Product category represented by the order.',
 'channel': 'Sales channel used for the order.',
 'units': 'Number of units sold.',
 'unit_price': 'List price per unit in INR before discount.',
 'discount_pct': 'Discount percentage, from 0 to 100.',
 'unit_cost': 'Product cost per unit in INR.'}

def explain_visual(index, container=st):
    title, purpose, reading, question, caution = VISUAL_GUIDE[index]
    container.markdown(f"**{title}: what this visual explains**")
    container.write(purpose)
    container.markdown("**How to read it:** " + reading)
    container.markdown("**Question it answers:** " + question)
    container.caption("Interpretation limit: " + caution)

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
sales_by_region = filtered.groupby("region")["revenue"].sum()
category_summary = filtered.groupby("category").agg(sales=("revenue","sum"), profit=("gross_profit","sum"), orders=("revenue","size"))
category_summary["margin"] = category_summary["profit"].div(category_summary["sales"].replace(0,float("nan")))
monthly_totals = filtered.groupby(filtered["order_date"].dt.to_period("M"))["revenue"].sum()
top_region = sales_by_region.idxmax()
top_category = category_summary["sales"].idxmax()
margin_category = category_summary["margin"].idxmax()
insights = [
 ("How much business is represented?", f"The selected {len(filtered):,} orders generated INR {revenue:,.2f} of net sales and INR {profit:,.2f} of gross profit. Total gross margin is {ratio(profit,revenue):.2%}."),
 ("Which region leads sales?", f"{top_region} has INR {sales_by_region[top_region]:,.2f}, or {ratio(sales_by_region[top_region],revenue):.1%} of selected sales. This is a revenue concentration, not a productivity ranking."),
 ("Which category leads volume of sales?", f"{top_category} leads category revenue at INR {category_summary.loc[top_category,'sales']:,.2f} across {category_summary.loc[top_category,'orders']:,.0f} orders."),
 ("Does the revenue leader also lead margin?", f"The highest aggregate margin belongs to {margin_category} at {category_summary.loc[margin_category,'margin']:.1%}. Revenue and margin answer different questions; inspect both before expanding a category."),
 ("What is a typical order worth?", f"Mean order value is INR {filtered['revenue'].mean():,.2f}; the median is INR {filtered['revenue'].median():,.2f}. Their difference shows how the order-value distribution affects the average."),
 ("Which month contributed most?", f"{monthly_totals.idxmax()} has the largest selected monthly sales total: INR {monthly_totals.max():,.2f}. Date filters can produce partial months, so compare equivalent exposure before calling this growth."),
]
kpi_values = [("Net sales (INR)", f"{revenue:,.2f}"),("Gross profit (INR)", f"{profit:,.2f}"),("Gross margin", f"{ratio(profit,revenue):.2%}"),("Average order (INR)", f"{filtered['revenue'].mean():,.2f}")]

# Build one report from the same filtered dataframe used by the charts.
scope_parts = []
for column in frame.select_dtypes(include="object").columns:
    if frame[column].nunique() <= 12:
        scope_parts.append(column.replace("_", " ") + ": " + ", ".join(map(str, sorted(filtered[column].unique()))))
for column in frame.select_dtypes(include="datetime").columns:
    scope_parts.append(f"{column}: observed records {filtered[column].min():%Y-%m-%d} to {filtered[column].max():%Y-%m-%d}")
scope_parts.append(f"Requested date window: {dates[0]} to {dates[1]} (inclusive)")
scope = "; ".join(scope_parts)

with st.expander("KPI definitions and calculation rules"):
    st.dataframe(pd.DataFrame(FORMULAS, columns=["Measure", "Calculation", "Business meaning"]), hide_index=True, width="stretch")
    st.caption("All cards, charts and findings use the same selected rows. Ratios use summed numerators and denominators where stated. A zero denominator makes the corresponding rate undefined; use the underlying counts before interpreting a displayed fallback zero.")

st.subheader("What the selected data answers")
for question, answer in insights[:3]:
    st.markdown(f"**{question}** {answer}")
st.caption(f"Analysis scope: {len(filtered):,} of {len(frame):,} source rows. " + scope)

report_parts = [
    "# " + '01 Retail Sales' + " - full analytical report",
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

overview, explore, data_tab, report_tab = st.tabs(["Sales dashboard", "Explore the data", "Data and quality", "Full report"])
with overview:
    monthly = filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)[["revenue","gross_profit"]].sum()
    st.plotly_chart(px.line(monthly, x="month", y=["revenue","gross_profit"], markers=True, title="Monthly sales and gross profit", labels={"value":"INR","month":"Month"}), use_container_width=True)
    explain_visual(0, st)
    by_region = filtered.groupby(["region","category"], as_index=False)["revenue"].sum()
    st.plotly_chart(px.bar(by_region, x="region", y="revenue", color="category", title="Where do sales come from?", labels={"revenue":"Net sales (INR)"}), use_container_width=True)
    explain_visual(1, st)
    st.dataframe(filtered.groupby("category").agg(orders=("revenue","size"), units=("units","sum"), sales=("revenue","sum"), gross_profit=("gross_profit","sum")).round(2), width="stretch")
    st.caption("The table above gives exact grouped values behind the dashboard. Group sizes matter: compare counts alongside totals or rates, and use the data tab to inspect individual observations.")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["revenue"], bins=20, color="#2563eb", edgecolor="white")
    ax.set(title="Order value distribution", xlabel="Net sales per order (INR)", ylabel="Orders")
    left.pyplot(fig); plt.close(fig)
    explain_visual(2, left)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="category", y="gross_profit", ax=ax, color="#a7f3d0")
    ax.set(title="Profit spread by category", xlabel="Category", ylabel="Gross profit (INR)")
    right.pyplot(fig); plt.close(fig)
    explain_visual(3, right)
    fig, ax = plt.subplots(figsize=(8,4))
    sns.heatmap(filtered[["units","discount_pct","revenue","gross_profit"]].corr(), annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Correlation: which measures move together?")
    st.pyplot(fig); plt.close(fig)
    explain_visual(4, st)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Source field dictionary")
    st.dataframe(pd.DataFrame(FIELD_GUIDE.items(), columns=["Field", "Meaning and units"]), hide_index=True, width="stretch")
    st.subheader("Filtered records")
    st.write("These are the exact selected observations used for the KPIs and charts, including any derived columns. Sorting this table does not change the analytical filters. Compare a few rows with the formulas before relying on an aggregate.")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_retail_sales.csv", "text/csv")
    st.subheader("Numeric summary")
    st.write("Count is the number of available values; mean is the arithmetic average; std measures spread; min/max are extremes; 25%, 50% and 75% are quartiles. The 50% value is the median. Identifier-like numeric columns and derived measures require business context before interpretation.")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Compare North and South with the same date range.\n2. Add a channel filter.\n3. Find categories with high revenue but low margin.\n4. Explain why correlation between sales and profit is partly built into the formulas.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")

with report_tab:
    st.download_button("Download full report (Markdown)", full_report, "01_retail_sales_report.md", "text/markdown")
    st.markdown(full_report)
