"""Budget versus Actuals: a beginner Streamlit project using a fictional teaching dataset."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Budget versus Actuals", page_icon=":bar_chart:", layout="wide")
st.title("Budget versus Actuals")
st.caption("Business Analytics Workshop | Fictional teaching data | Currency: INR")
st.write("Track expense budgets, find overspending and compare departments. Practice financial aggregation and variance analysis.")

# 1. Load the CSV beside this script, regardless of the terminal's directory.
# Keeping this uncached lets students edit the CSV and immediately rerun the app.
DATA_FILE = Path(__file__).resolve().with_name("department_budget.csv")
try:
    frame = pd.read_csv(DATA_FILE)
    frame["month"] = pd.to_datetime(frame["month"], errors="raise")
    numeric_columns = ['budget', 'actual']
    required_columns = ['month', 'department', 'expense_category', 'budget', 'actual']
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
selected_department = st.sidebar.multiselect("Departments", sorted(frame["department"].unique()), default=sorted(frame["department"].unique()), key="05_finance_budget_department")
filtered = filtered[filtered["department"].isin(selected_department)]
selected_expense_category = st.sidebar.multiselect("Expense categories", sorted(frame["expense_category"].unique()), default=sorted(frame["expense_category"].unique()), key="05_finance_budget_expense_category")
filtered = filtered[filtered["expense_category"].isin(selected_expense_category)]
dates = st.sidebar.date_input("Date range", (frame["month"].min().date(), frame["month"].max().date()), min_value=frame["month"].min().date(), max_value=frame["month"].max().date(), key="05_finance_budget_dates")
if len(dates) != 2:
    st.info("Choose both a start and an end date.")
    st.stop()
filtered = filtered[filtered["month"].dt.date.between(dates[0], dates[1])]
st.sidebar.caption(f"Showing {len(filtered):,} of {len(frame):,} rows")
if filtered.empty:
    st.info("No rows match these filters. Select at least one value or widen the date range.")
    st.stop()

# 3. Derive business measures, then compare totals, distributions and segments.
filtered["variance"] = filtered["budget"]-filtered["actual"]
budget = filtered["budget"].sum()
actual = filtered["actual"].sum()
columns = st.columns(4)
columns[0].metric("Budget (INR)", f"{budget:,.0f}")
columns[1].metric("Actual spend (INR)", f"{actual:,.0f}")
columns[2].metric("Unspent budget (INR)", f"{budget-actual:,.0f}")
columns[3].metric("Budget utilization", f"{ratio(actual,budget):.1%}")
st.caption("One row is a department/expense category for one month. Variance = budget - actual: a negative number means overspend. Unspent budget is not profit or cash flow.")
overview, explore, data_tab = st.tabs(["Finance dashboard", "Explore the data", "Data and quality"])
with overview:
    monthly = filtered.groupby("month", as_index=False)[["budget","actual"]].sum()
    st.plotly_chart(px.line(monthly, x="month", y=["budget","actual"], markers=True, title="Monthly expense plan and actuals", labels={"value":"INR"}), use_container_width=True)
    departments = filtered.groupby("department", as_index=False)[["budget","actual","variance"]].sum()
    departments["utilization_pct"] = 100*departments["actual"].div(departments["budget"].replace(0,float("nan")))
    st.plotly_chart(px.bar(departments, x="department", y="variance", color="variance", color_continuous_scale="RdYlGn", color_continuous_midpoint=0, title="Positive variance is under budget", labels={"variance":"Budget minus actual (INR)"}), use_container_width=True)
    st.dataframe(departments.round(2), hide_index=True, width="stretch")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["variance"], bins=20, color="#ea580c", edgecolor="white")
    ax.axvline(0, color="black", linestyle="--")
    ax.set(title="Variance distribution", xlabel="Budget minus actual (INR)", ylabel="Budget lines")
    left.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="expense_category", y="actual", ax=ax, color="#fed7aa")
    ax.set_title("Expense distribution by category")
    right.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9,4))
    sns.heatmap(filtered.pivot_table(index="department", columns="expense_category", values="variance", aggfunc="sum"), annot=True, fmt=".0f", cmap="RdYlGn", center=0, ax=ax)
    ax.set_title("Variance by department and expense category (INR)")
    st.pyplot(fig); plt.close(fig)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Filtered records")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_department_budget.csv", "text/csv")
    st.subheader("Numeric summary")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Identify the largest overspend and inspect its source records.\n2. Compare the first and second halves of the year.\n3. Add a cumulative spend line.\n4. Explain why averaging monthly utilization percentages can mislead.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")
