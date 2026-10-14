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

# This case study explains both the business question and how to read the evidence.
CASE = ('A fictional finance manager needs to know where expenses exceed the plan. An overall total can hide '
 'departments or expense categories that are overspending while others remain under budget.')
DECISION = ('Identify budget lines requiring explanation, distinguish spend concentration from overspend, and '
 'prepare questions for department owners.')
DATA_CONTEXT = ('One row is one month, department and expense category. There are 192 fictional expense lines for the '
 '12 months of 2025, four departments and four categories. These are budget-versus-actual expense '
 'records, not a balance sheet or cash-flow statement.')
FORMULAS = [('Budget', 'Sum of selected budget amounts', 'Planned expense in INR for the selected lines.'),
 ('Actual spend',
  'Sum of selected actual expenses',
  'Recorded expense in INR, not necessarily cash paid.'),
 ('Unspent budget / variance',
  'Total budget - total actual spend',
  'Positive means under budget; negative means overspend.'),
 ('Budget utilization',
  'Total actual spend / total budget x 100',
  'Over 100% means aggregate overspend. This is weighted by budget, not an average of monthly ratios.')]
VISUAL_GUIDE = [('Monthly expense plan and actuals',
  'Compare actual expenses with the plan over time.',
  'The x-axis is month and the y-axis is INR. Each line sums selected departments and categories in '
  'that month. An actual line above budget indicates aggregate monthly overspend.',
  'In which months does the selected activity exceed its plan?',
  'The lines are monthly totals, not cumulative totals. A date selection can exclude month-start '
  'records, since each budget line is dated on the first of its month.'),
 ('Department variance',
  'Locate aggregate over- and underspending by department.',
  'Bar height is budget minus actual in INR. Positive bars are under budget; negative bars are '
  'overspent. The color scale is centered on zero.',
  'Which department needs the largest expense-variance explanation?',
  'A large department can have a large INR variance with a modest percentage variance. Check '
  'utilization and underlying budget size too.'),
 ('Variance distribution',
  'See the balance of under- and overspent individual budget lines.',
  'Each histogram bin counts budget lines in an INR variance range. The dashed vertical line marks '
  'zero. Left of zero is overspend; right of zero is unspent budget.',
  'Is overspend widespread or driven by a few large lines?',
  'Budget lines have different sizes. Negative variance does not by itself establish waste or poor '
  'management.'),
 ('Expense distribution by category',
  'Compare typical expense size and variability by type.',
  'Boxes show actual INR expenses. The line is the median, the box the middle 50%, and whiskers use 1.5 '
  'interquartile ranges. Each observation is a month/department/category line.',
  'Which categories have larger or more variable recorded expense?',
  'This compares spend levels, not budget adherence. Use variance alongside it.'),
 ('Department and category variance heatmap',
  'Find combinations hidden by aggregate department totals.',
  'Each cell sums budget minus actual across selected months for one department/category. The scale is '
  'centered on zero: negative values mean overspend, positive values mean unspent budget.',
  'Which department/category combinations explain the overall variance?',
  'Positive and negative lines can offset inside a cell. Inspect individual months before deciding '
  'whether the variance is recurring.')]
RECOMMENDATIONS = ['Ask owners of the largest negative-variance lines to explain timing, volume and one-off events. Do '
 'not equate overspend with waste without context.',
 'Compare both INR variance and utilization percentage so that department size does not dominate the '
 'discussion.',
 'Add commitments, accrual policy, business output and approved forecast revisions before changing '
 'budgets.']
LIMITATIONS = ('Expense classification and budget baselines are assumed consistent. The data does not include income, '
 'cash timing, commitments, forecast revisions or output delivered. Unspent budget is neither profit '
 'nor available cash.')

with st.expander("Business problem and context", expanded=True):
    st.markdown("**The problem:** " + CASE)
    st.markdown("**Decision this dashboard supports:** " + DECISION)
    st.markdown("**What one row means:** " + DATA_CONTEXT)
    st.info("This is a fictional teaching case. Every finding below is calculated from the selected CSV rows, not a claim about a real business.")
    st.write("Start with the KPI cards, read the explanation under each visual, inspect the source data, then open Full report for the complete analysis and a downloadable copy. Filters recalculate the findings and report.")


FIELD_GUIDE = {'month': 'Budget month recorded on its first day; date filters select whole recorded budget '
          'lines.',
 'department': 'Department responsible for expense.',
 'expense_category': 'Expense classification.',
 'budget': 'Planned expense in INR for this month, department and category.',
 'actual': 'Recorded expense in INR for this budget line.'}

