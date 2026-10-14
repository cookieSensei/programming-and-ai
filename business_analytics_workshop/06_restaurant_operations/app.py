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

# This case study explains both the business question and how to read the evidence.
CASE = ('A fictional restaurant manager wants to improve service without losing sales. Branch totals alone '
 'cannot reveal whether large bills, slow service or meal-period differences are shaping the customer '
 'experience.')
DECISION = ('Identify branch and meal-period combinations for service investigation, using sales, waiting time, '
 'ratings and food-cost contribution together.')
DATA_CONTEXT = ('One row is one order. The dataset contains 600 fictional orders over January to April 2025 across '
 'three branches, three meal periods and three channels. Guests are counted within each order; '
 'staffing, menu mix and customer history are unavailable.')
FORMULAS = [('Sales', 'Sum of bill amount', 'Selected billed sales in INR.'),
 ('Average bill',
  'Total bill amount / selected orders',
  'An order-weighted mean, not spending per guest.'),
 ('Average wait',
  'Sum of waiting minutes / selected orders',
  'An order-weighted mean. The median and 90th percentile show additional service detail.'),
 ('Average rating',
  'Sum of ratings / selected orders',
  'Mean recorded score on the 1-5 scale, not a percentage satisfaction rate.'),
 ('Food-cost contribution',
  'Sales - food cost',
  'Excludes staffing, rent, delivery fees and tax; not net profit.'),
 ('Sales per guest',
  'Total sales / total guests',
  'Weighted across all guests, not the average of order-level ratios.')]
VISUAL_GUIDE = [('Daily sales by branch',
  'Compare branch sales patterns across the selected dates.',
  'The x-axis is date, y-axis is sales in INR, and color is branch. Each point sums the branch orders '
  'observed on that date.',
  'Which branches and dates account for the selected sales?',
  'Absent branch-date observations are not automatically zero sales. The chart connects observed '
  'points; this teaching data is not an audited complete trading calendar.'),
 ('Wait time and rating',
  'Explore the association between service time and customer scores.',
  'Each point is an order. X is wait in minutes, y is a 1-5 rating, color is sales channel, and bubble '
  'size reflects guests. Hover shows the order, branch and bill.',
  'Do longer waits tend to coincide with lower ratings in these selected orders?',
  'Many points overlap on the discrete rating scale. Association does not prove that waiting caused a '
  'rating; food, expectations and channel can also matter.'),
 ('Order value distribution',
  'Show the spread of customer bills.',
  'The histogram counts orders in 20 INR bill ranges. Its shape reveals concentration and a possible '
  'high-bill tail.',
  'Does the average bill describe a typical order?',
  'A larger bill can simply represent more guests. Compare sales per guest before interpreting customer '
  'spending behavior.'),
 ('Service time by meal period',
  'Compare typical waits and variation across service periods.',
  'The middle line is median wait, boxes contain the middle 50%, and whiskers extend within 1.5 '
  'interquartile ranges. The y-axis is minutes.',
  'Which meal periods have longer or less consistent service?',
  'Different branches, channels and party sizes are mixed. This chart does not show staffing levels or '
  'identify the operational cause.'),
 ('Branch and meal-period rating heatmap',
  'Locate differences hidden by an overall mean rating.',
  'Rows are branches, columns are meal periods, and cells are mean ratings. The color scale stays at '
  '1-5. Missing combinations are blank.',
  'Which branch/meal-period combinations deserve a closer look at the customer experience?',
  'Means can hide variation and small samples. Check the sample-size table in the report and '
  'investigate comments before ranking teams.')]
RECOMMENDATIONS = ['Investigate the slowest branch alongside meal period, sales channel and order size before changing '
 'staff schedules.',
 'Review the slowest 10% of orders with operational logs and customer comments to identify bottlenecks.',
 'Pilot a specific service change with a comparison group, tracking both wait and ratings as well as '
 'cost and sales.']
LIMITATIONS = ('No staffing, capacity, food preparation time, opening-hours or customer-comment data is included. '
 'Observations are fictional and not a complete trading ledger. Correlation does not show that reducing '
 'wait will cause a particular rating change; contribution is not net profit.')

with st.expander("Business problem and context", expanded=True):
    st.markdown("**The problem:** " + CASE)
    st.markdown("**Decision this dashboard supports:** " + DECISION)
    st.markdown("**What one row means:** " + DATA_CONTEXT)
    st.info("This is a fictional teaching case. Every finding below is calculated from the selected CSV rows, not a claim about a real business.")
    st.write("Start with the KPI cards, read the explanation under each visual, inspect the source data, then open Full report for the complete analysis and a downloadable copy. Filters recalculate the findings and report.")


FIELD_GUIDE = {'order_id': 'Synthetic order identifier; one row per order.',
 'date': 'Order date.',
 'branch': 'Restaurant branch.',
 'meal_period': 'Meal period during which the order was placed.',
 'channel': 'Order channel.',
 'guests': 'Number of guests associated with the order.',
 'bill_amount': 'Sales amount for the order in INR.',
 'food_cost': 'Food cost for the order in INR; excludes staffing and overhead.',
 'wait_minutes': 'Recorded service wait in minutes.',
 'rating': 'Customer rating from 1 to 5; higher means a better rating.'}

