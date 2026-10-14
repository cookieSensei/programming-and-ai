# Business Analytics Workshop

Six independent, beginner-friendly Streamlit projects. Each numbered project
folder contains exactly two files: `app.py` and its CSV dataset. No shared Python
helpers, API keys, database or internet connection are needed to run the apps.

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
| [05_finance_budget](05_finance_budget) | `department_budget.csv` | 192 month/department/expense-category lines | Budget utilization, variance, overspend and cumulative trends |
| [06_restaurant_operations](06_restaurant_operations) | `restaurant_orders.csv` | 600 orders | Sales, service time, ratings, contribution and operational comparisons |

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
2. Run the app, then read `app.py` from top to bottom. The numbered comments
   follow loading, filtering, calculation, visualization and data inspection.
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
