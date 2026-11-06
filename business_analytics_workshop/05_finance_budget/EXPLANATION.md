# Budget versus Actuals - Business Problem, Analysis, and Code Explained

This guide explains the [actual `app.py` in this folder](app.py), using its [department budget CSV](department_budget.csv). It is written for a learner who can read a spreadsheet but is still learning Python. The goal is to understand both **what the program does** and **why those operations help answer a business question**.

The code walkthrough refers to `app.py` at repository revision [`c10a61c36fffdd048b69dd78926e6663bc986fce`](https://github.com/cookieSensei/programming-and-ai/blob/c10a61c36fffdd048b69dd78926e6663bc986fce/business_analytics_workshop/05_finance_budget/app.py). Line numbers describe that version. This document adds teaching material; it does not change the application. The dataset is fictional, all amounts are INR, and its 2025 dates are a teaching period rather than current business results.

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

Imagine a finance manager reviewing departmental expenses. The organization approved a spending plan, then recorded what it actually spent. The manager wants to know whether spending is within plan, where differences arise, and which department owners should explain those differences.

A single total does not answer all of that. One department could overspend by INR 200,000 while another spends INR 180,000 less than planned. The combined overspend is only INR 20,000, although two much larger differences need explanation. Likewise, the department with the greatest expenses might simply have the greatest approved budget. High spending and poor budget adherence are different questions.

This project therefore examines several levels of evidence:

- **The selected portfolio of expenses:** total budget, actual expense, net variance, and utilization.
- **Departments and months:** groups that explain the totals.
- **Individual budget lines:** the number and size of overspends that totals can hide.
- **Department/category combinations:** a two-dimensional breakdown that can reveal where a department's expense gap is concentrated.

The useful business output is an investigation agenda: “Operations has the lowest aggregate variance; inspect its underlying categories and months, then ask about volume, timing, and approved changes.” The app does not establish that overspending was wasteful. An unplanned expense may have produced valuable business output, and an underspend may reflect delayed work rather than efficiency.

This is **exploratory data analysis**, or EDA. It organizes and summarizes observed records, shows distributions and comparisons, and suggests follow-up questions. It does not forecast future expenses, train an AI model, decide a new budget, or calculate company profit. The distinction matters because the dataset contains neither income nor a complete statement of costs, cash movements, commitments, or output delivered. The project's `CASE`, `DECISION`, and `LIMITATIONS` constants state this scope directly. [Source: `app.py`](app.py)

## Dataset and row meaning

### What one row represents

One row is **one department, one expense category, and one month**. This is the dataset's *grain*: the level of detail represented by a record. There are 192 rows: 12 months multiplied by four departments multiplied by four expense categories. A row is not one purchase, one employee, or one payment.

For example, the first CSV row is:

| month | department | expense_category | budget | actual |
| --- | --- | --- | ---: | ---: |
| 2025-01-01 | Sales | People | 112,000 | 131,473.15 |

Read this as: “The Sales department's People expense line for January has an approved amount of INR 112,000 and a recorded amount of INR 131,473.15.” It does not mean all that expense was paid on January 1. The first day is a label for the budget month. [Source: `department_budget.csv`](department_budget.csv)

### Field dictionary

| Field | Meaning | Type after loading | How the app uses it |
| --- | --- | --- | --- |
| `month` | Budget month, represented by its first day | pandas datetime | Inclusive date filtering and monthly aggregation |
| `department` | Responsible department | Text (`object` in the workshop version) | Sidebar selection, group totals, and heatmap rows |
| `expense_category` | Type of expense | Text | Sidebar selection, boxplot groups, and heatmap columns |
| `budget` | Planned expense in INR for this line | Numeric | Sum, variance, and utilization denominator |
| `actual` | Recorded expense in INR for this line | Numeric | Sum, variance, utilization numerator, and expense distribution |
| `variance` | `budget - actual` | Derived numeric column | Overspend detection, grouping, histogram, and heatmap |

The original CSV contains the first five fields. The sixth is calculated in memory at line 142. It is included in the filtered CSV download, but the app does not write it back into `department_budget.csv`.

The departments in the bundled file are Customer Success, Engineering, Operations, and Sales. Categories are Facilities, People, Software, and Travel. Dates run from January 1 to December 1, 2025, representing all 12 budget months. The CSV has no missing cells or exact duplicate rows in this revision. Those are structural observations about this file, not proof that its fictional amounts represent sound accounting. [Source: `department_budget.csv`](department_budget.csv)

### Why grain matters before calculation

Counting rows answers “How many budget lines are selected?” It cannot answer “How many employees are over budget?” Similarly, 109 overspent lines out of 192 means about 56.8% of the selected **lines**, not 56.8% of the money. A small INR 100 overspend and a large INR 50,000 overspend each count as one line.

The program assumes that the month/department/category combination is meaningful. It reports exact duplicate rows but does not enforce uniqueness of that combination. Two different rows for the same combination would both be summed. In a real import, decide whether those are legitimate revisions, separate sublines, or accidental duplication before analysis.

## Why pandas and the other libraries

### Why pandas fits this problem

The CSV is a rectangular table. pandas provides a `DataFrame`, which holds rows, named columns, an index, and a data type for each column. That makes the code resemble the questions being asked:

```python
frame = pd.read_csv(DATA_FILE)
filtered["variance"] = filtered["budget"] - filtered["actual"]
dept_summary = filtered.groupby("department")[["budget", "actual", "variance"]].sum()
```

The first line turns the text file into a table. The second subtracts matching columns **row by row**. The third separates rows by department, chooses the measures to summarize, and adds them within each department. The result is a new, smaller table with one row per department. pandas' [introductory guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html) and [grouping guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html) explain these structures and the split-apply-combine process.

You could implement the same calculations using Python's `csv` module, dictionaries, loops, and manual running totals. pandas is useful here because it gives readable, reusable operations for filtering, date parsing, grouping, summary statistics, and pivot tables. The choice reduces repeated bookkeeping; it does not make business assumptions automatically correct.

### Read the main pandas expressions

- `frame["budget"]` selects one column as a `Series`, a one-dimensional labeled collection.
- `frame[["budget", "actual"]]` selects two columns as a `DataFrame`. The inner brackets create a Python list of names; the outer brackets perform selection.
- `frame.copy()` creates a separate working table so derived columns can be added without changing the source table used for quality reporting.
- `filtered["department"].isin(selected_department)` produces one Boolean value per row: `True` if that department was selected, otherwise `False`.
- `filtered[mask]` keeps rows whose corresponding Boolean values are `True`. This is called Boolean indexing.
- `.sum()` produces a total; `.mean()` would produce an average. Choosing between them depends on the business question, not on the chart you want to draw.
- `.groupby("department")` defines groups; it does not itself choose how those groups are summarized. `.sum()` supplies the operation.
- `.idxmin()` returns the **index label** of the smallest value, not the smallest number. With department names as the index, it returns a department name.
- `.loc[label]` selects by an index label. It lets the app retrieve the row that explains a minimum variance.
- `.pivot_table(...)` arranges two grouping dimensions as rows and columns and computes one number for each combination.

### Each library has a separate job

| Import | Job in this app | Why it is used here |
| --- | --- | --- |
| `Path` from `pathlib` | Find the CSV beside the script | Avoid dependence on the directory from which the terminal command was launched |
| `pandas as pd` | Load, validate, filter, derive, aggregate, and export data | Express table analysis directly |
| `matplotlib.pyplot as plt` | Create figures and axes; draw the variance histogram | Give explicit control of bins, labels, and the zero reference line |
| `seaborn as sns` | Draw the category boxplot and department/category heatmap | Provide convenient statistical plotting on pandas tables |
| `plotly.express as px` | Build monthly line and department bar charts | Support interactive hover, zoom, and legend controls |
| `streamlit as st` | Build the browser interface | Connect Python results to controls, charts, tables, messages, and downloads |

The aliases `pd`, `plt`, `sns`, `px`, and `st` are short variable names for imported modules. They are conventions, not Python keywords. NumPy is included in the workshop installation command because it is part of the numerical environment; this app does not import or call NumPy directly.

## Connect business questions to code

| Business question | Relevant code and output | Why that operation answers it | Interpretation limit |
| --- | --- | --- | --- |
| How much was planned and recorded? | `filtered["budget"].sum()` and `filtered["actual"].sum()` at lines 143-144; KPI cards | Add every selected expense line exactly once | The totals cover the selected records, not necessarily all company expenses |
| Are we over or under budget overall? | `budget - actual`; unspent-budget card | The difference compares actual expense against the same scope of planned expense | Netting can hide large offsetting differences |
| What share of the plan was used? | `ratio(actual, budget)` | Divides total recorded expense by total available plan | Zero budget makes the rate undefined; the helper displays a fallback zero |
| How widespread is overspending? | `(filtered["variance"] < 0).sum()` | A Boolean test identifies overspent lines, and summing counts `True` values | It measures line frequency, not financial severity |
| Which department has the lowest variance? | `groupby("department").sum()`, then `idxmin()` | Combine each department's lines before comparing departments | The minimum can still be positive if every department is under budget |
| What is the largest individual overspend? | `filtered.loc[filtered["variance"].idxmin()]` | Identify the most negative row-level difference and retrieve its context | One exceptional line need not represent recurring behavior |
| Which months exceed plan? | Monthly totals followed by a negative-variance count | Compares each selected month's actual and plan at the same aggregation level | It does not count individual over-budget lines in those months |
| Which department/category pairs explain the gap? | Variance `pivot_table(..., aggfunc="sum")` | Group simultaneously on two dimensions | Opposite monthly variances can cancel inside one heatmap cell |

These are connected views of one filtered dataset. A chart visualizes an already defined calculation; choosing a chart type does not create the financial logic. The calculations appear in lines 142-165 and the visualizations in lines 204-232. [Source: `app.py`](app.py)

## Formulas and worked examples

### Variance: preserve the sign convention

For this app:

```text
variance = budget - actual
```

Using the first actual CSV row:

```text
112,000 - 131,473.15 = -19,473.15
```

The negative sign means recorded expense exceeded the plan by INR 19,473.15. If actual expense were INR 100,000 instead, variance would be positive INR 12,000: that much of the plan would be unspent. Many organizations use other sign conventions, so always read the formula before interpreting a red or green bar. This project consistently treats positive as under budget and negative as overspend.

Because subtraction distributes over addition, adding every row's variance gives the same net result as total budget minus total actual. That is why both the row-level histogram and the total KPI can be based on the same definition.

### Net overspend and gross overspend answer different questions

Consider this deliberately small **illustrative example**, separate from the bundled file:

| Line | Budget | Actual | Variance |
| --- | ---: | ---: | ---: |
| A | 100 | 130 | -30 |
| B | 100 | 80 | +20 |
| Total | 200 | 210 | -10 |

The net overspend is 10. The amount above plan on overspent lines is 30. The underspend on other lines is 20. Do not call 10 the total of all individual overspends: it already includes the offset.

The existing app calculates net variance, the count of overspent lines, and the largest overspent line. It does **not** display a KPI for the sum of only the negative variances. A suggested exercise below shows how to add that separate measure without confusing it with the existing total.

### Utilization: divide totals, not unweighted percentages

```text
utilization = total actual / total budget
displayed percentage = utilization x 100
```

Suppose one line has budget 100 and actual 150, while another has budget 900 and actual 900. Their utilizations are 150% and 100%. Averaging those percentages gives 125%, which gives equal influence to two very different budget sizes. The portfolio actually used 1,050 out of 1,000, or **105%**.

That is why the code first sums actual and budget and then divides. It is equivalent to weighting each valid line's utilization by that line's share of the total budget. It directly answers “What proportion of the selected plan was used?” The `:.1%` formatter multiplies the stored ratio by 100 for display, so `1.05` becomes `105.0%`; the calculation should not multiply by 100 again before applying that format.

### Count overspent lines before aggregation

```python
overspent_lines = int((filtered["variance"] < 0).sum())
```

First compare each line against zero. The result might look like `[True, False, True]`. Summing Booleans treats `True` as one and `False` as zero, producing two overspent lines. `int(...)` makes the result an ordinary integer for presentation.

Counting after grouping by department would answer a different question: “How many departments are overspent in total?” Those two counts are not interchangeable. A department can contain overspent lines while remaining under plan overall because other lines offset them.

### Zero denominators: a display safeguard, not a financial definition

The helper returns `numerator / denominator` when the denominator is nonzero and `0.0` otherwise. This prevents division-by-zero errors in the scalar KPI/report code. It does not mean that spending INR 500 against a zero budget is 0% utilization. That rate is undefined under the formula.

The department table uses a different approach: `.replace(0, float("nan"))` makes zero denominators missing, and `.div(...)` returns a missing rate. Both behaviors must be understood when using custom CSV data. The bundled dataset has no zero budgets, so its displayed utilization results do not use either fallback. The code also does not test for negative budgets or infinite values.

## How the Streamlit application works

### From an analysis script to a browser app

A normal Python analysis might load a CSV, calculate totals, and print them in the terminal. This program keeps the Python calculations and adds Streamlit calls around them:

1. `st.title`, `st.caption`, and text explain the question and context.
2. Sidebar widgets return the departments, categories, and dates the viewer selects.
3. pandas filters the source table using those returned values.
4. The code calculates measures from the selected rows.
5. `st.metric`, `st.plotly_chart`, `st.pyplot`, and `st.dataframe` display the results.
6. A Markdown string records the same analysis, and download buttons let the viewer save it or the filtered rows.

Streamlit runs the Python program on the machine hosting the app and presents its interface in a browser. The learner does not need to write HTML, CSS, JavaScript, a separate API, or a database just to build this dashboard. This describes the project's architecture, not a claim that those technologies are unnecessary for every web application. The [Streamlit main concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts) explain the framework's execution and display model.

### What happens after a filter changes

For this app's normal widget interactions, Streamlit reruns the script from top to bottom. The widgets return their current values. The CSV is read again, the selected rows are rebuilt, and all dependent calculations and text are regenerated. The project intentionally does not use `st.cache_data`; saving a CSV edit and rerunning therefore rereads the file. A file edit is not itself a continuously monitored data feed.

For example, choose only Operations. On the next run, `.isin(selected_department)` retains Operations rows, the category and date filters narrow them further, and every KPI/chart/report uses that resulting `filtered` table. The source-quality summary intentionally still examines `frame`, the full loaded source. “All charts use the selected rows” therefore does not mean that the source-quality counts are filtered.

Widget keys such as `05_finance_budget_department` give controls stable identities. They are not CSV columns. A `with overview:` block sends subsequent display calls into one tab. With the Streamlit version pinned for this workshop, creating tabs does not make their contents lazy: code in all tab blocks runs on a normal rerun. Expander contents are similarly computed even when their section is collapsed. This matters when judging performance; hiding a chart does not automatically avoid its calculation. [Streamlit tabs reference](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs)

Plotly hover/zoom, sorting the displayed data table, and ordinary tab switching change how existing output is viewed. They do not apply new sidebar filters or select different analytical records in this code. The app has no Plotly selection callback that would turn a clicked chart point into a pandas filter.

### Prevent incomplete analysis

The app stops early if it cannot load the required data, if a user has selected only one endpoint of a date interval, or if no rows match the filters. `st.stop()` ends the current script run after a helpful message. Without those checks, later operations such as `idxmin()` could fail on empty data, or the app could present a misleading partial calculation.

Date filters include both endpoints. Because budget dates are stored on the first of the month, a start date of January 15 excludes all January budget lines. There is no prorating of January's budget from the 15th onward. The default end date is December 1 because that is the final recorded month label; it includes all December lines in the file.

### Reports and downloads

The report is deterministic text generated from the Python variables. `report_parts` is a list of Markdown sections; `"\n\n".join(report_parts)` combines them. It is not an AI-generated explanation and does not call an external language model. Changing filters changes the numbers inserted into its strings.

The “Full report” tab displays the string and offers it as `05_finance_budget_report.md`. That file is an analysis of current filter results. This `EXPLANATION.md` is a separate, permanent teaching guide to how the app works. The filtered CSV export includes the selected original fields plus calculated `variance`, and `index=False` prevents pandas' row index from appearing as an extra CSV column.

## Understand the five charts

### 1. Monthly expense plan and actuals

The app groups by `month` and adds `budget` and `actual`. Plotly draws two lines, each with the same INR unit. Where actual is above budget, the selected month is overspent in aggregate. Hover gives exact values, and the legend lets the viewer hide or restore a series.

These are separate **monthly totals**, not cumulative balances. A higher month does not mean every department spent more, and connected points do not establish a forecast. The code contains no `.cumsum()` in this chart; adding a cumulative line is an extension exercise. Interpret the selected departments/categories together with the date window.

### 2. Department variance

The bar chart sums `budget`, `actual`, and `variance` by department. The plotted height is variance in INR. A positive bar means under budget; a negative bar means overspend. `color_continuous_midpoint=0` anchors the diverging color scale to the meaningful zero point.

The table below adds `utilization_pct`, making it possible to compare proportional adherence as well as money. A department with an INR 100,000 difference on a very large budget may have a smaller percentage deviation than one with an INR 20,000 difference on a small budget. Neither view alone establishes efficiency.

### 3. Variance distribution

Matplotlib places each selected budget line into one of 20 numeric intervals and counts how many lines fall there. The horizontal axis is INR variance; the vertical axis is the number of budget lines. The dashed zero line divides overspent from underspent lines.

The shape helps distinguish many small negative differences from a few large ones. Histogram height is a count, not the sum of money in that interval. Changing the number of bins would change the appearance without changing the underlying data. The app leaves unusual observations in place.

### 4. Expense distribution by category

The Seaborn boxplot compares individual `actual` amounts by category. Each box summarizes the middle half of values, with a median line. The default whiskers reach observed values within 1.5 interquartile ranges of the quartiles; separate points lie beyond that rule. They are potential outliers for investigation, not automatically bad data. [Seaborn boxplot reference](https://seaborn.pydata.org/generated/seaborn.boxplot.html)

This plot answers which categories have larger or more variable expense lines. It does **not** show variance: a high expense can be fully budgeted. Departments and months are mixed within each category unless the sidebar has narrowed the selection.

### 5. Department and category variance heatmap

`pivot_table(index="department", columns="expense_category", values="variance", aggfunc="sum")` creates a matrix. Each cell contains total variance across the selected months for one department/category pair. Seaborn turns the matrix into colored cells and annotates them with whole-INR text.

This is a financial summary heatmap, **not a correlation heatmap**. The numbers are amounts, not coefficients from -1 to 1. Zero-centered coloring keeps positive and negative values interpretable, but the scale is not fixed to identical bounds across filter changes. Compare labels and colorbar values rather than assuming the same shade always represents the same INR amount. A positive month can offset a negative one within a cell; inspect the filtered records before calling a pattern recurring.

## Verified results from the bundled CSV

These results were recomputed directly from this revision's CSV using the formulas in `app.py`, with all departments, all categories, and the full available date range. They are reference values for learning and checking your setup. Editing the CSV or filters should change them.

| Check | Result |
| --- | ---: |
| Selected budget lines | 192 |
| Total budget | INR 22,011,000.00 |
| Total actual expense | INR 22,486,668.08 |
| Budget minus actual | INR -475,668.08 |
| Budget utilization | 102.1610% (card: 102.2%) |
| Overspent individual lines | 109 of 192, about 56.8% |
| Observed months with aggregate overspend | 9 of 12 |
| Largest individual overspend | INR 65,141.08 |
| Context of that largest line | Customer Success / Travel / February 2025 |

The largest line has budget INR 165,000 and actual INR 230,141.08. Department totals are:

| Department | Budget (INR) | Actual (INR) | Variance (INR) | Utilization |
| --- | ---: | ---: | ---: | ---: |
| Customer Success | 5,671,000.00 | 5,823,416.49 | -152,416.49 | 102.69% |
| Engineering | 5,151,000.00 | 5,115,766.06 | 35,233.94 | 99.32% |
| Operations | 5,840,000.00 | 6,088,137.19 | -248,137.19 | 104.25% |
| Sales | 5,349,000.00 | 5,459,348.34 | -110,348.34 | 102.06% |

Operations has the lowest **department total** variance; Customer Success has the largest **individual line** overspend. Those are compatible findings because they refer to different levels of aggregation.

As an additional teaching calculation, summing only the overspent portions of lines gives INR 2,279,661.72. Summing the nonnegative variances gives INR 1,803,993.64. Their difference is the net overspend of INR 475,668.08. The existing interface does not show the first two sums as KPI cards; they illustrate how cancellation affects the reported net number. [Calculation inputs: `department_budget.csv`](department_budget.csv); [implemented formulas: `app.py`](app.py).

## Line-by-line guide to app.py

Read this section alongside the source file with line numbers visible in your editor. Every nonblank source line is accounted for. Consecutive lines that form one literal string or one tuple are grouped when they share a purpose; the range includes every continuation line. Blank lines only separate sections visually and do not calculate anything. The `#` lines are comments for readers, while quoted text is Python data that the app may display.

Code anchors are abbreviated when a source line is very long. They identify the exact line to inspect; the explanation covers the complete statement, including report construction.

### Lines 1-13: identify the project and load its tools

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 1 | ``"""Budget versus Actuals: a beginner Streamlit project using a fictional teaching dataset."""`` | A module docstring describes the script. It is documentation stored as a Python string; it does not create a visible page element or load data. |
| 2 | ``from pathlib import Path`` | Import the Path class from Python's standard library. Later, it will construct the CSV path relative to this script. |
| 4 | ``import matplotlib.pyplot as plt`` | Import Matplotlib's plotting interface as plt. The app uses it to create figure/axes objects, draw the histogram, and close finished figures. |
| 5 | ``import pandas as pd`` | Import pandas as pd. All CSV loading, table filtering, derived values, grouping, and exports use this module. |
| 6 | ``import plotly.express as px`` | Import Plotly Express as px. Its high-level functions build the interactive line and bar chart figures from tables. |
| 7 | ``import seaborn as sns`` | Import Seaborn as sns. It draws the statistical boxplot and matrix heatmap on Matplotlib axes. |
| 8 | ``import streamlit as st`` | Import Streamlit as st. This module connects Python values and controls to the browser page. |
| 10 | ``st.set_page_config(page_title="Budget versus Actuals", page_icon=":bar_chart:", layout="wide")`` | Set the browser page title, bar-chart icon, and wide layout before other interface calls. Keyword arguments name the settings; they do not define data columns. |
| 11 | ``st.title("Budget versus Actuals")`` | Render the large visible page title. This is distinct from the browser tab title set above. |
| 12 | ``st.caption("Business Analytics Workshop \| Fictional teaching data \| Currency: INR")`` | Render a small caption establishing the workshop, fictional dataset, and INR unit before a viewer interprets any amounts. |
| 13 | ``st.write("Track expense budgets, find overspending and compare departments. Practice financial aggregation and variance an...`` | Display the project's purpose in ordinary text. This explains why the user is looking at the dashboard. |

### Lines 15-75: store the case, definitions, and visual explanations

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 15 | ``# This case study explains both the business question and how to read the evidence.`` | A comment tells a code reader what the following constants are for. Python ignores comments during execution. |
| 16-17 | ``CASE = ('A fictional finance manager needs to know where expenses exceed the plan. An overall total can hide ' 'department...`` | Create CASE, the business problem string. Adjacent quoted strings inside parentheses concatenate automatically; line 17 continues the same sentence rather than creating another variable. |
| 18-19 | ``DECISION = ('Identify budget lines requiring explanation, distinguish spend concentration from overspend, and ' 'prepare q...`` | Create DECISION, describing which decisions the dashboard supports. Separating this text lets the interface and downloaded report reuse identical scope. |
| 20-22 | ``DATA_CONTEXT = ('One row is one month, department and expense category. There are 192 fictional expense lines for the ' '1...`` | Create DATA_CONTEXT, explaining row grain, 192 teaching records, departments/categories, and the limits of an expense dataset. The three physical lines form one string. |
| 23 | ``FORMULAS = [('Budget', 'Sum of selected budget amounts', 'Planned expense in INR for the selected lines.'),`` | Begin FORMULAS as a list of three-item tuples. The first tuple stores the label, rule, and interpretation for total budget. This is explanatory metadata, not executable arithmetic. |
| 24-26 | ``('Actual spend', 'Sum of selected actual expenses', 'Recorded expense in INR, not necessarily cash paid.'),`` | Add the actual-spend tuple: its name, summed-expense rule, and the reminder that recorded expense is not necessarily cash paid. The tuple's fields will become table columns. |
| 27-29 | ``('Unspent budget / variance', 'Total budget - total actual spend', 'Positive means under budget; negative means overspend.'),`` | Add the variance tuple and the project's sign convention. The actual subtraction is performed later; this text documents how to read its result. |
| 30-32 | ``('Budget utilization', 'Total actual spend / total budget x 100', 'Over 100% means aggregate overspend. This is weighted b...`` | Add utilization's ratio-of-totals rule and weighted interpretation, then close the tuple list. The string says x 100 because the business display is a percentage. |
| 33-39 | ``VISUAL_GUIDE = [('Monthly expense plan and actuals', 'Compare actual expenses with the plan over time.', 'The x-axis is mo...`` | Begin VISUAL_GUIDE and add the monthly plot's five fields: title, purpose, reading instructions, question, and caution. Continuation strings explain that month-start dates select whole recorded lines and totals are not cumulative. |
| 40-46 | ``('Department variance', 'Locate aggregate over- and underspending by department.', 'Bar height is budget minus actual in I...`` | Add the department variance chart's five-part explanation. The sign and zero-centered color are documented, while the caution distinguishes an INR gap from a proportional gap. |
| 47-53 | ``('Variance distribution', 'See the balance of under- and overspent individual budget lines.', 'Each histogram bin counts b...`` | Add the histogram guide: individual line counts across variance bins, zero as the sign boundary, and the warning that overspend does not by itself prove waste. |
| 54-59 | ``('Expense distribution by category', 'Compare typical expense size and variability by type.', 'Boxes show actual INR expen...`` | Add the category boxplot guide. It explains the median, middle half, whiskers, and that the plotted variable is actual expense, not adherence to budget. |
| 60-66 | ``('Department and category variance heatmap', 'Find combinations hidden by aggregate department totals.', 'Each cell sums b...`` | Add the department/category heatmap guide and close VISUAL_GUIDE. Its cells sum variance across selected months, so opposite monthly values can offset. |
| 67-68 | ``RECOMMENDATIONS = ['Ask owners of the largest negative-variance lines to explain timing, volume and one-off events. Do ' '...`` | Start RECOMMENDATIONS with a follow-up investigation of negative-variance lines. Adjacent string pieces form one list item, including the warning against equating overspend with waste. |
| 69-70 | ``'Compare both INR variance and utilization percentage so that department size does not dominate the ' 'discussion.',`` | Add a second recommendation to compare absolute amounts with utilization, so a large department is not judged solely by its scale. |
| 71-72 | ``'Add commitments, accrual policy, business output and approved forecast revisions before changing ' 'budgets.']`` | Add context needed before budget changes: commitments, accrual policy, output, and forecast revisions. Close the list of suggested investigations. |
| 73-75 | ``LIMITATIONS = ('Expense classification and budget baselines are assumed consistent. The data does not include income, ' 'c...`` | Build LIMITATIONS as one string stating missing accounting/business context. It explicitly separates unspent budget from profit and available cash. |

### Lines 77-98: display context and define a reusable explanation function

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 77 | ``with st.expander("Business problem and context", expanded=True):`` | Create an expander that is initially open. The with statement routes the following indented display calls into this container. |
| 78 | ``st.markdown("**The problem:** " + CASE)`` | Concatenate a bold Markdown label with CASE and display it. The plus operator joins strings here; it is not adding expense amounts. |
| 79 | ``st.markdown("**Decision this dashboard supports:** " + DECISION)`` | Display the decision statement with a bold introduction. Reusing DECISION avoids a separate, potentially inconsistent copy. |
| 80 | ``st.markdown("**What one row means:** " + DATA_CONTEXT)`` | Display the row definition and dataset context before metrics, helping the learner interpret what a count or sum represents. |
| 81 | ``st.info("This is a fictional teaching case. Every finding below is calculated from the selected CSV rows, not a claim abou...`` | Show an informational message identifying findings as calculations on fictional selected rows, rather than evidence about a real organization. |
| 82 | ``st.write("Start with the KPI cards, read the explanation under each visual, inspect the source data, then open Full report...`` | Give a reading sequence through the KPIs, charts, data, and report. This text also tells the viewer that filters change the analysis. |
| 85-86 | ``FIELD_GUIDE = {'month': 'Budget month recorded on its first day; date filters select whole recorded budget ' 'lines.',`` | Begin FIELD_GUIDE as a dictionary. The month key maps to a two-line string explaining first-day labels and whole-line date selection. |
| 87 | ``'department': 'Department responsible for expense.',`` | Map department to the responsible organizational unit. A dictionary associates a unique key with a value. |
| 88 | ``'expense_category': 'Expense classification.',`` | Map expense_category to its classification meaning. The exact underscore-separated key matches the CSV header. |
| 89 | ``'budget': 'Planned expense in INR for this month, department and category.',`` | Map budget to its planned INR amount and full month/department/category grain. |
| 90 | ``'actual': 'Recorded expense in INR for this budget line.'}`` | Map actual to recorded INR expense and close the dictionary. The app later converts these key/value pairs into tables. |
| 92 | ``def explain_visual(index, container=st):`` | Define explain_visual(index, container=st). It is reusable code that runs when called later; the default target is the main Streamlit context, but a column can be supplied. |
| 93 | ``title, purpose, reading, question, caution = VISUAL_GUIDE[index]`` | Select one VISUAL_GUIDE tuple by its zero-based index, then unpack its five items into descriptive variable names. |
| 94 | ``container.markdown(f"**{title}: what this visual explains**")`` | Use an f-string to insert the selected title into a bold Markdown heading in the chosen container. |
| 95 | ``container.write(purpose)`` | Write the selected purpose. Because container is a parameter, the same function works in the page or a side-by-side column. |
| 96 | ``container.markdown("**How to read it:** " + reading)`` | Display the chart-reading instructions with a bold label, making axes and units explicit. |
| 97 | ``container.markdown("**Question it answers:** " + question)`` | Display the business question the chart addresses. This links visual output to analytical intent. |
| 98 | ``container.caption("Interpretation limit: " + caution)`` | Render the interpretation caution as a caption. The function has no explicit return value; its purpose is to produce interface output. |

### Lines 100-122: read and validate the CSV

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 100 | ``# 1. Load the CSV beside this script, regardless of the terminal's directory.`` | Document the intended path behavior: use the CSV beside the script, independent of the terminal's working directory. |
| 101 | ``# Keeping this uncached lets students edit the CSV and immediately rerun the app.`` | Explain that loading is deliberately uncached. A later rerun rereads an edited file; this comment does not create a file watcher. |
| 102 | ``DATA_FILE = Path(__file__).resolve().with_name("department_budget.csv")`` | __file__ identifies this Python file; resolve() makes an absolute resolved path; with_name(...) swaps only the filename. The resulting Path points to the sibling CSV. |
| 103 | ``try:`` | Start a try block around loading and basic validation. Matching errors raised in this block will be handled by the except below. |
| 104 | ``frame = pd.read_csv(DATA_FILE)`` | Parse comma-separated records into a DataFrame called frame. pandas infers initial column types from the values; it does not know the business meaning yet. |
| 105 | ``frame["month"] = pd.to_datetime(frame["month"], errors="raise")`` | Convert month from text to pandas datetimes and assign the result back to the same column. errors="raise" rejects invalid date parsing rather than quietly coercing invalid strings. |
| 106 | ``numeric_columns = ['budget', 'actual']`` | List the columns that must be numeric. This list drives the conversion loop; it is not a new table. |
| 107 | ``required_columns = ['month', 'department', 'expense_category', 'budget', 'actual']`` | List the required schema. Extra CSV columns are permitted because the following check requires a subset, not exact equality. |
| 108 | ``if not set(required_columns).issubset(frame.columns):`` | Convert required names to a set and ask whether every name is present in frame.columns. not reverses the answer so the error branch runs when something is missing. |
| 109 | ``raise ValueError("The CSV is missing required columns.")`` | Raise a ValueError with a readable explanation. If month itself was absent, line 105 would already have raised a KeyError, which the same handler also catches. |
| 110 | ``if frame.empty:`` | Check whether the loaded table has no entries. A CSV with only the required headers can pass the column test but have no rows to analyze. |
| 111 | ``raise ValueError("The CSV contains no rows.")`` | Raise an error for empty input before the code tries to calculate date limits or extrema. |
| 112 | ``for column in numeric_columns:`` | Loop over budget and actual. Each iteration binds column to one field name. |
| 113 | ``frame[column] = pd.to_numeric(frame[column], errors="raise")`` | Convert that column with pd.to_numeric and replace its original contents. errors="raise" catches unparseable numeric text but does not enforce nonnegative or finite values. |
| 114 | ``if frame[required_columns].isna().any().any():`` | Select the required columns, mark missing cells with isna(), reduce within columns with the first any(), and reduce across columns with the second any(). One missing required cell triggers the branch. |
| 115 | ``raise ValueError("Fill missing values in the required analysis columns first.")`` | Raise a missing-value error. The policy is to ask the learner to fix required data rather than automatically discard or impute records. |
| 116 | ``except (OSError, ValueError, KeyError) as error:`` | Catch filesystem errors, value errors, and missing-key errors from the try block, binding the exception to error. This does not wrap the rest of the app. |
| 117 | ``st.error(f"Could not load {DATA_FILE.name}: {error}")`` | Display the CSV filename and exception message. DATA_FILE.name shows only the filename instead of its whole local path. |
| 118 | ``st.stop()`` | Stop this script run after the error message, preventing downstream code from using failed or incomplete input. |
| 120 | ``def ratio(numerator, denominator):`` | Define a small scalar division helper. Parameters are placeholders for the totals passed by later KPI/report calls. |
| 121 | ``"""Return zero for an empty denominator so filters never divide by zero."""`` | Document the helper's zero-denominator behavior with a function docstring. The actual decision is in the next line. |
| 122 | ``return numerator / denominator if denominator else 0.0`` | Return numerator divided by denominator if the denominator is truthy; numeric zero takes the 0.0 branch. This avoids a crash but is not a valid definition of utilization when the budget is zero. |

### Lines 124-139: obtain sidebar choices and select rows

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 124 | ``# 2. Apply sidebar filters before calculating any KPI or chart.`` | State the order of operations: select rows before calculating business outputs. This keeps all later results on the same scope. |
| 125 | ``st.sidebar.header("Filter the data")`` | Create a heading inside the sidebar rather than in the main page area. |
| 126 | ``filtered = frame.copy()`` | Copy the source table into a working DataFrame. frame remains available for source-wide quality counts, while filtered will acquire subsets and a derived column. |
| 127 | ``selected_department = st.sidebar.multiselect("Departments", sorted(frame["department"].unique()), default=sorted(frame["de...`` | Build the department multiselect from distinct source values, sorted for stable display, with all selected by default. Its key identifies the widget; its return value is the chosen Python list. |
| 128 | ``filtered = filtered[filtered["department"].isin(selected_department)]`` | Use isin to make a Boolean membership mask and retain matching department rows. An empty chosen list matches nothing. |
| 129 | ``selected_expense_category = st.sidebar.multiselect("Expense categories", sorted(frame["expense_category"].unique()), defau...`` | Build the category multiselect using all source categories and its own stable key. The choices are not dynamically limited to the already selected department. |
| 130 | ``filtered = filtered[filtered["expense_category"].isin(selected_expense_category)]`` | Apply the category membership mask to the rows that survived the department filter. Sequential filtering means both conditions must hold. |
| 131 | ``dates = st.sidebar.date_input("Date range", (frame["month"].min().date(), frame["month"].max().date()), min_value=frame["m...`` | Create a two-endpoint date widget using the source minimum and maximum as defaults and permitted bounds. date() changes pandas timestamps to Python date values for the control. |
| 132 | ``if len(dates) != 2:`` | A range can temporarily contain fewer than two endpoints while the viewer is choosing it. Check that length before accessing dates[0] and dates[1]. |
| 133 | ``st.info("Choose both a start and an end date.")`` | Explain that both endpoints are needed instead of presenting partial metrics. |
| 134 | ``st.stop()`` | Stop the current run until the date selection is complete. |
| 135 | ``filtered = filtered[filtered["month"].dt.date.between(dates[0], dates[1])]`` | Extract the date component, test inclusive membership between both endpoints, and keep matching rows. The method selects recorded month-start labels; it does not prorate amounts. |
| 136 | ``st.sidebar.caption(f"Showing {len(filtered):,} of {len(frame):,} rows")`` | Show selected-row and source-row counts. The :, formatting specifier adds thousands separators without changing the count. |
| 137 | ``if filtered.empty:`` | Check whether the combined department, category, and date conditions left no rows. |
| 138 | ``st.info("No rows match these filters. Select at least one value or widen the date range.")`` | Tell the user how to restore a nonempty selection. This is a filter outcome, not a loading failure. |
| 139 | ``st.stop()`` | Stop before totals, idxmin calls, and charts attempt to analyze an empty table. |

### Lines 141-165: calculate business measures and answers

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 141 | ``# 3. Derive business measures, then compare totals, distributions and segments.`` | Mark the transition from data selection to analysis. |
| 142 | ``filtered["variance"] = filtered["budget"]-filtered["actual"]`` | Subtract actual from budget element by element and save a variance value for each selected line. Positive means under budget and negative means overspend. |
| 143 | ``budget = filtered["budget"].sum()`` | Sum selected planned expenses into a scalar total named budget. This scalar is distinct from the budget column inside filtered. |
| 144 | ``actual = filtered["actual"].sum()`` | Sum selected actual expenses into a scalar total named actual. |
| 145 | ``columns = st.columns(4)`` | Create four equal-width display containers and store them in a list-like sequence. Index 0 addresses the first column. |
| 146 | ``columns[0].metric("Budget (INR)", f"{budget:,.0f}")`` | Display total budget in the first metric card. :,.0f adds grouping separators and rounds the displayed text to zero decimal places. |
| 147 | ``columns[1].metric("Actual spend (INR)", f"{actual:,.0f}")`` | Display total actual expense in the second card using the same INR formatting. |
| 148 | ``columns[2].metric("Unspent budget (INR)", f"{budget-actual:,.0f}")`` | Display net variance, calculated from the two totals, under the label Unspent budget. A negative value indicates overspend; this is not a cash balance. |
| 149 | ``columns[3].metric("Budget utilization", f"{ratio(actual,budget):.1%}")`` | Divide actual by budget through the helper and display one decimal percentage. The percentage formatter performs the factor-of-100 conversion for presentation. |
| 150 | ``st.caption("One row is a department/expense category for one month. Variance = budget - actual: a negative number means ov...`` | Explain row grain, variance direction, and the limits of unspent budget directly beneath the cards. |
| 151 | ``dept_summary = filtered.groupby("department")[["budget","actual","variance"]].sum()`` | Group by department, select three numeric columns, and sum each within each group. The result uses department names as its index. |
| 152 | ``worst_dept = dept_summary["variance"].idxmin()`` | Find the index label of the smallest department variance. The name worst_dept is a convenience; a minimum is not necessarily negative and does not establish poor management. |
| 153 | ``monthly_summary = filtered.groupby("month")[["budget","actual","variance"]].sum()`` | Group the same selected lines by month and sum budget, actual, and variance. This supports the count of over-plan months. |
| 154 | ``overspent_lines = int((filtered["variance"]<0).sum())`` | Compare each line's variance to zero, sum the True results, and convert to int. This counts lines before departmental or monthly aggregation. |
| 155 | ``largest_line = filtered.loc[filtered["variance"].idxmin()]`` | Find the source index label of the smallest row-level variance and use loc to retrieve the entire record. Its department/category/month explain the most negative individual line. |
| 156 | ``net_label = "overspend" if actual>budget else "unspent budget"`` | Choose wording for the net difference: overspend if actual is greater, otherwise unspent budget. Exact equality uses the latter label with a zero amount. |
| 157 | ``insights = [`` | Begin a list of question/answer pairs. This list drives the short page summary and the longer report. |
| 158 | ``("Is the selected activity within budget?", f"Budget is INR {budget:,.2f} and actual expense is INR {actual:,.2f}. The dif...`` | Create the portfolio answer with totals, the absolute size of the difference, its label, and utilization. abs removes the numeric sign only because net_label supplies the direction in words. |
| 159 | ``("How widespread is overspending?", f"{overspent_lines} of {len(filtered)} selected budget lines are overspent ({ratio(ove...`` | Report the overspent-line count and its proportion of selected lines. The answer explicitly separates line frequency from the share of expense. |
| 160 | ``("Which department has the lowest variance?", f"{worst_dept} has variance INR {dept_summary.loc[worst_dept,'variance']:,.2...`` | Retrieve the lowest-variance department's amounts with loc and compute its utilization. The text correctly allows a positive minimum if all departments are under budget. |
| 161 | ``("What is the largest individual overspend?", f"{largest_line['department']} / {largest_line['expense_category']} in {larg...`` | If the minimum row variance is negative, describe its department/category/month and positive overspend amount. Otherwise report that no selected line is overspent. The conditional prevents calling an underspend an overspend. |
| 162 | ``("How many selected months are over plan?", f"{int((monthly_summary['variance']<0).sum())} of {len(monthly_summary)} obser...`` | Count negative variances in the monthly grouped table and report them out of observed selected months. This is a different aggregation level from the line count. |
| 163 | ``("What has the dashboard answered?", "It quantifies the expense gap and locates the departments, categories and months beh...`` | Add a qualitative explanation of what the dashboard establishes and what it cannot establish about justified expense or cash. |
| 164 | ``]`` | Close the insights list. The preceding commas separate tuples, not independent function calls. |
| 165 | ``kpi_values=[("Budget (INR)",f"{budget:,.2f}"),("Actual expense (INR)",f"{actual:,.2f}"),("Budget minus actual (INR)",f"{bu...`` | Create report-ready label/value pairs for the four KPIs. Two-decimal formatting provides more precision than some cards, while using the same unrounded source totals. |

### Lines 167-184: describe scope and display definitions

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 167 | ``# Build one report from the same filtered dataframe used by the charts.`` | Document the rule that the report shares the charts' filtered DataFrame. No separate report dataset is loaded. |
| 168 | ``scope_parts = []`` | Create an empty list that will collect human-readable statements about the selection. |
| 169 | ``for column in frame.select_dtypes(include="object").columns:`` | Loop over source columns whose dtype is object, which includes the bundled text categories. This is a dtype check, not a list of explicit widget names. |
| 170 | ``if frame[column].nunique() <= 12:`` | Only include fields with at most 12 distinct source values. This heuristic avoids listing long identifier collections, but could omit a categorical field with many distinct values. |
| 171 | ``scope_parts.append(column.replace("_", " ") + ": " + ", ".join(map(str, sorted(filtered[column].unique()))))`` | Turn underscores into spaces in the label, sort distinct selected values, convert them to strings with map, join them with commas, and append the resulting description. |
| 172 | ``for column in frame.select_dtypes(include="datetime").columns:`` | Loop over datetime columns in the loaded source. This file has month after the explicit conversion. |
| 173 | ``scope_parts.append(f"{column}: observed records {filtered[column].min():%Y-%m-%d} to {filtered[column].max():%Y-%m-%d}")`` | Append the first and last observed selected dates using YYYY-MM-DD formatting. These observed limits can differ from the exact requested endpoints. |
| 174 | ``scope_parts.append(f"Requested date window: {dates[0]} to {dates[1]} (inclusive)")`` | Also record the requested inclusive date window. This preserves the viewer's requested scope even when no records lie exactly on an endpoint. |
| 175 | ``scope = "; ".join(scope_parts)`` | Join all scope statements into one semicolon-separated string. join is a string operation and does not merge DataFrames. |
| 177 | ``with st.expander("KPI definitions and calculation rules"):`` | Create an expander for KPI documentation. Its collapsed visual state does not skip the indented Python code. |
| 178 | ``st.dataframe(pd.DataFrame(FORMULAS, columns=["Measure", "Calculation", "Business meaning"]), hide_index=True, width="stret...`` | Convert the list of formula tuples into a three-column DataFrame and render it without the row index. width="stretch" uses the available container width. |
| 179 | ``st.caption("All cards, charts and findings use the same selected rows. Ratios use summed numerators and denominators where...`` | Display the common-filter and zero-denominator interpretation rules, making the helper's fallback visible to readers. |
| 181 | ``st.subheader("What the selected data answers")`` | Create the heading for the short set of calculated answers. |
| 182 | ``for question, answer in insights[:3]:`` | Slice insights to its first three pairs and unpack each pair into question and answer while iterating. |
| 183 | ``st.markdown(f"**{question}** {answer}")`` | Display each question in bold followed by its generated answer. These are rule-based strings, not outputs from an AI service. |
| 184 | ``st.caption(f"Analysis scope: {len(filtered):,} of {len(frame):,} source rows. " + scope)`` | Display row counts and the assembled scope string beneath the answers. |

### Lines 186-202: assemble the complete Markdown report

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 186 | ``report_parts = [`` | Begin report_parts, a Python list whose items are complete Markdown sections. Building text first lets the same result be displayed and downloaded. |
| 187 | ``"# " + '05 Finance Budget' + " - full analytical report",`` | Add the report's level-one heading. It names the project independently of the browser page title. |
| 188 | ``"## 1. Business problem\n" + CASE,`` | Add section 1 and the CASE string. The escaped newline places the case text below its heading. |
| 189 | ``"## 2. Context and decision\n" + DECISION + "\n\n" + DATA_CONTEXT,`` | Add section 2 by joining DECISION and DATA_CONTEXT with a blank line. This preserves both business purpose and row meaning in an exported report. |
| 190 | ``"## 3. Data and analysis scope\n" + f"Dataset: `{DATA_FILE.name}`. Selected rows: {len(filtered):,} of {len(frame):,}.\n\n...`` | Add section 3 with filename, selected/source row counts, scope, fictional-data status, INR units, and descriptive limits. The f-string evaluates current variables at this run. |
| 191 | ``"## 4. Executive summary\n" + "\n\n".join(answer for _,answer in insights[:3]),`` | Build the executive summary from the first three insight answers. The underscore ignores each question while the generator expression supplies its answer to join. |
| 192 | ``"## 5. KPI results\n\| Measure \| Selected result \|\n\| --- \| --- \|\n" + "\n".join(f"\| {name} \| {value} \|" for name,value in ...`` | Construct a Markdown table from kpi_values: a header, alignment separator, and one formatted row per pair. The table characters are text for Markdown, not Python arithmetic. |
| 193 | ``"## 6. Definitions and methods\n\| Measure \| Calculation \| Interpretation \|\n\| --- \| --- \| --- \|\n" + "\n".join(f"\| {name} ...`` | Construct the methods table from FORMULAS by unpacking each three-item tuple into name, formula, and meaning. |
| 194 | ``"## 7. Questions answered by the data\n" + "\n\n".join(f"### {question}\n{answer}" for question,answer in insights),`` | Include every insight, each with a level-three question heading and its answer. This is where answers omitted from the short page summary become visible. |
| 195 | ``"## 8. Every visual explained\n" + "\n\n".join(f"### {title}\n**Purpose:** {purpose}\n\n**How to read:** {reading}\n\n**Qu...`` | Convert all five VISUAL_GUIDE tuples into narrative chart explanations with purpose, reading instructions, question, and caution. The downloaded Markdown explains charts but does not embed rendered chart images. |
| 196 | ``"## 9. Data quality and aggregation\n" + f"Source rows: {len(frame):,}; exact duplicate rows: {frame.duplicated().sum():,}...`` | Add full-source row, exact-duplicate, and missing-cell counts, plus validation and outlier-handling explanations. These use frame rather than filtered, so they describe the source file. |
| 197 | ``"## 10. Suggested next steps\n" + "\n".join(f"{i}. {text}" for i,text in enumerate(RECOMMENDATIONS,1)) + "\n\nTreat these ...`` | Number recommendations beginning at one using enumerate, then append a reminder that they are investigation steps. The generator creates one string per recommendation. |
| 198 | ``"## 11. What this analysis cannot answer\n" + LIMITATIONS + "\n\nTies in automatically named leaders are resolved by the d...`` | Add limitations and shared methodological cautions. The tie wording is exact for grouped labels; row-level largest_line ties instead follow the first matching source index. No correlation chart is calculated in this finance app. |
| 199 | ``"## 12. Reproduce and extend the analysis\nOpen the CSV beside app.py, restore the filter selections listed above, and com...`` | Add reproduction and extension instructions, including data export and chart interactions. These instructions do not embed the source CSV or guarantee reproduction after that source changes. |
| 200 | ``]`` | Close the report section list. |
| 201 | ``report_parts[5] += "\n\n### Source field dictionary\n\| Field \| Meaning and units \|\n\| --- \| --- \|\n" + "\n".join(f"\| `{nam...`` | Append a source dictionary to report_parts[5], the KPI-results section because the report title occupies index 0. Iterating FIELD_GUIDE.items() supplies name/meaning pairs for Markdown rows; += extends that string. |
| 202 | ``full_report = "\n\n".join(report_parts)`` | Join all report sections with two newlines into full_report. This string is reused unchanged for display and download in the current run. |

### Lines 204-232: create tabs and draw all five visuals

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 204 | ``overview, explore, data_tab, report_tab = st.tabs(["Finance dashboard", "Explore the data", "Data and quality", "Full repo...`` | Create four tab containers and unpack them into named variables. Their names are Python references; the labels in the list are the text the viewer sees. |
| 205 | ``with overview:`` | Route subsequent indented display calls into Finance dashboard. The calculations inside still execute on a normal rerun even if another tab is selected. |
| 206 | ``monthly = filtered.groupby("month", as_index=False)[["budget","actual"]].sum()`` | Sum budget and actual by month with as_index=False so month remains a regular column that Plotly can address by name. |
| 207 | ``st.plotly_chart(px.line(monthly, x="month", y=["budget","actual"], markers=True, title="Monthly expense plan and actuals",...`` | Build a Plotly line figure with month on x and two numeric series on y, add markers/title/INR labeling, then render it in Streamlit. No cumulative sum is applied. |
| 208 | ``explain_visual(0, st)`` | Render VISUAL_GUIDE item 0, the monthly chart explanation, in the current Streamlit context. |
| 209 | ``departments = filtered.groupby("department", as_index=False)[["budget","actual","variance"]].sum()`` | Create a department totals table with department kept as an ordinary column for charting and display. |
| 210 | ``departments["utilization_pct"] = 100*departments["actual"].div(departments["budget"].replace(0,float("nan")))`` | Replace zero budgets with NaN, divide actual by budget elementwise, and multiply by 100 to store numeric percentage points. Unlike ratio(), a zero budget produces a missing table rate. |
| 211 | ``st.plotly_chart(px.bar(departments, x="department", y="variance", color="variance", color_continuous_scale="RdYlGn", color...`` | Build and display the department variance bar chart. Continuous color uses the variance itself and a zero midpoint; axis labels identify INR and the budget-minus-actual sign. |
| 212 | ``explain_visual(1, st)`` | Display VISUAL_GUIDE item 1, explaining the department comparison and the need to consider size. |
| 213 | ``st.dataframe(departments.round(2), hide_index=True, width="stretch")`` | Display rounded department totals/utilization as an exact-value companion to the chart. round(2) affects the returned display table, not the earlier analysis totals. |
| 214 | ``st.caption("The table above gives exact grouped values behind the dashboard. Group sizes matter: compare counts alongside ...`` | Explain that group context matters. This generic caption mentions counts, although this particular department table contains summed amounts and utilization rather than an explicit line-count column. |
| 215 | ``with explore:`` | Route subsequent content into Explore the data. |
| 216 | ``left, right = st.columns(2)`` | Create left and right columns to show the histogram and boxplot side by side. |
| 217 | ``fig, ax = plt.subplots(figsize=(7,4))`` | Create a Matplotlib Figure and Axes with a seven-by-four-inch figure size. fig is the whole canvas; ax is the plotting area. |
| 218 | ``ax.hist(filtered["variance"], bins=20, color="#ea580c", edgecolor="white")`` | Draw a histogram of individual line variances with 20 bins, an orange fill, and white edges. Matplotlib calculates the counts in each interval. |
| 219 | ``ax.axvline(0, color="black", linestyle="--")`` | Draw a dashed vertical reference line at zero so negative and positive variances can be distinguished visually. |
| 220 | ``ax.set(title="Variance distribution", xlabel="Budget minus actual (INR)", ylabel="Budget lines")`` | Set the chart title and both axis labels, explicitly identifying INR on x and budget-line counts on y. |
| 221 | ``left.pyplot(fig); plt.close(fig)`` | Render the figure in the left column, then close it in Matplotlib to release its managed figure resources. The semicolon separates two statements on one physical line. |
| 222 | ``explain_visual(2, left)`` | Display the histogram explanation in the left column through the same reusable helper. |
| 223 | ``fig, ax = plt.subplots(figsize=(7,4))`` | Create a fresh Figure and Axes for the boxplot rather than drawing over the histogram. |
| 224 | ``sns.boxplot(data=filtered, x="expense_category", y="actual", ax=ax, color="#fed7aa")`` | Ask Seaborn to group rows by expense_category and summarize their actual expenses as boxes on the supplied axes. The selected variable is actual, not variance. |
| 225 | ``ax.set_title("Expense distribution by category")`` | Set the boxplot title. Seaborn already derives axis labels from the named data columns. |
| 226 | ``right.pyplot(fig); plt.close(fig)`` | Render the boxplot in the right column, then close its Matplotlib figure. |
| 227 | ``explain_visual(3, right)`` | Display the category-distribution explanation beside its chart. |
| 228 | ``fig, ax = plt.subplots(figsize=(9,4))`` | Create a wider fresh figure for the matrix heatmap below the paired charts. |
| 229 | ``sns.heatmap(filtered.pivot_table(index="department", columns="expense_category", values="variance", aggfunc="sum"), annot=...`` | Pivot summed variance into department rows and category columns, then color the matrix around zero. annot=True writes values; fmt=".0f" displays whole INR. This is not a correlation calculation. |
| 230 | ``ax.set_title("Variance by department and expense category (INR)")`` | Set a title that identifies both grouping dimensions and the INR unit. |
| 231 | ``st.pyplot(fig); plt.close(fig)`` | Render the heatmap in the tab's full available area and close the underlying figure. |
| 232 | ``explain_visual(4, st)`` | Display VISUAL_GUIDE item 4, explaining how to interpret the cells and monthly offsets. |

### Lines 234-256: expose evidence, practice prompts, and report exports

| Source line(s) | Code anchor | What it does and why |
| --- | --- | --- |
| 234 | ``# 4. Inspect the underlying data and practice explaining the results.`` | Mark the data-inspection and learning section with a code comment. |
| 235 | ``with data_tab:`` | Route the following elements into Data and quality. |
| 236 | ``st.subheader("Source field dictionary")`` | Create the source-dictionary subheading. |
| 237 | ``st.dataframe(pd.DataFrame(FIELD_GUIDE.items(), columns=["Field", "Meaning and units"]), hide_index=True, width="stretch")`` | Turn the dictionary's item pairs into a two-column DataFrame and display it without a row index. This is a readable schema explanation, not a data transformation. |
| 238 | ``st.subheader("Filtered records")`` | Create the heading for selected observations. |
| 239 | ``st.write("These are the exact selected observations used for the KPIs and charts, including any derived columns. Sorting t...`` | Explain that displayed records include derived measures and that sorting the browser table does not change analytical filters. |
| 240 | ``st.dataframe(filtered, hide_index=True, width="stretch")`` | Display the filtered DataFrame, including its calculated variance column, while hiding its index visually. |
| 241 | ``st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_department_budget.csv", "text/csv")`` | Serialize filtered rows as CSV without the index and provide a download button with filename and text/csv MIME type. The operation does not overwrite the source file. |
| 242 | ``st.subheader("Numeric summary")`` | Add the numeric-summary heading. |
| 243 | ``st.write("Count is the number of available values; mean is the arithmetic average; std measures spread; min/max are extrem...`` | Explain count, mean, standard deviation, extrema, and quartiles in plain language before the summary table. |
| 244 | ``st.dataframe(filtered.select_dtypes(include="number").describe().round(2), width="stretch")`` | Select numeric columns, calculate describe() statistics, round for display, and show the result. Derived variance is included because it is numeric; text/date columns are excluded. |
| 245 | ``st.subheader("Source data quality")`` | Create a heading for source-wide data quality. |
| 246 | ``st.write(f"Rows: {len(frame):,} \| Exact duplicates: {frame.duplicated().sum():,} \| Missing cells: {frame.isna().sum().sum(...`` | Report the number of source rows, exact duplicate rows, and missing cells. duplicated() marks repeated complete rows; summing missing indicators twice counts cells, not rows. |
| 247 | ``st.dataframe(pd.DataFrame({"column": frame.columns, "type": frame.dtypes.astype(str).values, "missing": frame.isna().sum()...`` | Build a new DataFrame pairing each source column with its dtype string and missing count. .values supplies positional arrays aligned with frame.columns; derived variance is absent from frame. |
| 249 | ``with st.expander("Workshop exercises and chart guide"):`` | Create a workshop-exercise expander in the main page context, outside the preceding data-tab with block. |
| 250 | ``st.markdown('1. Identify the largest overspend and inspect its source records.\n2. Compare the first and second halves of ...`` | Display four practice prompts separated by escaped newlines. A cumulative line is suggested here but is not implemented by this text. |
| 251 | ``st.write("Matplotlib teaches figure and axes control. Seaborn compares distributions and relationships. Plotly charts supp...`` | Describe the distinct roles of Matplotlib, Seaborn, and Plotly as learning tools. |
| 252 | ``st.caption("Explore associations, then propose a business question. These fictional observations do not establish cause an...`` | Remind learners to distinguish exploratory associations from cause-and-effect claims. |
| 254 | ``with report_tab:`` | Route the last elements into Full report. |
| 255 | ``st.download_button("Download full report (Markdown)", full_report, "05_finance_budget_report.md", "text/markdown")`` | Offer full_report as a Markdown download with a fixed filename and text/markdown MIME type. It contains the current run's selected results. |
| 256 | ``st.markdown(full_report)`` | Render that same Markdown string in the report tab. Matching display and export come from reusing one variable, not recomputing a second report. |


## Run the project and investigate results

From the repository root, use Python 3.12 and the workshop versions listed in the [workshop README](../README.md):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit==1.50.0 pandas==2.2.3 numpy==2.3.5 matplotlib==3.10.8 seaborn==0.13.2 plotly==6.5.2
cd business_analytics_workshop/05_finance_budget
python -m streamlit run app.py
```

On Windows PowerShell, virtual-environment activation is `.venv\Scripts\Activate.ps1`. However, this repository's other phase folders contain `>` in their names, so the [root README](../../README.md) recommends using WSL or the Linux Cloud Lab for a full checkout. The numbered workshop folder itself does not need any renamed files.

In a CookieSensei workshop workspace, the environment is already supplied. For a separate instance, the documented folder layout is:

```bash
cd /home/coder/project/business_analytics_workshop/05_finance_budget
python -m streamlit run app.py --server.port 8502
```

Open the forwarded port in Coder. The built-in workshop dashboard uses port 8501, so 8502 avoids a conflict. If you cloned the repository into a different directory, use that actual path. Running `python app.py` is not equivalent to launching the interactive Streamlit server.

For a first investigation, keep all filters, compare the four cards with the reference totals above, then select Operations. Read its variance bar and department/category heatmap. Finally, narrow to one category and inspect the underlying rows. State the selected period and counts when explaining what changed.

Common problems have concrete causes:

| Symptom | Explanation and useful next step |
| --- | --- |
| `ModuleNotFoundError` | The active interpreter lacks a dependency. Activate the environment and install with that interpreter's `python -m pip`. |
| “Could not load department_budget.csv” | Confirm the CSV is beside `app.py`, has the expected filename/header, and contains parseable dates and numbers. Changing terminal directories alone will not fix a missing sibling file. |
| “Choose both a start and an end date” | Complete the range selection; the program intentionally stops before analysis. |
| “No rows match these filters” | Restore at least one category/department or widen the dates. Clearing every multiselect option selects no rows. |
| January disappears after choosing January 15 | January records are labeled January 1. The filter selects whole stored lines, not a fraction of the month's expense. |
| A percentage shows zero despite a zero budget | The scalar helper uses zero as a safe display fallback. Read the underlying amounts; the utilization formula is undefined. |
| A CSV edit does not appear in an already open browser | Save the file and rerun. There is no cache, but the analysis must execute again to reread the file. |
| The chart and report show different decimal precision | Cards often round to whole INR or one decimal percentage; the report uses two decimals. Formatting does not change the original calculations. |

## Worked practice and self-checks

These snippets are **extensions or separate checks**, not code already present in `app.py`. Insert them after line 142, where `variance` has been created, so they follow the filter/empty-data checks and can use that derived column. Keep source data unchanged while practicing unless your exercise explicitly calls for an edited copy.

### Exercise 1: verify a single line by hand

Choose Sales, People, and January 1 to January 1. The selected line should have budget INR 112,000 and actual INR 131,473.15. Its variance is INR -19,473.15 and utilization is approximately 117.39%. Explain the negative sign before looking at the chart color. You have checked the most basic link between a CSV record, the formula, and a displayed result.

### Exercise 2: compare the halves of the year fairly

Use January 1-June 1 for the first six recorded months and July 1-December 1 for the second six. Both windows contain six full monthly labels.

| Period | Budget (INR) | Actual (INR) | Variance (INR) |
| --- | ---: | ---: | ---: |
| January-June | 11,052,000.00 | 11,344,624.59 | -292,624.59 |
| July-December | 10,959,000.00 | 11,142,043.49 | -183,043.49 |

The second half has a smaller net overspend in this fictional file. That does not prove a management improvement: the planned mix and actual business activity could differ. An explanation should report the numbers and then identify the context needed to interpret them. [Source values: `department_budget.csv`](department_budget.csv)

### Exercise 3: add a cumulative view

```python
cumulative = (
    filtered.groupby("month", as_index=False)[["budget", "actual"]]
    .sum()
    .sort_values("month")
)
cumulative[["budget", "actual"]] = cumulative[["budget", "actual"]].cumsum()
st.plotly_chart(
    px.line(
        cumulative,
        x="month",
        y=["budget", "actual"],
        title="Cumulative budget and actual expense within the selection",
        labels={"value": "INR"},
    ),
    use_container_width=True,
)
```

Grouping produces one row per month. Sorting explicitly defines chronological order. `.cumsum()` replaces each monthly amount with the total from the beginning of the **selected period** through that month. If the filter begins in July, this is July-to-date within the selection, not January-to-date. It answers how the selected gap accumulates; it should supplement, not silently relabel, the existing monthly chart.

### Exercise 4: separate gross overspend from offsets

```python
overspent = filtered[filtered["variance"] < 0]
gross_overspend = -overspent["variance"].sum()
underspend = filtered.loc[filtered["variance"] > 0, "variance"].sum()
st.write({
    "Overspend on overspent lines": gross_overspend,
    "Unspent amount on underspent lines": underspend,
    "Net overspend after offsets": gross_overspend - underspend,
})
```

The negative sign turns a sum of negative variances into a positive amount above plan. Filtering before adding is essential; subtracting the portfolio totals first would already have netted the offsets. The last measure can be negative if the selected portfolio is under budget overall, so its label and sign need careful explanation.

### Exercise 5: explain why a mean of utilization percentages is wrong

Use the illustrative 100/150 and 900/900 example from the formulas section. Show both `(150 / 100 + 900 / 900) / 2 = 1.25` and `(150 + 900) / (100 + 900) = 1.05`. The first describes an equally weighted average across two line-level percentages; the second describes use of the total money budgeted. Select the second for the portfolio KPI because the business question is about the total plan.

### Exercise 6: find concentration without calling it overspend

```python
expense_mix = filtered.groupby("expense_category")["actual"].sum()
expense_share = expense_mix / expense_mix.sum()
st.dataframe(expense_share.rename("share_of_actual_expense"))
```

This describes each category's proportion of actual expense. A category can dominate expense and still be under budget. If all selected actual amounts sum to zero, the proportion is undefined and requires an explicit handling choice. The snippet demonstrates a new question; it does not replace variance analysis.

## Limits and possible improvements

The load block checks readable data, required columns, nonempty input, parseable numeric/date fields, and missing required values. It does not validate business ranges, finite numeric values, consistent month-start dates, uniqueness of month/department/category keys, or valid accounting classifications. Duplicate rows are counted later, not removed. The application cannot tell whether an amount is correct simply because it can parse it as a number.

Only loading errors are caught by the `try`/`except` block. Later calculation or plotting errors are not caught there. For example, unusual custom data can violate assumptions that the teaching CSV satisfies. A robust production import would define explicit validation and error messages for those cases, rather than quietly changing the dataset.

`idxmin()` selects the first label attaining the minimum. For grouped departments, pandas' default sorted group order affects tie resolution. For `largest_line`, tied individual minima resolve to the first matching row in the filtered source order. The generic generated report mentions sorted group order, but that wording is not an exact description of the row-level tie behavior. Inspect tied records before describing one item as uniquely worst.

The scope description includes object columns with at most 12 distinct source values and date ranges. It is a convenient description, not a stored filter configuration or a complete audit trail. Changing the CSV while keeping the same displayed filters can change the results. The downloaded Markdown also cannot reconstruct missing source data on its own.

Useful future improvements would be a uniqueness check, explicit handling of zero-budget utilization, a line-level overspend table with ties, an approved-budget revision field, commitments and accounting timing context, and an optional cumulative chart. These are suggestions; the current app does not already implement them. Its present purpose is to teach reliable descriptive comparisons before attempting broader financial conclusions.

## References

- [Project source: app.py](app.py), [dataset: department_budget.csv](department_budget.csv), and [workshop setup](../README.md) are the primary sources for project behavior and the numerical examples in this guide.
- [pandas 2.2 introductory guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html) explains DataFrames and common table operations.
- [pandas 2.2 indexing guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/indexing.html) explains Boolean selection and label-based selection.
- [pandas 2.2 group-by guide](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/groupby.html) explains grouping and aggregation.
- [Streamlit main concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts) explains the Python-to-browser execution model.
- [Streamlit 1.50.0 tabs](https://docs.streamlit.io/1.50.0/develop/api-reference/layout/st.tabs) documents tab containers and execution behavior for the workshop version.
- [Matplotlib histogram reference](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html), [Seaborn boxplot reference](https://seaborn.pydata.org/generated/seaborn.boxplot.html), and [Seaborn heatmap reference](https://seaborn.pydata.org/generated/seaborn.heatmap.html) explain the plot types used.
- [Plotly line charts](https://plotly.com/python/line-charts/) and [Plotly bar charts](https://plotly.com/python/bar-charts/) describe the interactive chart construction used here.
