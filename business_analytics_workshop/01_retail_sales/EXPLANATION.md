# Retail Sales Explorer - business questions, calculations and every line of code

This guide explains the [actual `app.py` in this folder](app.py), using its [bundled `retail_sales.csv`](retail_sales.csv). It is written for a learner who can open a Python file but has not yet built a data analysis application. Keep the source open beside this guide and enable line numbers in your editor.

**Source revision:** `c10a61c36fffdd048b69dd78926e6663bc986fce`. The line numbers below refer to the 264-line `app.py` at that revision. Blank lines separate ideas and do not execute; the walkthrough covers every nonblank line, including comments, display text and closing delimiters. If the Python file changes, its line numbers and example results may change too.

The data is fictional teaching material, not CookieSensei sales or another company's records. Amounts are INR. This document teaches how the application works; the app's **Full report** tab separately produces a report about whichever rows the user selects.

## Contents

1. [The business problem and the purpose of the solution](#1-the-business-problem-and-the-purpose-of-the-solution)
2. [Understand the dataset before writing code](#2-understand-the-dataset-before-writing-code)
3. [Why these Python libraries are used](#3-why-these-python-libraries-are-used)
4. [From a business question to a defensible calculation](#4-from-a-business-question-to-a-defensible-calculation)
5. [How the analysis becomes a Streamlit application](#5-how-the-analysis-becomes-a-streamlit-application)
6. [Run the project and reproduce the starting results](#6-run-the-project-and-reproduce-the-starting-results)
7. [Read all five charts correctly](#7-read-all-five-charts-correctly)
8. [Line-by-line walkthrough](#8-line-by-line-walkthrough)
9. [Data quality, edge cases and limits](#9-data-quality-edge-cases-and-limits)
10. [Practice and worked examples](#10-practice-and-worked-examples)
11. [Troubleshooting](#11-troubleshooting)
12. [Sources and further reading](#12-sources-and-further-reading)

## 1. The business problem and the purpose of the solution

Imagine that a retail manager receives a spreadsheet of orders. The manager can see individual purchases but cannot immediately answer: How much did we sell after discounts? How much remained after paying for the products? Which region produced most sales? Which category had the highest margin? Is our average order a good description of an ordinary order? Did sales and gross profit move together over time?

These are different questions. A category can sell expensive products and therefore lead revenue while earning little profit per rupee of sales. A region can have a large total because it has more orders, rather than because each order is more valuable. An unusually large order can lift the average without changing most customers' purchases. Reading only one total hides these distinctions.

The app solves this information problem by turning order records into a repeatable investigation. It loads the CSV, checks that essential information can be used, lets the reader select regions, categories and dates, calculates the same measures for that selection, and presents complementary views. A manager can inspect a large pattern, drill into source records, and export both the selected data and an explanatory report.

The intended decision is **where to investigate pricing, product costs, merchandising or promotions next**. The app does not automatically change a price, buy stock, forecast sales or decide that a promotion worked. Its output gives a reason to ask a more precise question. For example: "Electronics leads sales and has a relatively high aggregate margin in this selection; which products and order sizes explain that result?" is supported by this dataset. "Increasing the Electronics discount will increase future profit" is not established by the analysis.

This is exploratory data analysis, or EDA: inspect the data's structure, summarize it, compare groups, study distributions, and look for relationships worth investigating. It also includes descriptive reporting. No machine learning model is trained, and none is necessary to answer the questions actually implemented in this project. The project's own `CASE`, `DECISION` and `LIMITATIONS` strings define that scope in [the source](app.py).

## 2. Understand the dataset before writing code

### 2.1 What one row means

The unit represented by a row is often called its **grain**. Here one row is one order, assigned one category, one region and one sales channel. An order may contain multiple units, but this simplified dataset supplies one price and one cost per unit for that row. It does not contain separate product lines for a multi-category shopping basket.

The bundled CSV has **720 rows and 9 source columns**, covering **1 January through 29 June 2025**. The app describes this as January to June 2025; that description does not mean every day in June is present. There are 720 distinct order IDs, no exact duplicate rows and no missing cells in this bundled version. These are observations about the supplied file, not promises about a CSV you edit later.

Knowing the grain makes the calculation `filtered["revenue"].mean()` meaningful: because one row is one order, the mean of row revenues is average order value. If future data contained one row per product line, the same expression would instead calculate average line value. Before reusing code with another dataset, check what a row represents.

### 2.2 Source field dictionary

| Column | Meaning and units | Why the app needs it |
| --- | --- | --- |
| `order_id` | A synthetic order identifier, such as `ORD-0001` | Helps locate a transaction. The loader requires this field but does not enforce uniqueness. |
| `order_date` | The order's date | Supports inclusive date filters and monthly grouping. It is converted from CSV text into pandas datetime values. |
| `region` | East, North, South or West in the supplied file | Supports the region filter and regional sales comparisons. |
| `category` | Electronics, Fashion, Grocery or Home | Supports category filtering, category totals, margins and profit distributions. |
| `channel` | Store or Online | Describes where the order occurred. It appears in data and report scope, but the current sidebar has no channel filter. |
| `units` | Number of units in the order | Converts per-unit prices and costs into order amounts. |
| `unit_price` | INR per unit before the stated discount | The starting selling price in the revenue formula. |
| `discount_pct` | Percentage discount, intended to be between 0 and 100 | Converts list-price sales into sales after discount. A stored `10` means 10%, not 0.10%. |
| `unit_cost` | Product cost in INR per unit | Calculates the product cost associated with all units in the order. |

These definitions come from `FIELD_GUIDE` and the workshop [README](../README.md). The intended units are part of the data contract. A CSV column named `unit_price` containing paise rather than rupees could still parse as numeric, but its resulting business calculations would be wrong by a factor of 100.

### 2.3 Source columns and derived columns

The CSV does **not** already contain `revenue` or `gross_profit`. Lines 150-151 calculate them on the selected DataFrame. The filtered table and its CSV export therefore normally contain 11 columns: the 9 source fields plus these 2 derived fields. The raw `frame` remains the loaded source table; source-quality checks inspect that table rather than the derived columns.

This separation is useful. You can trace every reported amount back to its inputs without overwriting the original CSV. Changing a filter changes the in-memory selection; clicking a download saves a new file in the browser. Neither operation writes back to `retail_sales.csv`.

## 3. Why these Python libraries are used

### 3.1 Why pandas is central

A CSV is text arranged into rows and columns. Python can read text without pandas, but we would then need to write our own parsing, type conversion, filtering, grouping, aggregation and table-export code. Pandas supplies those operations in a form that maps directly to this problem. Its central two-dimensional object is a **DataFrame**; selecting one column usually produces a **Series**, a one-dimensional labeled collection. See the official [pandas introductory guide](https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/01_table_oriented.html).

In this app:

```python
frame = pd.read_csv(DATA_FILE)
```

creates a DataFrame. The column names become labels, and pandas supplies a row index. The index is not the `order_id` business identifier. For example, `frame["units"]` selects the entire units column, while `frame[["units", "unit_price"]]` selects a two-column DataFrame. The second example has nested square brackets because the outer brackets select columns and the inner brackets construct the list of column names.

Pandas **vectorized operations** apply calculations to a whole Series at once. In:

```python
filtered["units"] * filtered["unit_price"]
```

each order's quantity is multiplied by the corresponding order's price. We do not manually write a Python loop that retrieves each row and appends each result. This makes the business formula more visible and reduces opportunities to mix one row's quantity with another row's price. Pandas aligns Series by their index; here both Series come from the same DataFrame and therefore refer to matching rows.

Pandas also provides the vocabulary needed for the analysis:

| Operation | Meaning in this project |
| --- | --- |
| `read_csv()` | Parse the file into a table. |
| `to_datetime()` and `to_numeric()` | Convert dates and measures to types that support comparisons and arithmetic. |
| `.isin()` and Boolean indexing | Keep rows matching selected categories or regions. |
| `.dt.date.between()` | Keep rows inside an inclusive date interval. |
| `.sum()`, `.mean()`, `.median()` | Answer questions about total, average and typical order amounts. |
| `.groupby().agg()` | Collect orders into business groups and calculate multiple summaries per group. |
| `.corr()` | Quantify pairwise linear relationships between selected numeric measures. |
| `.describe()` | Produce a statistical overview of numeric columns. |
| `.to_csv(index=False)` | Serialize the current selected table for a download without adding the pandas row index. |

Pandas computes the analytical tables. It does not itself create the sidebar, run a web server, or decide what a manager should do.

### 3.2 Responsibilities of the other imports

| Import | Responsibility here | Why it is a separate tool |
| --- | --- | --- |
| `Path` from `pathlib` | Locate the CSV beside the Python script | File location should not depend on which directory the terminal happened to start in. |
| `matplotlib.pyplot as plt` | Create figures and axes; draw the histogram; provide axes for Seaborn | It gives explicit control over figure size, axes, labels and cleanup. |
| `plotly.express as px` | Build the interactive monthly line chart and stacked regional bar chart | Hover and zoom help a reader inspect exact groups and periods. |
| `seaborn as sns` | Draw the category boxplot and correlation heatmap on Matplotlib axes | It expresses distribution and statistical comparison plots compactly. |
| `streamlit as st` | Create the browser interface and connect widget values to Python execution | It exposes a Python analysis to a reader who should not have to edit code to explore it. |

The aliases `pd`, `plt`, `px`, `sns` and `st` are shorter local names introduced by `as`; they do not install libraries or change their behavior. This file does not import NumPy directly, although NumPy is included in the workshop environment. There are no external service calls, API keys, database queries or authentication routines inside this particular app. Those are separate concerns from its local CSV analysis.

### 3.3 Python syntax that will recur

`=` assigns a value to a name or a column. It does not mean mathematical equality testing; `==` would test equality. Parentheses call a function, group an expression, or delimit a tuple. Square brackets construct lists or select items. Curly braces in `{"key": "value"}` construct a dictionary. In an f-string such as `f"{revenue:,.0f}"`, braces insert a computed value into text; the format after `:` requests separators and a number of displayed decimal places.

Indentation defines a block. The lines indented beneath `if`, `for`, `try`, `except`, `def` or `with` belong to that statement. A `#` comment and a descriptive docstring explain code; they do not calculate a business metric. Strings written beside one another inside parentheses are joined by Python, which is why the long business explanations span several source lines without explicit `+` signs.

## 4. From a business question to a defensible calculation

### 4.1 Sales after discount

For each order:

```text
list-price order amount = units * unit_price
discount fraction = discount_pct / 100
retained fraction = 1 - discount fraction
net sales = list-price order amount * retained fraction
```

Line 150 writes this whole expression directly:

```python
filtered["revenue"] = (
    filtered["units"] * filtered["unit_price"]
    * (1 - filtered["discount_pct"] / 100)
)
```

This is the same calculation as the source, reformatted for reading. The parentheses matter: they calculate the retained fraction before multiplication. For a **made-up arithmetic example**, sell 2 units at INR 1,000 each with a 10% discount. The list-price amount is INR 2,000; the retained fraction is 0.90; net sales are INR 1,800. Using `discount_pct` directly as 10 would produce a negative multiplier; dividing by 100 converts percentage points to a fraction.

Why does summing this derived column answer the sales question? Each selected row represents one order and the derived value represents that order's net sales. Adding one amount for every selected order gives total net sales for that selection. It is not necessarily money collected: this file has no payment-status or cash-receipt information.

### 4.2 Gross profit and gross margin

Product cost for an order is `units * unit_cost`. Gross profit subtracts that amount from net sales. Continuing the made-up example, if each unit costs INR 600, total product cost is INR 1,200 and gross profit is INR 600. The gross margin is `600 / 1800 = 0.3333...`, displayed as 33.3%.

Why subtract cost for **every unit**? Subtracting only `unit_cost` would account for one unit while recording revenue from two. Both sides of the calculation must cover the same quantity and selected orders.

Why divide profit by revenue? Margin asks what fraction of sales remains after product costs. Dividing profit by cost instead would answer a different question, markup on cost. This app reports margin, not markup.

The app's total margin is:

```python
profit = filtered["gross_profit"].sum()
revenue = filtered["revenue"].sum()
total_margin = ratio(profit, revenue)
```

It does not average each order's margin. Consider two **invented** orders: one has INR 100 sales and INR 50 profit, and the other has INR 900 sales and INR 180 profit. Their margins are 50% and 20%. The unweighted average is 35%, but the overall business earned INR 230 from INR 1,000 sales: **23%**. Summing numerators and denominators gives the revenue-weighted answer. An average of percentages would give a tiny order equal weight to a large order.

Gross profit in this project excludes operating expenses and taxes. The file also omits refunds, acquisition costs and other information needed for a complete profitability picture. A positive gross profit is therefore not proof of positive net profit.

### 4.3 Average, median and distribution

Average order value is total selected revenue divided by the number of selected orders. `.mean()` implements that arithmetic mean. `.median()` finds the middle value after ordering the observations. With **invented** order values of 100, 120, 130, 150 and 1,000, the mean is 300 but the median is 130. The large order changes the mean strongly while leaving the middle order small.

The app therefore shows an average card, includes the median in its generated insights, and draws a histogram. These outputs answer related questions: the mean describes revenue per order overall, the median describes the center of the ordered observations, and the histogram shows how values are distributed rather than reducing everything to one number.

### 4.4 Grouping answers segment questions

```python
sales_by_region = filtered.groupby("region")["revenue"].sum()
```

means: partition selected rows by their region label, take each group's revenue column, and add the values. The result is a Series indexed by region. Calling `.idxmax()` returns the region label attached to the highest total; `.max()` would return the highest amount instead. The app needs the label to name the region in a sentence.

The category summary uses **named aggregation**:

```python
category_summary = filtered.groupby("category").agg(
    sales=("revenue", "sum"),
    profit=("gross_profit", "sum"),
    orders=("revenue", "size"),
)
```

Each output name is paired with the source column and operation. `size` counts rows in each group, which correspond to orders under this dataset's grain. It is not the number of units sold or a distinct-customer count. Category margin is then derived from each category's summed profit and sales, preserving the same weighted logic used for total margin.

### 4.5 Question-to-code map

| Business question | Actual calculation or display | Why it answers the question | Limit on interpretation |
| --- | --- | --- | --- |
| How much selected business occurred? | Derive row revenue and profit; sum both; count selected rows (150-153, 168) | Adds comparable order amounts over exactly the chosen scope | Orders are fictional; sales are not confirmed cash collections |
| Which region leads sales? | `groupby("region")`, `.sum()`, `.idxmax()` (160, 164, 169) | Compares total selected sales by region | Total sales do not measure productivity per store, person or customer |
| Which category leads sales? | Category aggregation and sales `.idxmax()` (161, 165, 170) | Identifies the largest category revenue total and its row count | The wording "volume of sales" refers to revenue here, not maximum units |
| Which category leads margin? | Category profit divided by category sales (162, 166, 171) | Compares profit per rupee of sales rather than absolute sales size | A high percentage can occur on a small sales base |
| What is a typical order worth? | Mean, median and histogram (172, 227) | Compares the average with the distribution's center and shape | Averages alone conceal variation and mix differences |
| Which month contributes most? | Group dates as monthly periods, sum revenue and find the maximum (163, 173) | Combines all selected dates belonging to the same calendar month | A partly selected month has less exposure than a complete month |
| Which measures move together? | `.corr()` and a heatmap (237) | Summarizes pairwise linear association | Shared inputs create mechanical relationships; correlation is not causation |

## 5. How the analysis becomes a Streamlit application

### 5.1 The execution cycle

The file is a normal Python script with Streamlit commands inserted where information or controls should appear. Running `streamlit run app.py` starts Streamlit's server. A browser connects to that server, while the Python calculations run in the Python environment. Streamlit translates calls such as `st.title()`, `st.metric()` and `st.plotly_chart()` into interface elements. You do not manually write HTML, CSS or JavaScript in this project.

On the initial run, all region and category values are selected and the date interval spans the source data. When a user changes an input widget, Streamlit normally reruns the script from top to bottom using that widget's current value. That execution model is why the code can be read as a single pipeline rather than a collection of manually wired browser event handlers. The official [Streamlit main concepts](https://docs.streamlit.io/develop/concepts/architecture/run-your-app) explain this model.

The sequence is:

1. Set the page title and display the case-study context.
2. Read and validate the CSV into `frame`.
3. Receive region, category and date choices from sidebar widgets.
4. Build `filtered` and stop early if the selection is incomplete or empty.
5. Calculate derived order measures, totals, grouped summaries and text insights.
6. Assemble report text using those same results.
7. Render charts, source records, quality tables, exercises and downloads.

The file intentionally has no `@st.cache_data` decoration. A rerun reads the CSV again, so a saved CSV edit is reflected on the next rerun. Editing the CSV is not itself a guarantee that Streamlit immediately reruns; trigger a rerun if necessary. At this small teaching-data size, understandable execution and visible edits are the design priority.

### 5.2 Widgets return data, not just decorations

`st.sidebar.multiselect()` returns the selected list of labels. The app converts that list into a Boolean mask with `.isin()`. A mask is a Series of `True` and `False`, one value for each current row. `filtered[mask]` retains only the `True` rows. Region, category and date filters are applied sequentially, so a row must satisfy all of them.

Each widget has a project-specific `key`. This identifies the widget's state; it does not name a CSV field or create a database entry. The available choices are read from the complete `frame`, not progressively narrowed by previous filters. Therefore, a user can choose a combination that contains no orders; the `filtered.empty` guard then displays guidance and stops the remainder of that run.

`st.date_input()` receives a pair of initial dates, making it a date-range widget. While the user is choosing a range, it may not yet return two dates. The app checks `len(dates) != 2` before trying to access both ends. It then uses `.between()` with its inclusive default, retaining orders on either boundary date.

### 5.3 Layout and outputs

`st.columns(4)` allocates four neighboring metric containers. `columns[0]` selects the first because Python indexing begins at zero. `with overview:` directs subsequent rendering calls into the dashboard tab. `with st.expander(...):` creates a collapsible explanation area. These `with` statements control where elements render; they do not change which rows belong to the analysis.

In the pinned Streamlit version, the code inside all four `st.tabs()` containers runs on each full script rerun, even though only one tab's content is visible at a time. A tab is not a lazy-loading condition. Likewise, collapsing an expander does not prevent its code from being executed. See the official [tabs API](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs).

The report is built from `insights`, `kpi_values`, scope information and the same filtered table used for the charts. The app does not ask an AI model to invent its findings: Python f-strings insert calculated values into predefined explanatory sentences. A download offers the assembled text; it does not modify this `EXPLANATION.md` or commit anything to GitHub.

## 6. Run the project and reproduce the starting results

### 6.1 Local environment

The workshop [README](../README.md) specifies Python 3.12 and the following package versions. From the repository root in a Linux/macOS terminal, create a virtual environment and install that environment's dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit==1.50.0 pandas==2.2.3 numpy==2.3.5 matplotlib==3.10.8 seaborn==0.13.2 plotly==6.5.2
cd business_analytics_workshop/01_retail_sales
python -m streamlit run app.py
```

Confirm that `python` points to Python 3.12 before creating the environment, or use your Python 3.12 executable explicitly. On Windows PowerShell, activation is `.venv\Scripts\Activate.ps1`; however, the full repository contains phase folder names with `>`, which native Windows filenames cannot represent. The repository [root README](../../README.md) recommends a Linux Cloud Lab or a clone inside WSL's Linux filesystem. The workshop subfolder itself uses ordinary compatible names.

Open the local URL printed by Streamlit, normally `http://localhost:8501`. The Python environment and server must stay running while the browser uses the application. Installation needs access to the package source, but the app's subsequent analysis uses its local CSV and makes no external data request.

### 6.2 CookieSensei Cloud Labs

For the prepared workshop workspace, follow its existing project selector or run a separate instance on port 8502, because the built-in dashboard already uses 8501:

```bash
cd /home/coder/project/business_analytics_workshop/01_retail_sales
streamlit run app.py --server.port 8502
```

Use the forwarded port offered by your workspace. The standalone script does not implement the shared project selector; the workspace supplies that surrounding interface. The workshop README also explains that previously copied student files are preserved and are not automatically overwritten by a repository update.

### 6.3 Check the bundled-data baseline

The following values were recalculated directly from the supplied CSV using the formulas in `app.py`, with all regions and categories selected and the complete available date range. They are baseline checks, not claims about a live retail business.

| Measure | Baseline result |
| --- | ---: |
| Selected orders | 720 |
| Net sales | INR 3,014,163.59 when formatted to two decimals as in the report |
| Gross profit | INR 991,908.14 |
| Gross margin | 32.91% |
| Average order value | INR 4,186.34 |
| Median order value | INR 2,847.03 |
| Sales-leading region | North, INR 864,633.53 |
| Sales-leading category | Electronics, INR 1,533,289.74 |
| Highest aggregate category margin | Electronics, about 33.44% |
| Highest monthly sales total | May 2025, INR 605,230.59 |

Cards show some amounts with zero decimal places and margin with one decimal place, while the report often shows two. Display rounding does not alter the underlying calculations. The app uses floating-point arithmetic and does not round every order amount to paise before summing. Its unrounded net-sales total is approximately 3,014,163.595; binary representation and formatting can affect the final displayed paisa. A production accounting system would need an explicit currency rounding policy.

You can reproduce selected values without launching the interface. Run this **standalone verification example** from the folder containing the CSV:

```python
import pandas as pd

orders = pd.read_csv("retail_sales.csv")
orders["revenue"] = orders["units"] * orders["unit_price"] * (1 - orders["discount_pct"] / 100)
orders["gross_profit"] = orders["revenue"] - orders["units"] * orders["unit_cost"]
print(len(orders))
print(f"Net sales: {orders['revenue'].sum():,.2f}")
print(f"Gross profit: {orders['gross_profit'].sum():,.2f}")
print(f"Margin: {orders['gross_profit'].sum() / orders['revenue'].sum():.2%}")
```

The first actual CSV row is also easy to check manually: `ORD-0001` has 7 units, unit price INR 1,043.19, discount 0%, and unit cost INR 658.69. Net sales are `7 * 1043.19 = 7302.33`; product cost is `7 * 658.69 = 4610.83`; gross profit is INR 2,691.50. This is a source-data example, unlike the invented arithmetic examples earlier.

## 7. Read all five charts correctly

### 7.1 Monthly sales and gross profit

Line 216 creates a new `month` column from each date's calendar month, groups orders by that month, and sums revenue and gross profit. The chart uses a common INR axis for both lines, making the distance between them meaningful as the difference between selected sales and gross profit. Markers identify actual monthly observations; hover reveals values.

A monthly total answers "how much in the selected portion of this month?" It does not measure revenue per day. If the user selects 20 January through 10 March, January and March are partial months. The code does not normalize by selected days or insert zero-sales months missing from the data. Apparent rises and falls need that context before being called growth or decline.

### 7.2 Regional category mix

Line 219 groups by the pair `region` and `category`, not by region alone. Each grouped amount becomes a colored segment in a stacked bar. Total bar height is regional revenue; colored portions show which categories contribute to it. This is useful when two regions have similar totals but different product mixes.

The chart does not show category margin. A large segment could have high cost or many orders. Use the category summary, filtered records and profit distributions to investigate why it is large rather than interpreting bar height as profitability.

### 7.3 Order value distribution

The Matplotlib histogram places order revenue into 20 bins and counts orders in each bin. Its horizontal unit is INR per order; its vertical unit is number of orders. It helps explain why mean and median differ. A long right tail means some relatively large orders extend far beyond most values.

Twenty is a chosen visualization setting, not a conclusion discovered by the data. Fewer bins smooth detail; more bins can make the plot look noisy. A high-value order is worth inspecting, but it is not automatically an error. The app does not delete outliers.

### 7.4 Profit spread by category

The boxplot works with **individual order profits**, not category total profit. Each category's box summarizes its order distribution. The middle line is the median, the box runs from the first to third quartile, and its height is the interquartile range. By default, whiskers reach the most extreme observations within 1.5 interquartile ranges of the box; farther observations are plotted separately. See the [Seaborn boxplot documentation](https://seaborn.pydata.org/generated/seaborn.boxplot.html).

A category can have the highest total profit because it has many orders, even if its median order profit is modest. Box widths here are not a sample-size encoding. Read counts in the category table before comparing how much evidence each distribution contains.

### 7.5 Correlation between measures

The heatmap compares `units`, `discount_pct`, `revenue` and `gross_profit`. `.corr()` defaults to Pearson correlation, which measures linear co-movement. Values near +1 indicate that larger values tend to accompany larger values; near -1 they tend to accompany smaller values; near 0 there is little measured linear association. Zero correlation does not rule out a curved relationship.

The color scale is fixed from -1 to +1, making a filtered chart's colors comparable in scale with another selection. The numbers printed in cells are rounded to two decimals. Constant columns or insufficient observations produce undefined correlations, shown as missing cells rather than meaningful zeros.

Revenue and gross profit share inputs by construction: gross profit is revenue minus product cost. Their correlation in the full bundled file is about 0.90. That is not independent evidence that a managerial intervention caused profit to rise. Similarly, the discount-profit relationship combines the formula's arithmetic with whatever product and order mix exists in the sample. The app calculates no causal model or significance test.

## 8. Line-by-line walkthrough

The line references in this section are for [app.py](app.py) at the revision stated at the top. Consecutive literal-string lines are occasionally grouped because together they construct one value. Every executable line, explanatory comment and delimiter is accounted for; blank lines are only visual spacing.

### 8.1 Imports and page setup: lines 1-15

| Line(s) | What happens and why |
| --- | --- |
| 1 | The triple-quoted module docstring identifies this as the Retail Sales Explorer teaching project. It documents the module; it is not rendered in the browser automatically. |
| 2 | `from pathlib import Path` imports the standard-library path class so the code can construct a file path from the script's location. |
| 4 | Imports Matplotlib's plotting interface under `plt`, used for figures, axes, the histogram and figure cleanup. |
| 5 | Imports pandas under `pd`, providing CSV loading, DataFrames, conversion, filtering and aggregation. |
| 6 | Imports Plotly Express as `px`, used to create interactive line and bar figures. |
| 7 | Imports Seaborn as `sns`, used for the boxplot and heatmap. |
| 8 | Imports Streamlit as `st`, giving Python commands for widgets and browser output. |
| 10 | Configures the browser page title, chart icon and wide layout. Keyword arguments name each option rather than relying on positional order. |
| 11 | Renders the visible page title. This is separate from the browser-tab title configured above. |
| 12 | Renders a smaller caption describing the workshop, fictional data and INR currency. |
| 13 | Renders the opening explanation so readers know the app compares revenue, discounts and gross profit. |
| 15 | A comment introduces the case-study text. Python ignores this line during computation. |

### 8.2 Reusable case-study content: lines 16-80

The uppercase names below are a convention for configuration-like content. Python does not make them immutable. These values are stored once per run and reused in the interface and exported report.

| Line(s) | What happens and why |
| --- | --- |
| 16-18 | Assigns one concatenated string to `CASE`. The three adjacent literals explain why revenue alone can conceal discounts, costs and unusual orders. Parentheses allow the assignment to span lines. |
| 19-20 | Assigns `DECISION`, defining investigation of pricing, merchandising and costs as the dashboard's intended decision context. |
| 21-23 | Assigns `DATA_CONTEXT`, explaining row grain, fictional sample size, teaching period and omitted expenses/customer history. This is static documentation, not a freshly calculated row count. |
| 24-26 | Begins the `FORMULAS` list and adds its first three-item tuple: net-sales name, formula text and interpretation. These strings explain a calculation; they do not execute it. |
| 27-29 | Adds the gross-profit definition and the cost scope it includes. |
| 30-32 | Adds the gross-margin definition and explicitly distinguishes total weighted margin from an average of order margins. |
| 33-35 | Adds the average-order definition and median comparison, then closes the tuple and `FORMULAS` list. |
| 36-42 | Starts `VISUAL_GUIDE` with a five-item tuple for monthly sales/profit: title, purpose, reading instructions, question and caution. Continued strings describe axes and partial-month limits. |
| 43-49 | Adds the regional-mix guide: a stacked regional sales view, its component categories and the limits of interpreting total revenue. |
| 50-55 | Adds the histogram guide: order-value bins, count axis, average representativeness and outlier caution. |
| 56-63 | Adds the category boxplot guide: median, middle 50%, whiskers, variable profitability and unequal sample sizes. |
| 64-71 | Adds the correlation guide: signed linear relationships, shared mathematical inputs, causation limits and undefined cells. The final `]` closes all five visual-guide entries. |
| 72-73 | Starts `RECOMMENDATIONS` with one string about comparing the revenue leader with the margin leader. |
| 74-75 | Adds a second recommendation to inspect unusual or negative-profit orders rather than assuming they are errors. |
| 76-77 | Adds the equal-period/additional-data recommendation and closes the list. |
| 78-80 | Builds `LIMITATIONS`, spelling out omitted costs and identifiers and the absence of forecasting or causal estimation. |

### 8.3 Context, dictionary and a reusable rendering function: lines 82-106

| Line(s) | What happens and why |
| --- | --- |
| 82 | Opens an expander titled Business problem and context, initially expanded. The indented commands render inside it. |
| 83 | Concatenates a bold Markdown label with `CASE` and displays it. `+` joins strings here; it is not adding numeric values. |
| 84 | Displays `DECISION` with its bold context label. |
| 85 | Displays the row-grain and dataset explanation from `DATA_CONTEXT`. |
| 86 | Adds an informational notice identifying the evidence as fictional teaching data. |
| 87 | Displays the suggested reading sequence and explains that filters recalculate outputs. |
| 90 | Begins `FIELD_GUIDE`, a dictionary mapping `order_id` to its meaning. |
| 91 | Adds the date definition, including inclusive filtering semantics. |
| 92 | Adds the region definition used for grouping. |
| 93 | Adds the product-category definition. |
| 94 | Adds the sales-channel definition. |
| 95 | Adds the units definition. |
| 96 | Adds the pre-discount INR-per-unit price definition. |
| 97 | Adds the discount-percentage definition and intended range. The string does not itself validate that range. |
| 98 | Adds product cost per unit and closes the dictionary. |
| 100 | Defines `explain_visual(index, container=st)`. It creates a reusable function; its body runs only when called. `container` defaults to Streamlit but can be a column container. |
| 101 | Selects one `VISUAL_GUIDE` tuple by zero-based index and unpacks its five elements into meaningful variable names. |
| 102 | Uses an f-string to insert the selected title into a bold Markdown heading in the requested container. |
| 103 | Writes the visual's purpose into that same container. |
| 104 | Displays its reading instructions beneath a bold label. |
| 105 | Displays the business question the chart addresses. |
| 106 | Displays the caution as a caption. One function keeps the explanation format consistent across all five charts. |

### 8.4 Load and validate: lines 108-130

| Line(s) | What happens and why |
| --- | --- |
| 108 | Comment introducing script-relative CSV loading. |
| 109 | Comment explaining the deliberate absence of caching so a subsequent rerun reads saved CSV changes. |
| 110 | `__file__` identifies this script. `Path(...)` wraps it, `.resolve()` makes an absolute resolved path, and `.with_name("retail_sales.csv")` replaces the filename while keeping its directory. |
| 111 | Starts a `try` block so expected file, conversion and lookup failures can be shown in the interface. |
| 112 | Reads the CSV into `frame`. The header supplies columns and pandas infers initial data types. |
| 113 | Parses the date column with errors raised instead of silently converting invalid dates to missing values. This access happens before the full required-column check, so a missing `order_date` triggers a caught `KeyError`. |
| 114 | Lists the four fields that must be numeric for this project's arithmetic. |
| 115 | Lists all required source columns, including identifiers and segmentation fields. |
| 116 | Converts required names to a set and checks that every required name is present in `frame.columns`. Extra columns are allowed. `not` reverses the success condition. |
| 117 | Raises a clear `ValueError` if required columns are absent, transferring control to the matching `except` block. |
| 118 | Checks whether the loaded table has no rows. A table can have headers and still be empty. |
| 119 | Raises a useful error instead of letting later date and summary operations run on empty data. |
| 120 | Loops over the numeric column names, binding the current name to `column`. |
| 121 | Converts that column with `pd.to_numeric(..., errors="raise")` and stores the converted Series back. Non-numeric text fails rather than silently becoming zero. |
| 122 | Restricts to required fields, marks missing cells with `.isna()`, then uses `.any()` twice: any missing cell in each column, then any such column overall. |
| 123 | Raises an error requiring the learner to fix essential missing values. It does not drop affected rows or fill them automatically. |
| 124 | Catches `OSError`, `ValueError` and `KeyError`, storing the exception object in `error` for a useful message. |
| 125 | Displays the CSV basename and exception text using `st.error()`. |
| 126 | Stops the current Streamlit script run, preventing downstream calculations from using invalid or unavailable data. |
| 128 | Defines a small helper for scalar division, accepting a numerator and denominator. |
| 129 | Documents its zero-denominator fallback. The docstring describes implementation behavior; mathematically the rate is undefined when its denominator is zero. |
| 130 | Returns the quotient if the denominator is truthy, otherwise `0.0`. For numeric zero this avoids division by zero. It is not general validation for NaN, infinity or negative denominators. |

### 8.5 Sidebar selection: lines 132-147

| Line(s) | What happens and why |
| --- | --- |
| 132 | Comment stating the important order: filter first, then calculate every KPI and chart. |
| 133 | Creates a sidebar heading for the controls. |
| 134 | Copies the source table into the working `filtered` variable so later derived columns do not overwrite `frame`. |
| 135 | Gets unique region names from the full source, sorts them for stable display, initially selects all, and assigns a unique widget key. The widget returns the current selected list. |
| 136 | `.isin(selected_region)` creates a True/False mask, and outer DataFrame indexing retains matching region rows. |
| 137 | Creates the category multiselect with the same pattern. Its choices come from full `frame`, even if a region has already been filtered out. |
| 138 | Further narrows current rows to selected categories, combining this condition with the earlier region choice. |
| 139 | Creates a date-range widget initialized and bounded by source min/max dates. `.date()` converts a Timestamp into a Python date suitable for the control. |
| 140 | Checks that the user has supplied both ends of the range before indexing the pair. |
| 141 | Displays instructions when a complete interval is not available yet. |
| 142 | Stops that incomplete run, avoiding an index error or ambiguous analysis period. |
| 143 | Extracts each timestamp's date with `.dt.date`, checks inclusive interval membership with `.between()`, and retains matching rows. |
| 144 | Displays selected and source row counts. The `:,` format adds separators but leaves the counts unchanged. |
| 145 | Checks whether the combined filter leaves zero rows. |
| 146 | Explains how to recover from an empty selection instead of displaying misleading zero totals or empty leader rankings. |
| 147 | Stops the empty-selection run. Everything below assumes at least one selected order. |

### 8.6 Measures, rankings and answer sentences: lines 149-175

| Line(s) | What happens and why |
| --- | --- |
| 149 | Comment introducing calculation of business measures and comparisons. |
| 150 | Creates a revenue value for each selected order from quantity, list price and the fraction remaining after discount. Column-wise arithmetic applies the formula to every selected row. |
| 151 | Creates each order's gross profit by subtracting total product cost, not merely one unit's cost, from its revenue. |
| 152 | Reduces the revenue Series to a scalar total using `.sum()`. The variable `revenue` is now a total; `filtered["revenue"]` remains a column. |
| 153 | Similarly reduces row gross profits to one selected total. |
| 154 | Creates four horizontal metric containers and stores them in `columns`. |
| 155 | Shows total net sales in the first container. `:,.0f` adds thousands separators and rounds only the displayed string to zero decimal places. |
| 156 | Shows gross profit in the second container with the same display format. |
| 157 | Shows total profit divided by total revenue. `:.1%` multiplies a fraction by 100 for display and adds a percent sign with one decimal; the stored ratio remains a fraction. |
| 158 | Shows mean order revenue in the fourth container. This is valid as average order value because one row is one order. |
| 159 | Adds an interpretation caption distinguishing discounted sales and gross profit from broader profit measures. |
| 160 | Groups orders by region and sums revenue, producing a region-indexed Series. |
| 161 | Builds a category-indexed table of summed sales, summed profit and row counts using named aggregations. |
| 162 | Divides category profit by category sales. Replacing zero denominators with `float("nan")` marks undefined group margins as missing rather than producing infinity. This differs from the scalar helper's zero fallback. |
| 163 | Converts dates to monthly periods and groups revenue by them; year and month stay together, so January of different years would not be merged. |
| 164 | Finds the region label at the highest regional sales value with `.idxmax()`. |
| 165 | Finds the category label at the highest category sales total. |
| 166 | Finds the category label at the highest defined category margin. This line assumes at least one margin is defined. |
| 167 | Starts a list of question-and-answer tuples, later reused for on-screen explanations and the exported report. |
| 168 | Builds the selected-scope answer from row count, total revenue, total profit and weighted total margin. The numbers are calculated, not manually typed findings. |
| 169 | Builds the leading-region answer, including its share of selected revenue. Series indexing by `top_region` retrieves that group's total. |
| 170 | Builds the leading-category revenue answer. `.loc[row_label, column_label]` retrieves the category's sales and order count from the summary table. |
| 171 | Builds the margin-leader answer using the category label and its aggregate margin. A wholly undefined margin column needs additional handling before this lookup could work on arbitrary data. |
| 172 | Builds the mean-versus-median answer to expose the influence of order-value distribution. |
| 173 | Builds the highest-month answer using `.idxmax()` for the period and `.max()` for the amount, then warns about partial months. |
| 174 | Closes the insights list. |
| 175 | Creates label/value pairs for report KPI rows, often with more decimal places than the metric cards. These are formatted strings for presentation, not replacement numeric columns. |

### 8.7 Scope and visible explanations: lines 177-194

| Line(s) | What happens and why |
| --- | --- |
| 177 | Comment explaining that the report should describe the same filtered table as the charts. |
| 178 | Creates an empty list to collect human-readable scope descriptions. |
| 179 | Iterates over source columns whose dtype is `object`, which includes the ordinary text columns in this CSV. |
| 180 | Includes only columns with at most 12 distinct source values, avoiding an enormous list of identifiers. This threshold is a display heuristic, not a business rule. |
| 181 | Replaces underscores in the field name, sorts distinct selected values, converts them to strings, joins them with commas, and appends one description to `scope_parts`. |
| 182 | Iterates over source datetime columns. In this project that includes parsed `order_date`. |
| 183 | Appends the earliest/latest **observed selected dates**, formatted as year-month-day. These may differ from requested boundaries if no order occurred on a boundary day. |
| 184 | Also records the user's requested date window, preserving both the control values and actual observed coverage. |
| 185 | Joins the separate scope descriptions with semicolons into one printable string. |
| 187 | Opens an expander for metric definitions. |
| 188 | Converts the list of formula tuples into a three-column DataFrame, displays it without its row index, and stretches it to the container width. |
| 189 | Explains that outputs share the selection, rates use appropriate totals, and zero-denominator fallbacks require interpretation. |
| 191 | Adds the section heading for calculated answers. |
| 192 | Iterates over only `insights[:3]`, a slice containing the first three question-answer pairs. The remaining insights still appear in the full report. |
| 193 | Displays each selected question in bold followed by its computed answer. |
| 194 | Displays selected/source row counts and the scope string beneath the answers. |

### 8.8 Build the downloadable report: lines 196-212

| Line(s) | What happens and why |
| --- | --- |
| 196 | Opens `report_parts`, a list whose elements are Markdown sections stored as strings. |
| 197 | Adds the report's top-level title. It becomes list position 0. |
| 198 | Adds section 1 using `CASE`; `\n` inserts a newline inside the resulting text. |
| 199 | Adds section 2 by combining decision context and dataset context, separated by a blank line (`\n\n`). |
| 200 | Adds section 3 with filename, row counts, current scope and a statement of descriptive/fictional status. |
| 201 | Adds the executive summary by joining the first three answer strings. The underscore variable ignores each question during tuple unpacking. |
| 202 | Builds a Markdown KPI table header and uses a generator expression to format one row for each `(name, value)` in `kpi_values`. |
| 203 | Builds a three-column definitions table from the three components of every `FORMULAS` tuple. This report section is list position 6, because the title occupies position 0. |
| 204 | Adds all six question-and-answer pairs as subheadings and answer text, including those not shown in the short summary. |
| 205 | Adds explanations for every visual by unpacking each five-item guide tuple. It exports written chart guidance, not the chart images themselves. |
| 206 | Adds source quality counts using full `frame`, not only selected rows, and describes what the checks can and cannot establish. `.duplicated().sum()` counts repeat rows after their first occurrence. |
| 207 | Numbers recommendation strings using `enumerate(RECOMMENDATIONS, 1)` and explicitly frames them as investigation steps. |
| 208 | Adds limitations, tie-handling information and cautions about confidence and correlation. No confidence interval is computed here. |
| 209 | Adds reproduction and extension instructions as static report text. |
| 210 | Closes the report section list. |
| 211 | Appends the field dictionary to `report_parts[5]`. Because indexing is zero-based and the title is element 0, this is actually the **KPI results section**, not Definitions and methods. The dictionary still appears in the report, but its placement follows this exact index. |
| 212 | Joins all report sections with blank lines into `full_report`, the single Markdown string displayed and downloaded later. |

### 8.9 Dashboard and exploratory charts: lines 214-240

| Line(s) | What happens and why |
| --- | --- |
| 214 | Creates four tabs and unpacks their containers into `overview`, `explore`, `data_tab` and `report_tab`. These names control output placement. |
| 215 | Enters the dashboard tab's output context. |
| 216 | `.assign()` creates a month label, `.dt.to_period("M")` extracts year-month, `.astype(str)` makes a chart-friendly string, and grouping sums revenue/profit. `as_index=False` keeps `month` as a normal column for Plotly. |
| 217 | Creates a Plotly line chart using `month` on x and two y columns, adds markers and INR labels, and renders the figure at container width. The chart receives already aggregated monthly data. |
| 218 | Calls guide entry 0 to explain the monthly line chart below it. |
| 219 | Groups by region and category simultaneously and returns one revenue total per present pair. |
| 220 | Creates a bar chart with region on x, revenue on y and category as color. Plotly's default relative bar layout stacks the category contributions for these positive values. |
| 221 | Renders guide entry 1 for the regional category mix. |
| 222 | Builds another category table with order count, total units, revenue and gross profit, rounds its displayed numbers to two decimals, and renders it. `orders` and `units` deliberately count different things. |
| 223 | Reminds readers to compare group sizes alongside totals or rates and inspect source observations when needed. |
| 224 | Enters the exploration tab's context. |
| 225 | Creates left and right containers so the first two exploratory plots appear side by side. |
| 226 | Creates a Matplotlib figure and axes, unpacked into `fig` and `ax`; `figsize=(7,4)` specifies inches for the underlying figure. |
| 227 | Draws a 20-bin histogram of order revenue, choosing a blue fill and white bin edges for readability. |
| 228 | Sets the histogram title and x/y labels, preserving the distinction between INR/order and order count. |
| 229 | Sends the figure to the left container, then closes its Matplotlib handle. The semicolon separates two statements on one physical line; closing avoids accumulating open figures across reruns. |
| 230 | Renders guide entry 2 in the left container beneath its histogram. |
| 231 | Creates a fresh figure and axes for the boxplot instead of reusing the histogram axes. |
| 232 | Draws category on x and individual order gross profit on y with Seaborn, explicitly targeting `ax` and selecting a uniform fill color. |
| 233 | Sets the boxplot's title and meaningful category/profit labels. |
| 234 | Displays the boxplot in the right container and closes the figure's Matplotlib handle. |
| 235 | Renders guide entry 3 under the boxplot in the right container. |
| 236 | Creates a wider figure and axes for the correlation matrix. |
| 237 | Selects four numeric measures, computes their Pearson correlation matrix and draws a heatmap. `annot=True` prints cell values, `fmt=".2f"` formats them, and `vmin=-1`, `vmax=1` fix a consistent scale. |
| 238 | Adds a descriptive title to the correlation axes. |
| 239 | Displays the heatmap in the tab's main area and closes the Matplotlib figure. |
| 240 | Renders guide entry 4 beneath the heatmap. |

### 8.10 Data inspection, exercises and export: lines 242-264

| Line(s) | What happens and why |
| --- | --- |
| 242 | Comment introducing underlying-data inspection and explanation practice. |
| 243 | Enters the Data and quality tab's output context. |
| 244 | Adds the field-dictionary heading. |
| 245 | Converts dictionary `.items()` pairs into a two-column DataFrame and displays readable field definitions without a numeric row index. |
| 246 | Adds the filtered-records heading. |
| 247 | Explains that this table contains the exact selected observations, including derived columns, and that browser table sorting does not change analytical filters. |
| 248 | Displays `filtered` as a table, hiding its pandas index and using available width. |
| 249 | Serializes `filtered` to CSV without its row index and provides a download named `filtered_retail_sales.csv` with MIME type `text/csv`. It does not overwrite the source file. |
| 250 | Adds the numeric-summary heading. |
| 251 | Explains count, average, spread, extremes and quartiles before displaying those statistics. |
| 252 | Selects only numeric columns, runs `.describe()`, rounds the displayed result to two decimals and renders it. Here derived revenue and profit are included. |
| 253 | Adds the source-quality heading. |
| 254 | Displays full-source row count, exact duplicate count and missing-cell count. Two `.sum()` operations reduce the missingness table first by column and then to one total. |
| 255 | Builds a new quality DataFrame containing each source column's name, dtype converted to text and missing-value count. `.values` supplies arrays aligned to the source column order. |
| 257 | Opens the workshop exercises expander outside the tab contexts. |
| 258 | Displays four numbered practice tasks using newline-separated Markdown text. These instructions are not automatically executed. |
| 259 | Explains the learning purpose of the three plotting libraries. |
| 260 | Adds a reminder to distinguish associations from cause and effect. |
| 262 | Enters the Full report tab's output context. |
| 263 | Offers `full_report` as a Markdown download with filename `01_retail_sales_report.md` and MIME type `text/markdown`. |
| 264 | Renders the same `full_report` string as Markdown inside the tab, so the visible report and its download share content. |

## 9. Data quality, edge cases and limits

### 9.1 What is checked

The loader catches missing/unreadable files, absent required columns, an empty dataset, dates or numeric fields that cannot be parsed, and missing values in required analysis columns. Filtering checks for an incomplete date interval and a selection containing no rows. These checks prevent several common beginner errors from becoming confusing chart failures.

Quality tables report missing cells and exact duplicate rows across the loaded source. They do not remove duplicates, fill missing data, repair labels, or prove that a row is accurate. A duplicate `order_id` with a changed amount is not an exact duplicate row and requires a separate uniqueness check. Rows with valid numbers but incorrect business meaning still need investigation.

### 9.2 What the current code does not validate

The current loader does not enforce positive quantities, nonnegative price/cost, whole-number quantities, finite numbers, a 0-100 discount range, known category labels, or unique order IDs. For example, a discount of 150 is numeric and nonmissing, so it passes these checks even though the documented discount convention is violated. Leading/trailing spaces in a region name can produce a separate group. Source data should be inspected before treating a successful render as proof of valid business data.

The `ratio()` helper safely substitutes `0.0` for a zero scalar denominator, but a zero sales denominator makes margin undefined, not a measured 0% profit margin. Group margins instead use NaN for zero sales. If every selected category has zero sales, all group margins can become NaN; the code's `.idxmax()` followed by `.loc[...]` does not guard that case. It may fail when building the margin-leader sentence. These guides document the current behavior rather than silently changing the app.

No exception handler surrounds the entire analysis after loading. A value that parses successfully but breaks a later operation is not covered by the initial `try` block. A small selection can also make a correlation undefined or a boxplot uninformative without representing an application defect.

### 9.3 How to phrase a useful conclusion

A strong conclusion states the selected scope, the measured result, a plausible investigation and the missing evidence. For example: "Across all 720 supplied teaching orders, North has the largest selected sales total. We should compare its order count, product mix and store coverage before interpreting that as stronger regional demand."

An unsupported conclusion would be: "North's manager is better" or "discounts cause customers to buy more." This dataset contains neither managerial-performance controls nor an experiment on discounts. The app also lacks customer identities, returns, store size, acquisition costs, operating expenses and tax. It cannot calculate repeat purchase, customer lifetime value, net profit or future demand from fields that do not exist.

Tied maximum values are another limit: `.idxmax()` names the first maximum encountered. With the source's default sorted grouping, that usually follows group-label order. A named leader therefore does not establish a unique winner when groups tie. Inspect the tables, especially after selecting a narrow sample.

## 10. Practice and worked examples

### Worked example 1: Explain the first order without running the app

**Task:** Use `ORD-0001` to calculate revenue and gross profit and identify which inputs determine them.

**Reasoning:** Its 7 units at INR 1,043.19 with no discount generate INR 7,302.33. Cost is 7 times INR 658.69, or INR 4,610.83. Gross profit is INR 2,691.50. `region` and `category` decide which groups include that order; they do not appear directly in its arithmetic formula.

### Worked example 2: Add a channel filter

**Task:** The source contains `channel`, but the sidebar currently filters only region, category and dates. How can you add Store/Online selection without making charts disagree with KPI cards?

**Suggested extension, not currently present in `app.py`:** Place this after the existing category filter and before derived measures are calculated:

```python
selected_channels = st.sidebar.multiselect(
    "Channels",
    sorted(frame["channel"].unique()),
    default=sorted(frame["channel"].unique()),
    key="01_retail_sales_channel",
)
filtered = filtered[filtered["channel"].isin(selected_channels)]
```

All downstream results already use `filtered`, so the new selection propagates to totals, plots, report and export. Do not add the filter only around one chart: that would make its scope different from the cards. Retain the empty-selection guard after all filters.

### Worked example 3: Compare North and South fairly

**Task:** Choose the same date interval for North and South. What should you compare beyond sales totals?

**Reasoning:** Compare order counts, average/median order values, category mix and aggregate margin. Larger sales may arise from more orders or more expensive categories. A comparison per store, customer or regional population requires fields absent from the CSV. Keep the date interval identical and report sample sizes so the comparison's scope is explicit.

### Worked example 4: Find high revenue with low margin

**Task:** Explain how a category can lead sales without leading margin.

**Reasoning:** Sales total depends on units and discounted prices. Margin also depends on the product costs relative to that revenue. Calculate category totals first, then `profit / sales`; do not average row margins. The supplied full dataset happens to have Electronics leading both sales and margin, so do not invent a different winner merely because the exercise asks you to investigate the possibility. Try legitimate filter changes and report what the selected data actually shows.

### Worked example 5: Change a discount as an arithmetic scenario

**Task:** In the invented two-unit example above, raise discount from 10% to 20% while holding quantity, list price and cost fixed.

**Reasoning:** Net sales become `2 * 1000 * 0.8 = 1600`; gross profit becomes `1600 - 1200 = 400`; margin becomes 25%. This is a calculation under explicit fixed-input assumptions. It does not predict how real customer demand would react to a larger discount, because the scenario fixes demand rather than estimating it.

### Worked example 6: Explain the two kinds of Markdown

**Task:** How does this file differ from the app's Download full report button?

**Reasoning:** `EXPLANATION.md` is a versioned teaching guide describing the code and methodology. `01_retail_sales_report.md` is generated at runtime from the current selection, with current results and scope. Editing this guide does not change app calculations, and changing a sidebar filter does not rewrite this file.

## 11. Troubleshooting

| Symptom | Likely reason and useful check |
| --- | --- |
| `ModuleNotFoundError` | The terminal is using an environment without a required library. Activate the intended environment and install the workshop versions with that interpreter's `python -m pip`. |
| Running `python app.py` does not give the normal app experience | Start the Streamlit runner with `python -m streamlit run app.py`. It establishes the server and script context. |
| The CSV cannot be loaded | Keep the correctly named `retail_sales.csv` beside `app.py`. The script resolves its neighbor, not an arbitrary CSV in the terminal's current directory. |
| A required-column error appears | Check spelling and capitalization in the CSV header. The field names are exact, such as `discount_pct` rather than `discount`. |
| Numeric or date parsing fails | Inspect the named field for text, invalid dates or symbols such as currency text embedded in numbers. Correct the source deliberately rather than replacing bad values with zero. |
| The app asks for an end date | Complete both ends of the date range; the guard intentionally stops until the interval is usable. |
| No rows match | Re-enable at least one category/region or widen the interval. Filter choices are drawn from the whole dataset, so not every combination must exist. |
| CSV edits are not visible yet | Save the CSV and rerun the app. Loading is uncached, but the next run still needs to be triggered. |
| A card and report show slightly different digits | Compare their formatting. Cards often round INR to whole numbers while the report keeps two decimals. Both use the same underlying selection and formulas. |
| Heatmap cells are blank after strong filtering | A constant column or very small sample cannot support a defined Pearson correlation. Restore a broader selection before interpreting a relationship. |
| Zero-valued edited data breaks a leader sentence | Check whether every category margin is undefined. The current leader lookup does not handle an all-NaN margin column. |
| Port 8501 is occupied in a Cloud Lab | Use the workshop's separate-instance example with port 8502 and open its forwarded port. |

## 12. Sources and further reading

Repository-specific statements and baseline calculations come from [this project's `app.py`](app.py), [its CSV](retail_sales.csv), the [workshop instructions](../README.md) and the [repository instructions](../../README.md), inspected at the source revision noted above. The official references below explain library behavior; they are references, not evidence about real retail performance. API documentation may describe releases newer than the pinned workshop environment, so use the project's versions when reproducing it.

- [Python `pathlib` documentation](https://docs.python.org/3/library/pathlib.html): paths, resolution and filename replacement.
- [Pandas: what kind of data does pandas handle?](https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/01_table_oriented.html): DataFrame and Series concepts.
- [Pandas indexing and selecting data](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html): column selection, Boolean masks and label-based access.
- [Pandas GroupBy guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html): grouping and named aggregation.
- [Pandas `DataFrame.corr`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.corr.html): pairwise correlations and defaults.
- [Streamlit architecture and concepts](https://docs.streamlit.io/develop/concepts/architecture/run-your-app): script execution and interaction.
- [Streamlit `st.tabs`](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs): tab containers and execution behavior.
- [Streamlit `st.download_button`](https://docs.streamlit.io/develop/api-reference/widgets/st.download_button): downloadable data and MIME types.
- [Matplotlib histogram reference](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html): binning and counts.
- [Matplotlib `close`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.close.html): releasing figure references.
- [Seaborn boxplot reference](https://seaborn.pydata.org/generated/seaborn.boxplot.html): quartiles, whiskers and outliers.
- [Seaborn heatmap reference](https://seaborn.pydata.org/generated/seaborn.heatmap.html): matrix visualization and annotations.
- [Plotly line charts](https://plotly.com/python/line-charts/) and [bar charts](https://plotly.com/python/bar-charts/): interactive chart construction from tabular data.
