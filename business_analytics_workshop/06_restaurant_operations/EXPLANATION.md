# Restaurant Operations - Business Problem, Analysis, and Code Explained

This is a teaching guide to the [actual `app.py` in this folder](app.py) and its [restaurant orders CSV](restaurant_orders.csv). It explains how the business questions become calculations, why those calculations are appropriate, how the browser interface is built, and what each source line contributes. It assumes you understand rows and columns but may be new to Python, pandas, or Streamlit.

The walkthrough refers to the source at repository revision [`c10a61c36fffdd048b69dd78926e6663bc986fce`](https://github.com/cookieSensei/programming-and-ai/blob/c10a61c36fffdd048b69dd78926e6663bc986fce/business_analytics_workshop/06_restaurant_operations/app.py). All dataset observations are fictional. INR amounts and January-April 2025 dates belong to a teaching example, not a live restaurant. The code is unchanged by this guide.

## Contents

1. [Business problem and intended decision](#business-problem-and-intended-decision)
2. [Dataset and row meaning](#dataset-and-row-meaning)
3. [Why pandas and the other libraries](#why-pandas-and-the-other-libraries)
4. [Connect business questions to code](#connect-business-questions-to-code)
5. [Formulas and worked examples](#formulas-and-worked-examples)
6. [How the Streamlit application works](#how-the-streamlit-application-works)
7. [Understand the five charts](#understand-the-five-charts)
8. [Verified results from the bundled CSV](#verified-results-from-the-bundled-csv)
9. [Line-by-line guide to app.py](#line-by-line-guide-to-apppy)
10. [Run the project and investigate results](#run-the-project-and-investigate-results)
11. [Worked practice and self-checks](#worked-practice-and-self-checks)
12. [Limits and possible improvements](#limits-and-possible-improvements)
13. [References](#references)

## Business problem and intended decision

A restaurant manager sees daily sales but also hears that some guests wait too long. They need to decide which branch and meal-period combinations to investigate. Sales alone are insufficient: a busy location could produce high revenue while some orders wait much longer than others. A low average rating does not identify its cause, and a high average bill may simply come from larger parties.

The project combines commercial and service measures:

- **Sales and average bill** describe the selected orders' billed value.
- **Food-cost contribution** subtracts one explicit cost category to show what remains before other operating costs.
- **Mean, median, and 90th-percentile wait** describe central and slow-end service experience.
- **Ratings and subgroup counts** show how recorded customer scores vary across branches and meal periods.
- **Wait/rating association** asks whether the two variables move together in the observed orders.

The useful result is a focused next question: “University has the longest mean wait among the selected branches, but how does that compare within the same channel, meal period, and party size?” That directs investigation. It does not prove the branch needs more staff, because the dataset contains no staffing or kitchen-capacity records.

This is **exploratory data analysis**, or EDA: inspect the data, define useful measures, summarize groups and distributions, and identify patterns worth investigating. The program does not predict ratings, recommend an optimized staffing schedule, place orders, or estimate the causal effect of reducing wait. It also does not calculate full restaurant profit. Those limits follow directly from the `CASE`, `DECISION`, `DATA_CONTEXT`, and `LIMITATIONS` text in [the application](app.py).

## Dataset and row meaning

### What one record represents

One row represents **one order**. The dataset has 600 orders, with guests counted inside each order. There are three branches, three meal periods, and three sales channels. An order is not necessarily a unique customer or a unique guest: the data contains no customer identifier with which to recognize repeat visits.

The first source record is:

| Field | Value |
| --- | --- |
| `order_id` | DINE-0001 |
| `date` | 2025-01-01 |
| `branch` | Central |
| `meal_period` | Dinner |
| `channel` | Takeaway |
| `guests` | 1 |
| `bill_amount` | INR 470.12 |
| `food_cost` | INR 102.74 |
| `wait_minutes` | 54 |
| `rating` | 3 |

This row says that the order had the recorded attributes above. It does not reveal why the wait was 54 minutes, whether the rating was submitted immediately, or how the guest judged food versus service. Those are questions about information that is not present. [Source: `restaurant_orders.csv`](restaurant_orders.csv)

### Field dictionary

| Column | Meaning and unit | Role in the app |
| --- | --- | --- |
| `order_id` | Synthetic order identifier | Row identity, hover detail, and order counts |
| `date` | Order date | Inclusive date filter and daily sales grouping |
| `branch` | Central, Riverside, or University | Sidebar filter, sales comparison, summary groups, and heatmap rows |
| `meal_period` | Breakfast, Lunch, or Dinner | Sidebar filter, wait-time distribution groups, and heatmap columns |
| `channel` | Delivery, Dine in, or Takeaway | Scatter color, report scope, and an extension exercise |
| `guests` | Number of guests associated with the order | Scatter bubble size, total guest count, and sales-per-guest denominator |
| `bill_amount` | Billed sales for the order, INR | Sales total, average bill, histogram, and daily line chart |
| `food_cost` | Food cost for the order, INR | Contribution calculation |
| `wait_minutes` | Recorded service wait, minutes | Means, median, percentile, boxplot, scatter, and correlation |
| `rating` | Recorded score from 1 to 5 | Mean rating, scatter, correlation, and heatmap |
| `contribution` | `bill_amount - food_cost`, INR | Derived value in the branch table, data export, and narrative |

The CSV has the first ten fields. The app creates `contribution` at line 153 in its working DataFrame. It does not save that new column back into the source file. A filtered download includes it because it belongs to the analyzed working table.

The bundled data spans January 1-April 30, 2025. All 600 rows have the required values, and there are no exact duplicate rows in this revision. Those checks do not make the data an audited trading ledger. In particular, absence of a branch/date combination is not a recorded zero-sales day. [Source: `restaurant_orders.csv`](restaurant_orders.csv)

### Grain determines valid comparisons

An average of `rating` gives every **order** equal weight. It is not a guest-weighted score unless you deliberately apply guest weights. Summing `guests` gives guest appearances associated with recorded orders, not the number of distinct people who visited. Counting `order_id` with `.size()` counts rows; it does not deduplicate repeated identifiers. If a custom CSV contains the same order twice, both rows will affect the results unless you resolve that duplication first.

## Why pandas and the other libraries

### Why pandas is useful here

pandas provides a `DataFrame`, a table with labeled columns, rows, types, and an index. This closely matches the input CSV and the analysis questions. Its methods let the program express operations such as “only these branches,” “sum sales by date,” or “average wait by meal period” without manually maintaining nested dictionaries and running totals.

```python
filtered["contribution"] = filtered["bill_amount"] - filtered["food_cost"]
daily = filtered.groupby(["date", "branch"], as_index=False)["bill_amount"].sum()
```

The first operation calculates one new value for every order by subtracting two aligned columns. The second groups selected orders that share both a date and a branch, then adds their bill amounts. `as_index=False` leaves the two group labels as ordinary columns, making them straightforward Plotly inputs. The [pandas introductory guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html) and [grouping guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html) explain these table and aggregation concepts.

The arithmetic could be written with standard Python loops. pandas is chosen because one coherent tool can read the CSV, validate types, filter rows, calculate derived columns, summarize distributions, pivot groups into a matrix, and export the result. It saves repetitive code, but the analyst must still choose the correct denominator and interpretation.

### Understand the table operations before the charts

- `frame["rating"]` selects one column as a `Series`; `frame[["rating", "wait_minutes"]]` selects a two-column DataFrame.
- `.unique()` lists distinct values; `sorted(...)` puts them in a stable display order.
- `.isin(chosen)` produces a Boolean test for each row. `filtered[that_test]` retains rows marked `True`.
- `.sum()` combines additive values such as billed sales; `.mean()` divides the sum by the number of valid values.
- `.median()` describes the middle of a sorted distribution, making it less affected by a few extreme waits than the mean.
- `.quantile(.9)` estimates a boundary near the upper 10% of the distribution. It does not automatically select the slowest orders or change the data.
- `.groupby(...).agg(...)` gives each group several named summaries at once. The app can count orders, add sales, and average wait in one result table.
- `.pivot_table(...)` puts one grouping variable on the rows, another on columns, and an aggregated measurement in each cell.
- `.corr(...)` calculates a correlation coefficient between aligned numeric series. It does not fit a causal model.

### What each library contributes

| Tool | Specific purpose in this project |
| --- | --- |
| `pathlib.Path` | Locate `restaurant_orders.csv` beside `app.py`, regardless of the terminal's working directory |
| `pandas as pd` | Read, parse, validate, filter, derive, aggregate, correlate, and export tabular data |
| `matplotlib.pyplot as plt` | Create and label figures/axes, draw the order-value histogram, and close figure resources |
| `seaborn as sns` | Draw wait-time boxplots and the branch/meal-period rating heatmap |
| `plotly.express as px` | Build interactive sales lines and a multivariable scatter chart |
| `streamlit as st` | Provide the browser page, sidebar controls, tabs, metric cards, tables, messages, and downloads |

`as pd`, for example, creates a shorter import name; it does not change pandas' behavior. NumPy appears in the shared environment installation command but is not directly imported or called by this app.

## Connect business questions to code

| Question | Calculation in the actual code | Why it fits the question | What it does not establish |
| --- | --- | --- | --- |
| How much sales value do selected orders represent? | `filtered["bill_amount"].sum()` | Each selected order contributes its recorded bill once | Cash collected, recognized accounting revenue, or completeness of trading records |
| What is the average order worth? | `filtered["bill_amount"].mean()` | Divides billed sales by selected order count because required bills are nonmissing | Typical spending by one guest or by one unique customer |
| What remains after food cost? | Per-row `bill_amount - food_cost`, then sums | Removes the particular recorded direct cost from corresponding orders | Net profit after wages, rent, fees, tax, or other costs |
| Where is average service slowest? | Group by branch, mean `wait_minutes`, then `idxmax()` | Compares order-weighted branch means on the selected records | Cause of delay or a statistically proven difference |
| How slow are the longer waits? | `median()` and `quantile(.9)` | Adds middle and upper-tail context that a mean can hide | A contractual service guarantee or maximum observed wait |
| Do waits and ratings move together? | `filtered["wait_minutes"].corr(filtered["rating"])` | Summarizes observed linear association | That changing wait alone will change rating by a particular amount |
| How much is spent per guest appearance? | Total sales divided by total guests | Gives each guest count proportional influence in the denominator | Distinct-customer lifetime value |
| Which branch/meal-period ratings need investigation? | Mean-rating pivot table plus group `.size()` | Combines subgroup averages with their evidence counts | A reliable ranking independent of sample size and order mix |

The app's present sidebar filters are **branch, meal period, and date**. Channel appears in the scatter and report but is not yet a sidebar filter. Adding a channel filter is an exercise, so a guide must not describe that feature as already implemented. [Source: `app.py`](app.py)

## Formulas and worked examples

### Sales, average bill, and contribution

For selected orders:

```text
sales = sum of bill_amount
average bill = sales / number of selected orders
contribution for one order = bill_amount - food_cost
total contribution = sum of those order contributions
```

The first actual CSV row has contribution `470.12 - 102.74 = 367.38` INR. That amount is before staffing, rent, delivery fees, tax, and other costs. It should not be labeled net profit. Since each order's two amounts belong together, row-wise subtraction preserves the correct pairing; summing those differences gives the same total as total bills minus total food cost.

The current top cards show sales, average bill, average wait, and average rating. Contribution is available in the narrative, branch summary, selected records, and downloaded CSV. It is not a fifth top card simply because the app computes it.

### Average bill and sales per guest have different denominators

Consider this deliberately small **illustrative example**, separate from the bundled file:

| Order | Bill (INR) | Guests | Bill per guest (INR) |
| --- | ---: | ---: | ---: |
| A | 100 | 1 | 100 |
| B | 900 | 3 | 300 |

Total sales are 1,000. Average bill is `1,000 / 2 = 500` INR per order. Sales per guest are `1,000 / 4 = 250` INR per guest. Averaging the two per-order guest rates gives `(100 + 300) / 2 = 200`, which gives a one-guest order the same weight as a three-guest order.

The app uses the ratio of totals for sales per guest. That answers how the total billed amount compares with the total guest count. It is equivalent to weighting order-level per-guest rates by each order's guest count, provided those counts are positive. The denominator is still guest appearances in recorded orders, not deduplicated people.

### Mean, median, and the 90th percentile of wait

The mean adds all wait values and divides by the number of selected orders. The median is the middle sorted value, or the midpoint of the two middle values. A few long waits can move the mean considerably without moving the median as much.

For the illustrative waits `[5, 10, 10, 15, 60]`, the mean is 20 minutes and the median is 10. A description that reports only “20 minutes on average” misses both the common shorter experience and the very long 60-minute observation.

The app's `quantile(.9)` estimates the 90th-percentile value using pandas' default interpolation. For those five illustrative values, the fractional zero-based position is `(5 - 1) * 0.9 = 3.6`, between 15 and 60, giving `15 + 0.6 * (60 - 15) = 42`. It need not equal an observed value. In small or tied samples, it is a summary boundary, not a promise that exactly 10% of rows are strictly above it. The bundled file's 90th percentile is 50 minutes. [pandas quantile reference](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.Series.quantile.html)

### Average rating is a score, not a satisfaction percentage

The code calculates the mean of recorded scores and formats it as a value out of five. A mean of 3.67 does not say that 73.4% of customers were satisfied; no satisfaction threshold is defined, and customers are not uniquely identified. The app uses a simple numeric average of the rating scale as a descriptive teaching measure.

The heatmap uses the same order-weighted mean inside each branch/meal-period group. Two cells with means of 4.0 can have very different sample sizes and distributions. Their matching means do not mean the evidence is equally strong.

### Pearson correlation: direction and strength of a linear association

`filtered["wait_minutes"].corr(filtered["rating"])` uses Pearson correlation by default. Its range is -1 to +1 when defined. A negative coefficient indicates that larger waits tend to accompany lower recorded ratings in these selected orders. A positive coefficient would indicate that they tend to rise together. A coefficient near zero indicates little *linear* association; it does not rule out all kinds of relationship.

The coefficient is not the number of rating points lost per extra minute. It has no time unit and is not a regression slope. Nor does a negative coefficient show that wait caused the score. Branch, channel, party size, food quality, expectations, and unrecorded factors could matter. The app reports an observed association and asks for further investigation.

The code explicitly avoids calculating correlation for fewer than two rows by setting it to `NaN`, meaning an unavailable numeric result. With two or more rows, constant wait or rating values can still make the coefficient undefined. `pd.notna(association)` chooses whether to display a numeric answer or an insufficient-variation explanation. No confidence interval or significance test is calculated. [pandas correlation reference](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.Series.corr.html)

### Small samples and safe division

The program calculates branch/meal-period group sizes with `.size()`. It reports how many observed groups have fewer than 20 orders. Twenty is an illustrative caution threshold, not a validated guarantee of statistical reliability. Groups absent from the filtered data are not present in this count series; their lack of observations must not be confused with a good rating.

`ratio(numerator, denominator)` returns zero if the denominator is zero. That prevents a scalar division-by-zero exception in sales-per-guest reporting, but a zero guest total makes sales per guest undefined. Treat a displayed fallback zero as a signal to inspect the inputs. The bundled file has no zero-guest orders; custom data is not checked for positive, integral, or finite guest values by the current loader.

## How the Streamlit application works

### The complete path from CSV to browser

This dashboard starts as an ordinary Python data analysis and adds an interface around it. Streamlit executes the Python code on the machine running the app. The viewer uses a browser page generated from the `st` calls. pandas performs the computations; Streamlit does not decide what sales, contribution, or correlation should mean.

The sequence is:

1. Show project context and find the source CSV beside the script.
2. Load dates and numbers, check the required schema, and stop with a message if the input is unusable.
3. Obtain branch, meal-period, and date selections from sidebar controls.
4. Filter the DataFrame and stop with a message if the selection is incomplete or empty.
5. Calculate contribution, KPIs, grouped summaries, correlation, and sample counts.
6. Build explanatory text and a Markdown report from those same values.
7. Render the charts, selected records, descriptive statistics, source-quality information, and downloads.

This allows a learner to make an interactive analytical tool without writing a separate HTML/JavaScript interface, API, or database. It is useful when a Python calculation needs to become something a manager can explore. The [Streamlit execution overview](https://docs.streamlit.io/get-started/fundamentals/main-concepts) explains this model.

### What changes when a control changes

In this app, a normal sidebar widget change reruns the script from top to bottom. The widgets return their current selections, and pandas rebuilds the selected records and outputs. The CSV load is deliberately uncached. If you edit and save the CSV, the next rerun rereads it; the script does not implement a background file-monitoring service.

`frame` represents the loaded source. `filtered` starts as a copy, then receives successive row filters and the derived contribution column. This distinction explains why the source-quality panel reports full-source counts while KPIs, charts, and analysis text use the selected rows.

The controls have stable keys such as `06_restaurant_operations_branch`. A key identifies a widget and is not a CSV field. `st.columns(4)` provides four display positions. `st.tabs(...)` provides containers for dashboard, exploration, data, and report. With Streamlit 1.50.0, all tab contents are computed on a normal rerun, even when their tab is not currently visible. The `with` blocks determine placement rather than deferring computation. [Streamlit 1.50.0 tabs reference](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs)

Hovering or zooming a Plotly chart, sorting the displayed table, or switching tabs changes how existing output is viewed. None of those interactions becomes an analytical row filter in this code. There is no chart-click callback that updates the pandas selection. To change which records feed the results, use the sidebar or deliberately extend the application.

### How early stops protect the result

`st.stop()` ends the current run after a message. The loader uses it after an input error. The filter section uses it when the date range is incomplete or no records match. Without those checks, the later `.idxmax()` and sample-size operations could fail or have no meaningful output.

Date filtering is inclusive: both start and end dates are allowed. An empty branch or meal-period selection means no rows, because membership in an empty list is always false. The interface does not silently interpret “nothing selected” as “everything selected.”

### How reports are created

The program builds a list named `report_parts`, using ordinary strings and f-strings. The strings insert the current results into a 12-section Markdown report, then `"\n\n".join(...)` combines them. This is deterministic template construction, not an AI call.

The “Full report” tab displays this string, offers a Markdown download, and adds a branch/meal-period sample-size table. That final sample-size table is rendered separately after `st.markdown(full_report)`: it is **not embedded as a full table in the downloaded Markdown**. The report text still contains the minimum observed cell count and the number of cells below 20 through the insight section.

The downloaded report summarizes the selected observations. This `EXPLANATION.md` instead explains the permanent project logic and source lines. The CSV download exports the filtered rows including contribution, with the index omitted, and does not overwrite `restaurant_orders.csv`.

## Understand the five charts

### 1. Daily sales by branch

The code groups on both date and branch and sums bills. Plotly draws one colored line per branch, with date on the horizontal axis and INR sales on the vertical axis. It answers which observed branch/dates account for sales and makes short-term variation visible.

It connects observed points. A missing branch/date group is not filled with zero, and the app does not construct a complete trading calendar. Consequently, a connecting line across a gap is not evidence about the missing day. Branch totals also are not adjusted for capacity, operating hours, or the number of days represented.

### 2. Wait time and rating scatter chart

Each point represents an order. Horizontal position is wait in minutes; vertical position is the 1-5 rating; color is channel; bubble size reflects guests. Hover includes the order identifier, branch, and bill. The opacity of 0.6 makes overlapping marks easier to notice.

This plot preserves order-level variation that grouped means hide. Because ratings are discrete, many points overlap on the same horizontal rating bands. Bubble size gives order-size context, but it does not mean the correlation calculation is guest-weighted. The code's Pearson coefficient still treats order observations equally. A visible pattern suggests a question, not proof that reducing wait will produce a specific improvement.

### 3. Order value histogram

Matplotlib divides bill amounts into 20 ranges and counts orders in each range. The horizontal axis is the bill in INR, and the vertical axis counts orders. A long high-bill tail can explain why mean bill exceeds median bill.

The plot describes orders, not guest spending. A high bill may reflect a large party. The app does not remove that order as an outlier, normalize it by guests in the histogram, or infer a high-value repeat customer from it. Bin choices affect the visual shape without changing the data.

### 4. Service time by meal period boxplot

Seaborn groups order waits by meal period. The middle line is the median; the box spans the middle half; default whiskers reach observed values within 1.5 interquartile ranges. Points beyond the whisker rule are observations to inspect, not records automatically deleted. [Seaborn boxplot reference](https://seaborn.pydata.org/generated/seaborn.boxplot.html)

The plot compares both usual waits and variability. One period might have a similar median but a wider spread or more long waits. Branches, channels, and party sizes remain mixed unless filtered or explicitly analyzed separately, so the plot does not establish a staffing cause.

### 5. Branch and meal-period rating heatmap

`pivot_table(index="branch", columns="meal_period", values="rating", aggfunc="mean")` creates one mean score for each observed branch/meal-period combination. The heatmap uses a fixed scale of 1 to 5, which helps keep the same rating meaning across filter changes. Cells without observations are blank where the matrix has missing combinations; wholly unobserved groups may be absent from its axes.

This is a table of mean ratings, not a correlation matrix. Its cell numbers are scores out of five, not association coefficients. Read the branch/meal-period sample-size table in the report alongside it. A cell based on three orders should not be treated as equally informative as one based on 100, and a single mean does not show whether scores are tightly clustered or polarized.

## Verified results from the bundled CSV

The following values were recomputed from the committed CSV using the application's formulas, selecting all branches, meal periods, and dates. They are checks for this fictional dataset; new data or filters will change them.

| Measure | Result |
| --- | ---: |
| Orders | 600 |
| Guest appearances associated with orders | 2,075 |
| Sales | INR 821,005.18 |
| Mean bill | INR 1,368.34 |
| Median bill | INR 1,177.315 before display rounding |
| Food cost | INR 227,093.30 |
| Food-cost contribution | INR 593,911.88 |
| Sales per guest | INR 395.67 |
| Mean wait | 29.5633 minutes (card: 29.6) |
| Median wait | 29 minutes |
| 90th-percentile wait | 50 minutes |
| Mean rating | 3.67 out of 5 |
| Wait/rating Pearson correlation | -0.740139 (report: -0.74) |
| Smallest observed branch/meal-period group | 58 orders |
| Observed groups with fewer than 20 orders | 0 |

The branch summary is:

| Branch | Orders | Sales (INR) | Contribution (INR) | Mean wait (minutes) | Mean rating |
| --- | ---: | ---: | ---: | ---: | ---: |
| Central | 196 | 268,251.90 | 195,821.64 | 29.03 | 3.6735 |
| Riverside | 196 | 270,820.33 | 197,322.47 | 29.64 | 3.6531 |
| University | 208 | 281,932.95 | 200,767.77 | 30.00 | 3.6827 |

University leads both total sales and mean wait in this selection. It also has more observed orders, and its mean wait is only slightly greater than the others. A useful interpretation reports those facts together and asks about mix and capacity; it does not jump directly to “University is badly managed.” The app computes no uncertainty estimate for that comparison.

For another denominator check, the mean of the **order-level** bill-per-guest values is approximately INR 399.40, whereas the app's ratio of total bills to total guests is INR 395.67. Both can be calculated, but they answer different weighting questions. The latter is the measure implemented as sales per guest. [Inputs: `restaurant_orders.csv`](restaurant_orders.csv); [implemented calculations: `app.py`](app.py).

## Line-by-line guide to app.py

Read this section with source line numbers visible in your editor. Every nonblank source line is covered. Literal-string continuations and tuple fields may be grouped into a numbered range, with all lines in that range explained together. Blank lines are visual separators and perform no calculation. Code anchors identify the statements and may abbreviate a long line; use the adjacent source file for the full text.

### Lines 1-13: import tools and create the page

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 1 | ``"""Restaurant Operations Dashboard: a beginner Streamlit project using a fictional teaching dataset."""`` | A module docstring identifies the script and fictional dataset. It documents the Python module; it does not render a visible element or execute analysis. |
| 2 | ``from pathlib import Path`` | Import Path from the standard library so a later expression can locate the CSV relative to this file. |
| 4 | ``import matplotlib.pyplot as plt`` | Import Matplotlib's pyplot interface as plt. The program uses it for figure/axes creation, the histogram, and cleanup. |
| 5 | ``import pandas as pd`` | Import pandas as pd for CSV parsing, table operations, descriptive measures, correlation, and exports. |
| 6 | ``import plotly.express as px`` | Import Plotly Express as px, the high-level chart interface used for the interactive sales line and scatter figures. |
| 7 | ``import seaborn as sns`` | Import Seaborn as sns for the wait-distribution boxplot and mean-rating heatmap. |
| 8 | ``import streamlit as st`` | Import Streamlit as st to create the browser application from Python statements. |
| 10 | ``st.set_page_config(page_title="Restaurant Operations Dashboard", page_icon=":bar_chart:", layout="wide")`` | Set browser metadata, the bar-chart icon, and wide page layout before displaying other elements. These keyword arguments configure the page, not the dataset. |
| 11 | ``st.title("Restaurant Operations Dashboard")`` | Display the main page heading. Its visible title is separate from the browser tab title configured above. |
| 12 | ``st.caption("Business Analytics Workshop \| Fictional teaching data \| Currency: INR")`` | Show a compact caption identifying the workshop, fictional observations, and INR unit. |
| 13 | ``st.write("Connect order value, service time and customer ratings. Compare branches and meal periods to identify operationa...`` | Explain that the analysis connects order value with service experience and identifies operational questions. |

### Lines 15-82: define the business case and chart-reading guidance

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 15 | ``# This case study explains both the business question and how to read the evidence.`` | A comment labels the purpose of the following constants. Python ignores it when executing calculations. |
| 16-18 | ``CASE = ('A fictional restaurant manager wants to improve service without losing sales. Branch totals alone ' 'cannot revea...`` | Create CASE as one string spanning three source lines. Adjacent string literals inside parentheses concatenate; the text describes the manager's question and the limits of branch totals. |
| 19-20 | ``DECISION = ('Identify branch and meal-period combinations for service investigation, using sales, waiting time, ' 'ratings...`` | Create DECISION, specifying investigation of branch/meal-period combinations using both commercial and service measures. It is shared by the page and report. |
| 21-23 | ``DATA_CONTEXT = ('One row is one order. The dataset contains 600 fictional orders over January to April 2025 across ' 'thre...`` | Create DATA_CONTEXT with row grain, the 600-record teaching period, three grouping dimensions, and missing context. This is fixed explanatory text, not a live row-count calculation. |
| 24 | ``FORMULAS = [('Sales', 'Sum of bill amount', 'Selected billed sales in INR.'),`` | Start FORMULAS, a list of three-item tuples, with the sales label, sum rule, and INR interpretation. The text documents a calculation performed later. |
| 25-27 | ``('Average bill', 'Total bill amount / selected orders', 'An order-weighted mean, not spending per guest.'),`` | Add the average-bill definition and its order denominator. The tuple warns that this is not spending per guest. |
| 28-30 | ``('Average wait', 'Sum of waiting minutes / selected orders', 'An order-weighted mean. The median and 90th percentile show ...`` | Add the mean-wait definition and the need for median and 90th-percentile context. These are descriptive rules, not yet executed aggregations. |
| 31-33 | ``('Average rating', 'Sum of ratings / selected orders', 'Mean recorded score on the 1-5 scale, not a percentage satisfactio...`` | Add the average-rating definition, preserving its 1-5 score interpretation rather than treating it as a satisfaction percentage. |
| 34-36 | ``('Food-cost contribution', 'Sales - food cost', 'Excludes staffing, rent, delivery fees and tax; not net profit.'),`` | Add food-cost contribution: sales minus food cost, excluding other costs. This distinction prevents the derived amount being mislabeled as net profit. |
| 37-39 | ``('Sales per guest', 'Total sales / total guests', 'Weighted across all guests, not the average of order-level ratios.')]`` | Add sales per guest as a ratio of totals and close the formula list. The wording explicitly distinguishes it from an unweighted average of order-level ratios. |
| 40-46 | ``VISUAL_GUIDE = [('Daily sales by branch', 'Compare branch sales patterns across the selected dates.', 'The x-axis is date,...`` | Begin VISUAL_GUIDE and add a five-part explanation for the daily sales chart: title, purpose, axes/grouping, question, and caution about missing dates not being zero sales. |
| 47-53 | ``('Wait time and rating', 'Explore the association between service time and customer scores.', 'Each point is an order. X i...`` | Add the scatter explanation, assigning wait/rating to position, channel to color, and guests to size. The caution addresses overlapping discrete scores and noncausal interpretation. |
| 54-60 | ``('Order value distribution', 'Show the spread of customer bills.', 'The histogram counts orders in 20 INR bill ranges. Its...`` | Add the histogram explanation: counts in bill-amount ranges and why larger parties can create high bills without higher per-guest spending. |
| 61-67 | ``('Service time by meal period', 'Compare typical waits and variation across service periods.', 'The middle line is median ...`` | Add the meal-period boxplot explanation, including median, middle-half spread, whisker rule, minutes, and mixing of branch/channel/party-size contexts. |
| 68-74 | ``('Branch and meal-period rating heatmap', 'Locate differences hidden by an overall mean rating.', 'Rows are branches, colu...`` | Add the mean-rating heatmap explanation, its fixed 1-5 scale, missing combinations, and the need to inspect sample sizes, then close the guide list. |
| 75-76 | ``RECOMMENDATIONS = ['Investigate the slowest branch alongside meal period, sales channel and order size before changing ' '...`` | Start RECOMMENDATIONS with investigating the slowest branch alongside order context before altering staff schedules. |
| 77 | ``'Review the slowest 10% of orders with operational logs and customer comments to identify bottlenecks.',`` | Add a recommendation to inspect slow-end orders with operational logs and comments. The existing app does not collect those logs or perform the investigation. |
| 78-79 | ``'Pilot a specific service change with a comparison group, tracking both wait and ratings as well as ' 'cost and sales.']`` | Add a suggested controlled service pilot with a comparison group and multiple outcomes. This is a next step, not an experiment executed by the code. |
| 80-82 | ``LIMITATIONS = ('No staffing, capacity, food preparation time, opening-hours or customer-comment data is included. ' 'Obser...`` | Build LIMITATIONS as one string identifying missing capacity/staff/context data, incomplete fictional observations, noncausal correlation, and incomplete profit measurement. |

### Lines 84-109: render context and reuse visual explanations

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 84 | ``with st.expander("Business problem and context", expanded=True):`` | Create an initially expanded context container. The with block places its indented display calls inside it. |
| 85 | ``st.markdown("**The problem:** " + CASE)`` | Display a bold Markdown label followed by CASE. Plus signs concatenate text here. |
| 86 | ``st.markdown("**Decision this dashboard supports:** " + DECISION)`` | Display DECISION under a bold label, making the intended use explicit before charts appear. |
| 87 | ``st.markdown("**What one row means:** " + DATA_CONTEXT)`` | Display DATA_CONTEXT so readers know what a row represents and which information is absent. |
| 88 | ``st.info("This is a fictional teaching case. Every finding below is calculated from the selected CSV rows, not a claim abou...`` | Show an information message explaining that findings are computed from selected fictional records. |
| 89 | ``st.write("Start with the KPI cards, read the explanation under each visual, inspect the source data, then open Full report...`` | Give a route through the page: KPIs, chart guidance, underlying data, and full report. The text states that filters recalculate findings. |
| 92 | ``FIELD_GUIDE = {'order_id': 'Synthetic order identifier; one row per order.',`` | Begin FIELD_GUIDE, a dictionary from exact CSV field names to descriptions, with the synthetic order identifier. |
| 93 | ``'date': 'Order date.',`` | Describe date as the order date. Its storage will be converted to a datetime column later. |
| 94 | ``'branch': 'Restaurant branch.',`` | Describe branch as the restaurant location used for filtering and grouping. |
| 95 | ``'meal_period': 'Meal period during which the order was placed.',`` | Describe meal_period as the order's service-period category. |
| 96 | ``'channel': 'Order channel.',`` | Describe channel, which is used for color and context but has no sidebar filter in the original app. |
| 97 | ``'guests': 'Number of guests associated with the order.',`` | Describe guests as the count associated with an order. This does not claim they are unique people across the file. |
| 98 | ``'bill_amount': 'Sales amount for the order in INR.',`` | Describe bill_amount as the order's sales amount in INR. |
| 99 | ``'food_cost': 'Food cost for the order in INR; excludes staffing and overhead.',`` | Describe food_cost and explicitly exclude staffing and overhead from its coverage. |
| 100 | ``'wait_minutes': 'Recorded service wait in minutes.',`` | Describe wait_minutes and its measurement unit. |
| 101 | ``'rating': 'Customer rating from 1 to 5; higher means a better rating.'}`` | Describe the intended 1-5 rating range and close the dictionary. This description alone does not validate the range. |
| 103 | ``def explain_visual(index, container=st):`` | Define explain_visual with a guide index and an optional display container. Defining a function stores reusable behavior; it executes only when later called. |
| 104 | ``title, purpose, reading, question, caution = VISUAL_GUIDE[index]`` | Select the indexed five-item guide tuple and unpack it into title, purpose, reading, question, and caution variables. |
| 105 | ``container.markdown(f"**{title}: what this visual explains**")`` | Insert the visual title into a bold Markdown heading in the supplied container. The f prefix enables variable interpolation. |
| 106 | ``container.write(purpose)`` | Display the purpose text through that container. |
| 107 | ``container.markdown("**How to read it:** " + reading)`` | Show reading instructions with a bold label, identifying how to interpret positions and values. |
| 108 | ``container.markdown("**Question it answers:** " + question)`` | Display the business question answered by the visual. |
| 109 | ``container.caption("Interpretation limit: " + caution)`` | Show its caution as a caption. Passing left or right later keeps this explanation beside the relevant chart. |

### Lines 111-133: load, check, and safely divide values

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 111 | ``# 1. Load the CSV beside this script, regardless of the terminal's directory.`` | Document the decision to locate the source relative to app.py rather than the current terminal directory. |
| 112 | ``# Keeping this uncached lets students edit the CSV and immediately rerun the app.`` | Document uncached reading so a rerun sees saved CSV edits. It does not promise an automatic rerun every time the CSV changes. |
| 113 | ``DATA_FILE = Path(__file__).resolve().with_name("restaurant_orders.csv")`` | Create a Path from __file__, resolve it to an absolute path, and replace the filename with restaurant_orders.csv. This finds the sibling input without hard-coding a machine-specific directory. |
| 114 | ``try:`` | Start a protected block for file reading and initial validation. Its error handler does not cover subsequent chart or analysis code. |
| 115 | ``frame = pd.read_csv(DATA_FILE)`` | Read CSV text into a pandas DataFrame named frame. Initial types are inferred from the stored values. |
| 116 | ``frame["date"] = pd.to_datetime(frame["date"], errors="raise")`` | Parse date strings into datetime values and assign the converted series back. errors="raise" rejects unparseable dates rather than silently coercing them. |
| 117 | ``numeric_columns = ['guests', 'bill_amount', 'food_cost', 'wait_minutes', 'rating']`` | List the five fields that must support numeric operations. This is a Python list of names used in a conversion loop. |
| 118 | ``required_columns = ['order_id', 'date', 'branch', 'meal_period', 'channel', 'guests', 'bill_amount', 'food_cost', 'wait_mi...`` | List all required fields. Additional CSV columns are allowed, since the next test checks inclusion rather than exact column equality. |
| 119 | ``if not set(required_columns).issubset(frame.columns):`` | Convert required names to a set and test whether each exists in frame.columns. not enters the error branch when that subset condition is false. |
| 120 | ``raise ValueError("The CSV is missing required columns.")`` | Raise a readable missing-schema error. If date itself was missing, line 116 would already have raised a KeyError handled below. |
| 121 | ``if frame.empty:`` | Check for an empty table after the required-header check. No data means no useful dates, means, or chart points. |
| 122 | ``raise ValueError("The CSV contains no rows.")`` | Raise an empty-input error before calculating widget bounds or group extrema. |
| 123 | ``for column in numeric_columns:`` | Iterate over the names of numeric columns, binding column to one name at a time. |
| 124 | ``frame[column] = pd.to_numeric(frame[column], errors="raise")`` | Convert each selected column to numbers and assign it back. errors="raise" catches invalid numeric text; positive guests, finite values, rating limits, and integer counts are not checked here. |
| 125 | ``if frame[required_columns].isna().any().any():`` | Mark missing cells in the required fields. The first any() finds columns containing any missing value; the second asks whether any such column exists. |
| 126 | ``raise ValueError("Fill missing values in the required analysis columns first.")`` | Raise an error for missing required data. The app asks learners to correct source values instead of automatically dropping or imputing them. |
| 127 | ``except (OSError, ValueError, KeyError) as error:`` | Catch filesystem, value, and key errors from this try block and bind the exception to error. |
| 128 | ``st.error(f"Could not load {DATA_FILE.name}: {error}")`` | Display the source filename and actual error text. DATA_FILE.name gives only the filename. |
| 129 | ``st.stop()`` | Stop the current run so a loading failure cannot flow into later computations. |
| 131 | ``def ratio(numerator, denominator):`` | Define a reusable scalar ratio function with numerator and denominator parameters. |
| 132 | ``"""Return zero for an empty denominator so filters never divide by zero."""`` | Document that the helper returns a fallback zero for an empty denominator. |
| 133 | ``return numerator / denominator if denominator else 0.0`` | Divide when the denominator is nonzero; otherwise return 0.0. This prevents zero-division failure but does not turn an undefined per-guest rate into a meaningful zero. |

### Lines 135-150: turn sidebar selections into a filtered dataset

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 135 | ``# 2. Apply sidebar filters before calculating any KPI or chart.`` | State that selection precedes all KPI and chart calculations. Order matters for consistent scope. |
| 136 | ``st.sidebar.header("Filter the data")`` | Create a heading in the sidebar container. |
| 137 | ``filtered = frame.copy()`` | Copy frame into a working DataFrame named filtered. The full source remains available for quality reporting, while the copy receives row subsets and contribution. |
| 138 | ``selected_branch = st.sidebar.multiselect("Branches", sorted(frame["branch"].unique()), default=sorted(frame["branch"].uniq...`` | Create a branch multiselect using sorted distinct source labels, selecting all by default. The stable key identifies this widget and its return value is the selected list. |
| 139 | ``filtered = filtered[filtered["branch"].isin(selected_branch)]`` | Test branch membership with isin and keep matching rows using Boolean indexing. Choosing no branch retains no rows. |
| 140 | ``selected_meal_period = st.sidebar.multiselect("Meal periods", sorted(frame["meal_period"].unique()), default=sorted(frame[...`` | Create the meal-period multiselect from all source meal labels with its own stable key. Options are not dynamically recomputed from the branch-filtered subset. |
| 141 | ``filtered = filtered[filtered["meal_period"].isin(selected_meal_period)]`` | Keep only rows whose meal period is selected, among rows already matching the chosen branches. The conditions therefore combine as AND. |
| 142 | ``dates = st.sidebar.date_input("Date range", (frame["date"].min().date(), frame["date"].max().date()), min_value=frame["dat...`` | Create a date-range input bounded by the source minimum and maximum dates. date() converts timestamps to Python date objects for the widget; the tuple supplies both default endpoints. |
| 143 | ``if len(dates) != 2:`` | Check that two endpoints have been supplied before accessing both positions. A partially selected interval is allowed as a temporary UI state. |
| 144 | ``st.info("Choose both a start and an end date.")`` | Tell the viewer to finish the date range. |
| 145 | ``st.stop()`` | Stop the current run until that selection is complete. |
| 146 | ``filtered = filtered[filtered["date"].dt.date.between(dates[0], dates[1])]`` | Use the datetime accessor to get date values, apply an inclusive between test, and retain matching records. |
| 147 | ``st.sidebar.caption(f"Showing {len(filtered):,} of {len(frame):,} rows")`` | Display selected and total source row counts. Number formatting adds thousands separators only to the visible text. |
| 148 | ``if filtered.empty:`` | Check whether the combined branch, meal, and date filters left no rows. |
| 149 | ``st.info("No rows match these filters. Select at least one value or widen the date range.")`` | Explain how to restore a valid selection instead of displaying empty metrics or failing during extrema calculations. |
| 150 | ``st.stop()`` | Stop before calculating group leaders or charts on an empty dataset. |

### Lines 152-176: calculate metrics, group comparisons, and service evidence

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 152 | ``# 3. Derive business measures, then compare totals, distributions and segments.`` | Mark the start of business measure derivation and comparison. |
| 153 | ``filtered["contribution"] = filtered["bill_amount"]-filtered["food_cost"]`` | Subtract food cost from bill amount for each selected order and save the resulting contribution column. It subtracts one recorded cost category, not all operating costs. |
| 154 | ``sales = filtered["bill_amount"].sum()`` | Add selected bill amounts into one scalar sales total. |
| 155 | ``columns = st.columns(4)`` | Create four equal-width display containers and store them in columns. Python indexing begins at zero. |
| 156 | ``columns[0].metric("Sales (INR)", f"{sales:,.0f}")`` | Show sales in the first card. :,.0f adds grouping separators and rounds the displayed INR amount to a whole number. |
| 157 | ``columns[1].metric("Average bill (INR)", f"{filtered['bill_amount'].mean():,.0f}")`` | Display the mean bill per order in the second card. Required bill values are nonmissing, so the mean uses all selected orders. |
| 158 | ``columns[2].metric("Average wait", f"{filtered['wait_minutes'].mean():.1f} min")`` | Display mean wait with one decimal and the minutes label. This mean gives each order one observation, not each guest one weight. |
| 159 | ``columns[3].metric("Average rating", f"{filtered['rating'].mean():.2f} / 5")`` | Display the average rating with two decimals and an explicit out-of-five label. |
| 160 | ``st.caption("One row is one order. Contribution = bill - food cost, before staffing, rent, delivery fees and tax. Ratings a...`` | Explain contribution's excluded costs and caution that observed rating patterns do not establish the effect of waiting time. |
| 161 | ``branch_summary = filtered.groupby("branch").agg(orders=("order_id","size"),sales=("bill_amount","sum"),wait=("wait_minutes...`` | Group by branch and create named columns for row count, sales sum, mean wait, and mean rating. size counts rows; it does not count unique order IDs. |
| 162 | ``sales_leader = branch_summary["sales"].idxmax()`` | Return the branch index label with the largest sales sum. idxmax finds a label, not the numeric total itself. |
| 163 | ``slowest = branch_summary["wait"].idxmax()`` | Return the branch label with the greatest mean wait. It identifies a descriptive leader, not a statistically established operational cause. |
| 164 | ``association = filtered["wait_minutes"].corr(filtered["rating"]) if len(filtered)>1 else float("nan")`` | Calculate Pearson correlation between wait and rating when more than one row exists; otherwise assign NaN. With multiple rows, constant variables can still yield an undefined result. |
| 165 | ``association_text = f"Pearson correlation is {association:.2f}. This describes a linear association, not a causal effect." ...`` | If the correlation is present, create text containing its rounded value and noncausal interpretation; otherwise explain insufficient variation or observations. |
| 166 | ``cell_counts = filtered.groupby(["branch","meal_period"]).size()`` | Count rows for each observed branch/meal-period combination. The result is a Series with a two-level index, used for sample-size cautions and the report-tab table. |
| 167 | ``insights = [`` | Begin insights as a list of question/answer tuples that can be reused in the page and report. |
| 168 | ``("What business is represented?", f"{len(filtered):,} orders for {filtered['guests'].sum():,} guests generated INR {sales:...`` | Report orders, guest appearances, sales, and total contribution. Sum guest counts and contribution across the selected records; the latter remains before other operating costs. |
| 169 | ``("Which branch leads sales?", f"{sales_leader} records INR {branch_summary.loc[sales_leader,'sales']:,.2f} across {branch_...`` | Retrieve the sales-leading branch's sales and order count by label. The answer explicitly says totals are not normalized for capacity or opening hours. |
| 170 | ``("Where is average service slowest?", f"{slowest} has the longest selected mean wait at {branch_summary.loc[slowest,'wait'...`` | Describe the greatest branch mean wait with its supporting order count and a reminder to consider channel/meal context before staffing decisions. |
| 171 | ``("What does the service tail look like?", f"Median wait is {filtered['wait_minutes'].median():.1f} minutes; the 90th perce...`` | Calculate median wait and the 90th percentile for the same selection, then explain that the percentile describes its slower end. |
| 172 | ``("Are wait time and rating related?", association_text),`` | Reuse association_text rather than computing a second correlation or inconsistent explanation. |
| 173 | ``("How much is spent per guest?", f"Sales per guest are INR {ratio(sales,filtered['guests'].sum()):,.2f}, compared with INR...`` | Compare sales per guest, a ratio of summed amounts/counts, with mean bill per order. The differing denominators are stated explicitly. |
| 174 | ``("How much evidence supports subgroup ratings?", f"The smallest observed branch/meal-period cell has {int(cell_counts.min(...`` | Report the minimum observed subgroup count and count of observed cells below 20. The threshold is illustrative, and combinations with no rows are absent from cell_counts. |
| 175 | ``]`` | Close the insights list. |
| 176 | ``kpi_values=[("Sales (INR)",f"{sales:,.2f}"),("Average bill (INR)",f"{filtered['bill_amount'].mean():,.2f}"),("Average wait...`` | Build report label/value pairs for five measures, including sales per guest. This list has five entries although only four top cards were created; contribution is discussed elsewhere. |

### Lines 178-195: describe the analytical scope and display definitions

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 178 | ``# Build one report from the same filtered dataframe used by the charts.`` | Comment that one report will use the same selected DataFrame as the charts. |
| 179 | ``scope_parts = []`` | Start an empty list of human-readable scope descriptions. |
| 180 | ``for column in frame.select_dtypes(include="object").columns:`` | Iterate over columns that have object dtype in the loaded source. This includes text labels and order IDs in the workshop environment. |
| 181 | ``if frame[column].nunique() <= 12:`` | Include only fields having at most 12 distinct source values. This heuristic excludes the many order IDs while usually retaining branch, meal_period, and channel. |
| 182 | ``scope_parts.append(column.replace("_", " ") + ": " + ", ".join(map(str, sorted(filtered[column].unique()))))`` | Convert underscores in the field label to spaces, sort unique selected values, convert them to strings, join with commas, and append the resulting statement. |
| 183 | ``for column in frame.select_dtypes(include="datetime").columns:`` | Loop over datetime fields in the source; date qualifies after explicit conversion. |
| 184 | ``scope_parts.append(f"{column}: observed records {filtered[column].min():%Y-%m-%d} to {filtered[column].max():%Y-%m-%d}")`` | Append the observed selected minimum and maximum date in YYYY-MM-DD form. Observed limits may be narrower than the requested range. |
| 185 | ``scope_parts.append(f"Requested date window: {dates[0]} to {dates[1]} (inclusive)")`` | Also append the actual requested inclusive endpoints, preserving selection intent separately from observed dates. |
| 186 | ``scope = "; ".join(scope_parts)`` | Join the collected scope statements with semicolons into a single string. |
| 188 | ``with st.expander("KPI definitions and calculation rules"):`` | Create an expander for metric definitions. It groups explanatory UI elements but does not make their code lazy. |
| 189 | ``st.dataframe(pd.DataFrame(FORMULAS, columns=["Measure", "Calculation", "Business meaning"]), hide_index=True, width="stret...`` | Create a three-column DataFrame from FORMULAS and display it without an index, stretched to the available width. |
| 190 | ``st.caption("All cards, charts and findings use the same selected rows. Ratios use summed numerators and denominators where...`` | State the common-row rule and the correct interpretation of zero-denominator fallback values. |
| 192 | ``st.subheader("What the selected data answers")`` | Display the heading for the short calculated answers. |
| 193 | ``for question, answer in insights[:3]:`` | Loop over the first three insight tuples, unpacking question and answer. The slice selects a concise subset for this page section. |
| 194 | ``st.markdown(f"**{question}** {answer}")`` | Render each question in bold followed by its generated answer string. |
| 195 | ``st.caption(f"Analysis scope: {len(filtered):,} of {len(frame):,} source rows. " + scope)`` | Show selected/source row counts and the assembled scope, keeping conclusions tied to their input selection. |

### Lines 197-213: construct the downloadable Markdown report

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 197 | ``report_parts = [`` | Start report_parts as a list of complete Markdown sections. The list is data assembled during this script run. |
| 198 | ``"# " + '06 Restaurant Operations' + " - full analytical report",`` | Add the report's project heading. It will be rendered by Streamlit and saved in the download. |
| 199 | ``"## 1. Business problem\n" + CASE,`` | Add section 1 and the CASE string with a newline after the heading. |
| 200 | ``"## 2. Context and decision\n" + DECISION + "\n\n" + DATA_CONTEXT,`` | Add section 2 with DECISION and DATA_CONTEXT separated by blank lines. |
| 201 | ``"## 3. Data and analysis scope\n" + f"Dataset: `{DATA_FILE.name}`. Selected rows: {len(filtered):,} of {len(frame):,}.\n\n...`` | Add the source filename, selected/source counts, scope, INR and fictional-data statements, and descriptive limits. F-string expressions use the current run's variables. |
| 202 | ``"## 4. Executive summary\n" + "\n\n".join(answer for _,answer in insights[:3]),`` | Build an executive summary by joining the first three insight answers. The underscore discards each pair's question inside the generator expression. |
| 203 | ``"## 5. KPI results\n\| Measure \| Selected result \|\n\| --- \| --- \|\n" + "\n".join(f"\| {name} \| {value} \|" for name,value in ...`` | Construct the KPI Markdown table with one row for each kpi_values pair. Pipes and separator characters are Markdown text inside strings, not calculations. |
| 204 | ``"## 6. Definitions and methods\n\| Measure \| Calculation \| Interpretation \|\n\| --- \| --- \| --- \|\n" + "\n".join(f"\| {name} ...`` | Construct a methods table from the three-field formula tuples, recording label, calculation, and meaning. |
| 205 | ``"## 7. Questions answered by the data\n" + "\n\n".join(f"### {question}\n{answer}" for question,answer in insights),`` | Include all seven insights, each with a question heading and corresponding answer. This includes service-tail and subgroup-evidence text absent from the short summary. |
| 206 | ``"## 8. Every visual explained\n" + "\n\n".join(f"### {title}\n**Purpose:** {purpose}\n\n**How to read:** {reading}\n\n**Qu...`` | Create a detailed explanation of all five visuals from VISUAL_GUIDE. The Markdown contains textual chart guides, not embedded Plotly or Matplotlib images. |
| 207 | ``"## 9. Data quality and aggregation\n" + f"Source rows: {len(frame):,}; exact duplicate rows: {frame.duplicated().sum():,}...`` | Add source-wide counts of rows, exact duplicate rows, and missing cells using frame, along with validation and outlier-handling explanations. |
| 208 | ``"## 10. Suggested next steps\n" + "\n".join(f"{i}. {text}" for i,text in enumerate(RECOMMENDATIONS,1)) + "\n\nTreat these ...`` | Number recommendations starting at one with enumerate, join them into a list, and remind readers that these are suggested investigations. |
| 209 | ``"## 11. What this analysis cannot answer\n" + LIMITATIONS + "\n\nTies in automatically named leaders are resolved by the d...`` | Add LIMITATIONS and shared caution text about ties, absent uncertainty tests, and insufficient data for correlations. Grouped maxima use sorted group order when ties are resolved. |
| 210 | ``"## 12. Reproduce and extend the analysis\nOpen the CSV beside app.py, restore the filter selections listed above, and com...`` | Add reproduction and extension instructions about filters, source rows, downloads, chart interaction, and further investigation. The string does not bundle the source CSV or rendered charts. |
| 211 | ``]`` | Close the report section list. |
| 212 | ``report_parts[5] += "\n\n### Source field dictionary\n\| Field \| Meaning and units \|\n\| --- \| --- \|\n" + "\n".join(f"\| `{nam...`` | Append the source field dictionary to report_parts[5], which is the KPI-results section because the title occupies index 0. Iterate dictionary items to build Markdown rows; += extends that section string. |
| 213 | ``full_report = "\n\n".join(report_parts)`` | Join report sections with blank lines into full_report. The display and download later use this identical string. |

### Lines 215-240: arrange tabs and draw all five charts

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 215 | ``overview, explore, data_tab, report_tab = st.tabs(["Operations dashboard", "Explore the data", "Data and quality", "Full r...`` | Create four tab containers and unpack their references into overview, explore, data_tab, and report_tab. Their contents all execute on a normal rerun in this workshop version. |
| 216 | ``with overview:`` | Route subsequent indented UI calls into Operations dashboard. |
| 217 | ``daily = filtered.groupby(["date","branch"], as_index=False)["bill_amount"].sum()`` | Group selected orders by both date and branch and sum bill_amount. as_index=False leaves date and branch as chart-addressable columns. |
| 218 | ``st.plotly_chart(px.line(daily, x="date", y="bill_amount", color="branch", title="Daily sales by branch", labels={"bill_amo...`` | Build and display a Plotly line figure with a separate colored series per branch. Each point represents an observed group total; absent date/branch combinations are not filled with zero. |
| 219 | ``explain_visual(0, st)`` | Display guide item 0, explaining the daily sales chart and missing-date caution. |
| 220 | ``st.plotly_chart(px.scatter(filtered, x="wait_minutes", y="rating", color="channel", size="guests", hover_data=["order_id",...`` | Create and render an order-level scatter: wait on x, rating on y, channel colors, guest-sized bubbles, and order/branch/bill hover fields. Opacity helps expose overlap; no guest weighting is applied to correlation. |
| 221 | ``explain_visual(1, st)`` | Display guide item 1, the scatter reading instructions and noncausal interpretation. |
| 222 | ``st.dataframe(filtered.groupby("branch").agg(orders=("order_id","size"), sales=("bill_amount","sum"), contribution=("contri...`` | Display a branch table with row counts, sales/contribution sums, mean wait, and mean rating, rounded to two decimals. The DataFrame index remains visible as the branch label. |
| 223 | ``st.caption("The table above gives exact grouped values behind the dashboard. Group sizes matter: compare counts alongside ...`` | Explain why the table's exact values and group counts should be consulted alongside totals or means. |
| 224 | ``with explore:`` | Route the next plots into Explore the data. |
| 225 | ``left, right = st.columns(2)`` | Create left and right columns for the histogram and boxplot. |
| 226 | ``fig, ax = plt.subplots(figsize=(7,4))`` | Create a seven-by-four-inch Matplotlib figure and axes. fig represents the whole canvas; ax is the area receiving chart commands. |
| 227 | ``ax.hist(filtered["bill_amount"], bins=20, color="#e11d48", edgecolor="white")`` | Draw a 20-bin histogram of order bills with a rose color and white bin edges. The bars count orders in numeric ranges. |
| 228 | ``ax.set(title="Order value distribution", xlabel="Bill amount (INR)", ylabel="Orders")`` | Set title and axes: INR bill amount on x and order count on y. |
| 229 | ``left.pyplot(fig); plt.close(fig)`` | Display the figure in the left column, then close its Matplotlib-managed resources. A semicolon separates these two Python statements on the same line. |
| 230 | ``explain_visual(2, left)`` | Display the histogram's guide in the left column. |
| 231 | ``fig, ax = plt.subplots(figsize=(7,4))`` | Create a fresh figure/axes for the boxplot, avoiding reuse of the histogram canvas. |
| 232 | ``sns.boxplot(data=filtered, x="meal_period", y="wait_minutes", ax=ax, color="#fecdd3")`` | Have Seaborn summarize wait distributions by meal_period on the supplied axes, using the selected order rows. |
| 233 | ``ax.set_title("Service time by meal period")`` | Set the boxplot title. Axis labels are derived from the named data variables unless otherwise specified. |
| 234 | ``right.pyplot(fig); plt.close(fig)`` | Render the boxplot in the right column, then close the underlying Matplotlib figure. |
| 235 | ``explain_visual(3, right)`` | Display the meal-period explanation in that same right column. |
| 236 | ``fig, ax = plt.subplots(figsize=(9,4))`` | Create a wider figure for the matrix of subgroup mean ratings. |
| 237 | ``sns.heatmap(filtered.pivot_table(index="branch", columns="meal_period", values="rating", aggfunc="mean"), annot=True, fmt=...`` | Pivot ratings into branch rows and meal-period columns with mean aggregation, then draw the heatmap. Annotations use two decimals; vmin=1 and vmax=5 keep a fixed score scale. No missing group is assigned a zero score. |
| 238 | ``ax.set_title("Average rating by branch and meal period")`` | Set the title identifying both grouping dimensions and the mean-rating measure. |
| 239 | ``st.pyplot(fig); plt.close(fig)`` | Display the heatmap in the current tab's main area, then close the Matplotlib figure. |
| 240 | ``explain_visual(4, st)`` | Render guide item 4, including the caution about group counts and variation hidden by means. |

### Lines 242-266: expose source evidence, practice prompts, and exports

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 242 | ``# 4. Inspect the underlying data and practice explaining the results.`` | Comment on the purpose of the final inspection and learning section. |
| 243 | ``with data_tab:`` | Route indented display calls into Data and quality. |
| 244 | ``st.subheader("Source field dictionary")`` | Add the source-field-dictionary heading. |
| 245 | ``st.dataframe(pd.DataFrame(FIELD_GUIDE.items(), columns=["Field", "Meaning and units"]), hide_index=True, width="stretch")`` | Convert dictionary item pairs into a two-column table of field names and meanings. Hide the row index and use available width. |
| 246 | ``st.subheader("Filtered records")`` | Add the heading for filtered records. |
| 247 | ``st.write("These are the exact selected observations used for the KPIs and charts, including any derived columns. Sorting t...`` | Explain that the table contains the exact selected rows with derived columns and that browser sorting does not modify the analytical selection. |
| 248 | ``st.dataframe(filtered, hide_index=True, width="stretch")`` | Display the filtered DataFrame, including contribution, with the numeric row index hidden. |
| 249 | ``st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_restaurant_orders.csv", "text/csv")`` | Convert selected rows to CSV without an index and offer a text/csv download. The filename is fixed, but the payload follows current filters; the source file is not overwritten. |
| 250 | ``st.subheader("Numeric summary")`` | Add the numeric-summary heading. |
| 251 | ``st.write("Count is the number of available values; mean is the arithmetic average; std measures spread; min/max are extrem...`` | Explain the summary statistics in ordinary language before displaying them. |
| 252 | ``st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")`` | Select numeric columns, compute describe() statistics, round the result, and display it. This includes derived contribution but excludes text identifiers and dates. |
| 253 | ``st.subheader("Source data quality")`` | Add the source-quality heading, signaling a different scope from selected rows. |
| 254 | ``st.write(f"Rows: {len(frame):,} \| Exact duplicates: {frame.duplicated().sum():,} \| Missing cells: {frame.isna().sum().sum(...`` | Show full-source row count, exact duplicates, and total missing cells. duplicated() compares complete rows, not just order_id values. |
| 255 | ``st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum()...`` | Build a per-source-column table of its name, dtype string, and missing count. The .values arrays align positionally with frame.columns; contribution is not in the source table. |
| 257 | ``with st.expander("Workshop exercises and chart guide"):`` | Create a workshop-exercise expander outside the preceding data-tab block. |
| 258 | ``st.markdown('1. Find the branch with the longest average wait.\n2. Add a channel filter and compare delivery with dine in....`` | Display four learner prompts separated by escaped newlines. The channel filter is proposed here; this text does not create such a widget. |
| 259 | ``st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts supp...`` | Describe what Matplotlib, Seaborn, and Plotly teach about figure control, statistical views, and interactive exploration. |
| 260 | ``st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause an...`` | Remind learners that the fictional observations do not establish cause and effect. |
| 262 | ``with report_tab:`` | Route the final elements into Full report. |
| 263 | ``st.download_button("Download full report (Markdown)", full_report, "06_restaurant_operations_report.md", "text/markdown")`` | Offer full_report as a text/markdown download with the restaurant report filename. The string contains this run's selected findings. |
| 264 | ``st.markdown(full_report)`` | Render the same report string in the tab, keeping on-screen report text and the exported text consistent. |
| 265 | ``st.subheader("Branch and meal-period sample sizes")`` | Add a separate sample-size table heading after the report. This Streamlit element is not appended to the full_report string. |
| 266 | ``st.dataframe(cell_counts.rename("orders").reset_index(), hide_index=True, width="stretch")`` | Rename the count Series to orders, turn its two-level branch/meal index back into columns with reset_index(), and display it. This full table is visible in the tab but not embedded in the downloaded Markdown. |


## Run the project and investigate results

Use Python 3.12 and the shared workshop environment. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit==1.50.0 pandas==2.2.3 numpy==2.3.5 matplotlib==3.10.8 seaborn==0.13.2 plotly==6.5.2
cd business_analytics_workshop/06_restaurant_operations
python -m streamlit run app.py
```

On Windows PowerShell, activation is `.venv\Scripts\Activate.ps1`. The repository's phase names elsewhere contain `>`, so the [root README](../../README.md) recommends WSL or a Linux Cloud Lab for a full clone rather than a normal Windows filesystem checkout. Use the existing project filenames; the app expects the named sibling CSV.

The [workshop README](../README.md) describes the CookieSensei environment. To run a separate instance when the built-in dashboard occupies port 8501:

```bash
cd /home/coder/project/business_analytics_workshop/06_restaurant_operations
python -m streamlit run app.py --server.port 8502
```

Open the forwarded port in Coder. Adjust the directory only if your checkout actually lives elsewhere. Launching with `python -m streamlit run` starts the Streamlit server using the selected Python environment; plain `python app.py` is not the equivalent browser-app launch. [Streamlit run instructions](https://docs.streamlit.io/develop/concepts/architecture/run-your-app)

First compare the all-data cards with the verified values above. Next choose one branch and one meal period. Read the sample count before comparing its rating with another group. Inspect some orders near the longest waits in the data table, then explain both what is visible and which operational details remain unknown.

| Symptom | Likely cause and next step |
| --- | --- |
| An import cannot be found | Activate the intended environment and install with its `python -m pip`. |
| The CSV cannot be loaded | Verify the file is beside the script, the header is intact, and required dates/numbers are parseable. |
| A date selection shows a message and no charts | Choose both endpoints; the app intentionally stops while the range is incomplete. |
| No rows match | Restore branch/meal selections or widen the date window. Empty multiselects select no records. |
| A correlation value is unavailable | There may be one row or no variation in wait/rating. More identical observations do not resolve a constant-variable correlation. |
| One heatmap group disappears | No selected rows may exist for that group. The code does not invent zero-rating observations. |
| Sales per guest shows zero with zero total guests | The scalar helper returned a safeguard value. The ratio is undefined; inspect the data instead of interpreting zero spending. |
| CSV changes do not appear | Save and rerun. The file is uncached, but it is reread only when the script executes. |
| A download has an extra `contribution` column | The app exports analyzed rows, including derived values. It has not modified the original CSV. |
| The report download lacks the full subgroup-count table | That table is a separate UI element after the report string. The report text includes summary counts, not the full table. |

## Worked practice and self-checks

These examples are learner exercises and extensions, not features already present. Unless a specific placement is given, put additional calculations after line 153, after filters and empty-data checks and after contribution has been derived. Match each new number with a clearly stated unit and denominator.

### Practice 1: trace one CSV order

Open the first CSV row. Calculate `470.12 - 102.74 = 367.38` INR contribution. Explain why that is not net profit, identify the order's recorded wait and rating, and list two unavailable facts needed to explain the score. A good explanation separates values that exist in the record from guesses about their cause.

### Practice 2: add a channel filter

The existing app has no channel filter. Add this code after its meal-period filtering, before date filtering and the final empty-data guard:

```python
selected_channel = st.sidebar.multiselect(
    "Channels",
    sorted(frame["channel"].unique()),
    default=sorted(frame["channel"].unique()),
    key="06_restaurant_operations_channel",
)
filtered = filtered[filtered["channel"].isin(selected_channel)]
```

The widget returns selected channel names. `.isin(...)` tests every surviving order against them. Because the new filter is applied before calculations, it changes KPIs, charts, insights, and report together. Placing it after the sales calculation would create inconsistent scopes. Keeping the existing final empty-data check ensures clearing the new selection also produces a helpful message.

Compare Delivery with Dine in while holding branch, meal period, and dates constant. State the number of orders in each comparison. Any difference remains descriptive because the groups may differ in party size, order type, or other unrecorded features.

### Practice 3: compare mean and tail waits by branch

```python
wait_summary = filtered.groupby("branch").agg(
    orders=("order_id", "size"),
    mean_wait=("wait_minutes", "mean"),
    median_wait=("wait_minutes", "median"),
    p90_wait=("wait_minutes", lambda values: values.quantile(0.9)),
)
st.dataframe(wait_summary.round(2))
```

Named aggregation gives the output readable column names. The lambda is a small function that receives each branch's wait series and returns its 90th percentile. This preserves counts beside the summaries. A branch could have a reasonable median but an unfavorable upper tail; the additional column makes that distinction visible. A tiny group's percentile still needs caution.

### Practice 4: put ratings and evidence counts together

```python
experience = filtered.groupby(["branch", "meal_period"]).agg(
    orders=("order_id", "size"),
    mean_rating=("rating", "mean"),
    median_wait=("wait_minutes", "median"),
)
st.dataframe(experience.round(2))
```

This table shows the rating and order count on the same row, alongside a service measure. It makes the subgroup evidence easier to inspect than reading a heatmap and count table separately. Do not convert a count of 20 into a claim of proven reliability; uncertainty depends on variability, sampling, and the decision being made.

### Practice 5: inspect slow orders without losing ties

```python
threshold = filtered["wait_minutes"].quantile(0.9)
slow_orders = filtered[filtered["wait_minutes"] >= threshold]
st.dataframe(
    slow_orders.sort_values("wait_minutes", ascending=False),
    hide_index=True,
)
```

This keeps every order at or beyond the estimated 90th-percentile threshold. Because waits can tie at the threshold, it can contain more than exactly 10% of orders. It answers which records meet a duration rule, not “which exact fixed number of customers are the slowest.” Compare their channels, meal periods, and party sizes, then identify operational logs you would need to explain the delays.

### Practice 6: reproduce the correct sales-per-guest measure

```python
selected_sales = filtered["bill_amount"].sum()
selected_guests = filtered["guests"].sum()
if selected_guests > 0:
    st.metric("Sales per guest (INR)", f"{selected_sales / selected_guests:,.2f}")
else:
    st.info("Sales per guest is undefined without a positive guest total.")
```

This extension adds a visible card with an explicit positive-denominator check. It does not change the original helper or imply that the current code already displays this card. Compare the ratio with `filtered["bill_amount"].div(filtered["guests"]).mean()` only after confirming every order's guest count is positive. Explain why the two weighting choices differ using the illustrative two-order example above.

### Practice 7: formulate a testable operational question

After finding a long-wait subgroup, write a question such as: “For comparable dinner orders at this branch, does a specified preparation change reduce waiting time without lowering ratings or contribution?” State what new data is needed, how a comparison group could be formed, and what costs should be measured. The dashboard helps select a question; it does not conduct that experiment or estimate its result.

## Limits and possible improvements

The input checks require the expected columns, at least one row, parseable numbers/dates, and nonmissing required fields. They do not check unique order IDs, positive integer guest counts, finite amounts, nonnegative waits, a rating range of 1-5, or whether food cost can exceed a bill. The field dictionary describes intended units and ranges; it does not enforce them. Exact duplicate rows are reported later without removal.

This matters for custom data. A negative guest count may be parseable but incompatible with a scatter marker size; an out-of-range rating may be accepted while the heatmap still has its fixed 1-5 scale. Only the loading block is covered by its `try`/`except`; the subsequent analysis and charting are not wrapped by that handler. The bundled file satisfies the teaching assumptions, but adding new validation would be a separate improvement.

Branch leaders are selected by `.idxmax()`, which returns the first label attaining a maximum. Grouping sorts labels by default, so tied branch results can produce one alphabetically earlier label rather than displaying every tie. Group means also mix different channel, meal, and party-size distributions; a reversal between overall and subgroup comparisons is possible. The app does not adjust for that mix or estimate statistical uncertainty.

The fixed written case says 600 orders across January-April 2025. If you replace the CSV with a different dataset, the numeric analysis and scope will update, but those narrative constants will not rewrite themselves. Update the case text and field meanings when changing the teaching scenario. The app's scope strings are descriptive summaries, not a serialized record of every widget setting or a guarantee that unchanged filters reproduce results after source edits.

Possible improvements include explicit domain validation, identifying tied leaders, presenting full subgroup counts beside the rating heatmap, adding a channel filter, including the count table in the Markdown export, recording source-data revisions, and extending data collection with staffing/capacity/context fields. None of these is claimed as an existing feature. The present project teaches how to build and explain a descriptive analytical application using the data actually available.

## References

- [Project source: app.py](app.py), [dataset: restaurant_orders.csv](restaurant_orders.csv), and [workshop setup](../README.md) are the primary sources for implemented behavior and the reference calculations.
- [pandas 2.2 introductory guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html), [indexing guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/indexing.html), and [group-by guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html) explain table operations used here.
- [pandas Series.quantile](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.Series.quantile.html) documents percentile interpolation, and [Series.corr](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.Series.corr.html) documents correlation behavior.
- [Streamlit main concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts), [run instructions](https://docs.streamlit.io/develop/concepts/architecture/run-your-app), and [Streamlit 1.50.0 tabs](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs) explain execution and layout.
- [Plotly Express overview](https://plotly.com/python/plotly-express/), [Matplotlib histogram](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html), [Seaborn boxplot](https://seaborn.pydata.org/generated/seaborn.boxplot.html), and [Seaborn heatmap](https://seaborn.pydata.org/generated/seaborn.heatmap.html) document the charting tools.