def explain_visual(index, container=st):
    title, purpose, reading, question, caution = VISUAL_GUIDE[index]
    container.markdown(f"**{title}: what this visual explains**")
    container.write(purpose)
    container.markdown("**How to read it:** " + reading)
    container.markdown("**Question it answers:** " + question)
    container.caption("Interpretation limit: " + caution)

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
dept_summary = filtered.groupby("department")[["budget","actual","variance"]].sum()
worst_dept = dept_summary["variance"].idxmin()
monthly_summary = filtered.groupby("month")[["budget","actual","variance"]].sum()
overspent_lines = int((filtered["variance"]<0).sum())
largest_line = filtered.loc[filtered["variance"].idxmin()]
net_label = "overspend" if actual>budget else "unspent budget"
insights = [
 ("Is the selected activity within budget?", f"Budget is INR {budget:,.2f} and actual expense is INR {actual:,.2f}. The difference is INR {abs(budget-actual):,.2f} of {net_label}; utilization is {ratio(actual,budget):.2%}."),
 ("How widespread is overspending?", f"{overspent_lines} of {len(filtered)} selected budget lines are overspent ({ratio(overspent_lines,len(filtered)):.1%}). This is a line count, not the share of total expense."),
 ("Which department has the lowest variance?", f"{worst_dept} has variance INR {dept_summary.loc[worst_dept,'variance']:,.2f} and utilization {ratio(dept_summary.loc[worst_dept,'actual'],dept_summary.loc[worst_dept,'budget']):.1%}. A negative variance means overspend; a positive one still means under budget."),
 ("What is the largest individual overspend?", f"{largest_line['department']} / {largest_line['expense_category']} in {largest_line['month']:%Y-%m}: INR {-largest_line['variance']:,.2f} above budget." if largest_line['variance']<0 else "No selected individual budget line is overspent."),
 ("How many selected months are over plan?", f"{int((monthly_summary['variance']<0).sum())} of {len(monthly_summary)} observed months have total actual expense above budget."),
 ("What has the dashboard answered?", "It quantifies the expense gap and locates the departments, categories and months behind it. It cannot determine whether those expenses were justified or what cash is available."),
]
kpi_values=[("Budget (INR)",f"{budget:,.2f}"),("Actual expense (INR)",f"{actual:,.2f}"),("Budget minus actual (INR)",f"{budget-actual:,.2f}"),("Utilization",f"{ratio(actual,budget):.2%}")]

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
    "# " + '05 Finance Budget' + " - full analytical report",
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

overview, explore, data_tab, report_tab = st.tabs(["Finance dashboard", "Explore the data", "Data and quality", "Full report"])
with overview:
    monthly = filtered.groupby("month", as_index=False)[["budget","actual"]].sum()
    st.plotly_chart(px.line(monthly, x="month", y=["budget","actual"], markers=True, title="Monthly expense plan and actuals", labels={"value":"INR"}), use_container_width=True)
    explain_visual(0, st)
    departments = filtered.groupby("department", as_index=False)[["budget","actual","variance"]].sum()
    departments["utilization_pct"] = 100*departments["actual"].div(departments["budget"].replace(0,float("nan")))
    st.plotly_chart(px.bar(departments, x="department", y="variance", color="variance", color_continuous_scale="RdYlGn", color_continuous_midpoint=0, title="Positive variance is under budget", labels={"variance":"Budget minus actual (INR)"}), use_container_width=True)
    explain_visual(1, st)
    st.dataframe(departments.round(2), hide_index=True, width="stretch")
    st.caption("The table above gives exact grouped values behind the dashboard. Group sizes matter: compare counts alongside totals or rates, and use the data tab to inspect individual observations.")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["variance"], bins=20, color="#ea580c", edgecolor="white")
    ax.axvline(0, color="black", linestyle="--")
    ax.set(title="Variance distribution", xlabel="Budget minus actual (INR)", ylabel="Budget lines")
    left.pyplot(fig); plt.close(fig)
    explain_visual(2, left)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="expense_category", y="actual", ax=ax, color="#fed7aa")
    ax.set_title("Expense distribution by category")
    right.pyplot(fig); plt.close(fig)
    explain_visual(3, right)
    fig, ax = plt.subplots(figsize=(9,4))
    sns.heatmap(filtered.pivot_table(index="department", columns="expense_category", values="variance", aggfunc="sum"), annot=True, fmt=".0f", cmap="RdYlGn", center=0, ax=ax)
    ax.set_title("Variance by department and expense category (INR)")
    st.pyplot(fig); plt.close(fig)
    explain_visual(4, st)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Source field dictionary")
    st.dataframe(pd.DataFrame(FIELD_GUIDE.items(), columns=["Field", "Meaning and units"]), hide_index=True, width="stretch")
    st.subheader("Filtered records")
    st.write("These are the exact selected observations used for the KPIs and charts, including any derived columns. Sorting this table does not change the analytical filters. Compare a few rows with the formulas before relying on an aggregate.")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_department_budget.csv", "text/csv")
    st.subheader("Numeric summary")
    st.write("Count is the number of available values; mean is the arithmetic average; std measures spread; min/max are extremes; 25%, 50% and 75% are quartiles. The 50% value is the median. Identifier-like numeric columns and derived measures require business context before interpretation.")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Identify the largest overspend and inspect its source records.\n2. Compare the first and second halves of the year.\n3. Add a cumulative spend line.\n4. Explain why averaging monthly utilization percentages can mislead.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")

with report_tab:
    st.download_button("Download full report (Markdown)", full_report, "05_finance_budget_report.md", "text/markdown")
    st.markdown(full_report)
