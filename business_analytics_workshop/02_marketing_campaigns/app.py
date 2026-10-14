"""Marketing Campaign Lab: a beginner Streamlit project using a fictional teaching dataset."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Marketing Campaign Lab", page_icon=":bar_chart:", layout="wide")
st.title("Marketing Campaign Lab")
st.caption("Business Analytics Workshop | Fictional teaching data | Currency: INR")
st.write("Compare reach, conversions and acquisition cost. Learn why campaign rates must use totals instead of averages of row percentages.")

# This case study explains both the business question and how to read the evidence.
CASE = ('A fictional marketing team must allocate a limited advertising budget. A channel with many clicks may '
 'generate few purchases, while a high-return channel may operate at a very small scale.')
DECISION = ('Choose which channel and campaign combinations to investigate for controlled budget experiments, '
 'balancing return, acquisition cost and conversion volume.')
DATA_CONTEXT = ('One row is one channel/campaign observation for one day. There are 360 fictional observations across '
 '90 days in January to March 2025. Revenue is attributed to campaigns; the data does not identify '
 'individual customers or prove incremental sales.')
FORMULAS = [('Ad spend', 'Sum of selected spend', 'The total advertising cost in INR.'),
 ('ROAS',
  'Total attributed revenue / total ad spend',
  'INR of attributed sales for every INR spent; a ratio of 3 means INR 3 revenue per INR 1 spend, not '
  'INR 3 profit.'),
 ('Cost per acquisition',
  'Total spend / total conversions',
  'Advertising cost per attributed conversion. N/A when there are no conversions.'),
 ('Conversion rate',
  'Total conversions / total clicks x 100',
  'Weighted by clicks. Averaging daily percentages can mislead.'),
 ('Click-through rate',
  'Total clicks / total impressions x 100',
  'Engagement with the advertisement, not final business return.')]
VISUAL_GUIDE = [('Daily spend and attributed revenue',
  'Compare the timing and scale of advertising cost and attributed sales.',
  'The x-axis is date; the y-axis is INR. The two lines sum all selected observations for each date. '
  'Hover to compare their actual amounts.',
  'Were high-revenue dates also high-spend dates?',
  'This is not a profit chart. Revenue may lag advertising, and attribution rules can assign sales that '
  'would have happened without an ad.'),
 ('Return per rupee by channel',
  'Compare channel efficiency using weighted aggregate ROAS.',
  'Each bar is a channel. Its height is total attributed revenue divided by total spend. Hover also '
  'shows spend, conversions and click-through rate.',
  'Which selected channel reports the highest ROAS, and at what scale?',
  'A high ratio with little spend may not persist when scaled. Channel audiences differ; this is not an '
  'experiment.'),
 ('Observation spend distribution',
  'Understand budget concentration among daily observations.',
  'Each histogram bin counts observations with spend in an INR range. The x-axis is spend per '
  'observation and the y-axis is observation count.',
  'Is spend spread evenly or concentrated in a few large daily observations?',
  'These are channel/campaign-day records, not separate customers or complete daily company budgets.'),
 ('Conversion distribution by channel',
  'Compare the typical daily conversion count and its variability.',
  'Each box summarizes conversions for one channel. The line is the median, the box the middle 50%, and '
  'whiskers use 1.5 interquartile ranges. Points outside are potential outliers.',
  'Which channel tends to bring more conversions per observation, and how variable is it?',
  'Conversion counts depend on spend and traffic. A taller box does not establish better efficiency.'),
 ('Spend versus attributed revenue',
  'Investigate individual campaign observations and their scale.',
  'Each Plotly point is one daily observation: x is spend, y is revenue, color is channel, and bubble '
  'size reflects conversions. Hover identifies the campaign and date.',
  'Which observations combine meaningful conversion volume with strong attributed revenue?',
  'A relationship between spend and revenue does not prove that additional spend will cause additional '
  'revenue. Budget constraints and attribution biases are missing.')]
RECOMMENDATIONS = ['Compare the ROAS leader with the conversion-volume leader before proposing a budget change.',
 'Run a bounded holdout or randomized budget experiment to test incrementality; define a spend limit '
 'and success metric in advance.',
 'Add contribution margin, repeat purchase value, attribution windows and conversion lag before setting '
 'an acquisition-cost target.']
LIMITATIONS = ('Campaign attribution is not causal evidence. The data has no customer deduplication, lifetime value, '
 'product margin, refunds or experiment assignment. A channel cannot be declared universally best from '
 'these observations.')

with st.expander("Business problem and context", expanded=True):
    st.markdown("**The problem:** " + CASE)
    st.markdown("**Decision this dashboard supports:** " + DECISION)
    st.markdown("**What one row means:** " + DATA_CONTEXT)
    st.info("This is a fictional teaching case. Every finding below is calculated from the selected CSV rows, not a claim about a real business.")
    st.write("Start with the KPI cards, read the explanation under each visual, inspect the source data, then open Full report for the complete analysis and a downloadable copy. Filters recalculate the findings and report.")


FIELD_GUIDE = {'date': 'Observation date; one row per channel/campaign/day.',
 'channel': 'Marketing channel receiving attributed results.',
 'campaign': 'Campaign label within the channel.',
 'impressions': 'Number of ad displays, not unique people.',
 'clicks': 'Number of recorded ad clicks, not unique visitors.',
 'conversions': 'Number of attributed conversions.',
 'spend': 'Advertising expense in INR.',
 'revenue': 'Attributed sales in INR; not profit or proven incremental revenue.'}

def explain_visual(index, container=st):
    title, purpose, reading, question, caution = VISUAL_GUIDE[index]
    container.markdown(f"**{title}: what this visual explains**")
    container.write(purpose)
    container.markdown("**How to read it:** " + reading)
    container.markdown("**Question it answers:** " + question)
    container.caption("Interpretation limit: " + caution)

# 1. Load the CSV beside this script, regardless of the terminal's directory.
# Keeping this uncached lets students edit the CSV and immediately rerun the app.
DATA_FILE = Path(__file__).resolve().with_name("marketing_campaigns.csv")
try:
    frame = pd.read_csv(DATA_FILE)
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    numeric_columns = ['impressions', 'clicks', 'conversions', 'spend', 'revenue']
    required_columns = ['date', 'channel', 'campaign', 'impressions', 'clicks', 'conversions', 'spend', 'revenue']
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
selected_channel = st.sidebar.multiselect("Channels", sorted(frame["channel"].unique()), default=sorted(frame["channel"].unique()), key="02_marketing_campaigns_channel")
filtered = filtered[filtered["channel"].isin(selected_channel)]
selected_campaign = st.sidebar.multiselect("Campaigns", sorted(frame["campaign"].unique()), default=sorted(frame["campaign"].unique()), key="02_marketing_campaigns_campaign")
filtered = filtered[filtered["campaign"].isin(selected_campaign)]
dates = st.sidebar.date_input("Date range", (frame["date"].min().date(), frame["date"].max().date()), min_value=frame["date"].min().date(), max_value=frame["date"].max().date(), key="02_marketing_campaigns_dates")
if len(dates) != 2:
    st.info("Choose both a start and an end date.")
    st.stop()
filtered = filtered[filtered["date"].dt.date.between(dates[0], dates[1])]
st.sidebar.caption(f"Showing {len(filtered):,} of {len(frame):,} rows")
if filtered.empty:
    st.info("No rows match these filters. Select at least one value or widen the date range.")
    st.stop()

# 3. Derive business measures, then compare totals, distributions and segments.
spend = filtered["spend"].sum()
revenue = filtered["revenue"].sum()
conversions = filtered["conversions"].sum()
columns = st.columns(4)
columns[0].metric("Ad spend (INR)", f"{spend:,.0f}")
columns[1].metric("ROAS", f"{ratio(revenue, spend):.2f}x")
columns[2].metric("Cost per acquisition (INR)", f"{ratio(spend, conversions):,.0f}" if conversions else "N/A")
columns[3].metric("Conversion rate", f"{ratio(conversions, filtered['clicks'].sum()):.1%}")
st.caption("One row is a channel/campaign observation for one day. ROAS = attributed revenue / spend; conversion rate = conversions / clicks. ROAS is not profit.")
channel_summary = filtered.groupby("channel")[["spend","revenue","clicks","impressions","conversions"]].sum()
channel_summary["roas"] = channel_summary["revenue"].div(channel_summary["spend"].replace(0,float("nan")))
best_channel = channel_summary["roas"].idxmax()
volume_channel = channel_summary["conversions"].idxmax()
ctr = ratio(filtered["clicks"].sum(),filtered["impressions"].sum())
insights = [
 ("What return does the selected activity report?", f"INR {spend:,.2f} of spend is associated with INR {revenue:,.2f} of attributed revenue: ROAS {ratio(revenue,spend):.2f}x. This is an attribution ratio, not a profit calculation."),
 ("How well does traffic convert?", f"The selected records contain {filtered['impressions'].sum():,} impressions, {filtered['clicks'].sum():,} clicks and {conversions:,} conversions. Weighted CTR is {ctr:.2%}; click-to-conversion rate is {ratio(conversions,filtered['clicks'].sum()):.2%}."),
 ("Which channel leads reported efficiency?", f"{best_channel} reports ROAS {channel_summary.loc[best_channel,'roas']:.2f}x on INR {channel_summary.loc[best_channel,'spend']:,.2f} of spend. Review scale and attribution before reallocating budget."),
 ("Which channel brings most conversions?", f"{volume_channel} contributes {channel_summary.loc[volume_channel,'conversions']:,.0f} conversions, or {ratio(channel_summary.loc[volume_channel,'conversions'],conversions):.1%} of the selected total. The volume leader and ROAS leader need not be the same."),
 ("What is acquisition costing?", f"Total spend per conversion is INR {ratio(spend,conversions):,.2f}. Product margin and customer lifetime value are needed to decide whether that cost is acceptable." if conversions else "There are no selected conversions, so cost per acquisition is undefined."),
 ("How variable is spending?", f"The median observation spends INR {filtered['spend'].median():,.2f}; the maximum spends INR {filtered['spend'].max():,.2f}. Use the histogram and hover details to investigate concentration."),
]
kpi_values=[("Ad spend (INR)",f"{spend:,.2f}"),("Attributed revenue (INR)",f"{revenue:,.2f}"),("ROAS",f"{ratio(revenue,spend):.2f}x"),("Cost per acquisition (INR)",f"{ratio(spend,conversions):,.2f}" if conversions else "N/A"),("Conversion rate",f"{ratio(conversions,filtered['clicks'].sum()):.2%}")]

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
    "# " + '02 Marketing Campaigns' + " - full analytical report",
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

overview, explore, data_tab, report_tab = st.tabs(["Campaign dashboard", "Explore the data", "Data and quality", "Full report"])
with overview:
    daily = filtered.groupby("date", as_index=False)[["spend","revenue"]].sum()
    st.plotly_chart(px.line(daily, x="date", y=["spend","revenue"], title="Daily spend and attributed revenue", labels={"value":"INR"}), use_container_width=True)
    explain_visual(0, st)
    channels = filtered.groupby("channel", as_index=False)[["impressions","clicks","conversions","spend","revenue"]].sum()
    channels["ROAS"] = channels["revenue"].div(channels["spend"].replace(0,float("nan")))
    channels["CTR_pct"] = 100*channels["clicks"].div(channels["impressions"].replace(0,float("nan")))
    st.plotly_chart(px.bar(channels, x="channel", y="ROAS", color="channel", title="Return per rupee spent", hover_data=["spend","conversions","CTR_pct"]), use_container_width=True)
    explain_visual(1, st)
    st.dataframe(channels.round(2), hide_index=True, width="stretch")
    st.caption("The table above gives exact grouped values behind the dashboard. Group sizes matter: compare counts alongside totals or rates, and use the data tab to inspect individual observations.")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["spend"], bins=20, color="#7c3aed", edgecolor="white")
    ax.set(title="Daily observation spend", xlabel="Spend (INR)", ylabel="Observations")
    left.pyplot(fig); plt.close(fig)
    explain_visual(2, left)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="channel", y="conversions", ax=ax, color="#ddd6fe")
    ax.set_title("Conversion distribution by channel")
    right.pyplot(fig); plt.close(fig)
    explain_visual(3, right)
    st.plotly_chart(px.scatter(filtered, x="spend", y="revenue", color="channel", size="conversions", hover_data=["campaign","date"], title="Spend versus revenue: hover to investigate"), use_container_width=True)
    explain_visual(4, st)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Source field dictionary")
    st.dataframe(pd.DataFrame(FIELD_GUIDE.items(), columns=["Field", "Meaning and units"]), hide_index=True, width="stretch")
    st.subheader("Filtered records")
    st.write("These are the exact selected observations used for the KPIs and charts, including any derived columns. Sorting this table does not change the analytical filters. Compare a few rows with the formulas before relying on an aggregate.")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_marketing_campaigns.csv", "text/csv")
    st.subheader("Numeric summary")
    st.write("Count is the number of available values; mean is the arithmetic average; std measures spread; min/max are extremes; 25%, 50% and 75% are quartiles. The 50% value is the median. Identifier-like numeric columns and derived measures require business context before interpretation.")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Calculate click-through rate as total clicks / total impressions.\n2. Compare high-ROAS and high-volume channels.\n3. Add a budget recommendation and explain its assumptions.\n4. Investigate whether one unusually strong day changes your conclusion.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")

with report_tab:
    st.download_button("Download full report (Markdown)", full_report, "02_marketing_campaigns_report.md", "text/markdown")
    st.markdown(full_report)
