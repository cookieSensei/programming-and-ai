# Business Analytics Workshop

Six independent, beginner-friendly Streamlit projects. Each numbered project
folder contains `app.py`, its CSV dataset, an `EXPLANATION.md` worked tutorial,
and a `tutorial_assets` folder containing the tutorial's chart outputs.
No shared Python helpers, API keys, database or internet connection are needed
to run the apps after the Python dependencies are installed.

All datasets are fictional, generated teaching examples, not real company or
customer records. Monetary values are INR. Dates are historical teaching periods
in 2025, not live business performance. The examples are designed to practice
analysis; their patterns are not evidence about real businesses.

| Project | Dataset | Rows and grain | What you will practice |
| --- | --- | --- | --- |
| [01_retail_sales](01_retail_sales) | `retail_sales.csv` | 720 orders | Discounts, net sales, gross margin, time trends, regional mix and correlation |
| [02_marketing_campaigns](02_marketing_campaigns) | `marketing_campaigns.csv` | 360 daily channel/campaign observations | Conversion funnels, weighted rates, ROAS and acquisition cost |
| [03_customer_churn](03_customer_churn) | `customer_churn.csv` | 480 customers in one snapshot | Segment comparisons, sample sizes, tenure, satisfaction and churn |
| [04_inventory_planning](04_inventory_planning) | `inventory.csv` | 180 SKU/warehouse pairs | Stock cover, reorder points, inventory value and a safety-buffer scenario |
| [05_finance_budget](05_finance_budget) | `department_budget.csv` | 192 month/department/expense-category lines | Budget utilization, variance, overspend and monthly trends |
| [06_restaurant_operations](06_restaurant_operations) | `restaurant_orders.csv` | 600 orders | Sales, service time, ratings, contribution and operational comparisons |

## Worked code cells with outputs

Open the guide beside each project's `app.py`. Each tutorial follows a practical
sequence: **business question, commented Python code cell, captured output, and
interpretation**. Tables and calculations are executed against the bundled CSV,
and chart cells include the generated chart images. Comments explain what the
operations do and why they help answer the question.

The tutorials build from loading and inspecting data to filtering, calculating
measures, grouping, plotting, and preparing reports and CSV downloads. A separate
Streamlit section shows how to connect the analysis to an interactive interface,
with an actual rendered-output summary from the runnable teaching example.

| Guide | Main questions explained |
| --- | --- |
| [Retail sales explanation](01_retail_sales/EXPLANATION.md) | How do discounts and product costs affect sales and gross profit? Which regions and categories lead, and what does a typical order look like? |
| [Marketing campaigns explanation](02_marketing_campaigns/EXPLANATION.md) | Which channels produce attributed revenue efficiently? Why do conversion rate, CPA and ROAS use different denominators? |
| [Customer churn explanation](03_customer_churn/EXPLANATION.md) | Which customer groups have higher observed churn proportions? How do sample sizes, tenure and satisfaction change the interpretation? |
| [Inventory planning explanation](04_inventory_planning/EXPLANATION.md) | Which SKU locations fall below the reorder threshold? How do demand, lead time and an extra buffer change suggested quantities and purchase cost? |
| [Finance budget explanation](05_finance_budget/EXPLANATION.md) | Where does actual spending exceed the budget? Why can an overall total hide overspent lines and departments? |
| [Restaurant operations explanation](06_restaurant_operations/EXPLANATION.md) | How do sales, wait times, ratings and food-cost contribution vary across branches and meal periods? |

Read the business problem first, then work through the analysis cells in order.
Markdown displays the code and saved output; it does not execute the cells on
GitHub. To run them, create a JupyterLab notebook in the same numbered project
folder as the CSV and copy the analysis cells in sequence. Their variables carry
forward from one cell to the next. The tutorial explains the separate instructions
for its Streamlit example, which runs as a Python app rather than a notebook cell.

The displayed outputs are reproducible snapshots of the supplied fictional data
and the selections shown in the code. Editing the CSV or changing a selection can
change the results. Static chart images show the captured output; the running
Streamlit app provides its interactive Plotly charts. Proposed extensions and
compact teaching examples are identified separately from the full `app.py`.

These static learning guides complement the app's **Full report** tab. The guides
teach how the program works; the downloaded report contains results for the
filters currently selected in the running app.

## Open in CookieSensei Coder

Create a workspace from **Business Analytics Workshop**. In VS Code and
JupyterLab, open `business_analytics_workshop` in the project file browser.
The **Business Analytics Dashboard** app opens the project selector. Select any
project in its sidebar, then change the filters and read the explanations below
each chart. **Guided workshop** opens the current course edition with detailed
reports. Choose **My editable projects** to run your personal `app.py` and CSV
changes from the project folder. Each app is also runnable independently.