def explain_visual(index, container=st):
    title, purpose, reading, question, caution = VISUAL_GUIDE[index]
    container.markdown(f"**{title}: what this visual explains**")
    container.write(purpose)
    container.markdown("**How to read it:** " + reading)
    container.markdown("**Question it answers:** " + question)
    container.caption("Interpretation limit: " + caution)

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
branch_summary = filtered.groupby("branch").agg(orders=("order_id","size"),sales=("bill_amount","sum"),wait=("wait_minutes","mean"),rating=("rating","mean"))
sales_leader = branch_summary["sales"].idxmax()
slowest = branch_summary["wait"].idxmax()
association = filtered["wait_minutes"].corr(filtered["rating"]) if len(filtered)>1 else float("nan")
association_text = f"Pearson correlation is {association:.2f}. This describes a linear association, not a causal effect." if pd.notna(association) else "Correlation cannot be estimated because there is insufficient variation or too few observations."
cell_counts = filtered.groupby(["branch","meal_period"]).size()
insights = [
 ("What business is represented?", f"{len(filtered):,} orders for {filtered['guests'].sum():,} guests generated INR {sales:,.2f} of sales. Food-cost contribution is INR {filtered['contribution'].sum():,.2f}, before other operating costs."),
 ("Which branch leads sales?", f"{sales_leader} records INR {branch_summary.loc[sales_leader,'sales']:,.2f} across {branch_summary.loc[sales_leader,'orders']:,.0f} orders. This total does not adjust for branch capacity or opening hours."),
 ("Where is average service slowest?", f"{slowest} has the longest selected mean wait at {branch_summary.loc[slowest,'wait']:.1f} minutes across {branch_summary.loc[slowest,'orders']:,.0f} orders. Use channel and meal-period context before changing staffing."),
 ("What does the service tail look like?", f"Median wait is {filtered['wait_minutes'].median():.1f} minutes; the 90th percentile is {filtered['wait_minutes'].quantile(.9):.1f} minutes. The latter describes the slow end of the selected service experience."),
 ("Are wait time and rating related?", association_text),
 ("How much is spent per guest?", f"Sales per guest are INR {ratio(sales,filtered['guests'].sum()):,.2f}, compared with INR {filtered['bill_amount'].mean():,.2f} per order. The denominators answer different questions."),
 ("How much evidence supports subgroup ratings?", f"The smallest observed branch/meal-period cell has {int(cell_counts.min())} orders. {int((cell_counts<20).sum())} cells have fewer than 20 orders; this illustrative caution threshold does not establish statistical reliability."),
]
kpi_values=[("Sales (INR)",f"{sales:,.2f}"),("Average bill (INR)",f"{filtered['bill_amount'].mean():,.2f}"),("Average wait (minutes)",f"{filtered['wait_minutes'].mean():.2f}"),("Average rating",f"{filtered['rating'].mean():.2f}/5"),("Sales per guest (INR)",f"{ratio(sales,filtered['guests'].sum()):,.2f}")]

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
    "# " + '06 Restaurant Operations' + " - full analytical report",
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

overview, explore, data_tab, report_tab = st.tabs(["Operations dashboard", "Explore the data", "Data and quality", "Full report"])
with overview:
    daily = filtered.groupby(["date","branch"], as_index=False)["bill_amount"].sum()
    st.plotly_chart(px.line(daily, x="date", y="bill_amount", color="branch", title="Daily sales by branch", labels={"bill_amount":"Sales (INR)"}), use_container_width=True)
    explain_visual(0, st)
    st.plotly_chart(px.scatter(filtered, x="wait_minutes", y="rating", color="channel", size="guests", hover_data=["order_id","branch","bill_amount"], opacity=.6, title="Wait time and rating"), use_container_width=True)
    explain_visual(1, st)
    st.dataframe(filtered.groupby("branch").agg(orders=("order_id","size"), sales=("bill_amount","sum"), contribution=("contribution","sum"), average_wait=("wait_minutes","mean"), rating=("rating","mean")).round(2), width="stretch")
    st.caption("The table above gives exact grouped values behind the dashboard. Group sizes matter: compare counts alongside totals or rates, and use the data tab to inspect individual observations.")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["bill_amount"], bins=20, color="#e11d48", edgecolor="white")
    ax.set(title="Order value distribution", xlabel="Bill amount (INR)", ylabel="Orders")
    left.pyplot(fig); plt.close(fig)
    explain_visual(2, left)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="meal_period", y="wait_minutes", ax=ax, color="#fecdd3")
    ax.set_title("Service time by meal period")
    right.pyplot(fig); plt.close(fig)
    explain_visual(3, right)
    fig, ax = plt.subplots(figsize=(9,4))
    sns.heatmap(filtered.pivot_table(index="branch", columns="meal_period", values="rating", aggfunc="mean"), annot=True, fmt=".2f", vmin=1, vmax=5, cmap="YlGnBu", ax=ax)
    ax.set_title("Average rating by branch and meal period")
    st.pyplot(fig); plt.close(fig)
    explain_visual(4, st)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Source field dictionary")
    st.dataframe(pd.DataFrame(FIELD_GUIDE.items(), columns=["Field", "Meaning and units"]), hide_index=True, width="stretch")
    st.subheader("Filtered records")
    st.write("These are the exact selected observations used for the KPIs and charts, including any derived columns. Sorting this table does not change the analytical filters. Compare a few rows with the formulas before relying on an aggregate.")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_restaurant_orders.csv", "text/csv")
    st.subheader("Numeric summary")
    st.write("Count is the number of available values; mean is the arithmetic average; std measures spread; min/max are extremes; 25%, 50% and 75% are quartiles. The 50% value is the median. Identifier-like numeric columns and derived measures require business context before interpretation.")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Find the branch with the longest average wait.\n2. Add a channel filter and compare delivery with dine in.\n3. Calculate sales per guest using totals.\n4. Compare group sizes before recommending a staffing change.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")

with report_tab:
    st.download_button("Download full report (Markdown)", full_report, "06_restaurant_operations_report.md", "text/markdown")
    st.markdown(full_report)
    st.subheader("Branch and meal-period sample sizes")
    st.dataframe(cell_counts.rename("orders").reset_index(), hide_index=True, width="stretch")
