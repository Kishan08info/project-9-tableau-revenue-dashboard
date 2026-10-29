"""Preview renders of the Tableau dashboard views, drawn from the exact
dashboard data files with matplotlib (same numbers the Tableau workbook
uses). These are NOT Tableau screenshots: no Tableau Desktop/Public
session is available in this build environment, so the packaged .twbx
is published for opening in Tableau Desktop / Tableau Public, and these
PNGs show exactly what each view plots. All data is SYNTHETIC.
"""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
IMG = ROOT / "images"
IMG.mkdir(exist_ok=True)

rows = list(csv.DictReader(open(DATA / "monthly_kpis.csv")))
months = [r["month"] for r in rows]
mrr = [float(r["mrr"]) for r in rows]
rev = [float(r["revenue_collected"]) for r in rows]
running = [float(r["running_revenue"]) for r in rows]
active = [int(r["active_subs"]) for r in rows]
new = [int(r["new_subs"]) for r in rows]
churned = [int(r["churned_subs"]) for r in rows]
churn_rate = [float(r["churn_rate_pct"]) if r["churn_rate_pct"] else None for r in rows]

plt.rcParams["figure.figsize"] = (10, 4.5)
x = range(len(months))

# 1. MRR trend
fig, ax = plt.subplots()
ax.plot(x, mrr, marker="o", linewidth=2)
ax.set_title("SYNTHETIC DATA — MRR trend (Jan 2025 – Jun 2026)")
ax.set_ylabel("MRR ($)")
ax.set_xticks(list(x)[::2]); ax.set_xticklabels([months[i] for i in list(x)[::2]], rotation=30, ha="right")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(IMG / "01_mrr_trend.png", dpi=150); plt.close(fig)

# 2. Revenue collected vs running revenue
fig, ax = plt.subplots()
ax.bar(x, rev, label="Revenue collected (month)")
ax.plot(x, running, color="darkorange", marker="o", linewidth=2, label="Running revenue (cumulative)")
ax.set_title("SYNTHETIC DATA — Revenue collected and running revenue")
ax.set_ylabel("$")
ax.set_xticks(list(x)[::2]); ax.set_xticklabels([months[i] for i in list(x)[::2]], rotation=30, ha="right")
ax.legend(); ax.grid(alpha=0.3, axis="y")
fig.tight_layout(); fig.savefig(IMG / "02_revenue_running.png", dpi=150); plt.close(fig)

# 3. Subscriber growth vs churn
fig, ax = plt.subplots()
ax.plot(x, active, marker="o", linewidth=2, label="Active subs")
ax.bar(x, new, alpha=0.6, label="New subs")
ax.bar(x, [-c for c in churned], alpha=0.6, label="Churned subs (negative)")
ax.set_title("SYNTHETIC DATA — Subscriber growth vs churn")
ax.set_ylabel("Subscribers")
ax.set_xticks(list(x)[::2]); ax.set_xticklabels([months[i] for i in list(x)[::2]], rotation=30, ha="right")
ax.legend(); ax.grid(alpha=0.3, axis="y")
fig.tight_layout(); fig.savefig(IMG / "03_subscribers_vs_churn.png", dpi=150); plt.close(fig)

# 4. Revenue by plan (stacked monthly)
plan_rows = list(csv.DictReader(open(DATA / "revenue_by_plan_monthly.csv")))
plans = sorted({r["plan"] for r in plan_rows})
fig, ax = plt.subplots()
bottom = [0.0] * len(months)
for plan in plans:
    vals = []
    for m in months:
        match = [r for r in plan_rows if r["month"] == m and r["plan"] == plan]
        vals.append(float(match[0]["revenue"]) if match else 0.0)
    ax.bar(x, vals, bottom=bottom, label=plan)
    bottom = [b + v for b, v in zip(bottom, vals)]
ax.set_title("SYNTHETIC DATA — Revenue by plan per month")
ax.set_ylabel("$")
ax.set_xticks(list(x)[::2]); ax.set_xticklabels([months[i] for i in list(x)[::2]], rotation=30, ha="right")
ax.legend(); ax.grid(alpha=0.3, axis="y")
fig.tight_layout(); fig.savefig(IMG / "04_revenue_by_plan.png", dpi=150); plt.close(fig)

# 5. Churn by channel
ch = list(csv.DictReader(open(DATA / "churn_by_channel.csv")))
fig, ax = plt.subplots()
ax.bar([r["channel"] for r in ch], [float(r["churn_share_pct"]) for r in ch])
ax.set_title("SYNTHETIC DATA — Churn share by acquisition channel (%)")
ax.set_ylabel("Churn share (%)")
ax.grid(alpha=0.3, axis="y")
fig.tight_layout(); fig.savefig(IMG / "05_churn_by_channel.png", dpi=150); plt.close(fig)

# Verified summary (recomputed from the CSVs, not copied from README text)
summary = {
    "months": len(rows),
    "period": f"{months[0]} to {months[-1]}",
    "mrr_first": mrr[0], "mrr_last": mrr[-1],
    "mrr_growth_pct": round((mrr[-1] - mrr[0]) / mrr[0] * 100, 1),
    "active_first": active[0], "active_last": active[-1],
    "total_revenue_collected": round(sum(rev), 2),
    "running_revenue_last": running[-1],
    "total_new_subs": sum(new), "total_churned_subs": sum(churned),
    "avg_monthly_churn_rate_pct": round(sum(v for v in churn_rate if v is not None) / len([v for v in churn_rate if v is not None]), 2),
    "revenue_by_plan_total": {p: round(sum(float(r["revenue"]) for r in plan_rows if r["plan"] == p), 2) for p in plans},
}
import json
(ROOT / "images" / "dashboard_summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
print("PNGs:", sorted(p.name for p in IMG.glob("*.png")))
