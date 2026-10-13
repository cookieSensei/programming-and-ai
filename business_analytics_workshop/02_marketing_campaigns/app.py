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
overview, explore, data_tab = st.tabs(["Campaign dashboard", "Explore the data", "Data and quality"])
with overview:
    daily = filtered.groupby("date", as_index=False)[["spend","revenue"]].sum()
    st.plotly_chart(px.line(daily, x="date", y=["spend","revenue"], title="Daily spend and attributed revenue", labels={"value":"INR"}), use_container_width=True)
    channels = filtered.groupby("channel", as_index=False)[["impressions","clicks","conversions","spend","revenue"]].sum()
    channels["ROAS"] = channels["revenue"].div(channels["spend"].replace(0,float("nan")))
    channels["CTR_pct"] = 100*channels["clicks"].div(channels["impressions"].replace(0,float("nan")))
    st.plotly_chart(px.bar(channels, x="channel", y="ROAS", color="channel", title="Return per rupee spent", hover_data=["spend","conversions","CTR_pct"]), use_container_width=True)
    st.dataframe(channels.round(2), hide_index=True, width="stretch")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(filtered["spend"], bins=20, color="#7c3aed", edgecolor="white")
    ax.set(title="Daily observation spend", xlabel="Spend (INR)", ylabel="Observations")
    left.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="channel", y="conversions", ax=ax, color="#ddd6fe")
    ax.set_title("Conversion distribution by channel")
    right.pyplot(fig); plt.close(fig)
    st.plotly_chart(px.scatter(filtered, x="spend", y="revenue", color="channel", size="conversions", hover_data=["campaign","date"], title="Spend versus revenue: hover to investigate"), use_container_width=True)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Filtered records")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_marketing_campaigns.csv", "text/csv")
    st.subheader("Numeric summary")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Calculate click-through rate as total clicks / total impressions.\n2. Compare high-ROAS and high-volume channels.\n3. Add a budget recommendation and explain its assumptions.\n4. Investigate whether one unusually strong day changes your conclusion.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")
