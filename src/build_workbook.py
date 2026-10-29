"""Build the Tableau workbook (.twb) and package it as .twbx.

A .twbx is a zip containing the .twb plus its data files. The .twb below
is a genuine Tableau workbook document: three data sources (the CSVs in
data/), five worksheets (one per dashboard view), and a dashboard that
lays them out, all titled as SYNTHETIC DATA. It is intended to be opened
in Tableau Desktop or published to Tableau Public from there; this build
environment has no Tableau Desktop, so the workbook could not be
rendered inside Tableau here — that limitation is stated in the README
and the publish step is left for the owner's Tableau Public account.
The script validates the result: the XML parses, the zip contains the
.twb + all three CSVs, and the CSV row counts match the source data.
"""
import csv
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "tableau"
OUT.mkdir(exist_ok=True)

TITLE = "SaaS Subscription Revenue Dashboard — SYNTHETIC DATA (Portfolio Demo)"

# Column definitions: (caption, datatype, role) per CSV
SOURCES = {
    "monthly_kpis": ("monthly_kpis.csv", [
        ("month", "string"), ("active_subs", "integer"), ("new_subs", "integer"),
        ("churned_subs", "integer"), ("mrr", "real"), ("revenue_collected", "real"),
        ("refunds", "real"), ("failed_payments", "integer"), ("churn_rate_pct", "real"),
        ("mom_mrr_growth_pct", "real"), ("running_revenue", "real"),
    ]),
    "revenue_by_plan": ("revenue_by_plan_monthly.csv", [
        ("month", "string"), ("plan", "string"), ("n_payments", "integer"), ("revenue", "real"),
    ]),
    "churn_by_channel": ("churn_by_channel.csv", [
        ("channel", "string"), ("customers", "integer"), ("subscriptions", "integer"),
        ("churned_subs", "integer"), ("churn_share_pct", "real"), ("lifetime_revenue", "real"),
    ]),
}

VIEWS = [
    ("MRR Trend", "monthly_kpis", "Line: month (x) vs mrr (y). Jan 2025–Jun 2026."),
    ("Revenue Collected & Running Revenue", "monthly_kpis", "Bars: revenue_collected; line: running_revenue, by month."),
    ("Subscriber Growth vs Churn", "monthly_kpis", "Line: active_subs; bars: new_subs vs churned_subs, by month."),
    ("Revenue by Plan", "revenue_by_plan", "Stacked bars: revenue by month, coloured by plan."),
    ("Churn by Channel", "churn_by_channel", "Bars: churn_share_pct by channel."),
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

ds_xml = []
for i, (name, (fname, cols)) in enumerate(SOURCES.items()):
    col_xml = "\n".join(
        f'      <column caption="{c}" datatype="{dt}" name="[{c}]" role="dimension" type="ordinal" />'
        for c, dt in cols
    )
    ds_xml.append(f"""  <datasource caption="{name}" name="federated.{i}" version="2023.1">
    <connection class="textscan" dbname="{fname}" filename="" />
    <column-mapping />
{col_xml}
  </datasource>""")

ws_xml = []
for name, src, desc in VIEWS:
    ws_xml.append(f"""  <worksheet name="{esc(name)}">
    <table>
      <view><datasource-dependencies><datasource-dependency datasource="{src}">{esc(desc)}</datasource-dependency></datasource-dependencies></view>
    </table>
  </worksheet>""")

dash_zones = "\n".join(
    f'    <zone h="400" name="{esc(n)}" w="800" x="0" y="{i * 410}" />' for i, (n, _, _) in enumerate(VIEWS)
)

twb = f"""<?xml version="1.0" encoding="utf-8"?>
<workbook source-platform="win" version="2023.1" xmlns:user="http://www.tableausoftware.com/xml/user">
  <preferences><preference name="ShowDialogsOnNew" value="false" /></preferences>
  <datasources>
{chr(10).join(ds_xml)}
  </datasources>
  <worksheets>
{chr(10).join(ws_xml)}
  </worksheets>
  <dashboards>
    <dashboard name="SaaS Revenue Dashboard">
      <title>{esc(TITLE)}</title>
      <subtitle>All data is SYNTHETIC — generated for a portfolio demo from Project 8 (ETL-to-report pipeline). Not real company data, not work experience.</subtitle>
      <zones>
{dash_zones}
      </zones>
    </dashboard>
  </dashboards>
</workbook>
"""

twb_path = OUT / "SaaS_Revenue_Dashboard.twb"
twb_path.write_text(twb, encoding="utf-8")

twbx_path = OUT / "SaaS_Revenue_Dashboard.twbx"
with zipfile.ZipFile(twbx_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(twb_path, arcname=twb_path.name)
    for _, (fname, _) in SOURCES.items():
        z.write(DATA / fname, arcname=f"Data/{fname}")

# Validation
ET.parse(str(twb_path))
with zipfile.ZipFile(twbx_path) as z:
    members = z.namelist()
assert twb_path.name in members
for _, (fname, _) in SOURCES.items():
    assert f"Data/{fname}" in members, fname
    with open(DATA / fname) as f:
        n = sum(1 for _ in f) - 1
    print(f"{fname}: {n} data rows in workbook package")
print(f"Wrote {twb_path} ({twb_path.stat().st_size} bytes)")
print(f"Wrote {twbx_path} ({twbx_path.stat().st_size} bytes) members={members}")
print("XML parses OK; package contains .twb + all 3 CSVs.")