Every project explains the business problem, decision context, row meaning, KPI
formulas, chart axes and units, interpretation, and unanswered questions. The
**Full report** tab presents a complete 12-section report with an executive
summary, results calculated from your filters, explanations of all five visuals,
data quality, suggested investigations, limitations, and reproduction steps.
Download it as Markdown with **Download full report (Markdown)**. Both the report
and the filtered CSV reflect the current selections.

New workspaces receive a pinned copy of this folder. An existing workspace must
be updated to the workshop-projects template version and restarted by its owner
to receive the folder. Student files are preserved, so repository updates do not
automatically overwrite a previously copied workshop folder. After an owner
updates the workspace, Guided workshop shows the new explanations while
My editable projects preserves their existing work.

To run a separate app in a Coder terminal:

```bash
cd /home/coder/project/business_analytics_workshop/01_retail_sales
streamlit run app.py --server.port 8502
```

The built-in dashboard already uses port 8501. Forward port 8502 through Coder
for your separate instance. Keep the default authenticated, owner-only access.
You can substitute any other numbered project directory in the command.

## Run on your own computer

Use Python 3.12 and install these tested workshop versions in a virtual
environment. The Coder template already includes them.

```bash
python -m venv .venv
source .venv/bin/activate
# On Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install streamlit==1.50.0 pandas==2.2.3 numpy==2.3.5 matplotlib==3.10.8 seaborn==0.13.2 plotly==6.5.2
cd business_analytics_workshop/01_retail_sales
streamlit run app.py
```

## Suggested learning sequence

1. Read a project's CSV and identify what one row represents.
2. Open `EXPLANATION.md` and run its commented analysis cells in order in a
   notebook beside the CSV. Compare each result with the captured output, then
   read the corresponding operations in `app.py`.
3. Compare the dashboard KPIs with a manual calculation on a small filtered
   sample. Rates use summed numerators and denominators where appropriate.
4. Open **Explore the data** for Matplotlib histograms and Seaborn distribution
   plots or heatmaps. Use Plotly hover, zoom and legend toggles on the dashboard.
5. Inspect **Data and quality** for source types, missing cells, duplicate rows,
   descriptive statistics, and a filtered CSV download.
6. Read **Full report**, change a filter and compare the updated findings.
   Download the report and explain one conclusion and one unanswered question.
7. Complete the exercises at the bottom of each app. Add one filter, one chart,
   and a short explanation of a business finding and its limitations.

Start with retail and marketing, then try churn, inventory, finance and
restaurant operations. Clearing every filter value shows a helpful empty-state
message. Selecting only one date asks for the end date. Required missing or
invalid numeric data produces an error so students can fix the source instead
of silently analyzing discarded rows.

## Dataset field guide

- **Retail:** `order_id` identifies one order, `order_date` is its date;
  `region`, `category`, `channel` are segments; `units`, `unit_price`,
  `discount_pct` (0-100) and `unit_cost` determine sales and gross profit.
  Net sales = units x price x (1 - discount_pct / 100).
- **Marketing:** `date`, `channel`, `campaign` identify an observation;
  `impressions`, `clicks`, `conversions` are counts; `spend` and `revenue`
  are attributed amounts. ROAS = revenue / spend; CPA = spend / conversions;
  conversion rate = conversions / clicks. Attributed revenue is not profit.
- **Churn:** `customer_id` is a synthetic ID; `region`, `contract` are
  segments; `tenure_months`, `monthly_fee`, `support_tickets`,
  `satisfaction_score` (1-10) describe the customer; `churned` is 0 or 1.
  This is a snapshot proportion, not a monthly churn rate or predictive model.
- **Inventory:** `sku` repeats across `warehouse` locations; `category`
  is the product group; `stock_on_hand` and `safety_stock` are units;
  `daily_demand` is assumed units/day; `lead_time_days` is days; `unit_cost`
  is INR/unit. The interactive buffer is additional days of demand.
- **Finance:** `month`, `department`, `expense_category` identify a budget
  line; `budget` and `actual` are expenses in INR. Positive variance is under
  budget, negative variance is overspend. This is not a profit/cash-flow report.
- **Restaurant:** `order_id`, `date`, `branch`, `meal_period`, `channel`
  identify and segment orders; `guests` is a count; `bill_amount` and
  `food_cost` are INR; `wait_minutes` is minutes; `rating` is 1-5.
  Contribution excludes staffing, rent, delivery fees and taxes.

Correlation does not establish causation. Compare sample sizes and aggregation
levels before suggesting business action.
