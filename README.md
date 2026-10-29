# SaaS Subscription Revenue Dashboard — Tableau (SYNTHETIC DATA)

> **All data in this project is SYNTHETIC.** It was generated for a portfolio
> demo (Project 8's ETL pipeline, seed 20261028). This is a **portfolio skill
> demo, NOT work experience** and NOT real company data. Never present it as
> job experience.

## Business question

For a fictional SaaS business, how did revenue, subscribers, and churn evolve
from January 2025 to June 2026 — and which plans and acquisition channels
drove (or dragged) the result?

## What this demonstrates

- **Tableau dashboard design**: one dashboard, five views, built from
  dashboard-ready data rather than raw dumps.
- **Reusing a real pipeline's output**: the monthly KPIs come from Project 8
  (`etl-reporting-pipeline`: raw billing CSVs → SQLite warehouse → SQL KPI
  marts with CTEs and window functions). The plan and channel breakdowns are
  queried from that same warehouse (`mart_plan_monthly`,
  `mart_churn_by_channel`) — no numbers were invented for this dashboard.
- **Honest scope**: only views the data supports. There is no plan-level
  subscriber series or channel-level monthly series in the source marts, so
  those views are not claimed.

## Dashboard views (all titled SYNTHETIC DATA)

1. **MRR trend** — MRR over time.
2. **Revenue collected / running revenue** — monthly revenue bars with the
   cumulative running-revenue line.
3. **Subscriber growth vs churn** — active subscribers with new vs churned
   subscribers per month.
4. **Revenue by plan** — stacked monthly revenue by plan (starter / growth /
   pro / enterprise).
5. **Churn by channel** — churn share by acquisition channel (organic,
   paid_search, referral, partner).

## Verified results (recomputed from the CSVs by `src/make_previews.py`)

- Period: **Jan 2025 – Jun 2026 (18 months)**
- MRR: **$11,050.40 → $163,506.10 (+1,379.6%)**
- Active subscribers: **48 → 894**; new subscribers total **1,200**,
  churned total **336**; average monthly churn rate **5.16%**
- Total revenue collected: **$1,624,082.60** (running revenue ends at the
  same figure, as it must)
- Revenue by plan: enterprise **$726,073.20**, pro **$484,454.40**,
  growth **$298,564.20**, starter **$114,990.80** — enterprise is ~44.7% of
  revenue
- Churn share by channel: organic 29.4%, referral 28.6%, partner 28.2%,
  paid_search 25.7% — nearly flat, paid search lowest

## Files

- `tableau/SaaS_Revenue_Dashboard.twbx` — packaged Tableau workbook
  (.twb + the three data CSVs). Open in Tableau Desktop, then publish to
  Tableau Public from there.
- `tableau/SaaS_Revenue_Dashboard.twb` — workbook document alone.
- `data/monthly_kpis.csv` — 18 monthly KPI rows (from Project 8's
  `dashboard_ready.csv`).
- `data/revenue_by_plan_monthly.csv` — 72 rows, revenue by plan per month.
- `data/churn_by_channel.csv` — 4 rows, churn by acquisition channel.
- `src/build_workbook.py` — builds the .twb and packages the .twbx, then
  validates the XML and the package contents.
- `src/make_previews.py` — recomputes the summary and renders preview
  charts of each view from the same CSVs.
- `images/01–05_*.png` — preview renders of the five views.
  **These are matplotlib renders of the exact dashboard data, NOT Tableau
  screenshots** (no Tableau Desktop is available in this build environment).
  `images/dashboard_summary.json` holds the recomputed numbers.

## Publish to Tableau Public (needs the owner's account)

This repo deliberately contains **no Tableau account and no credentials**.
To publish:

1. Open `tableau/SaaS_Revenue_Dashboard.twbx` in Tableau Desktop (free
   trial / licensed) or Tableau Public Desktop.
2. Check the five worksheets render against the packaged CSVs.
3. Server → Publish Workbook → Tableau Public, signed in as your own
   Tableau Public account, keeping "SYNTHETIC DATA" in the title.
4. Paste the Tableau Public URL here and on LinkedIn.

Until that step is done, the workbook + preview images in this repo are the
shipped artifact, and the Tableau Public publish is the one remaining step.

## Reproduce

```bash
python3 src/make_previews.py   # renders images/ + dashboard_summary.json
python3 src/build_workbook.py  # builds + validates tableau/*.twb/*.twbx
```

## 60-second interview pitch

> "I took the output of my ETL-to-report pipeline — monthly SaaS KPIs — and
> built a Tableau dashboard on it: MRR trend, revenue versus running
> revenue, subscriber growth versus churn, plus revenue by plan and churn
> by channel. The story the data tells is that MRR grew about 14x in 18
> months to $163k, driven disproportionately by enterprise — 7% of
> subscriptions but about 45% of revenue — while churn by channel was
> nearly flat, so channel wasn't the churn lever. All the data is synthetic;
> the point of the project is the dashboard and the pipeline behind it,
> not the numbers themselves."

## Likely Q&A

- **Why Tableau instead of another chart?** Tableau is what Data Analyst
  postings keep asking for; this closes that specific gap with a real
  workbook, not a screenshot.
- **Is this real company data?** No — synthetic, labelled everywhere, from
  my own Project 8 pipeline.
- **Why isn't it live on Tableau Public yet?** Publishing needs a personal
  Tableau Public account sign-in, which I do deliberately in my own
  account rather than through an agent session; the packaged workbook is
  in the repo ready to publish.
