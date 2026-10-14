"""Customer Churn Explorer: a beginner Streamlit project using a fictional teaching dataset."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Customer Churn Explorer", page_icon=":bar_chart:", layout="wide")
st.title("Customer Churn Explorer")
st.caption("Business Analytics Workshop | Fictional teaching data | Currency: INR")
st.write("Explore a customer snapshot and compare churn across contracts, tenure and satisfaction. This is descriptive analysis, not a prediction model.")

# This case study explains both the business question and how to read the evidence.
CASE = ('A fictional subscription team wants to understand which customer groups show more churn. Overall '
 'churn hides differences in contract type, tenure, support experience and satisfaction.')
DECISION = ('Prioritize customer research and retention experiments in clearly defined segments, while checking '
 'sample sizes and avoiding unsupported claims about what causes churn.')
DATA_CONTEXT = ('One row is one synthetic customer in a single snapshot of 480 customers. churned is 1 for churned and '
 '0 for retained. There is no churn date or observation window, so this is not a monthly churn-rate '
 'dataset.')
FORMULAS = [('Customers', 'Count of selected rows', 'Each customer ID represents one fictional customer.'),
 ('Snapshot churn rate',
  'Sum of churned / number of customers x 100',
  'Share marked churned in this snapshot; not a monthly or annual rate.'),
 ('Average satisfaction',
  'Sum of satisfaction scores / customers',
  'A mean score on a 1-10 scale; compare group sizes and distributions.'),
 ('Churned monthly fees',
  'Sum of monthly fee where churned = 1',
  "A descriptive total of those customers' listed fees, not measured revenue loss or a forecast.")]
VISUAL_GUIDE = [('Churn by contract',
  'Compare the share churned in each contract group.',
  'The x-axis is contract type and the y-axis is percentage churned. Hover shows the number of '
  'customers used in each percentage.',
  'Which contract group has the highest observed churn proportion?',
  'Groups differ in size and characteristics. A contract association is not evidence that changing a '
  'contract prevents churn.'),
 ('Tenure and monthly fee',
  'Locate customer segments in tenure and price space.',
  'Each point is a customer. The x-axis is tenure in months, y is monthly fee in INR, and color '
  'distinguishes retained from churned. Hover identifies the synthetic customer and contract.',
  'Do churned and retained customers occupy visibly different parts of tenure and fee space?',
  'Points overlap, so visual density is approximate. This is descriptive, not a classifier or a '
  'forecast.'),
 ('Tenure distribution by churn status',
  'Compare how long customers in each status have been subscribed.',
  'Both colored histograms use the same 12 bins from 0 to 60 months. Heights are customer counts, not '
  'normalized percentages.',
  'Are many churned customers early or late in their subscription history?',
  'The larger retained group can have taller bars simply because it has more members. Compare medians '
  'and group sizes too.'),
 ('Satisfaction and churn',
  'Compare the center and spread of satisfaction between groups.',
  'Each box is a churn status. Its line is the median satisfaction, box the middle 50%, and whiskers '
  'extend within 1.5 interquartile ranges. The original scale is 1-10.',
  'Do churned customers report different satisfaction in this snapshot?',
  'Timing is unknown. Low satisfaction could precede or follow churn, and other variables may influence '
  'both.'),
 ('Contract and region churn heatmap',
  'Look beyond overall averages to combined segments.',
  'Rows are contracts, columns are regions, and each cell is the percentage marked churned. A fixed '
  '0-100 scale makes colors comparable. Blank cells have no observations.',
  'Which contract-region combinations warrant investigation?',
  'Small cells are unstable. Check the segment sample-size table in the report before comparing '
  'percentages; no significance test is performed.')]
RECOMMENDATIONS = ['Investigate the highest-churn contract group with interviews and support-history review before '
 'changing policy.',
 'Report customer counts with every subgroup percentage. Pool or investigate very small groups rather '
 'than confidently ranking them.',
 'Collect observation dates, cancellation dates and pre-churn measurements; use a controlled retention '
 'experiment to evaluate a proposed intervention.']
LIMITATIONS = ('This single snapshot cannot estimate time-to-churn, monthly churn, customer lifetime value, causal '
 'drivers or individual future risk. No statistical significance test or predictive model is included. '
 'A 20-customer caution threshold is illustrative only.')

with st.expander("Business problem and context", expanded=True):
    st.markdown("**The problem:** " + CASE)
    st.markdown("**Decision this dashboard supports:** " + DECISION)
    st.markdown("**What one row means:** " + DATA_CONTEXT)
    st.info("This is a fictional teaching case. Every finding below is calculated from the selected CSV rows, not a claim about a real business.")
    st.write("Start with the KPI cards, read the explanation under each visual, inspect the source data, then open Full report for the complete analysis and a downloadable copy. Filters recalculate the findings and report.")


FIELD_GUIDE = {'customer_id': 'Synthetic customer identifier in a single snapshot.',
 'region': 'Customer region.',
 'contract': 'Contract category.',
 'tenure_months': 'Recorded customer tenure in months.',
 'monthly_fee': 'Monthly charge in INR; not lifetime revenue.',
 'support_tickets': 'Recorded support ticket count; no common time window is supplied.',
 'satisfaction_score': 'Satisfaction on a 1 to 10 scale; higher means more satisfied.',
 'churned': '1 identifies a churned customer, 0 a retained customer. No monthly observation window '
            'is provided.'}

def explain_visual(index, container=st):
    title, purpose, reading, question, caution = VISUAL_GUIDE[index]
    container.markdown(f"**{title}: what this visual explains**")
    container.write(purpose)
    container.markdown("**How to read it:** " + reading)
    container.markdown("**Question it answers:** " + question)
    container.caption("Interpretation limit: " + caution)

# 1. Load the CSV beside this script, regardless of the terminal's directory.
# Keeping this uncached lets students edit the CSV and immediately rerun the app.
DATA_FILE = Path(__file__).resolve().with_name("customer_churn.csv")
try:
    frame = pd.read_csv(DATA_FILE)
    # This dataset is a single snapshot, so it has no date filter.
    numeric_columns = ['tenure_months', 'monthly_fee', 'support_tickets', 'satisfaction_score', 'churned']
    required_columns = ['customer_id', 'region', 'contract', 'tenure_months', 'monthly_fee', 'support_tickets', 'satisfaction_score', 'churned']
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
selected_region = st.sidebar.multiselect("Regions", sorted(frame["region"].unique()), default=sorted(frame["region"].unique()), key="03_customer_churn_region")
filtered = filtered[filtered["region"].isin(selected_region)]
selected_contract = st.sidebar.multiselect("Contracts", sorted(frame["contract"].unique()), default=sorted(frame["contract"].unique()), key="03_customer_churn_contract")
filtered = filtered[filtered["contract"].isin(selected_contract)]
st.sidebar.caption(f"Showing {len(filtered):,} of {len(frame):,} rows")
if filtered.empty:
    st.info("No rows match these filters. Select at least one value or widen the date range.")
    st.stop()

# 3. Derive business measures, then compare totals, distributions and segments.
filtered["status"] = filtered["churned"].map({0:"Retained",1:"Churned"})
churned = filtered["churned"].sum()
columns = st.columns(4)
columns[0].metric("Customers", f"{len(filtered):,}")
columns[1].metric("Snapshot churn rate", f"{filtered['churned'].mean():.1%}")
columns[2].metric("Average satisfaction", f"{filtered['satisfaction_score'].mean():.1f} / 10")
columns[3].metric("Churned monthly fees (INR)", f"{filtered.loc[filtered['churned']==1,'monthly_fee'].sum():,.0f}")
st.caption("One row is one customer in a fictional snapshot. Churned fees are a descriptive total, not a forecast or accounting revenue. No time-based churn rate can be inferred.")
contract_summary = filtered.groupby("contract").agg(customers=("churned","size"),churn_rate=("churned","mean"))
highest_contract = contract_summary["churn_rate"].idxmax()
status_summary = filtered.groupby("status").agg(customers=("churned","size"),median_satisfaction=("satisfaction_score","median"),median_tenure=("tenure_months","median"))
status_details = "; ".join(f"{label}: {int(row['customers'])} customers, median satisfaction {row['median_satisfaction']:.1f}/10, median tenure {row['median_tenure']:.1f} months" for label,row in status_summary.iterrows())
segment_counts = filtered.groupby(["contract","region"]).size()
insights = [
 ("How much churn is observed?", f"{int(churned):,} of {len(filtered):,} selected customers are marked churned, a snapshot share of {filtered['churned'].mean():.2%}. No monthly rate is implied."),
 ("Which contract group has the highest share?", f"{highest_contract}: {contract_summary.loc[highest_contract,'churn_rate']:.1%} among {contract_summary.loc[highest_contract,'customers']:,.0f} customers. This identifies a segment for research, not a cause."),
 ("How do retained and churned groups compare?", status_details + ". If only one status is selected, no between-status comparison is possible."),
 ("What monthly fees are associated with churned customers?", f"Their listed fees total INR {filtered.loc[filtered['churned']==1,'monthly_fee'].sum():,.2f}. Without dates, billing history or cancellation timing, this is not recognized lost revenue."),
 ("How reliable are the combined segments?", f"There are {len(segment_counts)} observed contract-region cells. The smallest contains {int(segment_counts.min())} customers; {int((segment_counts<20).sum())} cells have fewer than 20. Twenty is a teaching caution threshold, not a statistical guarantee."),
 ("What has the dashboard answered?", "It describes where churn is concentrated and how tenure and satisfaction differ. It has not predicted individual churn or established a retention treatment effect."),
]
kpi_values=[("Customers",str(len(filtered))),("Churned customers",str(int(churned))),("Snapshot churn rate",f"{filtered['churned'].mean():.2%}"),("Average satisfaction",f"{filtered['satisfaction_score'].mean():.2f}/10")]

# Build one report from the same filtered dataframe used by the charts.
scope_parts = []
for column in frame.select_dtypes(include="object").columns:
    if frame[column].nunique() <= 12:
        scope_parts.append(column.replace("_", " ") + ": " + ", ".join(map(str, sorted(filtered[column].unique()))))
for column in frame.select_dtypes(include="datetime").columns:
    scope_parts.append(f"{column}: observed records {filtered[column].min():%Y-%m-%d} to {filtered[column].max():%Y-%m-%d}")
scope = "; ".join(scope_parts)

with st.expander("KPI definitions and calculation rules"):
    st.dataframe(pd.DataFrame(FORMULAS, columns=["Measure", "Calculation", "Business meaning"]), hide_index=True, width="stretch")
    st.caption("All cards, charts and findings use the same selected rows. Ratios use summed numerators and denominators where stated. A zero denominator makes the corresponding rate undefined; use the underlying counts before interpreting a displayed fallback zero.")

st.subheader("What the selected data answers")
for question, answer in insights[:3]:
    st.markdown(f"**{question}** {answer}")
st.caption(f"Analysis scope: {len(filtered):,} of {len(frame):,} source rows. " + scope)

report_parts = [
    "# " + '03 Customer Churn' + " - full analytical report",
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

overview, explore, data_tab, report_tab = st.tabs(["Retention dashboard", "Explore the data", "Data and quality", "Full report"])
with overview:
    contracts = filtered.groupby("contract", as_index=False).agg(customers=("churned","size"),churn_rate=("churned","mean"))
    contracts["churn_pct"] = 100*contracts["churn_rate"]
    st.plotly_chart(px.bar(contracts, x="contract", y="churn_pct", color="contract", hover_data=["customers"], title="Churn by contract", labels={"churn_pct":"Customers churned (%)"}), use_container_width=True)
    explain_visual(0, st)
    st.plotly_chart(px.scatter(filtered, x="tenure_months", y="monthly_fee", color="status", hover_data=["customer_id","contract","satisfaction_score"], opacity=.65, title="Tenure and monthly fee"), use_container_width=True)
    explain_visual(1, st)
    st.dataframe(contracts[["contract","customers","churn_pct"]].round(2), hide_index=True, width="stretch")
    st.caption("The table above gives exact grouped values behind the dashboard. Group sizes matter: compare counts alongside totals or rates, and use the data tab to inspect individual observations.")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    for status, group in filtered.groupby("status"):
        ax.hist(group["tenure_months"], bins=12, range=(0,60), alpha=.6, label=status)
    ax.set(title="Customer tenure distribution", xlabel="Tenure (months)", ylabel="Customers")
    ax.legend()
    left.pyplot(fig); plt.close(fig)
    explain_visual(2, left)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="status", y="satisfaction_score", ax=ax, color="#a5f3fc")
    ax.set_title("Satisfaction and churn")
    right.pyplot(fig); plt.close(fig)
    explain_visual(3, right)
    segments = filtered.pivot_table(index="contract", columns="region", values="churned", aggfunc="mean")*100
    fig, ax = plt.subplots(figsize=(9,4))
    sns.heatmap(segments, annot=True, fmt=".1f", cmap="YlOrRd", vmin=0, vmax=100, ax=ax)
    ax.set_title("Churn percentage by contract and region")
    st.pyplot(fig); plt.close(fig)
    explain_visual(4, st)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Source field dictionary")
    st.dataframe(pd.DataFrame(FIELD_GUIDE.items(), columns=["Field", "Meaning and units"]), hide_index=True, width="stretch")
    st.subheader("Filtered records")
    st.write("These are the exact selected observations used for the KPIs and charts, including any derived columns. Sorting this table does not change the analytical filters. Compare a few rows with the formulas before relying on an aggregate.")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_customer_churn.csv", "text/csv")
    st.subheader("Numeric summary")
    st.write("Count is the number of available values; mean is the arithmetic average; std measures spread; min/max are extremes; 25%, 50% and 75% are quartiles. The 50% value is the median. Identifier-like numeric columns and derived measures require business context before interpretation.")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Compare contract groups and report their sample sizes.\n2. Add a support-ticket filter.\n3. Compare the median satisfaction of retained and churned customers.\n4. Explain why this snapshot cannot prove that contract type causes churn.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")

with report_tab:
    st.download_button("Download full report (Markdown)", full_report, "03_customer_churn_report.md", "text/markdown")
    st.markdown(full_report)
    st.subheader("Contract and region sample sizes")
    st.dataframe(segment_counts.rename("customers").reset_index(), hide_index=True, width="stretch")
