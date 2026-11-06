# Customer Churn Explorer - business questions, analysis and code explained

This guide explains the **actual [app.py](app.py) in this folder**, using the accompanying [customer_churn.csv](customer_churn.csv). It is written for someone who can read a spreadsheet but is still learning Python, pandas and Streamlit.

The source examined is commit [c10a61c36fffdd048b69dd78926e6663bc986fce](https://github.com/cookieSensei/programming-and-ai/blob/c10a61c36fffdd048b69dd78926e6663bc986fce/business_analytics_workshop/03_customer_churn/app.py). Line numbers below refer to that version. The CSV contains **480 fictional customers**, not records from a real company. Numerical examples identified as bundled-data results were recalculated from that CSV with all regions and contracts selected. They change if you edit the data or filters.

## Contents

1. [The business problem and what a solution means](#1-the-business-problem-and-what-a-solution-means)
2. [Understand one row before calculating anything](#2-understand-one-row-before-calculating-anything)
3. [Why Python, pandas and the plotting libraries are used](#3-why-python-pandas-and-the-plotting-libraries-are-used)
4. [Questions, formulas and worked examples](#4-questions-formulas-and-worked-examples)
5. [How the analysis becomes a Streamlit app](#5-how-the-analysis-becomes-a-streamlit-app)
6. [Read every line of app.py](#6-read-every-line-of-apppy)
7. [How to read the five charts](#7-how-to-read-the-five-charts)
8. [Validation, assumptions and current limitations](#8-validation-assumptions-and-current-limitations)
9. [Run the project and reproduce the analysis](#9-run-the-project-and-reproduce-the-analysis)
10. [Practice, troubleshooting and useful next questions](#10-practice-troubleshooting-and-useful-next-questions)
11. [Source and reference links](#11-source-and-reference-links)

## 1. The business problem and what a solution means

Imagine a subscription business whose manager knows that some customers have left. A single total does not tell the manager whether churn is concentrated among monthly contracts, customers in one region, new subscribers or customers reporting low satisfaction. Looking down hundreds of spreadsheet rows makes these patterns difficult to see consistently.

The project turns a customer snapshot into a repeatable investigation. A manager chooses a region and contract group, sees the size of that population, compares its churn proportion with other groups, and examines the customers behind the summary. The result supports questions for customer interviews, support-history review and retention experiments.

Here, **churn** means a customer has been marked as having left; **retained** means the customer has not been marked as having left in this snapshot. The dataset does not say when someone joined, when someone left, or the common period over which churn was measured. Consequently, the app answers “What share of these selected records is marked churned?” It cannot answer “What percentage of active customers did we lose this month?”

### The questions are different, so their calculations are different

| Business question | Data operation in this app | Result to inspect | Why this operation fits |
| --- | --- | --- | --- |
| How many customers are represented? | `len(filtered)` | Customer KPI | Each valid row is intended to represent one customer; counting rows measures the analysis population. |
| What share is marked churned? | `filtered["churned"].mean()` | Snapshot churn KPI | With binary values, averaging 0s and 1s is the same as dividing churned customers by all selected customers. |
| Which contracts have higher observed churn? | `groupby("contract").agg(..., churn_rate=("churned", "mean"))` | Contract bar chart and table | The same proportion is calculated separately inside each contract group. |
| How do customer profiles differ by churn status? | Status grouping, medians and distribution plots | Satisfaction boxes, tenure histograms and report | Medians and distributions show the center and spread rather than reducing each group to one total. |
| Where are differences hidden inside contract averages? | Contract-region pivot table | Churn heatmap | Dividing each contract into regions exposes combined segments that an overall average can hide. |
| How much listed monthly fee belongs to churned customers? | Boolean selection, then fee sum | Fee KPI and report question | Only records marked 1 contribute to this descriptive total. |
| Are the compared groups large enough to interpret carefully? | Group sizes and `segment_counts` | Table in the Full report tab | A percentage computed from a few people is much easier to move than one computed from many people. |

A useful analyst conclusion is: “In this fictional snapshot, monthly-contract customers have a higher observed churn proportion; investigate their experience and compare other characteristics.” An unsupported conclusion is: “Monthly contracts cause churn, so forcing everyone onto annual contracts will prevent it.” The app measures an association. It does not run a controlled experiment, estimate a treatment effect or train a prediction model.

The practical product is therefore a **decision-support dashboard**: a transparent way to find questions worth investigating, verify them against rows and share the analysis. The downloaded report is part of that communication, not a substitute for additional evidence.

## 2. Understand one row before calculating anything

The **grain** of a table is what one row represents. Here the grain is one synthetic customer in one snapshot. The bundled data has 480 distinct customer IDs and 480 rows. A customer is not an order, a support ticket or a monthly billing event.

Grain determines valid arithmetic. Summing monthly fees across customers gives a total of their listed monthly charges. Counting rows gives customers only while the intended one-customer-per-row rule holds. If you later append another snapshot of the same customers, blindly counting the combined rows would count customer observations, not unique people.

### Source field dictionary

| Column | Meaning and unit | How this app uses it | What to avoid assuming |
| --- | --- | --- | --- |
| `customer_id` | Synthetic identifier such as `CUST-0001` | Scatter hover and record inspection | The label contains no predictive information or actual personal identity. |
| `region` | Customer region: East, North, South or West in the bundled file | Sidebar filter and heatmap columns | Region totals are not normalized by a real market's population. |
| `contract` | Annual, Monthly or Two year | Sidebar filter, grouping and heatmap rows | A longer contract is not proved to prevent churn. |
| `tenure_months` | Recorded subscription tenure, in months | Scatter x-axis, histogram and status medians | There is no start date or cancellation date to reconstruct a timeline. |
| `monthly_fee` | Listed monthly charge, in INR | Scatter y-axis and fee total for churned records | It is not lifetime value, profit or measured revenue lost. |
| `support_tickets` | Recorded ticket count | Data table, numeric summary and an extension exercise | Ticket counts do not have a common documented exposure period. |
| `satisfaction_score` | Recorded score on the intended 1-10 scale | Mean, medians, boxplot and scatter hover | The measurement may precede or follow churn; timing is unknown. |
| `churned` | Intended binary flag: 0 retained, 1 churned | Counts, proportions, status labels and segment heatmap | Other numbers would break the business meaning even if Python could read them. |

The only added column is `status`. The app derives it from `churned` using `{0: "Retained", 1: "Churned"}`. It provides readable chart labels without changing the underlying binary field.

### Read a few actual rows

These are the first five records in the bundled file, with selected fields shown:

| Customer | Region | Contract | Tenure, months | Monthly fee, INR | Satisfaction | Churned |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| CUST-0001 | East | Two year | 13 | 799 | 8 | 0 |
| CUST-0002 | South | Monthly | 27 | 499 | 7 | 1 |
| CUST-0003 | West | Annual | 49 | 499 | 7 | 0 |
| CUST-0004 | North | Two year | 12 | 999 | 9 | 0 |
| CUST-0005 | South | Monthly | 54 | 499 | 7 | 0 |

Notice that the second and fifth customers have the same contract and monthly fee but different churn flags. A group-level pattern is not a rule that every individual follows.

There is no date column. The absence of a date filter is deliberate. There is also no upload control: `app.py` reads the named CSV beside the script. To experiment with other records, edit a copy of that file while preserving its expected columns and meaning.

## 3. Why Python, pandas and the plotting libraries are used

### Separate the jobs

| Component | Responsibility in this project | Concrete example |
| --- | --- | --- |
| Python | Execution, variables, functions, loops, conditions and strings | Stop when the selected table is empty; build report sentences with calculated values. |
| `pathlib.Path` | Locate a file reliably | Find `customer_churn.csv` beside `app.py` even when the terminal starts elsewhere. |
| pandas, imported as `pd` | Read, validate, filter, group and summarize tabular data | Calculate churn means separately for each contract. |
| Streamlit, imported as `st` | Browser interface and interaction | Show multiselect filters, metric cards, tabs and download buttons. |
| Plotly Express, imported as `px` | Interactive charts | Inspect a customer's contract and satisfaction through scatter-plot hover. |
| Matplotlib, imported as `plt` | Explicit figure and axes control | Draw two tenure histograms on the same axes with matching bins. |
| Seaborn, imported as `sns` | Statistical plotting on Matplotlib axes | Compare satisfaction distributions with a boxplot and segment rates with a heatmap. |

Pandas does not turn the code into a website. Streamlit does not decide what churn means. The plotting libraries do not automatically prove a business conclusion. Each component has a separate role, and the application combines them.

### What a DataFrame is

A pandas **DataFrame** is a table with named columns and an index identifying row positions or labels. `pd.read_csv(DATA_FILE)` constructs that table from the CSV. The variable `frame` holds the source table; `filtered` holds the currently selected subset.

Compare these operations:

```python
frame["churned"]                  # One column: a pandas Series
frame[["contract", "churned"]]     # Two columns: a DataFrame
frame["region"] == "East"         # One True/False answer per row
frame[frame["region"] == "East"]   # Keep only the rows whose answer is True
```

A **Series** is one labeled column. It has methods such as `sum()` and `mean()`. The double brackets in the second expression are not decorative: the inner list says which columns to select, and the outer brackets perform that selection.

### Why pandas is helpful here

Without pandas, you could read each CSV row manually, convert number strings, maintain separate counters for contracts and regions, and calculate every average yourself. That is possible but introduces repeated bookkeeping. Pandas expresses the operation at the level of the business question: select these customers, split them by contract, and summarize each group.

For example:

```python
contract_summary = filtered.groupby("contract").agg(
    customers=("churned", "size"),
    churn_rate=("churned", "mean"),
)
```

Read this as three steps:

1. Take the selected customer rows.
2. Split them into groups sharing the same contract.
3. For each group, count rows into `customers` and average the binary flag into `churn_rate`.

The named aggregations make the output readable. `("churned", "mean")` identifies the input column and operation; `churn_rate=` names the resulting column. The summary has one row per contract, not one row per customer.

Vectorized expressions apply an operation to all rows together. `filtered["churned"] == 1` returns a Boolean Series rather than a single Boolean. Using that Series inside `.loc[...]` selects the corresponding rows without writing an explicit loop.

Pandas also keeps indexes aligned during many operations. After filtering, original row labels may have gaps. That is normal and does not mean rows were secretly renumbered or customers disappeared incorrectly. `len(filtered)` counts the actual remaining rows.

### Small Python syntax choices that matter

- `=` assigns a value; `==` compares values. `churned = ...` creates a variable, while `filtered["churned"] == 1` produces a mask.
- `.` accesses a method or property. `.mean()` calls a method; `.empty` reads a property.
- `[...]` selects, indexes or defines a list depending on context. `insights[:3]` takes the first three entries; it does not include entry at index 3.
- A colon and indentation start a block after `if`, `for`, `with`, `try` or `def`.
- `f"..."` is a formatted string. Expressions inside braces are evaluated when that statement runs.
- `:.1%` formats a proportion as a percentage with one decimal place. `0.20625` becomes `20.6%`; the stored number remains `0.20625`.
- `:,.0f` shows grouping commas and no decimals. This changes the display, not the underlying calculation.
- `.join(...)` combines strings with a chosen separator. `"; ".join(parts)` makes one sentence from several pieces.

These foundations explain most of the apparently complicated one-line expressions later in the script. The [pandas introductory guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html) and [grouping guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html) provide the API background.

## 4. Questions, formulas and worked examples

### A. How many customers and how much churn?

The customer count is:

```python
customers = len(filtered)
```

The churned count is:

```python
churned = filtered["churned"].sum()
```

When every value is 0 or 1, each 1 contributes one customer and each 0 contributes nothing. Thus:

**Snapshot churn proportion = churned customers / selected customers.**

The actual KPI uses `filtered["churned"].mean()`. For binary values, the arithmetic mean is exactly the same calculation:

```text
mean(churned) = sum(churned flags) / number of flags
```

For the five CSV records shown earlier, the flags are 0, 1, 0, 0, 0. Their sum is 1, their count is 5, and their mean is 0.2, displayed as 20%. This example uses the first five CSV records for hand calculation; the app has no “first five” filter.

For the complete bundled dataset:

| Measure | Recalculated result |
| --- | ---: |
| Selected customers | 480 |
| Customers marked churned | 99 |
| Customers marked retained | 381 |
| Snapshot churn proportion | 99 / 480 = 0.20625 |
| Snapshot churn percentage | 20.625% |
| Card display with one decimal place | 20.6% |
| Report percentage with two decimal places | 20.62% |

The two-decimal display follows Python's floating-point formatting; it is not a second, different measure. Keep the unrounded proportion for calculation and treat display rounding as presentation.

### B. Why compare groups using rates and counts?

For the complete file, the contract summaries are:

| Contract | Customers | Churned | Snapshot churn percentage |
| --- | ---: | ---: | ---: |
| Annual | 167 | 29 | 17.3653% |
| Monthly | 159 | 53 | 33.3333% |
| Two year | 154 | 17 | 11.0390% |

The mean of the raw binary flags within each group answers “What share of this group's customers churned?” The accompanying count tells you the denominator.

Do not average the three displayed percentages and assume the result is the overall rate. Their denominators differ. The overall rate is:

```text
(29 + 53 + 17) / (167 + 159 + 154)
= 99 / 480
= 20.625%
```

The app calculates the overall mean directly from customer rows, so every customer has equal weight. It does not give each contract equal weight.

If one fictional segment had 1 churned customer out of 2 and another had 100 out of 1,000, their rates would be 50% and 10%. The first percentage is higher, but changing the status of one person changes it by 50 percentage points. This invented example illustrates why the app keeps sample sizes visible.

### C. Why mean satisfaction and median satisfaction both appear

Average satisfaction uses:

```python
filtered["satisfaction_score"].mean()
```

The first five CSV scores are 8, 7, 7, 9 and 7. Their total is 38, so the mean is 38 / 5 = 7.6.

The complete file's mean is **6.8625**, shown on the KPI card as **6.9 / 10**. A mean summarizes the score across selected customers, but it does not describe every customer's experience. A group can contain very satisfied and very dissatisfied customers while still having a moderate mean.

The report also computes status medians:

| Status | Customers | Median satisfaction | Median tenure |
| --- | ---: | ---: | ---: |
| Churned | 99 | 6.0 / 10 | 31.0 months |
| Retained | 381 | 7.0 / 10 | 32.0 months |

A median is the middle value after sorting. It is less affected by extreme values than a mean. The boxplot shows additional spread around that center. Neither statistic establishes whether dissatisfaction caused churn.

### D. What “churned monthly fees” actually adds

The important expression is:

```python
filtered.loc[filtered["churned"] == 1, "monthly_fee"].sum()
```

Read it from the inside out:

1. `filtered["churned"] == 1` identifies the churned rows.
2. `.loc[mask, "monthly_fee"]` selects their fees.
3. `.sum()` adds those selected values.

For the first five records, only CUST-0002 contributes, so the result is INR 499. Across the complete file, the total is **INR 84,101**.

That does not establish that INR 84,101 was lost during a particular month. There is no cancellation timing, billing history, refund history or counterfactual revenue. The label describes the association between customer status and listed fees, not an accounting measure.

### E. Why a pivot table answers a more detailed question

```python
segments = filtered.pivot_table(
    index="contract",
    columns="region",
    values="churned",
    aggfunc="mean",
) * 100
```

The row axis is contract; the column axis is region. Within each contract-region cell, pandas calculates the average of the binary flag, then the code multiplies by 100 for percentage units.

The complete-file Monthly/North cell is **10 / 23 = 43.4783%**. Monthly/East is **17 / 42 = 40.4762%**. Their similar colors do not mean equally stable estimates: the denominators differ.

The app separately calculates `segment_counts` with `groupby(["contract", "region"]).size()`. The complete file has 12 observed cells, the smallest contains 23 customers, and none contains fewer than 20. The number 20 is an illustrative caution threshold. It is not a significance test, a confidence level or a guarantee of representativeness.

## 5. How the analysis becomes a Streamlit app

### From a calculation to a usable interface

A basic script could read the CSV and print the contract table to the terminal. This app keeps that analytical core and adds browser controls and displays:

1. Load the data and stop if required input cannot be analyzed.
2. Create sidebar widgets whose return values are selected regions and contracts.
3. Filter the DataFrame using those selections.
4. Calculate KPIs, summaries, report text and chart data from the same `filtered` table.
5. Render those results with `st.metric`, `st.dataframe`, `st.plotly_chart` and `st.pyplot`.
6. Offer CSV and Markdown downloads for the current selection.

The program does not require handwritten HTML, a separate React frontend or API routes. Streamlit runs the Python script on its server process and provides the browser interface. The official [run-an-app guide](https://docs.streamlit.io/develop/concepts/architecture/run-your-app) explains the launch model.

### The rerun model explains the interactivity

In the workshop's Streamlit 1.50 setup, changing a widget normally causes the script to rerun from top to bottom. A multiselect is both a displayed control and a function returning a Python list. On a rerun, that list reflects the selection held by the widget.

The script then rebuilds `filtered`, recalculates the metrics, and reconstructs the report. `st.stop()` ends the current script run when a guard fails; it does not shut down the Streamlit server, so the user can correct the selection and trigger another run. There is no separate “apply filters” button because the selected values already drive the calculation.

The widget `key` values give controls stable identities. They do not refer to columns, create a database or modify the CSV. The app does not explicitly use `st.session_state`, callbacks or forms.

The CSV read is intentionally **uncached**. There is no `@st.cache_data` decorator. A new run rereads the file, so a saved CSV edit is seen when the app reruns. Saving the CSV is not itself guaranteed to trigger a rerun; use the app's rerun control or change a widget after saving.

### Containers organize output, not different analyses

`with st.expander(...):` sends its indented display calls into an expandable section. `with overview:` sends calls into the first tab. `left.pyplot(fig)` displays a figure in the left column.

The four tabs are:

- **Retention dashboard:** contract rates and customer scatter plot.
- **Explore the data:** tenure distributions, satisfaction boxes and the combined-segment heatmap.
- **Data and quality:** selected records, a CSV download, summaries and source checks.
- **Full report:** generated Markdown, its download, and the separate segment sample-size table.

For [Streamlit 1.50 tabs](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs), all tab content is computed, including content in tabs not currently selected. Clicking a different tab is a layout choice; it is not a rule that only that tab's Python block will execute.

### A static teaching guide and a generated report have different jobs

This file explains the source and reasoning. It is not rebuilt when a filter changes. The app's `full_report` is a string rebuilt during each run from the current data selection. Its twelve sections combine explanatory constants with calculated results and analysis scope.

The filtered CSV includes the selected source columns plus the derived `status` column. The report downloads as `03_customer_churn_report.md`. Neither download changes the source CSV or saves an updated app to the repository.

A current implementation detail matters: the **contract-region sample-size table is displayed after the Markdown report in the tab**. It is not appended to `full_report`, so the Markdown download includes the segment-count summary sentence but not the complete count table. Inspect or copy that table separately when interpreting individual heatmap cells.

## 6. Read every line of app.py

Open [app.py](app.py) beside this guide and enable editor line numbers. Every nonblank source line is covered below. Ranges group only closely related literal continuations or explicitly described statements. Blank lines separate ideas visually and do not perform calculations. Code fragments in the tables identify the relevant expression; the source file remains the full executable program.

### Lines 1-13: imports and page identity

| Line(s) | What the line does and why |
| --- | --- |
| 1 | The opening triple-quoted string is the module docstring. It describes the project for readers and inspection tools; it does not draw browser text. |
| 2 | `from pathlib import Path` imports a file-path class from Python's standard library. The app later uses it to locate its CSV relative to the script. |
| 4 | `import matplotlib.pyplot as plt` imports figure/axes plotting tools under a short alias used for histograms and figure cleanup. |
| 5 | `import pandas as pd` imports table-processing tools. `pd` is an alias, not a separate package or a special Python keyword. |
| 6 | `import plotly.express as px` imports Plotly's concise chart-building interface. It creates the interactive bar and scatter figures. |
| 7 | `import seaborn as sns` imports statistical plotting functions for the satisfaction boxplot and churn heatmap. |
| 8 | `import streamlit as st` imports the functions that build browser controls and display results. |
| 10 | `st.set_page_config(...)` sets the browser page title, chart icon and wide layout before the main interface is rendered. These arguments affect presentation, not data. |
| 11 | `st.title(...)` writes the large visible page heading. This is separate from the browser title set on line 10. |
| 12 | `st.caption(...)` places the workshop context, fictional-data reminder and INR unit in smaller text. |
| 13 | `st.write(...)` gives the reader the task and explicitly identifies the work as descriptive analysis rather than prediction. |

### Lines 15-76: business explanations stored as data

These are ordinary Python strings, tuples and lists. They centralize explanations so the charts and report can reuse them. Adjacent quoted strings inside parentheses are concatenated by Python; wrapping the source across lines improves readability without creating a list of separate paragraphs.

| Line(s) | What the line does and why |
| --- | --- |
| 15 | A comment introduces the case-study definitions. Python ignores the comment during execution. |
| 16-17 | `CASE` stores the problem: an overall churn figure hides differences between customer groups. The second string continues the same sentence. |
| 18-19 | `DECISION` stores the intended use: prioritize research and retention experiments while respecting sample-size and causal limits. |
| 20-22 | `DATA_CONTEXT` defines one row, the 480-customer snapshot, the 0/1 meaning and the missing observation window. |
| 23 | Starts `FORMULAS` with the customer-count definition. Each entry is a three-item tuple: name, calculation description and business meaning. |
| 24-26 | Adds the snapshot churn formula and states that it is not a monthly or annual rate. |
| 27-29 | Adds the mean-satisfaction formula and its intended 1-10 scale. |
| 30-32 | Adds the churned-fee formula and its limitation; closes the formula list. These text definitions describe the computations performed later. |
| 33-39 | Adds the contract-bar entry to `VISUAL_GUIDE`: title, purpose, axis reading, question and causal caution. |
| 40-46 | Adds the tenure-versus-fee scatter guide, including one-point-per-customer grain, status color and overlap limitation. |
| 47-53 | Adds the tenure-histogram guide: shared 12 bins across 0-60 months, count heights and the unequal-group-size caution. |
| 54-60 | Adds the satisfaction-boxplot guide, including median, middle 50%, whiskers and unknown measurement timing. |
| 61-67 | Adds the contract-region heatmap guide: percentage cells, fixed color scale, missing combinations and sample-size caution; closes the visual list. |
| 68-69 | Begins `RECOMMENDATIONS` with interviews and support-history review before contract-policy changes. |
| 70-71 | Adds the recommendation to show denominators and investigate small groups. |
| 72-73 | Adds collection of dates and pre-churn measurements plus a controlled experiment; closes the recommendation list. |
| 74-76 | `LIMITATIONS` records unavailable time-based, causal and predictive conclusions and qualifies the illustrative 20-customer threshold. |

### Lines 78-102: display context and define a reusable chart explainer

| Line(s) | What the line does and why |
| --- | --- |
| 78 | Opens an expander, initially expanded. The indented calls below appear inside it. `with` establishes the display container. |
| 79 | Combines a bold Markdown label with `CASE` and displays the business problem. |
| 80 | Displays `DECISION` under the decision label. |
| 81 | Displays `DATA_CONTEXT` so readers know what the observations represent before interpreting results. |
| 82 | Renders an information callout identifying the data as fictional and the results as calculated from selected rows. |
| 83 | Gives a suggested reading sequence and explains that filters update findings and report. |
| 86 | Starts `FIELD_GUIDE`, a dictionary mapping exact CSV column names to descriptions, with `customer_id`. |
| 87 | Describes `region`. The dictionary key must match the CSV name to be useful as documentation. |
| 88 | Describes `contract`. |
| 89 | Describes `tenure_months` and its month unit. |
| 90 | Describes `monthly_fee` as a monthly charge rather than lifetime revenue. |
| 91 | Describes `support_tickets` and the missing common measurement window. |
| 92 | Describes the intended satisfaction scale and direction. |
| 93-94 | Describes the binary churn flag and missing monthly observation window, then closes the dictionary. |
| 96 | Defines `explain_visual(index, container=st)`. It runs when called later; `container` defaults to the main Streamlit context but can be a column. |
| 97 | Selects one tuple from `VISUAL_GUIDE` and unpacks its five fields into five variable names. List indexes begin at 0. |
| 98 | Displays the visual title in bold using an f-string. |
| 99 | Writes the purpose in the chosen container. |
| 100 | Displays the reading instructions with a Markdown label. |
| 101 | Displays the business question the chart answers. |
| 102 | Uses a caption for the interpretation limitation. Reusing this helper keeps each chart paired with the appropriate explanation. |

### Lines 104-126: load data, validate structure and define a helper

| Line(s) | What the line does and why |
| --- | --- |
| 104 | Comment explains the file-location strategy. |
| 105 | Comment explains the deliberate lack of caching so a later rerun reads students' saved CSV edits. |
| 106 | `Path(__file__).resolve().with_name("customer_churn.csv")` starts from this script's path, resolves it and substitutes the CSV filename in the same directory. |
| 107 | Starts a `try` block. Expected file/data errors inside it will be handled by the matching `except`. |
| 108 | `pd.read_csv(DATA_FILE)` parses the CSV into `frame`. CSV text is converted to a DataFrame with inferred column types. |
| 109 | Comment records that the snapshot has no date filter. It does not add a date or remove one. |
| 110 | Lists the five columns that must be explicitly converted to numbers. |
| 111 | Lists all eight required input columns. Extra columns are allowed; this is not an exact-column equality test. |
| 112 | Converts required names to a set and checks they are all present in `frame.columns`. `not` enters the error branch when at least one is absent. |
| 113 | Raises `ValueError` with a useful message. Execution leaves the normal loading path and reaches the handler. |
| 114 | Tests whether the DataFrame contains no rows. Having headers alone is insufficient for analysis. |
| 115 | Raises a descriptive error for an empty CSV table. |
| 116 | Loops over the numeric column names one at a time. |
| 117 | Converts that column with `pd.to_numeric(..., errors="raise")` and stores it back. Unparseable text is rejected rather than silently replaced with missing values. |
| 118 | Selects required columns, marks missing cells, reduces each column with `any()`, then reduces those results again. The final Boolean asks whether any required cell is missing. |
| 119 | Raises an error if that check found missing data. The app does not silently drop these customer rows. |
| 120 | Catches the listed file, value and key errors raised inside the loading block and binds the exception to `error`. It does not catch every possible error later in the app. |
| 121 | Shows the filename and error message in the browser. `DATA_FILE.name` supplies only the filename. |
| 122 | `st.stop()` halts this run so no KPIs are computed from unavailable or invalid required input. |
| 124 | Defines the function `ratio(numerator, denominator)`. |
| 125 | Its docstring describes the zero-denominator fallback. |
| 126 | A conditional expression divides when the denominator is truthy and returns `0.0` when it is zero. **This helper is not called anywhere in this churn app.** Its presence does not mean it controls the churn KPI; the KPI uses `mean()`. |

### Lines 128-138: filter the customer population

| Line(s) | What the line does and why |
| --- | --- |
| 128 | Comment marks the filter stage, which must precede calculations to keep selected outputs consistent. |
| 129 | Adds the sidebar heading. |
| 130 | Starts `filtered` as a copy of `frame`. Later derived columns belong to the selected working table, while source-quality checks retain access to `frame`. |
| 131 | Gets unique source regions, sorts them, shows a multiselect with every region selected initially, and stores its returned list in `selected_region`. The key identifies this widget. |
| 132 | `.isin(selected_region)` builds a row mask; the outer brackets keep rows whose region appears in the chosen list. |
| 133 | Builds the contract multiselect from all source contracts, initially selecting all, with its own widget key. Options come from `frame` rather than only the already-filtered regions. |
| 134 | Keeps the remaining rows whose contract is selected. Applying both masks sequentially means region AND contract conditions must hold. |
| 135 | Shows selected and source row counts with thousands separators. |
| 136 | Checks whether the selection left no rows. |
| 137 | Displays a helpful empty-state message. Its generic “widen the date range” wording is reused from other apps; this project has no date control. Restore a region or contract instead. |
| 138 | Stops the run before means, rankings and plots are attempted on an empty selection. |

### Lines 140-162: derive labels, calculate metrics and compose answers

| Line(s) | What the line does and why |
| --- | --- |
| 140 | Comment starts business calculations. |
| 141 | Maps 0 and 1 to readable status strings in a new `status` column. A value outside this mapping would become missing, a reason binary validation matters. |
| 142 | Sums the raw binary flags into the churned count. This relies on valid 0/1 input. |
| 143 | Creates four side-by-side metric containers and stores them in `columns`. |
| 144 | Displays the selected row count in the first card. `columns[0]` refers to the first container. |
| 145 | Displays mean churn flag as a percentage with one decimal place. Percentage formatting supplies the factor of 100 for presentation. |
| 146 | Displays average satisfaction to one decimal place and adds the scale label. |
| 147 | Selects fees where the flag equals 1, adds them, and displays INR with no decimals. |
| 148 | States the snapshot grain and fee-interpretation limits beside the metrics. |
| 149 | Groups by contract and creates named customer-count and mean-churn columns. Contract labels become the summary index by default. |
| 150 | `idxmax()` returns the contract label at the largest churn rate, not the numerical rate itself. Ties select the first occurrence in the grouped result. |
| 151 | Groups by readable status and computes customer counts, median satisfaction and median tenure for each observed status. |
| 152 | Iterates through those summary rows, formats one sentence per status and joins them with semicolons. `int` prevents a count being presented as a decimal. |
| 153 | Groups by the pair of contract and region, counting observations in each observed cell. The result is a Series with a two-level index. |
| 154 | Starts `insights`, a list of question-and-answer tuples. |
| 155 | Builds the observed-churn answer from the selected count, churn sum and mean, while restating the time-window limit. |
| 156 | Uses the top contract label to look up its rate and count through `.loc`. The wording describes a research segment rather than a cause. |
| 157 | Reuses `status_details` and adds the warning that one observed status cannot support a between-status comparison. There is no dedicated status filter, but a region-contract subset could contain only one status. |
| 158 | Formats the selected churned-fee total to two decimals and explains why it is not recognized lost revenue. |
| 159 | Counts observed cells, finds the smallest size, counts cells below 20 and qualifies the threshold as illustrative. Unobserved combinations are not counted as zero-sized observed cells. |
| 160 | Adds a concise statement of what the dashboard has and has not answered. |
| 161 | Closes the insight list. |
| 162 | Builds the report KPI list. It includes customers, churned customers, churn percentage and satisfaction. It does **not** include the fee KPI in this table; fees appear in the question-and-answer section instead. |

### Lines 164-180: document the scope and show initial findings

| Line(s) | What the line does and why |
| --- | --- |
| 164 | Comment explains that report and charts should share the same selected DataFrame. |
| 165 | Starts an empty list of scope-description strings. |
| 166 | Loops through source columns with object dtype, which in the bundled file includes IDs, regions and contracts. |
| 167 | Keeps only source columns with at most 12 distinct values for the short scope summary. This normally includes region and contract, not 480 customer IDs. |
| 168 | Builds a readable column label, joins the distinct selected values and appends that description. Underscores are replaced only in displayed labels, not in the DataFrame's column names. |
| 169 | Loops through source datetime columns if any exist. None exist in the bundled churn dataset, so its body does not execute here. |
| 170 | For such a column, it would append the earliest and latest selected observed dates. The generic scaffold does not convert text dates into datetime columns by itself. |
| 171 | Joins scope parts into one semicolon-separated string. |
| 173 | Opens the KPI-definition expander. |
| 174 | Converts `FORMULAS` to a three-column DataFrame and displays it without the index, using the available width. |
| 175 | Adds a generic explanation of ratios and zero-denominator fallbacks. The current churn percentage does not call `ratio()`, and empty selections have already stopped. |
| 177 | Displays the findings section heading. |
| 178 | Iterates over the first three question-and-answer pairs. |
| 179 | Displays each question in bold followed by its calculated answer. |
| 180 | Displays row counts and the scope string so readers know which customers the results describe. |

### Lines 182-198: build the downloadable Markdown report

| Line(s) | What the line does and why |
| --- | --- |
| 182 | Starts a list containing separate Markdown sections. Keeping sections as strings makes their final order explicit. |
| 183 | Creates the report's top-level heading. |
| 184 | Adds section 1 from `CASE`. `\n` inserts an actual line break in the string. |
| 185 | Adds section 2 from `DECISION` and `DATA_CONTEXT`, separated by a blank line. |
| 186 | Adds section 3 with the actual filename, selected/source counts, scope and fictional-data/interpretation limits. |
| 187 | Adds section 4 by extracting the answers from the first three insight tuples. The underscore variable ignores the question in this generator expression. |
| 188 | Adds section 5, a Markdown table built from `kpi_values`. Each generated row contains a label and formatted result. |
| 189 | Adds section 6, a methods table generated from the three fields of each `FORMULAS` tuple. |
| 190 | Adds section 7 with every insight question as a subheading and its answer underneath. This includes answers omitted from the short on-page preview. |
| 191 | Adds section 8 by unpacking all five fields of each visual-guide tuple and formatting purpose, reading, question and caution. It includes explanatory text, not embedded chart images. |
| 192 | Adds section 9 with whole-source duplicate and missing-cell counts. It explains checks and makes clear they do not prove representativeness or accuracy. |
| 193 | Adds section 10 by numbering the recommendation list from 1 with `enumerate(..., 1)` and stating that these are investigations. |
| 194 | Adds section 11 with limitations and generic ranking/statistical cautions. The source performs no confidence-interval, significance-test or correlation calculation for this project. |
| 195 | Adds section 12 with reproduction and extension instructions. Some wording about periods and correlation is shared with other workshop apps; this snapshot still has no date analysis. |
| 196 | Closes the section list. |
| 197 | Appends a source dictionary table to `report_parts[5]`. Index 5 is the sixth list entry: the KPI results section, because index 0 is the report title; `+=` extends that string. |
| 198 | Joins all sections with blank lines to create the single `full_report` Markdown string used by both display and download. |

### Lines 200-229: render all five visualizations

| Line(s) | What the line does and why |
| --- | --- |
| 200 | Creates four tabs and unpacks their container objects into names used by later `with` blocks. |
| 201 | Directs the following output into the retention dashboard tab. |
| 202 | Recreates the contract summary with `as_index=False` so contract is a normal column that Plotly can address by name. |
| 203 | Converts the proportion column to percentage numbers for the chart's numeric y-axis. Unlike an f-string percentage, this is an actual multiplication. |
| 204 | Builds the Plotly contract bar chart from summarized rows. Height is churn percentage; color identifies contract; hover includes customer count. `st.plotly_chart` places the figure in the app. |
| 205 | Prints explanation entry 0, matching the contract chart. |
| 206 | Builds a scatter from individual customer rows: tenure on x, monthly fee on y, status color, selected hover fields and opacity 0.65 to make overlap somewhat easier to see. |
| 207 | Prints visual-guide entry 1 for the scatter. |
| 208 | Displays contract, customer count and percentage as an exact table rounded to two decimals for presentation. |
| 209 | Explains why group counts should accompany totals and rates. |
| 210 | Directs subsequent output into the exploration tab. |
| 211 | Creates left and right columns for two charts. |
| 212 | Creates a Matplotlib Figure and Axes, 7 by 4 inches. The Figure is the canvas; the Axes is the plotting region. |
| 213 | Iterates over each observed status and its customer subset. |
| 214 | Adds that group's tenure histogram to the same axes, with 12 bins across 0-60, transparency 0.6 and a legend label. The heights are counts, not normalized proportions. |
| 215 | Sets histogram title and labeled units. |
| 216 | Displays the legend distinguishing the groups. |
| 217 | Shows the figure in the left column, then closes its Matplotlib handle. The semicolon separates two statements; cleanup reduces accumulation across reruns. |
| 218 | Adds the tenure-histogram explanation below the left chart. |
| 219 | Creates a separate figure/axes pair for the satisfaction plot. |
| 220 | Draws a Seaborn satisfaction boxplot grouped by status on the supplied axes, with a chosen fill color. |
| 221 | Sets its title. |
| 222 | Renders the boxplot on the right, then closes the figure. |
| 223 | Adds the matching explanation in the right column. |
| 224 | Builds the contract-region table of mean churn flags and multiplies by 100. This is the matrix passed to the heatmap. |
| 225 | Creates a wider 9-by-4-inch figure for that matrix. |
| 226 | Draws the heatmap, writes one-decimal values in cells and fixes the color scale to 0-100. Missing combinations remain missing rather than being treated as 0% churn. |
| 227 | Adds a descriptive title. |
| 228 | Displays the heatmap in the main tab area and closes its figure. |
| 229 | Prints the final visual explanation, including the sample-size caution. |

### Lines 231-255: inspection, downloads and learning prompts

| Line(s) | What the line does and why |
| --- | --- |
| 231 | Comment starts source inspection and learning tools. |
| 232 | Sends the following displays into the Data and quality tab. |
| 233 | Adds the field-dictionary heading. |
| 234 | Converts dictionary key/value pairs to a two-column table and displays it. `FIELD_GUIDE.items()` supplies those pairs. |
| 235 | Adds the selected-record heading. |
| 236 | Explains that these rows underlie the analysis and that sorting the display does not change analytical filters. |
| 237 | Displays the complete filtered DataFrame, including `status`. |
| 238 | Serializes the filtered table with `to_csv(index=False)` and supplies it to a download button named `filtered_customer_churn.csv` with CSV MIME type. No pandas index column is exported. |
| 239 | Adds the numeric-summary heading. |
| 240 | Explains the descriptive-statistics rows and warns that interpretation depends on the column's meaning. |
| 241 | Keeps numeric columns, computes `describe()` and rounds the displayed result. The binary churn mean is a proportion; the support-ticket mean is a count average. |
| 242 | Adds the source-quality heading. |
| 243 | Shows whole-source row count, exact duplicate-row count and total missing cells. These are based on `frame`, not only the selected customers. |
| 244 | Builds a column-by-column source-quality table from names, type strings and missing counts. `.values` supplies aligned arrays for the new table. |
| 246 | Opens the exercise expander outside the tab blocks. |
| 247 | Displays four numbered learning tasks stored as one Markdown string with line breaks. They are prompts, not code executed by the app. |
| 248 | Explains the different plotting-library roles. |
| 249 | Repeats the association/causation limit for the fictional observations. |
| 251 | Directs output to the Full report tab. |
| 252 | Offers the current `full_report` string as a Markdown download with a descriptive filename and MIME type. |
| 253 | Renders that same string in the app. |
| 254 | Adds a heading for a separate contract-region sample-size table. |
| 255 | Gives the count Series the name `customers`, converts its two index levels to columns with `reset_index()` and displays it. This display is outside `full_report` and is therefore not included as a table in its download. |

## 7. How to read the five charts

### Contract churn bar chart: compare proportions, then denominators

Every bar represents a contract group. Its height is the share of that group's customers marked churned, in percentage units. It does not show total customers or total fees.

Read the bar and its hover count together. In the complete bundled data, Monthly has the largest share, 33.3333%, across 159 customers. Annual has 167 customers and a lower share. These statements describe the selected snapshot. They do not compare equal exposure times or adjust for the characteristics of people choosing each contract.

### Tenure versus monthly fee: see observations, not a fitted relationship

Each point represents one customer. Moving right means longer recorded tenure; moving up means a higher listed monthly fee. Color identifies status; hover reveals customer ID, contract and satisfaction.

Opacity reduces the visual impact of overlapping points but does not turn the display into an accurate density estimate. Several customers may share the same tenure and fee. The scatter contains no trend line, classification boundary, probability estimate or forecast.

### Tenure histograms: compare shape without confusing counts with rates

The app uses common bins: 12 intervals across 0 to 60 months, so the bin width is 5 months. Shared bins make positions comparable between groups. Height is the number of customers from that status inside the bin.

A higher retained bar can occur simply because the dataset has 381 retained customers and 99 churned customers. It does not automatically mean retention is better at that tenure. To calculate a tenure-specific churn proportion, you would need churned count divided by all customers within each tenure band; that is a possible extension, not what this histogram currently plots.

Values outside the fixed 0-60 range would not appear in the histogram even if loaded. The bundled tenure values fit that range. The loader does not enforce it.

### Satisfaction boxplot: inspect center and spread

For each status, the middle line is the median, the box spans the 25th to 75th percentiles, and the default whiskers extend to observations within 1.5 interquartile ranges of the box limits. Points beyond the whiskers are potential outliers relative to that distribution, not automatically mistakes.

The plot supports comparison of recorded satisfaction between status groups. Because score timing is unknown, lower satisfaction could precede leaving, follow a bad cancellation experience or be associated with another factor. The [Seaborn boxplot reference](https://seaborn.pydata.org/generated/seaborn.boxplot.html) documents the plot's statistical construction.

### Contract-region heatmap: locate detailed segments

The matrix divides each contract into regions. A 40% cell means 40% of the selected records in that cell are marked churned. It does not mean the cell accounts for 40% of all churned customers.

The fixed 0-100 color range allows consistent color interpretation after filtering. A blank cell means no available result, not zero churn. Use the Full report tab's count table for denominators. With all original data selected, all 12 combinations are observed, but filtered or edited data can create absent combinations.

## 8. Validation, assumptions and current limitations

### What the code checks

The loader checks file access, expected column names, a nonempty table, numeric convertibility and missing cells in required fields. The selection stage checks that the chosen regions/contracts leave rows to analyze. It stops with a browser message when these conditions fail.

The source-quality section also reports exact duplicate rows, total missing cells and column types. A count is information for review; it is not a cleaning operation. Duplicate rows are not removed automatically. No imputation, outlier deletion or deduplication is performed.

### What those checks do not prove

The current code does not explicitly enforce:

- Unique customer IDs.
- `churned` values restricted to exactly 0 and 1.
- Satisfaction values within 1-10.
- Nonnegative or integral tenure and support-ticket counts.
- Nonnegative monthly fees or finite numeric values.
- Comparable observation windows or consistent definitions across imported data.

These distinctions matter. A churn value of 2 is numeric and nonmissing, so it could pass loading. It would add 2 to the churn count, distort the mean and map to missing `status`. Grouping by status normally excludes missing group labels, creating inconsistent apparent populations. This is an example of why **valid Python data types are not the same as valid business data**.

The bundled file was checked for this guide: its customer IDs are distinct, churn flags are binary, satisfaction values are within 1-10, and it has no missing cells or exact duplicate rows. Those properties belong to this file; the app does not enforce all of them for future edits.

### Interpretation boundaries

This snapshot supplies no time-based churn rate, survival analysis, customer lifetime value, individual risk prediction or causal driver estimate. It contains no model training, train/test split, evaluation metric or experiment.

The support-ticket field is available for inspection, but the shipped charts do not estimate the effect of support tickets. The histogram is descriptive, and the heatmap gives no confidence intervals. The 20-customer caution rule is only a teaching prompt.

The report's scope uses the selected regions/contracts, while source-quality counts use the full source. If you see 40 selected customers and a quality section showing 480 rows, those numbers refer to different tables intentionally.

Automatic contract leaders use the first maximum in the sorted grouped result when rates tie. The app does not list every tied leader in the generated sentence, so inspect the exact table if differences are absent or tiny.

## 9. Run the project and reproduce the analysis

The [workshop README](../README.md) specifies Python 3.12 and these dependency versions. From the repository root in Linux, macOS or WSL:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit==1.50.0 pandas==2.2.3 numpy==2.3.5 matplotlib==3.10.8 seaborn==0.13.2 plotly==6.5.2
cd business_analytics_workshop/03_customer_churn
streamlit run app.py
```

Use a Python 3.12 interpreter for the first command; check `python --version` if unsure. NumPy is part of the workshop environment although this particular script does not import it directly.

The repository contains other directories with `>` in their names, which native Windows filesystems cannot represent. Follow the root README's WSL guidance when cloning the whole repository. If working with only a copied workshop folder on Windows, virtual-environment activation in PowerShell is `.venv\Scripts\Activate.ps1`.

In the configured CookieSensei workshop environment, the packages are already supplied. For a separate instance:

```bash
cd /home/coder/project/business_analytics_workshop/03_customer_churn
streamlit run app.py --server.port 8502
```

The workshop dashboard already uses port 8501. Open the forwarded port for the separate instance as described in the workshop README.

Running `python app.py` is not equivalent to launching the Streamlit server. The `streamlit run` command starts the app runtime and serves the interface. Dependencies must be installed first, but this app's analysis uses the local CSV and does not call a business API or require a database.

### A reproducible reading session

1. Leave all regions and contracts selected. Confirm 480 customers, 20.6% displayed churn, 6.9/10 displayed satisfaction and INR 84,101 associated fees.
2. Open the contract table and verify the group counts add to 480.
3. Select Monthly and confirm the population becomes 159 customers, with 53 churned and a 33.3% card.
4. Select only North in Regions, keeping Monthly selected, and inspect the 23-customer cell. Explain what changes in the denominator.
5. Download the filtered CSV and full report. Record selections when sharing results.
6. Restore all filters before comparing with the complete-data examples in this guide.

You can independently check the core results from this project directory without importing the Streamlit app:

```python
import pandas as pd

customers = pd.read_csv("customer_churn.csv")
print(len(customers))
print(customers["churned"].sum())
print(customers["churned"].mean())
print(customers.loc[customers["churned"] == 1, "monthly_fee"].sum())
print(
    customers.groupby("contract").agg(
        customers=("churned", "size"),
        churned=("churned", "sum"),
        churn_rate=("churned", "mean"),
    )
)
```

This verification snippet is a teaching example, not additional code already present in `app.py`.

## 10. Practice, troubleshooting and useful next questions

### Practice with a reason for each change

**Add a support-ticket filter.** First decide the meaning: selecting customers with at least a chosen number of recorded tickets. A widget alone changes nothing unless its value is used in a Boolean filter before metrics and charts are calculated. Keep the missing ticket-exposure window in the interpretation.

**Create tenure bands and compare churn proportions.** Group customers into clearly labeled tenure intervals, count customers and sum churn flags within each interval, then divide. Check that the denominator is all customers in the interval, not just the churned customers. This would answer a different question from the existing count histogram.

**Display all tied highest-rate contracts.** Compare the summary rates with their maximum and retain every matching row. This makes the definition of “leader” visible when two groups tie.

**Add explicit domain validation in a separate practice copy.** For example, check that every churn flag belongs to `[0, 1]` and every satisfaction score lies between 1 and 10. Decide how the browser should explain an invalid value instead of allowing a misleading metric.

**Make a careful business statement.** State the selected population, the numerator and denominator, the observation and the remaining uncertainty. For example: “Among the 23 Monthly/North customers in this fictional snapshot, 10 are marked churned. Their experience warrants investigation; the table does not establish a monthly churn rate or contract effect.”

### Common problems and what they mean

| Symptom | Likely reason | Useful next step |
| --- | --- | --- |
| `ModuleNotFoundError` | The interpreter running Streamlit lacks a package | Activate the intended environment and install the workshop dependencies there. |
| CSV could not be loaded | File missing, renamed or inaccessible | Keep `customer_churn.csv` beside `app.py` and inspect the displayed error. |
| Missing required columns | A header was deleted or changed, including capitalization | Compare the CSV header with `required_columns`. |
| Numeric conversion error | A numeric column contains text such as “unknown” or currency symbols | Repair the input or explicitly design a cleaning rule in a practice copy. |
| Empty-state message | No region or no contract is selected, or the combination has no records | Restore valid choices; this project has no date filter despite the generic message text. |
| A rate looks implausible | Invalid binary values, duplicate customers or a misunderstood denominator | Inspect raw records and validate grain before interpreting the chart. |
| The chart and source-quality counts differ | Charts use `filtered`; source-quality checks use `frame` | Compare like scopes and read the analysis-scope caption. |
| A CSV edit does not appear yet | The script has not rerun after the save | Save, then rerun or change a widget. The reader is uncached, but a rerun is still needed. |

Before presenting the project, practice explaining these questions without referring to function names alone: Why does the mean of a binary column give a proportion? Why does a heatmap cell need a sample size? Why is the fee total not measured revenue loss? Which additional dates would be necessary for a monthly churn metric? What evidence would be needed to test a retention intervention?

## 11. Source and reference links

Project facts, calculations, line references and behavior in this guide come from [app.py](app.py), [customer_churn.csv](customer_churn.csv) and the [workshop README](../README.md). The full-data numerical examples are direct recalculations of the bundled CSV.

For the general APIs used here:

- [pandas 2.2: ten-minute introduction](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html)
- [pandas 2.2: grouping and aggregation](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html)
- [Streamlit: run your app](https://docs.streamlit.io/develop/concepts/architecture/run-your-app)
- [Streamlit 1.50: tabs and their execution behavior](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs)
- [Plotly Express overview](https://plotly.com/python/plotly-express/)
- [Seaborn boxplot reference](https://seaborn.pydata.org/generated/seaborn.boxplot.html)
- [Matplotlib: close a figure](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.close.html)

Read these API references alongside the actual project: a library describes what an operation can do; the chosen fields, filters, denominators and limitations determine what this particular business analysis means.
