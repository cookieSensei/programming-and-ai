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
overview, explore, data_tab = st.tabs(["Retention dashboard", "Explore the data", "Data and quality"])
with overview:
    contracts = filtered.groupby("contract", as_index=False).agg(customers=("churned","size"),churn_rate=("churned","mean"))
    contracts["churn_pct"] = 100*contracts["churn_rate"]
    st.plotly_chart(px.bar(contracts, x="contract", y="churn_pct", color="contract", hover_data=["customers"], title="Churn by contract", labels={"churn_pct":"Customers churned (%)"}), use_container_width=True)
    st.plotly_chart(px.scatter(filtered, x="tenure_months", y="monthly_fee", color="status", hover_data=["customer_id","contract","satisfaction_score"], opacity=.65, title="Tenure and monthly fee"), use_container_width=True)
    st.dataframe(contracts[["contract","customers","churn_pct"]].round(2), hide_index=True, width="stretch")
with explore:
    left, right = st.columns(2)
    fig, ax = plt.subplots(figsize=(7,4))
    for status, group in filtered.groupby("status"):
        ax.hist(group["tenure_months"], bins=12, range=(0,60), alpha=.6, label=status)
    ax.set(title="Customer tenure distribution", xlabel="Tenure (months)", ylabel="Customers")
    ax.legend()
    left.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,4))
    sns.boxplot(data=filtered, x="status", y="satisfaction_score", ax=ax, color="#a5f3fc")
    ax.set_title("Satisfaction and churn")
    right.pyplot(fig); plt.close(fig)
    segments = filtered.pivot_table(index="contract", columns="region", values="churned", aggfunc="mean")*100
    fig, ax = plt.subplots(figsize=(9,4))
    sns.heatmap(segments, annot=True, fmt=".1f", cmap="YlOrRd", vmin=0, vmax=100, ax=ax)
    ax.set_title("Churn percentage by contract and region")
    st.pyplot(fig); plt.close(fig)

# 4. Inspect the underlying data and practice explaining the results.
with data_tab:
    st.subheader("Filtered records")
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_customer_churn.csv", "text/csv")
    st.subheader("Numeric summary")
    st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")
    st.subheader("Source data quality")
    st.write(f"Rows: {len(frame):,} | Exact duplicates: {frame.duplicated().sum():,} | Missing cells: {frame.isna().sum().sum():,}")
    st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum().values}), hide_index=True, width="stretch")

with st.expander("Workshop exercises and chart guide"):
    st.markdown('1. Compare contract groups and report their sample sizes.\n2. Add a support-ticket filter.\n3. Compare the median satisfaction of retained and churned customers.\n4. Explain why this snapshot cannot prove that contract type causes churn.')
    st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts support hover, zoom, legend toggles and image download.")
    st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause and effect.")
