# Inventory Planning Desk - business questions, analysis and code explained

This guide explains the **actual [app.py](app.py) in this folder**, together with its [inventory.csv](inventory.csv). It connects each inventory question to the calculation, Python statement and dashboard element that answers it.

The source examined is commit [c10a61c36fffdd048b69dd78926e6663bc986fce](https://github.com/cookieSensei/programming-and-ai/blob/c10a61c36fffdd048b69dd78926e6663bc986fce/business_analytics_workshop/04_inventory_planning/app.py). Line references below use that version. The file contains **180 fictional SKU-location records for 60 SKUs in three warehouses**. This is a teaching scenario, not a live stock ledger or an automated ordering system.

Numbers identified as bundled-data results were recalculated from the accompanying CSV with all warehouses and categories selected. The default extra safety buffer is zero days. Changing the file, filters or buffer changes the corresponding results.

## Contents

1. [The inventory problem and the purpose of the dashboard](#1-the-inventory-problem-and-the-purpose-of-the-dashboard)
2. [Understand the data and its units](#2-understand-the-data-and-its-units)
3. [Why pandas and the other libraries are used](#3-why-pandas-and-the-other-libraries-are-used)
4. [Derive the formulas and work through examples](#4-derive-the-formulas-and-work-through-examples)
5. [How the calculation becomes a Streamlit application](#5-how-the-calculation-becomes-a-streamlit-application)
6. [Read every line of app.py](#6-read-every-line-of-apppy)
7. [Read the five charts and the replenishment worklist](#7-read-the-five-charts-and-the-replenishment-worklist)
8. [Validation, model assumptions and current limitations](#8-validation-model-assumptions-and-current-limitations)
9. [Run the app and reproduce its results](#9-run-the-app-and-reproduce-its-results)
10. [Practice, troubleshooting and extensions](#10-practice-troubleshooting-and-extensions)
11. [Sources and API references](#11-sources-and-api-references)

## 1. The inventory problem and the purpose of the dashboard

An operations manager has two competing concerns. Too little stock may leave customer demand unmet; too much stock holds money in products that may sit unused. Looking at one grand total does not resolve either concern. A warehouse can hold substantial inventory value while a particular product is close to running out.

This project examines stock at the level where that problem occurs: **one SKU at one warehouse**. It estimates how much demand the current stock could cover, calculates a simple replenishment threshold, and lists the locations below that threshold. A slider adds extra days of demand to the threshold so the learner can see how a more conservative assumption changes suggested units and purchase cost.

A **SKU**, or stock keeping unit, identifies a product type in this example. A SKU can be stocked in multiple warehouses. Delhi's stock of SKU-001 cannot be assumed to be immediately available to a customer served from Mumbai. That is why location remains part of the record's identity.

### What each business question requires

| Business question | Calculation or transformation | Output in the app | Why this solves the stated question |
| --- | --- | --- | --- |
| How much stock value is represented? | Add `stock_on_hand * unit_cost` across selected rows | Stock-value KPI and warehouse bar chart | It converts physical units into a common monetary basis before adding different products. |
| Which locations are below the scenario threshold? | Compare current units with demand over lead time plus buffers | Reorder-count KPI, colored scatter and worklist | The comparison is performed for each SKU-location pair rather than hidden inside a total. |
| How many units does the rule suggest? | Positive gap between threshold and current stock | Suggested-units KPI and worklist | A location above threshold contributes zero rather than a negative order. |
| What would those units cost? | Sum each suggested quantity multiplied by its own unit cost | Purchase-cost KPI and report | Expensive and inexpensive products are costed individually before totals are added. |
| How long could current stock last? | `stock_on_hand / daily_demand` | Days-cover histogram and category boxplot | The ratio converts units into days under the assumed constant demand. |
| Where is the review workload concentrated? | Mean of a Boolean reorder flag within warehouse/category cells | Heatmap | Averaging True/False flags gives the share of locations flagged in each cell. |
| What changes when extra safety days increase? | Recalculate the rule and compare purchase cost with buffer zero | Slider, KPIs and report | It isolates the effect of the selected buffer while keeping the selected records fixed. |

The app's **solution** is a transparent review process. It makes the rule, inputs, outputs and assumptions visible. It does not discover the mathematically optimal inventory policy, estimate future demand from history, negotiate with suppliers or place purchase orders.

The decision it supports is: “Which locations should we investigate, and how much additional purchasing does this chosen buffer imply?” Before ordering stock, an operations team would still need information such as inbound orders, supplier constraints, demand variability, stock transfers and service targets.

### Why a total alone would mislead

Suppose two locations each have the same inventory value. One might sell its stock within two days, while the other might take six months. Cost value answers “How much value is held?” Days cover answers “How much demand could this stock serve under the assumption?” A reorder flag answers “Is the stock below this particular threshold?”

These are related but different questions. The dashboard keeps separate columns and visuals because no single measure answers them all.

## 2. Understand the data and its units

### One row is a SKU-location pair

The bundled data contains 60 distinct SKUs, each represented at Delhi, Mumbai and Bengaluru, giving 180 rows. The pair `(sku, warehouse)` identifies a row. Repeated `sku` values across warehouses are expected.

The complete file has no duplicate SKU-warehouse pairs, no exact duplicate rows and no missing source cells. Those properties were checked for this guide. The app's validation is narrower than that full check, as explained later.

Counting `len(filtered)` means counting selected **SKU locations**. Counting `filtered["sku"].nunique()` means counting distinct product codes. With all data selected, the results are 180 and 60. With only Delhi selected, they are both 60. Their difference is caused by the grain, not an arithmetic error.

### Source field dictionary

| Column | Meaning and unit | Where it enters the analysis | Important interpretation |
| --- | --- | --- | --- |
| `sku` | Product identifier such as SKU-001 | Hover labels, worklist and distinct-SKU count | Repeats across locations are legitimate. |
| `warehouse` | Delhi, Mumbai or Bengaluru | Filter, grouping and heatmap row | A location is part of the row's identity. |
| `category` | Electronics, Home, Fashion or Grocery | Filter, stacked bars, boxplot and heatmap | Category totals combine several product types. |
| `stock_on_hand` | Units currently held at that location | Value, cover, gaps and stockout count | A snapshot of current stock, not inventory position including incoming orders. |
| `daily_demand` | Assumed units per day | Lead-time demand, extra buffer and cover | Supplied as an input; the app does not fit a forecast. |
| `lead_time_days` | Assumed replenishment lead time, in days | Demand expected during supplier lead time | Treated as fixed, not a distribution of delivery delays. |
| `safety_stock` | Baseline safety inventory, in units | Added to the threshold | Already a quantity; it must not be mistaken for days. |
| `unit_cost` | Cost per unit, in INR/unit | Current inventory value and proposed purchase cost | Does not include all procurement or carrying costs. |

### Derived columns

The app creates five new columns after filters are applied:

| Added column | Unit/type | Meaning |
| --- | --- | --- |
| `reorder_point` | Units | The selected scenario's threshold: lead-time demand, extra buffer demand and baseline safety stock. |
| `reorder_units` | Units | The positive gap from current stock to that threshold. |
| `inventory_value` | INR | Current units multiplied by the row's unit cost. |
| `days_cover` | Days, possibly missing | Current units divided by assumed daily demand; zero demand is deliberately made undefined. |
| `needs_reorder` | Boolean | True when the suggested top-up is greater than zero. |

The extra `buffer` is a scalar: one selected number of days applied across every currently selected row. It is not an additional CSV column. Each row responds differently because its daily demand, lead time and current stock differ.

### Start with an actual CSV record

The first row is:

| Field | Value |
| --- | --- |
| SKU and warehouse | SKU-001 at Delhi |
| Category | Electronics |
| Stock on hand | 316 units |
| Daily demand | 19 units/day |
| Lead time | 12 days |
| Safety stock | 27 units |
| Unit cost | INR 1,103/unit |

These units explain the formulas. Multiplying units/day by days gives units. Multiplying units by INR/unit gives INR. Dividing units by units/day gives days. Dimensional reasoning is a useful way to catch business errors before looking at Python syntax.

## 3. Why pandas and the other libraries are used

### Their responsibilities are different

| Tool | What it contributes | Example from this app |
| --- | --- | --- |
| Python | Variables, control flow, functions and formatted text | Build a different insight sentence when no location needs a top-up. |
| `pathlib.Path` | File location | Locate `inventory.csv` beside the script. |
| pandas, `pd` | Table loading, validation, filtering and calculations | Calculate a separate threshold for each SKU-location row. |
| Streamlit, `st` | Interactive browser interface | Return selected warehouses and buffer days from widgets. |
| Plotly Express, `px` | Interactive figures | Hover over a stock-demand point to inspect its SKU and threshold. |
| Matplotlib, `plt` | Figure and axes control | Construct the days-cover histogram and close figures after rendering. |
| Seaborn, `sns` | Statistical views on Matplotlib axes | Compare category distributions and draw the reorder-share heatmap. |

You could perform the arithmetic in a spreadsheet or with Python loops. Pandas is useful because the data is already a table and the same operations must be applied consistently to many records. It keeps the code close to the analytical question.

The project intentionally uses three plotting libraries to teach different ways of building visuals. An inventory dashboard does not inherently require all three; these are the tools chosen by this particular workshop implementation.

### A table, a column and a mask

`pd.read_csv(DATA_FILE)` creates a DataFrame named `frame`. A DataFrame is a table with labeled columns and an index. One selected column, such as `frame["daily_demand"]`, is a Series.

```python
frame["warehouse"]                         # One column
frame[["sku", "warehouse"]]                 # A table containing two columns
frame["warehouse"] == "Delhi"               # A True/False value per row
frame[frame["warehouse"] == "Delhi"]         # Only the Delhi rows
```

A Boolean mask has one decision per row. `.isin(selected_warehouse)` makes the decision “Does this row's warehouse belong to the list the user selected?” The outer DataFrame selection keeps True rows.

Both warehouse and category filters are applied before the calculations. Therefore the cards, chart data and generated answers describe the same selected population. Sorting an on-screen table later does not change that population.

### Vectorized arithmetic is row-by-row arithmetic expressed once

Consider the actual formula:

```python
filtered["reorder_point"] = (
    filtered["daily_demand"]
    * (filtered["lead_time_days"] + buffer)
    + filtered["safety_stock"]
)
```

Each named column is a Series. Pandas performs the operation across aligned rows: row A's demand multiplies row A's lead time plus the shared buffer, then row A's safety stock is added. It does not multiply a grand total of demand by a grand total of lead time.

That distinction matters because products have different lead times. In general:

```text
sum(demand_i * lead_time_i)
is not the same as
sum(demand_i) * sum(lead_time_i)
```

The subscript `i` in this explanatory notation means “for each row.” It is not a variable used in the app.

### Grouping changes the grain of the result

```python
grouped = filtered.groupby(
    ["warehouse", "category"],
    as_index=False,
)["inventory_value"].sum()
```

This takes the selected SKU-location rows, collects rows with the same warehouse/category pair, and sums their monetary values. The result has one row per warehouse/category combination. That is the proper input for a stacked bar that shows total value, not individual stock items.

`as_index=False` keeps the group names as regular columns, which Plotly can reference with `x="warehouse"` and `color="category"`. Without it, group labels would normally form the index. Neither option changes the business definition of the sum.

A pivot table takes the grouped result into a matrix layout:

```python
filtered.pivot_table(
    index="warehouse",
    columns="category",
    values="needs_reorder",
    aggfunc="mean",
) * 100
```

The Boolean mean counts True as 1 and False as 0. A cell with 4 True values among 15 records becomes 4 / 15 * 100 = 26.6667%. This measures the share of locations requiring review under the rule, not the share of stock units or money.

The [pandas introduction](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html) explains Series/DataFrames, while the [grouping guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html) explains these aggregation operations.

### Reading common syntax

- `=` assigns a result; `==` compares values. The stockout check uses equality to zero.
- `> 0` creates the reorder flag. A gap exactly equal to zero is not flagged.
- `.sum()` reduces many values to one total; `.mean()` reduces them to an average.
- `.clip(lower=0)` replaces negative gap values with zero while retaining positive gaps.
- `.loc[mask, columns]` selects specified rows and fields by labels.
- `.iloc[0]` selects the first row by position after sorting.
- `f"{value:,.0f}"` displays commas and no decimals; it does not round the stored value used by later arithmetic.
- `if condition else other_value` chooses between two expressions.
- `with` and indentation direct Streamlit output into an expander, tab or other container.

## 4. Derive the formulas and work through examples

### A. Current stock value

For one record:

**Inventory value = stock on hand × unit cost.**

For SKU-001 at Delhi:

```text
316 units × INR 1,103/unit = INR 348,548
```

The app computes that product for every selected row and adds the products. This is cost value of current stock. It is not retail selling value, sales revenue or cash immediately available to spend.

The complete bundled file totals **INR 55,448,799**, distributed as:

| Warehouse | Current stock value, INR |
| --- | ---: |
| Bengaluru | 19,865,405 |
| Delhi | 17,190,670 |
| Mumbai | 18,392,724 |
| Total | 55,448,799 |

A high value alone does not prove excess stock. An expensive product, high demand or a long supplier lead time could explain it.

### B. Reorder point and its units

The app's rule is:

**Reorder point = daily demand × (lead time days + extra buffer days) + safety stock.**

It adds three components:

1. Expected demand during lead time.
2. Additional demand corresponding to the user-selected extra days.
3. Baseline safety stock already supplied in units.

For SKU-001 at Delhi with buffer zero:

```text
19 × (12 + 0) + 27 = 255 units
```

With buffer seven:

```text
19 × (12 + 7) + 27 = 388 units
```

Why is this a threshold rather than a prediction? The demand and lead-time inputs are taken as given. The app calculates the consequences of those assumptions; it does not learn them from sales history or produce a probability that stock will run out.

### C. Suggested top-up and why negative gaps become zero

**Suggested units = max(reorder point - stock on hand, 0).**

The code uses:

```python
(filtered["reorder_point"] - filtered["stock_on_hand"]).clip(lower=0)
```

At buffer zero, the first record's gap is 255 - 316 = -61. The app suggests zero units, not an order of -61. At buffer seven, its gap is 388 - 316 = 72, so it suggests 72 units.

Clipping represents a business rule: this calculation recommends top-ups only. It does not automatically recommend returning, liquidating or transferring surplus stock.

The app names the threshold `reorder_point` and also uses it as the target for the proposed top-up. Some inventory policies distinguish a reorder trigger from a separate order-up-to target. This teaching app uses one threshold for both roles; it does not implement those more elaborate policies.

### D. Estimated purchase cost

For each selected record:

**Suggested purchase cost = suggested units × that row's unit cost.**

For the first record at buffer seven:

```text
72 × INR 1,103 = INR 79,416
```

The total is the sum of those row-specific costs. Multiplying total units by an unweighted average unit cost would generally give the wrong result because the proposed quantities differ between products.

The cost is approximate: shipping, supplier discounts, taxes, order multiples and minimum quantities are not modeled. No purchase is executed.

### E. Days of cover

**Days cover = stock on hand / daily demand.**

For the first record:

```text
316 units / 19 units per day = 16.6316 days
```

Days cover is unaffected by the extra buffer slider. The slider changes the replenishment rule, not the current stock or assumed daily demand.

If daily demand were zero, the app replaces that denominator with `NaN`, a missing numeric value, before division:

```python
filtered["stock_on_hand"].div(
    filtered["daily_demand"].replace(0, float("nan"))
)
```

This avoids presenting an infinite number as an ordinary cover value. The histogram then explicitly drops missing cover values. Such a row can still have stock value and can still enter the reorder rule through its baseline safety stock. Zero demand is absent from the bundled file, but the code includes this handling for future edits.

### F. Stockout and reorder are different conditions

The stockout count uses:

```python
(filtered["stock_on_hand"] == 0).sum()
```

The reorder count uses:

```python
filtered["needs_reorder"].sum()
```

A stockout is zero current stock. A reorder flag means current stock is below the chosen rule's threshold. A location may still have units available and nevertheless need replenishment before demand uses them up.

The bundled file has **zero zero-stock locations** but **53 locations flagged at buffer zero**. There is no contradiction: the rule anticipates replenishment before stock necessarily reaches zero.

### G. A second actual record makes the worklist concrete

With all filters selected and buffer zero, the largest suggested quantity is **SKU-051 at Mumbai**:

| Input or result | Value |
| --- | ---: |
| Stock on hand | 65 units |
| Daily demand | 25 units/day |
| Lead time | 14 days |
| Baseline safety stock | 10 units |
| Unit cost | INR 1,528/unit |
| Threshold at buffer zero | 25 × 14 + 10 = 360 units |
| Suggested top-up | 360 - 65 = 295 units |
| Estimated top-up cost | 295 × 1,528 = INR 450,760 |
| Current days cover | 65 / 25 = 2.6 days |

The record has positive stock, so it is not a stockout. Its cover is short compared with the assumed lead time, so it is an obvious candidate for investigation under this rule. The app still lacks information about an already scheduled inbound delivery that might resolve the issue.

### H. Compare scenarios with the same selected population

Complete-file results are:

| Extra safety days | Flagged SKU locations | Suggested units | Estimated purchase, INR | Extra cost above buffer zero, INR |
| --- | ---: | ---: | ---: | ---: |
| `0` | 53 | 5,065 | 5,866,261 | 0 |
| `3` | 69 | 8,043 | 9,800,855 | 3,934,594 |
| `7` | 87 | 12,996 | 16,314,861 | 10,448,600 |
| `14` | 112 | 24,486 | 31,040,854 | 25,174,593 |

These are deterministic calculations from the bundled teaching records, not recommended purchase commitments.

The app always calculates `base_purchase` using zero extra buffer on the **same filtered rows**. It compares the current scenario with that fixed baseline. If warehouse/category filters change, both the baseline and the current scenario change together.

Extra cost need not increase by the same amount for every added day. A well-stocked location can remain below zero in the raw gap for several days of buffer, contributing no top-up until its threshold passes current stock. After that crossing, further buffer days add demand-weighted units. With the bundled nonnegative inputs, increasing the buffer cannot reduce suggested units, but the relationship is not a single straight line across all locations.

## 5. How the calculation becomes a Streamlit application

### The pipeline

The script starts with data loading, then passes through checks and selections before producing results:

1. **Locate and load:** read the CSV beside the script.
2. **Validate:** ensure required columns, parse numbers and reject missing required cells.
3. **Select:** obtain warehouse/category choices from sidebar widgets and keep matching rows.
4. **Guard against empty input:** explain an empty selection and stop the current run.
5. **Set a scenario:** read extra safety days from a slider.
6. **Calculate:** add row-level measures, summarize them and build the narrative.
7. **Present:** render cards, charts, a worklist, source tables and report.
8. **Export:** provide selected rows and generated Markdown as downloads.

The code is still Python. Streamlit supplies the app runtime and browser interface around its widget and display calls. There is no separate HTML template, JavaScript application, database schema or supplier API in this folder.

### A widget is also a Python value

`st.sidebar.multiselect(...)` displays a control and returns a list of selected categories. `st.sidebar.slider(...)` returns the selected integer buffer. Those return values are ordinary Python variables that subsequent statements use.

In the workshop's Streamlit 1.50 setup, a normal widget change reruns the script from the top. The existing widget identities preserve the relevant selections, the CSV is reread, filters are reapplied and outputs are recalculated. There is no separate “calculate” button.

The CSV read is uncached: no `@st.cache_data` decorator is used. A saved CSV change is picked up on the next run. Saving the CSV does not by itself guarantee an automatic app rerun; rerun the app or change a widget after saving.

`st.stop()` stops the current script execution when a guard fails. It does not shut down the Streamlit server. The user can restore a valid selection and cause another run.

Plotly hover/zoom, viewing a different tab, and sorting a displayed table are presentation interactions; they are not new analytical filters added to `filtered`. Sidebar selections and the buffer are the controls that explicitly drive the current calculations.

### Tabs and columns arrange the same analysis

The four tabs are Inventory dashboard, Explore the data, Data and quality, and Full report. `with overview:` directs display calls into the first tab. `left.pyplot(fig)` directs a Matplotlib figure into a column.

In [Streamlit 1.50](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs), all tab content is computed even when a tab is not visible. Putting a calculation inside a tab does not defer it until that tab is clicked.

### Reports and exports remain tied to the selection

The app builds `full_report` from constants, formatted KPI values, scope and question-answer pairs. The twelve numbered sections explain the data, methods, findings, chart meanings, limitations and reproduction. The same string is rendered and downloaded, so those two versions match the current run.

The static teaching guide you are reading is different: it explains the implementation and default examples. It does not recalculate with the slider.

The filtered CSV includes the five added analytical columns. The Markdown report includes descriptions of the charts rather than embedded chart images. Downloading either file does not modify the source CSV, place an order or write changes back to GitHub.

## 6. Read every line of app.py

Open [app.py](app.py) with line numbers enabled. Every nonblank source line is accounted for below. Ranges group literal continuations that make one definition; ordinary executable statements are explained separately. Blank lines only divide sections visually. Fragments shown in explanations identify the expression and are not substitutes for the complete source.

### Lines 1-13: imports and page setup

| Line(s) | What the line does and why |
| --- | --- |
| 1 | The module docstring labels the project as a fictional teaching example. It documents the file without displaying a page element. |
| 2 | Imports `Path` from Python's standard library so the CSV can be located relative to the script. |
| 4 | Imports Matplotlib's plotting interface as `plt` for creating figures, drawing the histogram and closing figures. |
| 5 | Imports pandas as `pd` for reading and manipulating the inventory table. |
| 6 | Imports Plotly Express as `px` for concise interactive chart construction. |
| 7 | Imports Seaborn as `sns` for the category boxplot and warehouse/category heatmap. |
| 8 | Imports Streamlit as `st` to create widgets, layouts, messages and downloads. |
| 10 | Sets the browser page title, icon and wide layout. These settings change presentation, not the inventory rule. |
| 11 | Displays the large visible title. |
| 12 | Displays workshop context, the fictional-data label and INR currency unit. |
| 13 | Introduces replenishment analysis and the purpose of changing the safety buffer. |

### Lines 15-77: case, definitions and chart-reading guidance

| Line(s) | What the line does and why |
| --- | --- |
| 15 | Comment explains the role of the following case-study definitions. |
| 16-17 | `CASE` stores the tension between availability and cash in stock, and why totals can hide local shortages. Adjacent strings form one string. |
| 18-19 | `DECISION` defines the supported task: build a review list and compare buffer implications. |
| 20-22 | `DATA_CONTEXT` explains SKU-location grain, 180 records, 60 SKUs, the three warehouses and demand as an assumption. |
| 23-25 | Starts `FORMULAS` with the stock-value name, multiplication rule and cost-value interpretation. |
| 26-28 | Adds the deterministic reorder-point definition and its units. |
| 29-31 | Adds the positive-gap formula for suggested units and notes that existing orders are ignored. |
| 32-34 | Adds the days-cover ratio and constant-demand assumption. |
| 35-37 | Adds estimated purchase cost and exclusions, then closes the definition list. |
| 38-43 | Starts `VISUAL_GUIDE` with warehouse value: purpose, axes, category colors, question and the warning that high value is not automatically excess. |
| 44-49 | Adds the stock-demand scatter guide, explaining one bubble per SKU-location, status color, cost size and scenario dependence. |
| 50-56 | Adds the cover-histogram guide, its days unit and explicit exclusion of undefined zero-demand cover. |
| 57-62 | Adds the category boxplot guide: median, quartiles, whiskers and differences in justified coverage. |
| 63-69 | Adds the reorder-share heatmap guide, fixed percentage scale and equal-location weighting; closes the visual-guide list. |
| 70-71 | Begins `RECOMMENDATIONS` with review of zero stock, large proposals, customer commitments and incoming stock. |
| 72 | Adds comparison of scenarios and incremental cash requirement. |
| 73-74 | Adds the operational inputs needed for a more realistic model and closes the list. |
| 75-77 | `LIMITATIONS` records fixed demand/lead time and omitted order, supplier, expiry and transfer considerations; it states that the dashboard places no purchase. |

These strings are reusable content. The later report and explanation helper consume them. Defining a formula in a string does not execute the arithmetic; lines 142-158 implement the calculations.

### Lines 79-102: show the context and define explanation reuse

| Line(s) | What the line does and why |
| --- | --- |
| 79 | Opens an initially expanded context section. Indented display calls appear inside it. |
| 80 | Displays the problem label and `CASE`. |
| 81 | Displays the supported decision and `DECISION`. |
| 82 | Displays the row definition and `DATA_CONTEXT`. |
| 83 | Shows a callout emphasizing that calculations describe selected fictional records. |
| 84 | Explains how to read the page and that filters update findings and report. |
| 87 | Starts `FIELD_GUIDE` with the SKU definition and its valid repetition across warehouses. |
| 88 | Describes warehouse and the composite row identity. |
| 89 | Describes product category. |
| 90 | Defines current stock in units. |
| 91 | Defines assumed demand in units/day and states that the app does not fit a forecast. |
| 92 | Defines supplier lead time in days. |
| 93 | Defines baseline safety stock in units. |
| 94 | Defines cost per unit in INR and closes the dictionary. |
| 96 | Defines `explain_visual(index, container=st)`. The function is used later with either the main context or a column container. |
| 97 | Retrieves one visual-guide tuple and unpacks its five fields. |
| 98 | Displays a bold title using a formatted string. |
| 99 | Writes the visual's purpose. |
| 100 | Displays axis/reading instructions with a bold label. |
| 101 | Displays the business question. |
| 102 | Displays the interpretation limit in a caption. |

### Lines 104-126: read and validate the CSV

| Line(s) | What the line does and why |
| --- | --- |
| 104 | Comment explains that the loader follows the script location rather than the terminal directory. |
| 105 | Comment records the deliberate uncached read for student editing. |
| 106 | Resolves `__file__` to this script's path and substitutes `inventory.csv` as the sibling filename. |
| 107 | Starts the loading `try` block so anticipated input failures can become useful browser messages. |
| 108 | Parses the CSV into a pandas DataFrame called `frame`. |
| 109 | Comment states that the snapshot has no date filter. It is not a time series. |
| 110 | Lists the five fields requiring numeric conversion. |
| 111 | Lists all eight required field names. Extra columns are not prohibited. |
| 112 | Tests whether every required name belongs to the actual column index. A missing name enters the error branch. |
| 113 | Raises a descriptive `ValueError` for missing columns. |
| 114 | Checks whether the source table has zero rows. |
| 115 | Raises an error for an empty table. |
| 116 | Iterates through numeric field names. |
| 117 | Converts the current field with `pd.to_numeric(..., errors="raise")` and stores it back. Text that cannot be interpreted numerically produces an error. |
| 118 | Checks for any missing required cell by reducing a Boolean missingness table first by column and then across columns. |
| 119 | Raises an error rather than silently discarding incomplete inventory records. |
| 120 | Handles the listed OS/file, value and key errors arising inside this block and names the exception `error`. It does not catch arbitrary later chart failures. |
| 121 | Displays the source filename and error explanation. |
| 122 | Ends this script run, preventing downstream calculations on unusable input. The server remains available. |
| 124 | Defines a scalar `ratio` helper used later for a warehouse's share of total value. |
| 125 | Documents its zero-denominator fallback. |
| 126 | Divides if the denominator is nonzero; otherwise returns `0.0`. A fallback zero prevents a division error but is not evidence that an undefined share is mathematically zero. This is not the days-cover implementation. |

### Lines 128-138: define the selected population

| Line(s) | What the line does and why |
| --- | --- |
| 128 | Comment marks filtering before calculations. |
| 129 | Displays the sidebar heading. |
| 130 | Starts a working copy of the source so derived columns and selections can be kept separate from whole-source inspection. |
| 131 | Builds a warehouse multiselect from sorted unique source warehouses, selects all initially, assigns a stable key and stores the returned choices. |
| 132 | Uses `.isin` to keep rows whose warehouse is selected. |
| 133 | Builds a category multiselect from all source categories with all initially selected and its own key. It does not restrict the options to the already-selected warehouses. |
| 134 | Keeps remaining rows whose category is selected. The two conditions therefore act together. |
| 135 | Displays selected versus source row counts. These are SKU-location counts, not unique SKU counts. |
| 136 | Tests whether the filters left an empty table. |
| 137 | Displays a generic empty-selection message. Its date-range suggestion is reused wording; this particular app has no date filter. |
| 138 | Stops before totals, rankings and positional selection run on an empty DataFrame. |

### Lines 140-168: calculate the scenario and its narrative

| Line(s) | What the line does and why |
| --- | --- |
| 140 | Comment starts derived business measures. |
| 141 | Creates the extra safety-buffer slider from 0 to 14 days, initially 0, using an integer step by inference from the integer arguments. The return value is `buffer`. |
| 142 | Calculates each row's threshold from demand over lead time plus extra days, then adds baseline safety units. The scalar buffer is applied across all selected rows. |
| 143 | Subtracts current stock from the threshold and clips negative differences to zero, producing suggested top-up units. |
| 144 | Calculates current cost value for each row from units and cost/unit. |
| 145 | Replaces zero demand with missing before dividing stock by demand. Undefined cover remains `NaN` instead of an ordinary finite value. |
| 146 | Compares proposed quantity with zero to create a Boolean reorder flag. Equality to zero produces False. |
| 147 | Creates four metric containers. |
| 148 | Adds all selected inventory values and displays the sum as INR with no decimals. |
| 149 | Adds Boolean reorder flags to count True rows. It counts SKU locations needing a top-up, not distinct product codes. |
| 150 | Adds proposed quantities and formats the displayed total with no decimals. This display format does not force every stored quantity to an integer. |
| 151 | Multiplies proposed units by each row's cost, sums the products and displays the current scenario's estimated purchase cost. |
| 152 | Places the row grain, threshold formula and important omitted inputs beside the KPIs. |
| 153 | Groups cost value by warehouse and sums it, yielding one monetary total per selected warehouse. |
| 154 | `idxmax()` returns the warehouse label at the largest total. It returns a label, not the monetary value. |
| 155 | Counts rows with current stock exactly zero and converts the result to a plain integer for narrative use. |
| 156 | Recalculates proposed units with zero extra buffer on the same selected records. This establishes a comparable baseline. |
| 157 | Costs those baseline proposals and sums them into `base_purchase`. |
| 158 | Costs the current proposals and stores their total as `purchase` for reuse. |
| 159 | Sorts selected rows by proposed quantity descending and takes the first row by position. The earlier empty check guarantees a row exists. No explicit secondary tie-break column is specified. |
| 160 | Starts the six-entry `insights` list of question-and-answer tuples. |
| 161 | Reports selected location count, distinct SKU count and current stock value, explaining why a SKU can be repeated. |
| 162 | Reports the leading warehouse's value and its share of total selected value using the scalar `ratio` helper. |
| 163 | Reports reorder flags and current zero-stock counts as separate conditions. |
| 164 | Reports proposed units and cost and states that no order is placed. |
| 165 | Subtracts the zero-buffer baseline cost from the current cost and includes the chosen buffer days. |
| 166 | Uses the largest row to describe the biggest proposed quantity if positive; otherwise gives the no-positive-suggestion message. The conditional expression avoids calling a zero-gap row a replenishment requirement. |
| 167 | Closes the insight list. |
| 168 | Creates the report KPI list: current value, flagged locations, proposed units, purchase cost and extra buffer. The first and fourth values retain two decimals in the report. |

### Lines 170-187: build analysis scope and preview findings

| Line(s) | What the line does and why |
| --- | --- |
| 170 | Comment explains that the report shares the charts' filtered table. |
| 171 | Creates an empty list of scope descriptions. |
| 172 | Iterates through object-typed source columns such as SKU, warehouse and category. |
| 173 | Restricts short scope descriptions to fields with at most 12 distinct values in the source. The bundled 60-SKU field is therefore skipped. |
| 174 | Appends a human-readable field label and sorted selected values. Replacing underscores changes only displayed text. |
| 175 | Iterates through source datetime columns if any exist. The bundled inventory table has none. |
| 176 | Would append observed date bounds for a datetime column. The loop does nothing for this CSV; it does not invent an inventory date. |
| 177 | Joins the scope descriptions with semicolons. |
| 178 | Appends the selected extra safety days, because that scenario parameter is necessary to reproduce the proposals. |
| 180 | Opens the calculation-definition expander. |
| 181 | Turns `FORMULAS` into a three-column table and displays it without an index. |
| 182 | Explains shared selection scope, ratio aggregation and zero-denominator interpretation. |
| 184 | Adds the short findings heading. |
| 185 | Iterates over the first three insights, not the whole list. |
| 186 | Displays each question in bold followed by its calculated answer. |
| 187 | Adds source/selected row counts and the scope including the buffer. |

### Lines 189-205: construct the full Markdown report

| Line(s) | What the line does and why |
| --- | --- |
| 189 | Starts a list of report-section strings. |
| 190 | Adds the top-level report title; this occupies list index 0. |
| 191 | Adds numbered section 1 with the stored business problem. |
| 192 | Adds section 2 with decision and row context, separated with line breaks. |
| 193 | Adds section 3 with filename, selected/source counts, scope and teaching-data limitations. |
| 194 | Adds section 4 by joining the first three calculated answers into an executive summary. The question field is ignored in this generator expression. |
| 195 | Adds section 5 as a Markdown KPI table created from `kpi_values`. |
| 196 | Adds section 6 as a definition/method table created from `FORMULAS`. |
| 197 | Adds section 7 with all six questions and their answers, including buffer cost and largest proposed quantity. |
| 198 | Adds section 8 by formatting each visual-guide tuple into title, purpose, reading, question and caution text. Chart images are not embedded. |
| 199 | Adds section 9 with whole-source duplicate/missing counts and a description of what the checks can establish. |
| 200 | Adds section 10 by numbering recommendations from 1 and qualifying them as investigation steps. |
| 201 | Adds section 11 with limitations and generic tie/statistical cautions. The group-order tie statement fits the warehouse `idxmax` leader; it does not supply a missing tie-break rule for line 159's row sort. |
| 202 | Adds section 12 with reproduction and extension instructions. Generic references to periods or correlation do not mean this snapshot app calculates a time trend or correlation matrix. |
| 203 | Closes the report-section list. |
| 204 | Appends the field dictionary to `report_parts[5]`. Because index 0 is the title, index 5 is the **KPI results section**, not the definitions section. |
| 205 | Joins sections with blank lines into `full_report`, the string used for both browser display and Markdown download. |

### Lines 207-234: charts and replenishment worklist

| Line(s) | What the line does and why |
| --- | --- |
| 207 | Creates four tabs and assigns their container objects to the four names used later. |
| 208 | Sends the following output to the inventory dashboard tab. |
| 209 | Groups selected rows by warehouse and category, keeps those labels as columns and sums current stock value. The chart input is aggregated monetary value. |
| 210 | Creates a Plotly bar chart by warehouse, with category color segments, INR value and an explanatory title, then displays it at container width. |
| 211 | Shows visual-guide entry 0 under the warehouse value chart. |
| 212 | Creates a scatter from individual rows: daily demand on x, stock on y, reorder flag as color, cost as bubble size and SKU/location/threshold in hover. |
| 213 | Shows the scatter's matching explanation. |
| 214 | Adds the replenishment worklist heading. |
| 215 | Explains the positive-quantity restriction, sort order, field meanings and review-only purpose. |
| 216 | Uses `.loc` with the Boolean flag to keep only reorder rows, selects five named fields, sorts quantity descending and displays the table. The worklist contains individual SKU-location records, not grouped totals. |
| 217 | Adds a generic caution about exact values and group sizes. Its “grouped values” wording is shared with other apps; the preceding worklist is row-level. |
| 218 | Sends later displays into the exploration tab. |
| 219 | Creates two columns for the histogram and boxplot. |
| 220 | Creates a 7-by-4-inch Matplotlib Figure and Axes. |
| 221 | Draws the cover histogram with 20 bins after dropping missing cover values. Fill and edge colors affect appearance, not the counts. |
| 222 | Sets the histogram title and axis labels, including the days formula and SKU-location count unit. |
| 223 | Renders the histogram in the left column, then closes the figure handle. The semicolon separates those two statements. |
| 224 | Shows the cover-distribution explanation in that column. |
| 225 | Creates a new figure/axes pair for the category plot. |
| 226 | Uses Seaborn to draw days-cover distributions by category on those axes with a chosen fill color. |
| 227 | Sets the boxplot title. |
| 228 | Renders the boxplot on the right and closes its Matplotlib handle. |
| 229 | Shows the category-boxplot explanation in the same column. |
| 230 | Creates a wider figure for the matrix plot. |
| 231 | Pivots Boolean reorder flags by warehouse/category, averages each cell and multiplies by 100. Seaborn draws the heatmap with one-decimal annotations and a fixed 0-100 color range. |
| 232 | Titles the heatmap in percentage terms. |
| 233 | Displays the heatmap and closes its figure. |
| 234 | Shows the fifth visual-guide entry, including equal-location weighting and missing cost/urgency information. |

### Lines 236-258: inspect data, download results and practice

| Line(s) | What the line does and why |
| --- | --- |
| 236 | Comment marks source inspection and learning tools. |
| 237 | Directs output into the Data and quality tab. |
| 238 | Adds the field dictionary heading. |
| 239 | Converts `FIELD_GUIDE.items()` to a two-column DataFrame and renders field names and meanings. |
| 240 | Adds the selected-record heading. |
| 241 | Explains that these are the actual analytical rows including derived fields, and that sorting the displayed table is not changing filters. |
| 242 | Displays the full selected DataFrame. |
| 243 | Converts it to CSV without the pandas index and provides a `filtered_inventory.csv` download with CSV MIME type. Derived measures are included. |
| 244 | Adds the numeric-summary heading. |
| 245 | Explains count, mean, spread, extremes and quartiles, reminding readers that business meaning matters. |
| 246 | Selects numeric columns, calculates `describe()` and rounds for display. The Boolean `needs_reorder` column is not selected by `include="number"`; its count is shown elsewhere. |
| 247 | Adds the source-quality heading. |
| 248 | Displays total source rows, exact duplicate rows and missing source cells from `frame`. Derived missing cover in `filtered` is not counted in this source-only message. |
| 249 | Builds a field-level quality table containing source column names, type strings and missing-value counts. |
| 251 | Opens an exercise expander outside the tab blocks. |
| 252 | Displays four numbered practice tasks as Markdown: buffer cost, stockouts/cover, grain and incoming orders. These are learning prompts, not executed calculations. |
| 253 | Explains why the project includes Matplotlib, Seaborn and Plotly. |
| 254 | Restates that fictional observational data do not establish cause and effect. |
| 256 | Sends output into the Full report tab. |
| 257 | Supplies the current `full_report` string to a download button named `04_inventory_planning_report.md`, with Markdown MIME type. |
| 258 | Renders that same report string in the browser. |

## 7. Read the five charts and the replenishment worklist

### Warehouse value bars: where cost value is held

Each bar is a warehouse and each color segment is a category. The total bar height is the sum of units multiplied by unit cost in INR.

The app groups before plotting, so the visual is based on total value per warehouse/category pair rather than overlapping bars for individual rows. With all bundled data selected, Bengaluru has the largest total value. That fact does not say it has the most units, the longest cover or the greatest need to buy more.

Changing the buffer does not change this chart's underlying values, because current stock and cost remain the same. Changing warehouse/category filters does change the included rows.

### Demand versus stock scatter: inspect individual locations

Each point is a SKU-location pair. X is assumed units demanded per day; y is current units. Bubble size reflects **unit cost**, not total inventory value, total suggested cost or demand.

Color changes according to `needs_reorder`. Moving the buffer slider can therefore change a point's color even though its x and y coordinates stay fixed. This is a useful demonstration of an assumption changing a classification without changing observed inputs.

Do not draw a single universal diagonal and treat it as the exact rule for every point. Lead time and safety stock differ between rows, so two locations with similar demand and stock can have different thresholds. Hover provides each row's threshold.

The chart does not show a probability of stockout or a confidence interval. A colored point means only that the current deterministic rule produces a positive gap.

### Days-cover histogram: how coverage is distributed

The histogram counts selected locations within intervals of cover. It helps distinguish a collection of similar cover levels from a mixture of very short and very long cover.

Its y-axis is number of SKU locations. It does not weight by unit cost or stock quantity. A cheap low-volume SKU and an expensive high-volume SKU each contribute one observation.

Zero-demand cover values are undefined and explicitly excluded by `dropna()`. The app does not remove such rows from all calculations. A histogram can therefore contain fewer observations than the selected row count after an edited CSV introduces zero demand.

For the bundled finite data, the 20 bin boundaries are based on the selected cover values, so filter changes can change them. Compare axes when comparing different selections.

### Category boxplot: compare typical cover and variation

For each category, the center line is median cover, the box is the middle 50% and default whiskers extend to observations within 1.5 interquartile ranges of the box limits. Points beyond them invite investigation; they are not automatically deleted.

A high median can reflect slow demand, large stock holdings or longer justified lead times. A wide box means cover differs substantially within that category. It does not identify which explanation is true by itself.

Seaborn draws the statistical plot onto a Matplotlib Axes. Streamlit displays the resulting Figure. The code then calls `plt.close(fig)` to release Matplotlib's reference after rendering; this does not remove the image already sent to the app.

### Reorder-share heatmap: breadth of workload

Each cell is the percentage of selected locations in one warehouse/category group with a positive suggestion.

In the full bundled data, each warehouse/category group contains 15 SKU locations. At buffer zero:

- Bengaluru/Electronics has 4 flagged locations, so the cell is 4 / 15 × 100 = 26.7% when displayed.
- Mumbai/Home has 7 flagged locations, so the cell is 7 / 15 × 100 = 46.7% when displayed.

A cell with a higher percentage has a larger **share of locations** requiring review. It need not require more units or money. A small number of expensive replenishments can cost more than many cheap ones.

The fixed 0-100 color range prevents a low percentage in one selection from being colored as though it were equivalent to a high percentage in another selection. If an edited or filtered dataset has no observations for a combination, that is a missing combination, not proof that no reorder is needed there.

### The worklist: the record-level explanation behind the flag

The worklist shows SKU, warehouse, current units, threshold and suggested units for records with a positive gap. It is sorted by suggested quantity, largest first.

This is a quantity ranking, not a ranking by urgency, stockout risk, expected lost sales or purchase cost. Different unit costs can make the cash ranking very different. The largest proposal is a useful starting point for review, but the app does not claim it is the optimal first action.

Equality produces no worklist row: if stock equals threshold, suggested units are zero and the Boolean condition `> 0` is False.

## 8. Validation, model assumptions and current limitations

### What the current code validates

The loader checks required fields, nonempty data, numeric conversion and missing required values. It catches specified loading failures and shows them in the app. The filter stage prevents downstream analysis of an empty selection.

The quality section reports exact duplicate rows and missing source cells, but it does not remove duplicates or repair values. No outliers are automatically dropped and no imputation is performed.

### What numeric conversion does not validate

A value can be numeric and still be nonsensical for this model. The app does not explicitly reject negative stock, negative demand, negative cost, negative safety stock or fractional quantities. It does not enforce finite values, integer units or a unique SKU-warehouse key.

These gaps have concrete consequences:

- Negative demand can produce negative cover and violate the expected monotonic response to increasing buffer days.
- Negative unit cost can make purchase totals meaningless and may break a chart that uses cost as marker size.
- Duplicate SKU-location rows would count and cost the same logical location more than once.
- Fractional suggestions can remain stored even though card formatting shows no decimals; the app does not implement pack-size rounding.
- Infinite numbers are not the same as missing values and are not rejected by the missingness check alone.

The provided CSV uses positive demand and cost, nonnegative stock/safety values and distinct SKU-warehouse pairs. That supports the bundled examples. It does not make the loader a complete validator for arbitrary operational data.

### Three separate kinds of zero or missing value

1. **No matching rows:** the app displays a message and stops the current run.
2. **Zero total inventory value:** the scalar `ratio` helper displays a fallback zero for a warehouse share; the actual proportion is undefined if the denominator is zero.
3. **Zero daily demand:** days cover becomes `NaN` and is omitted from the cover histogram; the row remains available for other measures.

These are different conditions with different handling. Do not describe them as one generic “division by zero fix.”

### What the scenario leaves out

The model assumes a constant average demand and fixed lead time. It does not estimate a service level, probability of stockout or demand distribution. Baseline safety stock is an input, not calculated from forecast error.

It also ignores incoming purchase orders, backorders, supplier calendars, minimum quantities, case packs, quantity discounts, capacity, expiry, transfers and carrying cost. Stock on hand is used directly; a fuller replenishment policy often needs inventory position and expected events before arrival.

Current stock value is fixed across buffer scenarios. Estimated purchase is hypothetical future acquisition cost. The app does not automatically add proposed units to stock, simulate their arrival or recalculate a future warehouse balance.

For tied warehouse totals, `idxmax()` returns the first maximum in the sorted grouped result. For tied largest reorder quantities, `sort_values(...).iloc[0]` has no explicit secondary tie-break rule and the default sort is not guaranteed stable. The report's generic statement about sorted group order should not be interpreted as an alphabetical guarantee for tied SKUs.

Finally, a high suggested total does not establish that the business should buy that amount. It demonstrates what the stated rule implies for the supplied fictional data. Improving the rule requires additional evidence and a defined operating objective.

## 9. Run the app and reproduce its results

The [workshop README](../README.md) specifies Python 3.12 and a pinned workshop environment. From the repository root on Linux, macOS or WSL:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit==1.50.0 pandas==2.2.3 numpy==2.3.5 matplotlib==3.10.8 seaborn==0.13.2 plotly==6.5.2
cd business_analytics_workshop/04_inventory_planning
streamlit run app.py
```

Check that `python` refers to Python 3.12 before creating the environment. NumPy is part of the workshop package set even though this file does not import it directly.

The repository contains other folder names with `>`, which native Windows filesystems cannot represent. Use the root README's WSL guidance when cloning the entire repository. If using only a copied workshop folder on Windows, activate its virtual environment in PowerShell with `.venv\Scripts\Activate.ps1`.

In the configured CookieSensei workshop workspace, the packages are already provided. To launch a separate copy:

```bash
cd /home/coder/project/business_analytics_workshop/04_inventory_planning
streamlit run app.py --server.port 8502
```

The main workshop dashboard uses port 8501. Follow the workshop README's port-forwarding instructions for the separate instance.

`streamlit run app.py` starts the app runtime; ordinary `python app.py` is not an equivalent browser-app launch. After dependencies are available, the analysis reads a local CSV and does not require a database, API key or supplier connection. See the official [Streamlit run guide](https://docs.streamlit.io/develop/concepts/architecture/run-your-app).

### Reproduce the default analysis

1. Select all warehouses and categories, and set extra safety days to 0.
2. Confirm 180 selected rows representing 60 unique SKUs.
3. Compare the cards with INR 55,448,799 current stock value, 53 flagged locations, 5,065 proposed units and INR 5,866,261 proposed purchase.
4. Inspect SKU-051 at Mumbai in the worklist and verify 25 × 14 + 10 - 65 = 295 units.
5. Set buffer to 7. Confirm 87 flagged locations, 12,996 proposed units and INR 16,314,861 estimated purchase.
6. Observe that current stock value remains unchanged while the reorder classifications and proposals change.
7. Read the report's INR 10,448,600 increase above the zero-buffer scenario for the same selected data.
8. Download the selected CSV and report if you want to preserve that scenario's outputs.

You can independently check the arithmetic from this project directory without importing the Streamlit app:

```python
import pandas as pd

stock = pd.read_csv("inventory.csv")
buffer = 0
point = stock["daily_demand"] * (stock["lead_time_days"] + buffer) + stock["safety_stock"]
suggested = (point - stock["stock_on_hand"]).clip(lower=0)

print("Locations:", len(stock))
print("Distinct SKUs:", stock["sku"].nunique())
print("Current value:", (stock["stock_on_hand"] * stock["unit_cost"]).sum())
print("Flagged locations:", (suggested > 0).sum())
print("Suggested units:", suggested.sum())
print("Estimated purchase:", (suggested * stock["unit_cost"]).sum())
```

This is a teaching check, not additional code already included in `app.py`. Changing `buffer` in the snippet should reproduce the corresponding scenario table while all rows remain selected.

## 10. Practice, troubleshooting and extensions

### Extend one idea at a time

**Compare quantity and cost rankings.** In a separate practice copy, calculate a row-level proposed cost column, then sort by it. Explain why the top quantity and top cost records might differ. Keep both stock units and INR labels visible.

**Add incoming orders carefully.** A possible first extension would add a column for confirmed inbound units. Before subtracting it from a gap, ask whether those units arrive before the stock is needed. A simple arithmetic addition does not solve delivery timing. Document the assumption clearly rather than claiming an operationally complete formula.

**Check grain explicitly.** Count duplicated pairs of SKU and warehouse. Explain why checking duplicate SKU values alone would incorrectly flag legitimate cross-warehouse records.

**Show denominators beside the heatmap.** Calculate group sizes for warehouse/category combinations. This makes a 50% cell based on two records distinguishable from one based on many. The bundled cells happen to be evenly sized; a changed dataset may not be.

**Investigate high cover without deleting it.** Locate an unusually large cover value, inspect its demand and stock, and ask whether seasonality, a long lead time or a slow-moving product could explain it. A boxplot outlier is a prompt for inquiry.

**Define what “best buffer” would mean.** The current slider explores the cost implications of a choice. Selecting an optimal buffer would require an objective and information about tradeoffs such as service level, uncertainty, shortage cost and carrying cost. The existing calculations do not provide that optimization.

### Common problems

| Symptom | Explanation to check | Useful action |
| --- | --- | --- |
| Import error | The active environment lacks a dependency | Install the workshop versions in the interpreter used to launch Streamlit. |
| CSV loading error | The expected file is missing, renamed or inaccessible | Keep `inventory.csv` next to the script and inspect the browser error. |
| Required-column error | A header changed or was deleted | Compare exact names with `required_columns`. |
| Numeric conversion error | A numeric field contains labels or formatted currency text | Correct the source or deliberately implement a cleaning rule in a practice copy. |
| No matching rows | Empty warehouse/category selections or an absent combination | Restore a valid selection; there is no date filter in this project. |
| Buffer changes some charts but not others | Only the threshold-related calculations depend on buffer | Explain why inventory value and days cover remain fixed for the same rows. |
| Source missing count is zero but cover has blanks | Cover is a derived field and zero demand produces undefined values | Inspect source demand and distinguish source-quality checks from derived-value checks. |
| Proposed quantities appear rounded | Cards format numbers with zero decimal places | Inspect the detailed table; formatting is not pack-size or integer-order logic. |
| A worklist row is present despite positive stock | Reorder means below threshold, not necessarily zero stock | Compare current units with the row's threshold. |
| A saved CSV edit has not appeared | A new app run has not occurred yet | Save, then rerun or interact with a widget. |

A clear explanation of this project should connect every output to its denominator or unit. “53 locations need attention” means 53 SKU-warehouse records under the default rule. “INR 5,866,261” means the modeled cost of proposed top-ups at listed unit costs. “16.63 days” means the first record's current stock divided by assumed daily demand. None of those statements needs an unsupported claim about future outcomes.

## 11. Sources and API references

The project-specific source of truth is [app.py](app.py), supported by [inventory.csv](inventory.csv) and the [workshop README](../README.md). Numerical tables in this guide are recalculations from the bundled fictional data using the formulas implemented in that source.

Official background references:

- [pandas 2.2: ten-minute introduction](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html)
- [pandas 2.2: grouping and aggregation](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html)
- [Streamlit: run your app](https://docs.streamlit.io/develop/concepts/architecture/run-your-app)
- [Streamlit 1.50: tab execution behavior](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs)
- [Plotly Express overview](https://plotly.com/python/plotly-express/)
- [Seaborn boxplot reference](https://seaborn.pydata.org/generated/seaborn.boxplot.html)
- [Matplotlib: close a figure](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.close.html)

The libraries make the calculations and presentation convenient. The analytical responsibility remains in the chosen grain, units, assumptions and interpretation, which is why this guide explains those alongside the code.
