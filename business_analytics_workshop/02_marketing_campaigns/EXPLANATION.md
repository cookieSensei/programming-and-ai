# Marketing Campaign Lab - business questions, weighted metrics and every line of code

This guide explains the [actual `app.py` in this folder](app.py) and its [bundled `marketing_campaigns.csv`](marketing_campaigns.csv). It assumes you are learning Python, pandas and Streamlit together. Open the source beside this document with editor line numbers enabled, and connect each calculation to the marketing question it answers.

**Source revision:** `c10a61c36fffdd048b69dd78926e6663bc986fce`. The walkthrough refers to the 256-line `app.py` at that revision. It covers every nonblank source line, including introductory text, chart explanations and report assembly. Blank lines organize the file visually and do not execute. If the Python file changes, revisit the line references and baseline results.

All observations are fictional teaching data. INR is the currency. This is a descriptive exploration of attributed campaign results, not a connection to an advertising platform, an automated budget allocator, or a claim about the effectiveness of real advertising channels. The app's own `CASE`, `DATA_CONTEXT` and `LIMITATIONS` establish these boundaries.

## Contents

1. [The business problem and intended solution](#1-the-business-problem-and-intended-solution)
2. [Understand the observation and the source fields](#2-understand-the-observation-and-the-source-fields)
3. [Why pandas and the other libraries are used](#3-why-pandas-and-the-other-libraries-are-used)
4. [Why each metric answers a different question](#4-why-each-metric-answers-a-different-question)
5. [How Streamlit turns calculations into an application](#5-how-streamlit-turns-calculations-into-an-application)
6. [Run the project and reproduce its baseline](#6-run-the-project-and-reproduce-its-baseline)
7. [How to read the five charts](#7-how-to-read-the-five-charts)
8. [Line-by-line walkthrough](#8-line-by-line-walkthrough)
9. [Validation, undefined rates and analytical limits](#9-validation-undefined-rates-and-analytical-limits)
10. [Practice and worked examples](#10-practice-and-worked-examples)
11. [Troubleshooting](#11-troubleshooting)
12. [Sources and further reading](#12-sources-and-further-reading)

## 1. The business problem and intended solution

A marketing team has limited money to spend on campaigns. Its spreadsheet contains impressions, clicks, conversions, spend and attributed revenue. Different measures suggest different winners: one channel attracts many clicks, another produces more conversions, and another reports a high revenue-to-spend ratio. Which result should the team investigate before changing its budget?

The problem is not simply a lack of charts. It is a mismatch between different business questions. Clicks measure recorded interaction with advertisements; conversions measure recorded outcomes under the dataset's conversion definition; revenue measures money attributed to those outcomes; spend measures advertising cost. Comparing channels requires knowing which of these quantities is being compared and whether the channel operated at a meaningful scale.

This app creates a repeatable way to examine those distinctions. The reader selects channels, campaign labels and a date interval. The app calculates total spend, return on ad spend, acquisition cost and conversion rate for exactly those selected observations. It compares daily amounts, aggregate channel efficiency, spending distributions, conversion variability and individual observations. It also exposes the underlying rows, source-quality checks and a downloadable explanatory report.

The useful outcome is an informed **investigation or controlled budget experiment**. For example, "This selection's Display observations have the largest aggregate reported ROAS and substantial conversion volume; examine attribution, contribution margin and performance under a bounded experiment before scaling" connects evidence to a next question. "Display is always the best channel" goes beyond this dataset.

No predictive model is trained. No advertising account is read or changed. No attribution algorithm is implemented. The app accepts the `revenue` and `conversions` fields already present in the CSV and summarizes them. Understanding that boundary is essential: a dashboard can accurately summarize an attribution system while that system still fails to measure the incremental effect of advertising.

## 2. Understand the observation and the source fields

### 2.1 Row grain: a campaign observation, not a customer

One row represents one **channel/campaign observation on one day**. That description is the dataset's grain. The bundled CSV has **360 rows and 8 columns**, spanning **1 January through 31 March 2025**, or 90 dates. In this file there are four rows per date, one for each of Display, Email, Search and Social; each row has one of three campaign labels: Always on, Launch or Seasonal.

Do not reinterpret the row count as customers, campaigns or days. The 360 rows are observations across days and channels. The same channel repeats across dates; a campaign label also repeats. The file does not contain customer identifiers, so neither 360 rows nor 11,634 conversions is a verified count of distinct acquired customers.

The supplied file has no missing cells, no exact duplicate rows and no duplicates of the `date`, `channel`, `campaign` combination. These facts were checked from this particular CSV. The app does not enforce that combination as a unique key; duplicate business observations added later could be counted twice.

### 2.2 Field dictionary

| Source column | Meaning and units | Role in the analysis |
| --- | --- | --- |
| `date` | Observation date | Converted to datetime; used for inclusive interval filtering and daily totals. |
| `channel` | The marketing channel receiving the attributed results | Sidebar selection, group summaries, bar colors and comparisons. |
| `campaign` | A campaign label within the observations | Sidebar selection and hover context. A label alone is not an individual customer's identity. |
| `impressions` | Number of ad displays | Denominator for click-through rate. Repeated displays can belong to the same person. |
| `clicks` | Recorded ad clicks | Numerator for CTR and denominator for click-to-conversion rate; not necessarily unique visitors. |
| `conversions` | Attributed conversion events | Used for conversion volume, conversion rate, acquisition cost and scatter-marker size. |
| `spend` | Advertising cost in INR | Total cost, the ROAS denominator and CPA numerator. |
| `revenue` | Revenue already attributed to the observation, in INR | ROAS numerator and revenue comparisons; not net profit or proven incremental revenue. |

These meanings are stated in the project's `FIELD_GUIDE` and the workshop [README](../README.md). For another dataset, agree on what a conversion means before reusing the formulas. A form submission, account registration and paid purchase are different outcomes even if each is labeled `conversions` in a CSV.

### 2.3 Existing amounts versus derived ratios

Unlike the retail project, this app does not derive revenue from units, price and discount. Both `spend` and `revenue` already exist in the input. It sums them and derives ratios from the sums. There is no hidden price, customer or product-cost lookup.

The `filtered` table retains the eight source columns, with `date` parsed into a datetime type. Group-derived `ROAS` and `CTR_pct` columns are created in the separate `channels` summary table. They do **not** get added to `filtered`. Consequently, the current Download filtered CSV button exports selected source observations, not a per-row ROAS column or the grouped channel table.

This distinction prevents a common confusion: seeing ROAS in the dashboard does not mean the app has stored a row-level rate in the original CSV. The code creates temporary analysis objects in memory and leaves the source file unchanged.

## 3. Why pandas and the other libraries are used

### 3.1 Why a DataFrame is useful here

The questions require operations on tables: load a CSV, interpret dates and numbers, select subsets, add totals, group by channel/date, calculate ratios and export a selection. Pandas supplies a **DataFrame**, a two-dimensional labeled table, and a **Series**, a one-dimensional labeled collection such as a single column. Those concepts are introduced in the official [pandas table-oriented data tutorial](https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/01_table_oriented.html).

```python
frame = pd.read_csv(DATA_FILE)
```

means "parse the CSV and give me a table called `frame`." A reference such as `frame["clicks"]` selects a Series. `frame[["clicks", "conversions"]]` selects a two-column DataFrame: the inner brackets construct a list, and the outer brackets apply the selection. A name such as `spend` later in the file is a scalar total, while `filtered["spend"]` is still a column of amounts. Distinguishing those types makes the code much easier to follow.

Without pandas, Python could still solve these problems using dictionaries, lists and loops, but we would need to implement all of those transformations manually. Pandas lets the central business operation stay visible. For example:

```python
filtered.groupby("channel")[["spend", "revenue"]].sum()
```

reads almost like the question: group selected observations by channel, choose spend and revenue, and sum both within each group. The result has one row per channel rather than one row per original observation. This is the table on which channel-level ROAS should be calculated.

Pandas is useful here because its methods fit the data problem, not because pandas makes a conclusion automatically correct. A perfectly valid `.sum()` can still double-count duplicated observations. A valid ratio can still use the wrong denominator. The learner's job is to connect code, units, grain and interpretation.

### 3.2 The project's main pandas operations

| Operation | What it contributes |
| --- | --- |
| `read_csv()` | Reads the file's headers and rows into a table. |
| `to_datetime()` | Makes dates comparable and groupable as dates rather than arbitrary text. |
| `to_numeric()` | Ensures counts and amounts can participate in arithmetic; invalid text raises an error. |
| `.copy()` | Starts a separate working table while retaining the full loaded source for quality checks. |
| `.unique()`, `sorted()` | Supplies stable, distinct widget choices. `sorted()` is a Python built-in used with pandas results. |
| `.isin()` and Boolean indexing | Converts channel/campaign choices into selected rows. |
| `.dt.date.between()` | Filters observations using an inclusive requested interval. |
| `.groupby().sum()` | Aggregates related observations before comparing channels or dates. |
| `.div()` with `.replace(0, NaN)` | Calculates grouped rates while representing zero-denominator group rates as undefined. |
| `.idxmax()` | Finds the group label attached to the maximum value, rather than only the numeric maximum. |
| `.describe()` | Summarizes the distribution of each numeric field. |
| `.to_csv(index=False)` | Makes a downloadable CSV string without an extra pandas-index column. |

The [pandas GroupBy guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html) calls the grouping pattern split-apply-combine: split rows into groups, apply an aggregation, combine the results into a new table. Here that pattern turns hundreds of daily observations into a few channel summaries.

### 3.3 Why several plotting libraries appear

| Import | Actual purpose in this app |
| --- | --- |
| `Path` | Locates `marketing_campaigns.csv` relative to `app.py`, making loading independent of the terminal's current folder. |
| `matplotlib.pyplot as plt` | Creates figure/axes objects, draws the spending histogram and manages figure cleanup. |
| `pandas as pd` | Loads, validates, filters, aggregates and exports tabular observations. |
| `plotly.express as px` | Builds interactive daily line, channel bar and observation scatter charts. |
| `seaborn as sns` | Builds the per-channel conversion boxplot on Matplotlib axes. |
| `streamlit as st` | Renders browser controls, layout, tables, charts, text, notices and downloads. |

The workshop intentionally exposes complementary plotting styles. Matplotlib teaches direct figure/axes control; Seaborn expresses a statistical distribution comparison; Plotly Express produces interactive figures from a DataFrame with compact declarations. Streamlit displays each figure in the app. Pandas computes the values; plotting libraries encode them visually; Streamlit connects the analysis to a usable interface.

There is no direct NumPy import in this file even though NumPy is part of the pinned workshop environment. There is no need to invent a NumPy step when explaining this program.

### 3.4 Python syntax worth recognizing

`import ... as ...` gives a library a short alias. `=` assigns a value, whereas `==` would compare values. `def` defines a function; its body executes when called. `if` chooses whether a block runs. `for` repeats a block. Indentation tells Python which statements belong to those blocks.

An f-string such as `f"{ratio(revenue, spend):.2f}x"` calls the ratio function, formats the result to two decimal places, and adds the literal `x`. The `x` is a label for a multiple, not a multiplication operator inside that string. `:.1%` instead formats a fraction as a percentage, multiplying by 100 for display. Mixing up these two formats would make the same underlying number appear to mean something different.

## 4. Why each metric answers a different question

### 4.1 The funnel and the units

Conceptually, the fields follow stages: advertisements are displayed, some displays generate clicks, and some clicks are associated with attributed conversions. The CSV stores event counts for those stages. Ratios compare different stages, but those counts are not unique people and the code does not verify an individual-level journey.

Consider this **invented arithmetic example**, separate from the supplied CSV:

| Impressions | Clicks | Conversions | Spend | Attributed revenue |
| ---: | ---: | ---: | ---: | ---: |
| 10,000 | 300 | 24 | INR 2,400 | INR 9,600 |

This one example supports several different questions:

- CTR is `300 / 10000 = 0.03`, or 3%: recorded clicks per ad display.
- Click-to-conversion rate is `24 / 300 = 0.08`, or 8%: attributed conversions per recorded click.
- CPA is `2400 / 24 = 100`: INR 100 advertising spend per attributed conversion.
- ROAS is `9600 / 2400 = 4`: INR 4 attributed revenue for every INR 1 of ad spend.

Each denominator represents the quantity against which performance is normalized. Replacing clicks with impressions changes the conversion question. Replacing spend with revenue changes the efficiency ratio. Correct code is not just code that runs; it must divide by the quantity that matches the intended question.

### 4.2 Total ad spend

```python
spend = filtered["spend"].sum()
```

adds the advertising cost of all selected observations. It answers how much advertising cost the selected records represent. No ratio is needed for an amount. It should be read with the selected interval and campaigns: a larger spend total can simply represent more days or more selected channels.

### 4.3 Return on ad spend

The app calculates:

```python
ratio(revenue, spend)
```

where both arguments are totals of the selected observations. ROAS is a multiple. A reported 3.43x means about INR 3.43 attributed sales per INR 1 spent, under the dataset's attribution definition. It does not mean INR 3.43 profit per INR 1 spent.

Why not subtract spend from revenue and call the difference profit? Revenue also needs to pay product/service delivery costs and other expenses. This file contains none of those costs. It also does not establish which sales would have happened without advertising. Even `revenue - spend` would be an incomplete accounting measure and would not demonstrate advertising's causal contribution.

### 4.4 Cost per acquisition

```python
ratio(spend, conversions)
```

calculates advertising spend per attributed conversion. The UI calls it cost per acquisition, but the actual denominator is **conversion events**. Without distinct-customer information or a first-purchase flag, the program cannot prove that every conversion represents a newly acquired customer.

When `conversions` is zero, the metric card and report explicitly display `N/A`. If no conversions occurred, a positive advertising cost cannot be divided into a meaningful cost per conversion. Showing zero cost would falsely suggest perfect efficiency. This is why the CPA display has its own `if conversions else "N/A"` condition even though the shared `ratio()` helper returns zero for a zero denominator.

### 4.5 Conversion rate and click-through rate

Conversion rate is total conversions divided by total clicks. CTR is total clicks divided by total impressions. The app computes both as fractions and uses percentage formatting when displaying them. For the grouped channel hover/table, it instead multiplies the CTR fraction by 100 and stores that percentage value in a field named `CTR_pct`.

This distinction matters when extending the code. If a value is already multiplied by 100, formatting it again with `%` would multiply it a second time. A fraction of `0.04` becomes 4% with `:.0%`; a stored `CTR_pct` of `4.0` should be read as 4 percentage points, not formatted as 400%.

CTR concerns ad interaction, not final return. A channel may get inexpensive attention but few paid outcomes. Conversion rate concerns conversion among recorded clicks; it is influenced by audience, offer, landing-page experience and other unobserved differences. Neither rate independently identifies what caused a difference between channels.

### 4.6 Why ratios must use totals

Suppose two **invented** observations have these clicks and conversions:

| Observation | Clicks | Conversions | Row conversion rate |
| --- | ---: | ---: | ---: |
| A | 10 | 5 | 50.00% |
| B | 990 | 45 | About 4.55% |
| Combined | 1,000 | 50 | **5.00%** |

The simple average of 50% and 4.55% is about 27.27%, which does not describe the combined activity. Observation A contains only 10 clicks but receives half the weight in that simple average. The correct combined rate is `sum(conversions) / sum(clicks) = 50 / 1000 = 5%`. Equivalently, weight each row's rate by its click count.

The same principle applies to ROAS. An observation with INR 100 spend and INR 1,000 attributed revenue reports 10x. Another with INR 900 spend and INR 900 revenue reports 1x. The mean of their ROAS values is 5.5x, but the combined result is `1900 / 1000 = 1.9x`. Aggregate ROAS weights by spend, because spend is the denominator of the underlying ratio.

More generally, the appropriate weights follow each measure's denominator: clicks for conversion rate, impressions for CTR, spend for ROAS, and conversions for aggregate CPA. The app avoids a list of special weighted-average calculations by summing the relevant numerators and denominators first. See how `channel_summary` sums five measures before it derives `roas`.

### 4.7 Efficiency and scale are different questions

The code identifies one channel by maximum aggregate `roas` and another by maximum `conversions`. They can be different. A tiny channel can have a high ratio but contribute few conversions; a large channel can generate many conversions at lower reported efficiency. The grouped table and hover fields keep spend and volume visible beside the ratio.

In the full bundled dataset, Display happens to lead both aggregate ROAS and conversion count. That is a result of this selection, not a requirement built into the app. A different campaign/date selection can lead to a different comparison, and a valid analysis must report the actual result even when it does not illustrate the contrast a teacher expected.

### 4.8 Question-to-code map

| Question | Code mechanism | Why the mechanism answers it | What remains unanswered |
| --- | --- | --- | --- |
| How much advertising cost is represented? | Sum selected `spend` (146) | Adds the amounts for the exact chosen scope | Whether every relevant expense was recorded |
| How much attributed revenue per INR spent? | Total revenue divided by total spend (147, 151) | Normalizes reported revenue by advertising cost | Incremental revenue, margin and net profit |
| How expensive is each attributed conversion? | Total spend divided by total conversions; N/A if none (148, 152) | Matches advertising cost with counted outcomes | Unique new customers, lifetime value and acceptable acquisition cost |
| How well does selected traffic convert? | Total conversions divided by total clicks (153, 162) | Measures conversion events relative to recorded clicks | Why the rate differs, or whether clicks/users are deduplicated |
| Which channel has highest reported efficiency? | Group sums, derive ROAS, find label at maximum (155-157) | Compares like-defined aggregate channel ratios | Whether efficiency persists if budget is increased |
| Which channel brings most conversions? | Maximum grouped conversions (158, 164) | Ranks observed outcome volume independently of the ratio | Quality, profit or incremental value of those outcomes |
| Is spending concentrated in some observations? | Median/max and histogram (166, 222) | Exposes center, extremes and distribution | Whether concentration was deliberate or commercially wise |

## 5. How Streamlit turns calculations into an application

### 5.1 A Python script becomes a browser interface

Starting the program with `streamlit run app.py` runs a Streamlit server. The Python code runs in the server's environment while the user views and controls the app in a browser. Commands such as `st.title()`, `st.sidebar.multiselect()`, `st.metric()` and `st.dataframe()` describe what should appear on that page. This app does not manually define HTML pages, JavaScript event handlers or web API endpoints.

The official [Streamlit run-your-app guide](https://docs.streamlit.io/develop/concepts/architecture/run-your-app) describes the runner. The key programming model is that normal input-widget changes trigger a rerun of the script from top to bottom with the current widget values. Consequently, the author can express one clear sequence: load, validate, filter, aggregate, interpret and render.

The top-of-file constants are reusable explanatory content. The sidebar widgets return actual Python values. A multiselect returns a list of selected channel/campaign labels; the date-range widget returns date selections. The app uses those returned values to construct the analysis population. The controls are therefore inputs to the calculation, not merely visual decoration.

### 5.2 One selected table drives the outputs

The application starts with `filtered = frame.copy()`. It then applies three conditions in order:

1. Channel membership in the selected channel list.
2. Campaign membership in the selected campaign list.
3. Date membership in the chosen inclusive interval.

Sequential filtering means a retained observation satisfies **all three** conditions. The app checks for an empty result before calculating rankings or drawing charts. Cards, answers, chart data, the selected-record table and report scope are then built from `filtered`, ensuring they refer to the same observations.

The widget options are read from full `frame`. Selecting Search does not dynamically rebuild campaign options to show only combinations present for Search. An empty combination is allowed as an input but is handled by the empty-state message. Unique widget keys such as `02_marketing_campaigns_channel` identify Streamlit controls; they are unrelated to database keys or marketing attribution.

### 5.3 Reruns, tabs and uncached data

The source intentionally does not cache `read_csv()`. If you edit and save the CSV, the next rerun reads it again. That does not imply a special CSV watcher automatically reruns the app immediately after every file edit; trigger a rerun if needed. The small teaching dataset makes the straightforward behavior easy to understand.

The four tabs organize output: Campaign dashboard, Explore the data, Data and quality, and Full report. In the pinned Streamlit 1.50 behavior, the code in all tab containers executes on a full rerun, not only in the currently visible tab. The same principle applies to an expander's content: collapsing it hides the output but does not make the block a conditional computation. See the [Streamlit 1.50 tabs API](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs).

The app uses `with` blocks as rendering contexts. `with overview:` sends subsequent Streamlit elements to the dashboard tab; it does not select rows. Plotly hover/zoom and interactive table sorting help inspect a view, but they are not additional analytical filters in this code. In particular, sorting the source-record table does not change the KPI population.

### 5.4 Reports and downloads are assembled from calculated values

`insights` is a list of predefined questions and calculated answer strings. F-strings insert totals, ratios, labels and amounts. `report_parts` combines those answers with explanations, scope, quality checks and limitations. The report is deterministic Python text assembly, not a call to an AI model.

The same `full_report` string is displayed with `st.markdown()` and offered with `st.download_button()`. It includes written chart explanations but does not embed chart image files. A separate download serializes selected source rows as CSV. Neither button modifies the source dataset or this guide, and neither sends information to an advertising account.

## 6. Run the project and reproduce its baseline

### 6.1 Local setup

Use the environment documented in the workshop [README](../README.md): Python 3.12 with the versions below. From the repository root in a Linux/macOS terminal:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit==1.50.0 pandas==2.2.3 numpy==2.3.5 matplotlib==3.10.8 seaborn==0.13.2 plotly==6.5.2
cd business_analytics_workshop/02_marketing_campaigns
python -m streamlit run app.py
```

Make sure `python` is your Python 3.12 interpreter before creating the environment, or call your Python 3.12 executable explicitly. The environment keeps this project's packages separate from other projects. `python -m pip` and `python -m streamlit` use the same interpreter selected by `python`, reducing confusion when multiple Python installations exist.

On Windows PowerShell, environment activation is `.venv\Scripts\Activate.ps1`. However, the full repository contains phase-folder names with `>`, which native Windows filesystems cannot use. Follow the root [README](../../README.md) and use a Linux Cloud Lab or clone within WSL's Linux filesystem for the full repository. The workshop folder itself does not contain those special phase names.

Open the URL printed by Streamlit, usually `http://localhost:8501`, while the server is running. The app needs its local dataset and installed libraries, not an API key, database or advertising-platform connection. Installing packages may require network access; loading the included CSV does not.

### 6.2 In the prepared CookieSensei workshop workspace

The workspace may already provide the Business Analytics Dashboard project selector. To run a separate editable app in its terminal, use the folder and port described in the workshop instructions:

```bash
cd /home/coder/project/business_analytics_workshop/02_marketing_campaigns
streamlit run app.py --server.port 8502
```

The built-in dashboard uses port 8501, so forward/open 8502 for this separate instance. The project selector belongs to the surrounding workspace; this `app.py` remains an independent app. Existing student copies are preserved, so updating repository content does not automatically overwrite every older workspace copy.

### 6.3 Baseline from all supplied observations

These results were independently recalculated from the bundled CSV with all channels, all campaign labels and the full available date interval. They describe teaching data, not real advertising results.

| Measure | Full-selection value |
| --- | ---: |
| Observation count | 360 |
| Date count | 90 |
| Impressions | 3,484,268 |
| Clicks | 146,788 |
| Conversions | 11,634 |
| Total ad spend | INR 2,431,713.93 |
| Total attributed revenue | INR 8,338,864.84 |
| Aggregate ROAS | 3.43x |
| Spend per attributed conversion | INR 209.02 |
| Click-to-conversion rate | 7.93% |
| Click-through rate | 4.21% |
| Median spend per observation | Approximately INR 5,031.51 |
| Maximum spend per observation | INR 33,200.45 |

The display cards round ad spend and CPA to whole INR and conversion rate to one decimal place. The report usually retains two decimals. These differences are formatting choices, not separate calculation methods. The app does not round every intermediate amount to paise before aggregating.

The channel comparison explains the default leader statements:

| Channel | Observations | Spend (INR) | Attributed revenue (INR) | Conversions | Aggregate ROAS |
| --- | ---: | ---: | ---: | ---: | ---: |
| Display | 90 | 645,963.35 | 2,580,802.82 | 3,391 | 4.00x |
| Email | 90 | 627,985.17 | 1,979,780.89 | 2,837 | 3.15x |
| Search | 90 | 558,090.56 | 1,883,842.10 | 2,701 | 3.38x |
| Social | 90 | 599,674.85 | 1,894,439.03 | 2,705 | 3.16x |

The leader's rounded 4.00x is about 3.9953 before formatting. Do not use rounded displayed values as the inputs to reproduce another calculation; use the source sums.

You can check the key totals in a separate Python session without launching the interface. This **standalone verification example** assumes the current directory contains the CSV:

```python
import pandas as pd

observations = pd.read_csv("marketing_campaigns.csv")
spend = observations["spend"].sum()
revenue = observations["revenue"].sum()
clicks = observations["clicks"].sum()
conversions = observations["conversions"].sum()
impressions = observations["impressions"].sum()
print(f"Spend: {spend:,.2f}")
print(f"Revenue: {revenue:,.2f}")
print(f"ROAS: {revenue / spend:.2f}x")
print(f"CPA: {spend / conversions:,.2f}")
print(f"Conversion rate: {conversions / clicks:.2%}")
print(f"CTR: {clicks / impressions:.2%}")
```

For a manual source-row check, the first observation is Search / Seasonal on 1 January 2025: 14,074 impressions, 984 clicks, 96 conversions, INR 6,793.68 spend and INR 94,378.06 attributed revenue. Its row CTR is approximately 6.99%, conversion rate 9.76%, CPA INR 70.77 and ROAS 13.89x. These row-level rates are a teaching calculation from the CSV; the existing app displays aggregate selected/grouped rates rather than creating those row columns.

## 7. How to read the five charts

### 7.1 Daily spend and attributed revenue

The app first groups selected rows by date and sums spend and revenue. There can be several observations on a date, so plotting each raw row as though it were a complete daily total would be misleading. The grouped line chart shows one selected total per date for each of the two measures, both on an INR axis.

This view answers whether periods of larger reported revenue coincide with larger spend. It does not show profit. It also does not match an advertisement to the future date of a customer's purchase or estimate conversion lag. The code neither inserts dates absent from the selected data nor normalizes totals by the number of observations on a date. Check scope before interpreting changes.

### 7.2 Return per rupee by channel

The bar chart uses channel totals to derive ROAS. Its y-axis is a ratio, not rupees: a height of 4 means four rupees of attributed revenue per rupee spent. Each channel has its own color. Hover exposes spend, conversions and `CTR_pct` so the reader can examine scale beside efficiency.

A high bar with very little spend is not evidence that unlimited extra spending would retain the same return. Audiences, campaign mix, available reach and attribution practices can differ between groups. In this descriptive dataset the ratio is an observation, not an experimentally established response to increasing the budget.

### 7.3 Observation spend distribution

The histogram uses raw selected `spend` values, divided into 20 bins. Each bar counts **channel/campaign-day observations** whose spend lies in that bin. It is not a histogram of complete daily company budgets. For the supplied file, a typical day has four observations; aggregating to daily company spend first would answer a different question.

Use this chart to ask whether most observations operate at similar scale or a few absorb much larger amounts. A long right tail would make a maximum or average less representative of an ordinary observation. The median in the generated insights supplies a useful comparison. Changing the bin count would change appearance, so investigate underlying rows before interpreting a visually isolated bin as an error.

### 7.4 Conversion distribution by channel

The Seaborn boxplot summarizes conversions per selected observation within each channel. The median line gives the distribution's center; the box covers its middle 50%; whiskers extend to observations within the default 1.5-interquartile-range rule; more distant points are drawn separately. The [official boxplot reference](https://seaborn.pydata.org/generated/seaborn.boxplot.html) documents these semantics.

The vertical quantity is **count per observation**, not a conversion percentage. A channel can have more conversions because it receives more spend or more clicks. A higher box therefore does not automatically indicate greater efficiency. The chart also does not display sample size through box width. Check observation counts and the grouped totals before comparing how much evidence supports each distribution.

### 7.5 Spend versus attributed revenue

The scatter plot retains individual selected observations. Its x-axis is spend in INR, y-axis is attributed revenue in INR, color identifies channel and marker size represents conversions. Hover identifies the campaign and date, allowing the reader to trace an interesting point back to its row.

The point's slope from the origin corresponds conceptually to revenue divided by spend, but the app does not draw a fitted regression line or compute a correlation coefficient here. A cluster farther to the upper right is larger in spend and revenue, not necessarily better in ROAS. Marker size provides conversion scale, but a larger marker does not mean a higher conversion rate.

A spend/revenue association can arise because larger campaigns produce larger measured amounts, because successful campaigns receive larger budgets, or because of unobserved differences. This plot alone cannot establish that an extra rupee of spend causes a specific increase in revenue. That question needs a suitable design and additional evidence.

## 8. Line-by-line walkthrough

Refer to [app.py](app.py) alongside these tables. Numbers are source lines, not steps you must run manually. Groups of continued string literals are explained together because they form one textual value. Blank lines supply spacing; all nonblank lines are covered below.

### 8.1 Imports and page configuration: lines 1-15

| Line(s) | What the code does and why |
| --- | --- |
| 1 | The module docstring identifies this as the Marketing Campaign Lab and states its fictional teaching purpose. It is source documentation, not an automatic browser element. |
| 2 | Imports `Path` from the standard-library `pathlib` module for script-relative dataset location. |
| 4 | Imports Matplotlib's plotting interface as `plt` for figure/axes construction, the histogram and closing figures. |
| 5 | Imports pandas as `pd` for reading and transforming tabular data. |
| 6 | Imports Plotly Express as `px` for interactive line, bar and scatter figures. |
| 7 | Imports Seaborn as `sns` for the conversion boxplot. |
| 8 | Imports Streamlit as `st` for page controls and rendered content. |
| 10 | Sets the browser page title, chart icon and wide layout using named arguments. |
| 11 | Adds the visible Marketing Campaign Lab page title. |
| 12 | Adds a smaller caption identifying the workshop, fictional data and INR currency. |
| 13 | Displays the opening learning objective: compare reach, conversions and cost, and calculate campaign rates from totals. |
| 15 | A comment introduces the business question and reading guidance stored below. Comments do not execute as calculations. |

### 8.2 Case study and reusable explanation data: lines 16-77

The uppercase variable names are a convention for reusable descriptive content; Python does not make them constant automatically. Adjacent string literals inside parentheses are concatenated into one string. Tuples keep related pieces of a definition or chart guide together.

| Line(s) | What the code does and why |
| --- | --- |
| 16-17 | Builds `CASE`, describing limited advertising budget and the distinction between clicks, purchases and high return at small scale. |
| 18-19 | Builds `DECISION`, framing the outcome as choosing combinations to investigate in controlled experiments, balancing return, cost and volume. |
| 20-22 | Builds `DATA_CONTEXT`: one channel/campaign-day row, 360 fictional observations, 90 days, attributed revenue and no customer-level incrementality proof. This is static documentation, not a dynamically calculated row count. |
| 23 | Starts `FORMULAS` and adds a three-item tuple explaining total ad spend. The strings document a formula; they do not compute the sum. |
| 24-27 | Adds ROAS name, numerator/denominator description and the interpretation of revenue per rupee spent. Continued lines explicitly distinguish that from profit. |
| 28-30 | Adds the CPA definition and the undefined-no-conversions case. |
| 31-33 | Adds conversion-rate definition and the requirement to aggregate with click-based weighting. |
| 34-36 | Adds CTR definition and its engagement interpretation, then closes the formulas list. |
| 37-43 | Starts `VISUAL_GUIDE` with the daily line-chart tuple: title, purpose, axis/aggregation explanation, question and caution about attribution/lag. |
| 44-50 | Adds the channel ROAS chart guide, including aggregate-rate logic, scale in hover information and limits on extrapolating a high ratio. |
| 51-56 | Adds the spend histogram guide, identifying bins, observation counts and the channel/campaign-day grain. |
| 57-62 | Adds the conversion boxplot guide, explaining median, quartiles, whiskers and the distinction between counts and efficiency. |
| 63-69 | Adds the scatter guide, mapping x, y, color, size and hover, and warning that spend/revenue association does not prove a causal response. The final bracket closes all five guide entries. |
| 70 | Starts `RECOMMENDATIONS` with the need to compare the ROAS leader and conversion-volume leader. |
| 71-72 | Adds one continued string recommending a bounded holdout or randomized experiment with explicit limits and success criteria. This text does not run an experiment. |
| 73-74 | Adds a continued string requesting margin, repeat-purchase value and attribution/lag information before setting acquisition-cost targets, then closes the list. |
| 75-77 | Builds `LIMITATIONS`, describing missing customer deduplication, lifetime value, product margin, refunds and experimental assignment. |

### 8.3 Context, field definitions and reusable chart captions: lines 79-102

| Line(s) | What the code does and why |
| --- | --- |
| 79 | Opens the Business problem and context expander, initially expanded, and establishes the container for its indented commands. |
| 80 | Displays a bold Markdown problem label plus the `CASE` string. |
| 81 | Displays the intended decision context. |
| 82 | Displays the row meaning and dataset context. |
| 83 | Adds an informational notice separating fictional teaching findings from claims about real businesses. |
| 84 | Displays a suggested reading sequence and tells the reader that filters recalculate the findings and report. |
| 87 | Starts `FIELD_GUIDE` with the observation-date definition. |
| 88 | Adds the channel definition. |
| 89 | Adds the campaign-label definition. |
| 90 | Defines impressions as ad displays, explicitly excluding a unique-person interpretation. |
| 91 | Defines clicks as recorded events, explicitly excluding a unique-visitor interpretation. |
| 92 | Defines conversions as attributed conversion events. |
| 93 | Defines spend as advertising expense in INR. |
| 94 | Defines revenue as attributed sales, not profit or proven incremental revenue, and closes the dictionary. |
| 96 | Defines `explain_visual(index, container=st)`. The optional container allows the same function to render in the page or a left/right column. The body does not execute until called. |
| 97 | Selects one five-item visual tuple by zero-based index and unpacks it into named parts. |
| 98 | Renders a bold heading containing that visual's title using an f-string. |
| 99 | Writes the purpose into the selected container. |
| 100 | Displays the reading instructions with a Markdown label. |
| 101 | Displays the corresponding business question. |
| 102 | Displays the interpretation caution as a caption, keeping chart explanations consistent. |

### 8.4 Loading, type checks and division helper: lines 104-126

| Line(s) | What the code does and why |
| --- | --- |
| 104 | Comment introducing dataset location relative to the Python script. |
| 105 | Comment explaining that loading is uncached so a later rerun reads the saved CSV again. |
| 106 | Wraps `__file__` in `Path`, resolves an absolute path and replaces the script filename with `marketing_campaigns.csv`. The data remains beside the script regardless of the terminal's working directory. |
| 107 | Starts a `try` block around loading and validation so expected errors can be displayed usefully. |
| 108 | Parses the CSV into a DataFrame called `frame`; pandas infers initial types from file contents. |
| 109 | Converts `date` into pandas datetime values and raises on invalid date parsing. This happens before the full schema check, so an absent date field becomes a caught `KeyError`. |
| 110 | Lists the five numeric fields: three counts and two monetary amounts. |
| 111 | Lists the full required eight-column schema. |
| 112 | Checks whether every required name is present in the source columns. Extra columns are allowed because the test is a subset check. |
| 113 | Raises `ValueError` if a required column is missing. |
| 114 | Checks whether the table has no observations. Headers alone do not provide analyzable rows. |
| 115 | Raises a clear empty-file error instead of continuing to minimum dates or rankings. |
| 116 | Loops over each numeric column name. |
| 117 | Converts that field to numeric values with errors raised for invalid text, and assigns the resulting Series back to the table. It does not enforce integer or nonnegative counts. |
| 118 | Marks missing cells in required fields, uses `.any()` to reduce each column, then `.any()` again to ask whether any required field contains a missing cell. |
| 119 | Raises an error asking the learner to fix missing analysis values rather than silently dropping affected observations. |
| 120 | Catches file-system, value-conversion and key-lookup errors, exposing the exception as `error`. |
| 121 | Displays the CSV name and error message with Streamlit's error element. |
| 122 | Stops the current script run, preventing later use of invalid or unavailable source data. |
| 124 | Defines `ratio()` for scalar numerator/denominator division used by cards and sentences. |
| 125 | Documents the implementation's zero-denominator fallback. It is a programming safeguard, not a mathematical definition of an undefined rate. |
| 126 | Returns the quotient for a truthy denominator and `0.0` otherwise. It handles numeric zero but is not a validator for NaN, infinity, negative amounts or impossible counts. |

### 8.5 Filter the observation population: lines 128-143

| Line(s) | What the code does and why |
| --- | --- |
| 128 | Comment establishing the order: apply controls before calculating any chart or KPI. |
| 129 | Adds the sidebar filter heading. |
| 130 | Copies the source table into `filtered`, retaining `frame` for source-quality reporting. |
| 131 | Creates a channel multiselect from sorted distinct source channels, initially selecting all, and gives it a project-specific widget key. The return value is the currently selected list. |
| 132 | Creates a Boolean membership mask with `.isin(selected_channel)` and retains only matching channel rows. |
| 133 | Creates a campaign multiselect from full-source campaign labels, also initially selecting all. Its options do not automatically shrink to the preceding channel selection. |
| 134 | Retains only observations whose campaign label is in the chosen list, combining this condition with the existing channel filter. |
| 135 | Creates the date-range control using source min/max dates for its initial pair and limits. `.date()` converts pandas Timestamp boundaries to Python date objects. |
| 136 | Checks that both dates are currently selected before reading two elements from the returned value. |
| 137 | Displays a completion message if only part of the date interval exists. |
| 138 | Stops the incomplete run, preventing an invalid interval lookup. |
| 139 | Extracts each timestamp's date and uses `.between()` to keep both boundary dates and all dates between them. |
| 140 | Displays how many source rows survived all filters, with thousands separators for readability. |
| 141 | Checks whether the current selection has zero observations. |
| 142 | Displays recovery guidance for an empty population. |
| 143 | Stops before totals, group leaders and plots are calculated from empty data. |

### 8.6 Totals, weighted rates and calculated insights: lines 145-168

| Line(s) | What the code does and why |
| --- | --- |
| 145 | Comment introducing business measures and comparisons. This project derives aggregate rates rather than adding per-observation revenue. |
| 146 | Sums selected advertising cost into the scalar `spend`. |
| 147 | Sums already attributed source revenue into the scalar `revenue`. It does not estimate revenue from clicks. |
| 148 | Sums conversion counts into `conversions`; the result is conversion events, not verified unique customers. |
| 149 | Creates four horizontal containers for the metric cards. |
| 150 | Displays total ad spend in the first container. `:,.0f` adds separators and rounds only the rendered string to whole INR. |
| 151 | Displays total revenue divided by total spend with two decimals and an `x` suffix. Aggregating first avoids averaging observation ROAS values incorrectly. |
| 152 | Displays spend per conversion with whole-INR formatting if conversions exist; otherwise displays `N/A` instead of the helper's zero fallback. |
| 153 | Displays total conversions divided by total clicks as a percentage with one decimal place. It does not average observation conversion rates. |
| 154 | Reminds readers of the observation grain, ROAS and conversion formulas, and the distinction between attributed return and profit. |
| 155 | Groups by channel and sums spend, revenue, clicks, impressions and conversions. The channel labels form the result's index. |
| 156 | Creates channel-level `roas` from summed revenue divided by summed spend, replacing zero spend with NaN so an undefined group rate is not represented as infinity. |
| 157 | Finds the channel label at the maximum defined ROAS. `.idxmax()` returns a label; `.max()` would return the ratio itself. It assumes a defined group ratio exists. |
| 158 | Finds the channel label with the greatest conversion count, which can differ from the efficiency leader. |
| 159 | Calculates overall CTR from summed clicks and impressions. The result is a fraction until formatted for display. |
| 160 | Starts a list of question/answer tuples to reuse in the screen summary and full report. |
| 161 | Builds the spend/revenue/ROAS answer using calculated totals, then warns that attribution ratio is not profit. |
| 162 | Builds the funnel answer from total impressions, clicks and conversions plus aggregate CTR and click-to-conversion rate. `:,` formats counts; `:.2%` formats fractions. |
| 163 | Builds the efficiency-leader answer by using `.loc[best_channel, ...]` to fetch that channel's ratio and spend, keeping scale visible. |
| 164 | Builds the conversion-volume-leader answer and its share of all selected conversions. The helper provides a fallback if the total conversion count is zero. |
| 165 | Builds either a CPA sentence or an explicit undefined-CPA sentence using a conditional expression. Additional margin/lifetime-value context is requested rather than invented. |
| 166 | Builds a spending-variability answer from the median and largest per-observation spend, not aggregated company-day spend. |
| 167 | Closes the insights list. |
| 168 | Creates five report KPI label/value pairs. Unlike the four cards, this list includes total attributed revenue explicitly; formatting usually uses two decimal places. |

### 8.7 Scope and short answer display: lines 170-187

| Line(s) | What the code does and why |
| --- | --- |
| 170 | Comment stating that the report should use the same filtered table as the charts. |
| 171 | Creates an empty list for human-readable descriptions of the current scope. |
| 172 | Iterates over source columns with dtype `object`, which includes ordinary text channel and campaign labels here. |
| 173 | Restricts scope lists to fields having at most 12 distinct source values, avoiding unwieldy lists if high-cardinality fields are later added. |
| 174 | Makes each field name readable, extracts/sorts distinct selected values, converts them to strings, joins them with commas and appends the resulting description. |
| 175 | Iterates over datetime source columns, including the parsed observation date. |
| 176 | Appends the earliest/latest selected observed dates using a year-month-day format. Observed bounds can differ from requested bounds if selected boundary dates contain no rows. |
| 177 | Separately appends the actual requested inclusive date window from the control. |
| 178 | Joins all scope descriptions with semicolons into one string. |
| 180 | Opens the KPI-definitions expander. |
| 181 | Converts `FORMULAS` tuples into a three-column DataFrame and renders it without the pandas row index. `width="stretch"` uses the available container width. |
| 182 | States the shared-scope and summed-denominator rules and explains why zero-denominator display fallbacks need caution. |
| 184 | Adds a heading for answers calculated from the selected observations. |
| 185 | Loops over `insights[:3]`, which contains only the first three question/answer pairs. The other insights are still used in the report. |
| 186 | Displays each question in bold followed by its answer. |
| 187 | Displays selected/source row counts and the generated scope string beneath those answers. |

### 8.8 Assemble a complete report: lines 189-205

| Line(s) | What the code does and why |
| --- | --- |
| 189 | Starts `report_parts`, a list of Markdown strings that will become one report. |
| 190 | Adds the report title as list element 0. |
| 191 | Adds section 1 using the case-study problem. `\n` produces a newline in the output string. |
| 192 | Adds section 2 with decision and data context separated by a blank line. |
| 193 | Adds section 3 with source filename, selected/source row counts, current scope and descriptive/fictional qualification. |
| 194 | Adds an executive summary by joining the first three answer strings; the `_` variable discards each question during tuple unpacking. |
| 195 | Creates the KPI Markdown table: a header followed by one formatted row from each `kpi_values` tuple. |
| 196 | Creates the definitions table using the name, formula and business interpretation in each `FORMULAS` tuple. This is list element 6 because the title occupies index 0. |
| 197 | Formats all question/answer pairs as report subsections, including the three not shown in the short on-screen summary. |
| 198 | Formats all five visual explanations by unpacking each visual tuple. The report contains their text, not rendered chart images. |
| 199 | Adds full-source quality statistics and notes what those checks can establish. `.duplicated().sum()` counts repeated identical rows after the first copy; missing-cell sums are reduced across columns. |
| 200 | Numbers each investigation recommendation with `enumerate(..., 1)` and adds the caution that these are not already-proved decisions. |
| 201 | Adds limitations and explains tie selection, absent significance tests and insufficient-data caveats. It does not run any of those tests. |
| 202 | Adds reproduction/extension instructions as static text. The generic reference to adding a variable or experiment describes future work, not an implemented feature. |
| 203 | Closes the report-section list. |
| 204 | Appends a Markdown field dictionary to `report_parts[5]`. Because the title is element 0, element 5 is **KPI results**, while Definitions and methods is element 6. This explains the actual dictionary placement in the generated report. |
| 205 | Joins all sections with blank lines to create the single `full_report` string. |

### 8.9 Campaign dashboard: lines 207-218

| Line(s) | What the code does and why |
| --- | --- |
| 207 | Creates four tab containers and assigns them to variables by tuple unpacking. The names specify where later elements render. |
| 208 | Enters the Campaign dashboard tab's context. |
| 209 | Groups selected observations by date and sums spend and revenue. `as_index=False` keeps date as a normal column so Plotly can reference it by name. |
| 210 | Creates a Plotly line chart with date on x and spend/revenue as separate y series, labels the value axis INR and renders it at container width. |
| 211 | Renders visual-guide entry 0 below the daily chart. |
| 212 | Builds another channel summary, this time with channel kept as a normal column. This table is suited for Plotly's `x="channel"` argument and on-screen display. |
| 213 | Adds uppercase `ROAS` to that chart/table DataFrame by dividing group revenue by group spend, replacing zero denominators with NaN. It matches the lowercase `roas` logic in `channel_summary`. |
| 214 | Adds `CTR_pct` by dividing group clicks by group impressions and multiplying by 100. It is already in percentage units, unlike the earlier fractional `ctr` variable. |
| 215 | Creates and renders the channel bar chart: channel on x, aggregate ROAS on y, channel colors, and spend/conversion/CTR fields in hover details. |
| 216 | Renders guide entry 1, explaining channel return and scaling limits. |
| 217 | Displays the grouped `channels` table after rounding numeric display values to two decimals and hiding the pandas index. The original CSV is unaffected. |
| 218 | Explains that exact grouped values and group sizes should accompany interpretation and invites source-row inspection. |

### 8.10 Exploratory charts: lines 219-232

| Line(s) | What the code does and why |
| --- | --- |
| 219 | Enters the exploration tab's output context. |
| 220 | Allocates left and right layout columns for the histogram and boxplot. |
| 221 | Creates a Matplotlib figure and axes with a 7-by-4-inch base figure size, unpacking the two returned objects into `fig` and `ax`. |
| 222 | Draws a 20-bin histogram of per-observation spend with purple bars and white edges. It uses raw selected records, not the daily aggregate table. |
| 223 | Labels the figure so x is INR spend and y is observation count; the title identifies the daily-observation grain. |
| 224 | Displays the figure in the left container and then calls `plt.close(fig)` to release its Matplotlib registration. The semicolon separates two statements on the same source line. |
| 225 | Renders guide entry 2 in the same left container. |
| 226 | Creates a new figure and axes for the boxplot, keeping its drawing separate from the histogram. |
| 227 | Uses Seaborn to summarize per-observation conversions by channel, drawing onto the explicit axes with one fill color. |
| 228 | Sets the boxplot title. Seaborn already uses the selected source field names for axis labels. |
| 229 | Displays the boxplot in the right container and closes its Matplotlib figure handle to avoid accumulating figures across reruns. |
| 230 | Renders guide entry 3 below the boxplot in the right container. |
| 231 | Creates an interactive scatter plot from individual selected observations: spend on x, revenue on y, channel color, conversion-dependent marker size, and campaign/date hover details. No regression or causal model is fitted. |
| 232 | Renders guide entry 4 below the scatter plot. |

### 8.11 Data tables, learning prompts and report export: lines 234-256

| Line(s) | What the code does and why |
| --- | --- |
| 234 | Comment introducing data inspection and practice explaining results. |
| 235 | Enters the Data and quality tab's context. |
| 236 | Adds the source-field-dictionary heading. |
| 237 | Converts `FIELD_GUIDE.items()` key/value pairs into a two-column DataFrame and renders its definitions without a numeric row index. |
| 238 | Adds the filtered-records heading. |
| 239 | Explains that selected observations drive the analysis and that table sorting does not alter filters. Its generic phrase about derived columns is conditional; this app does not add ROAS/CTR columns to `filtered`. |
| 240 | Displays the selected eight-column source table, with dates parsed and the pandas index hidden. |
| 241 | Converts selected records to CSV text with `index=False` and creates a download named `filtered_marketing_campaigns.csv` with MIME type `text/csv`. This is not the grouped channel summary. |
| 242 | Adds the numeric-summary heading. |
| 243 | Explains the meaning of count, mean, standard deviation, minimum/maximum and quartiles before rendering descriptive statistics. |
| 244 | Selects numeric columns, calculates `.describe()`, rounds its displayed table to two decimals and renders it. Counts and INR amounts still require their different business units to be interpreted. |
| 245 | Adds the source-quality heading. |
| 246 | Displays row count, exact-duplicate count and missing-cell count for full `frame`, not just the selected rows. |
| 247 | Builds a quality DataFrame containing each column name, its dtype converted to a string, and its missing-value count. `.values` supplies arrays following source column order. |
| 249 | Opens the Workshop exercises and chart guide expander outside the tab contexts. |
| 250 | Displays four numbered practice prompts using newline-separated Markdown. These are text prompts, not automatically executed analysis. |
| 251 | Explains the distinct educational roles of Matplotlib, Seaborn and Plotly. |
| 252 | Reminds readers that observed associations in the fictional data do not prove cause and effect. |
| 254 | Enters the Full report tab's rendering context. |
| 255 | Offers the existing `full_report` string as `02_marketing_campaigns_report.md` with MIME type `text/markdown`. The browser download does not alter this explanation guide. |
| 256 | Renders that same string as Markdown in the tab, aligning visible and downloadable report contents. |

## 9. Validation, undefined rates and analytical limits

### 9.1 What the current loader guarantees

The code requires the named fields, at least one source observation, parseable dates, parseable numeric measures and nonmissing values in required analysis fields. File and expected parsing/schema problems are presented as Streamlit errors, followed by `st.stop()`. The sidebar separately guards incomplete intervals and empty selections.

These are useful prerequisites, but they are not a complete marketing-data audit. A number that parses is not necessarily a truthful or sensible number. A row can be structurally complete while being duplicated, incorrectly attributed or recorded in the wrong currency.

### 9.2 Checks not implemented

The app does not enforce nonnegative spend/revenue, nonnegative integer counts, finite numeric values, a unique observation key, or the funnel convention `conversions <= clicks <= impressions`. It also does not trim/normalize category labels or verify that all sources share one attribution window. Such checks may be appropriate for a real dataset, depending on its agreed event definitions, but they are not present merely because the interface shows a Source data quality tab.

Exact duplicate counts are reported, not automatically removed. An observation with the same date/channel/campaign but a changed amount is not an exact duplicate row and will not be identified by that count alone. Adding rows without checking their meaning can inflate sums even when no required value is missing.

A negative conversion count can pass numeric parsing and later cause problems because Plotly uses conversions as marker size. Infinite spend can also pass a simple numeric conversion and disrupt a histogram. The loading `try` block does not surround all later plotting and analysis. These examples explain why successful parsing is only an initial check.

### 9.3 Zero is not always a meaningful result

The scalar `ratio()` helper returns `0.0` when a denominator is zero. Thus the ROAS or conversion-rate display can show zero as a fallback for an undefined rate. The captions correctly ask the reader to inspect underlying counts before interpreting that value. CPA has a clearer special branch: when no conversions exist it displays `N/A` and its sentence explains why.

Grouped channel rates use another approach: zero spend or impressions are replaced with NaN before division. NaN represents a missing/undefined result, which can appear as a missing bar/table value. If at least one channel has a defined ROAS, the leader calculation can choose among those defined values. If **every** selected channel has zero spend, the entire `roas` column can be NaN. The current `.idxmax()` and later `.loc[best_channel, ...]` path does not guard this situation and may fail while constructing the leader sentence.

Zero conversions across all selected channels also make a volume leader uninformative: every group ties at zero. `.idxmax()` returns the first maximum encountered rather than proving that one channel is uniquely best. The app's report notes tie handling; investigate the grouped table before repeating an automatic leader label as a strong conclusion.

### 9.4 What the charts cannot establish

The input has no customer deduplication, first-acquisition flag, product margin, refunds, customer lifetime value, experiment assignment or controlled exposure information. The code calculates no confidence interval, significance test, forecast, budget-response curve or attribution model. It cannot derive those missing facts from a scatter plot or a high ROAS bar.

A small sample can have an extreme ratio; a large sample can still be biased. Date filters may mix complete and incomplete periods. Different campaign mixes can make channel comparisons unfair even though the aggregate arithmetic is correct. Revenue may be assigned to the date of a click, a purchase or another attribution rule; the CSV does not provide enough provenance to settle all those possibilities.

Useful reporting therefore names the population, formula and limit. For example: "Across the complete supplied teaching file, Display has approximately 4.00x attributed ROAS on INR 645,963.35 spend and 3,391 conversion events. These observations motivate an experiment; they do not prove that increasing Display spend would retain the same return."

## 10. Practice and worked examples

These examples are public learning material intended to make the reasoning visible. They extend or interpret the current code; any extension snippet below is explicitly separate from the existing implementation.

### Worked example 1: Show why a mean of percentages can mislead

Use the invented 10-click/5-conversion observation and 990-click/45-conversion observation from Section 4. Calculate both the simple average of their row rates and the ratio of their total conversions to total clicks.

**Reasoning:** The simple mean is about 27.27%, while the combined rate is 5%. The first observation receives far too much influence in the simple mean. In code, `filtered["conversions"].sum() / filtered["clicks"].sum()` preserves the denominator's exposure. A mean of a derived row-rate column would answer the average rate of an observation, not the overall rate across clicks.

### Worked example 2: Add a visible CTR metric

The source already computes `ctr` at line 159, but the top metric row has four cards and no CTR card. To display it as a separate element, a learner could add the following **extension** after `ctr` has been calculated:

```python
st.metric("Click-through rate", f"{ctr:.2%}")
```

**Reasoning:** `ctr` is already the aggregate fraction, so percentage formatting is sufficient. Placing this above its assignment would cause a name error. Multiplying `ctr` by 100 and then using `:.2%` would double-convert the units. If you redesign the top card row instead, account for when the needed variable is computed.

### Worked example 3: Export grouped channel results

The existing CSV download exports filtered observations. To export the exact channel summary as well, add this **extension** inside the dashboard after `channels` and its derived rate columns exist:

```python
st.download_button(
    "Download channel summary",
    channels.to_csv(index=False),
    "marketing_channel_summary.csv",
    "text/csv",
)
```

**Reasoning:** This uses the DataFrame that already contains grouped totals, `ROAS` and `CTR_pct`. It should not be confused with adding those rates to every source row. The exported summary has one row per selected channel, while the existing download has one row per selected observation. State that grain difference when sharing either file.

### Worked example 4: Investigate an unusually strong day

Select a channel and campaign, inspect the scatter plot for a high-revenue observation and note its date. Compare the selected totals with and without that observation in a separate analysis copy. Keep the reason for comparison explicit rather than deleting it merely because it is large.

**Reasoning:** One extreme observation may strongly affect a total or ratio, especially in a narrow selection. A sensitivity check asks whether a conclusion depends on that observation. It does not establish that the observation is invalid. The original app offers date-range filtering and row inspection but no built-in "remove this one observation" control. A custom exclusion should be identified as an extension, not described as an existing feature.

### Worked example 5: Compare scale with efficiency

Read the full-selection channel table. Display leads both ROAS and conversion volume in this bundled file. Then select one campaign label and a shorter interval and repeat the comparison.

**Reasoning:** The app's two `.idxmax()` calls answer different questions even when they happen to return the same label. Record the selected scope, spend and conversion count beside each ratio. If the ranking changes, investigate mix and sample size before claiming that the channel's underlying quality changed.

### Worked example 6: Explain why CPA is not yet customer acquisition cost

Suppose a real customer makes three attributed purchases. If each purchase is counted as a conversion, the denominator includes three events even though there is only one person.

**Reasoning:** Spend divided by conversion events can be a useful cost-per-outcome measure, but the app cannot count distinct new customers without customer identifiers and an acquisition definition. To calculate actual new-customer acquisition cost, the dataset and denominator would need to change. Renaming an existing field or adding a chart cannot recover an identity that was never recorded.

### Worked example 7: Distinguish this guide from the generated report

Change the channel filter, then download the full Markdown report. Compare its scope and KPI values with the previous selection.

**Reasoning:** `02_marketing_campaigns_report.md` is generated from current runtime selections. This `EXPLANATION.md` is a static guide to the source and method. Changing a filter changes the report's values; it does not rewrite the guide or modify the CSV. That separation lets the same teaching document support many different investigations.

## 11. Troubleshooting

| Symptom | Explanation and next check |
| --- | --- |
| A library is missing | Check which interpreter the terminal is using, activate the intended virtual environment and install the pinned dependencies with `python -m pip`. |
| `python app.py` does not open a usable app | Use `python -m streamlit run app.py`, which creates the required Streamlit runner and server context. |
| The dataset cannot be found | Keep `marketing_campaigns.csv` beside this script with the exact filename. The code resolves the script's neighbor, not a file elsewhere in the terminal's current directory. |
| A required column is missing | Inspect exact header names and capitalization. The code expects `conversions`, not an informal alternative such as `purchases`. |
| Parsing fails after editing the CSV | Check date validity and numeric fields for text/currency symbols or malformed values. The app deliberately raises instead of silently dropping bad records. |
| An incomplete-date notice appears | Select both dates; the code stops until a complete interval is available. |
| No observations match | Broaden dates or re-enable channel/campaign values. All conditions must be satisfied simultaneously. |
| Report figures change after a filter | That is the intended behavior. The report is reconstructed from the same newly selected rows as the charts. |
| CSV changes appear stale | Save the file and trigger a rerun. Reads are uncached, but a new execution is still necessary. |
| CPA displays `N/A` | The selected conversion count is zero. Cost per conversion is undefined, rather than free. |
| A zero rate looks suspicious | Inspect the denominator. Some scalar rates use a zero fallback even when mathematically undefined. |
| All-zero spend causes a leader lookup failure | All grouped ROAS values may be NaN. The current leader selection does not explicitly handle an entirely undefined ratio column. |
| The downloaded CSV has no ROAS field | The existing download exports filtered observations. ROAS belongs to the separate grouped channel summary table. |
| Histogram values do not match daily line-chart totals | The histogram uses observation spend, while the line chart sums observations by date. They intentionally have different grains. |
| Cards and report show different decimal places | Cards round some amounts to whole INR and rate percentages to one decimal; report values are often more precise. |
| A separate Cloud Lab instance cannot use 8501 | The built-in dashboard may already occupy it. Run and forward the documented separate-instance port 8502. |

## 12. Sources and further reading

The project-specific behavior, fields, formulas and example outputs are grounded in [this folder's `app.py`](app.py), [the supplied CSV](marketing_campaigns.csv), the [workshop README](../README.md) and the [repository README](../../README.md), inspected at the revision identified above. The library references below explain Python and API behavior. They do not substantiate claims about real marketing performance, and current documentation can describe a newer release than the pinned workshop environment.

- [Python `pathlib`](https://docs.python.org/3/library/pathlib.html): script-relative file paths and filename replacement.
- [Pandas table-oriented data introduction](https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/01_table_oriented.html): DataFrame and Series.
- [Pandas 2.2 ten-minute introduction](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html): selecting, manipulating and summarizing tabular data.
- [Pandas 2.2 GroupBy guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html): group aggregation and output structure.
- [Pandas indexing guide](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html): Boolean selection and `.loc` label lookups.
- [Streamlit run-your-app guide](https://docs.streamlit.io/develop/concepts/architecture/run-your-app): starting the server and executing the app.
- [Streamlit 1.50 tabs reference](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs): layout containers and execution of hidden-tab contents.
- [Streamlit download-button reference](https://docs.streamlit.io/develop/api-reference/widgets/st.download_button): offering CSV and text data for browser download.
- [Plotly Express overview](https://plotly.com/python/plotly-express/): DataFrame-driven chart construction.
- [Plotly scatter plots](https://plotly.com/python/line-and-scatter/): color, size and hover encodings.
- [Matplotlib histogram reference](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html): bins and observation counts.
- [Matplotlib `close`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.close.html): closing figures after display.
- [Seaborn boxplot reference](https://seaborn.pydata.org/generated/seaborn.boxplot.html): distribution summaries, quartiles and whiskers.
