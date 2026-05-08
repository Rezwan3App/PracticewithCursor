"""One-shot generator: embed MBA Grads.xlsx + pwc-logo.svg into Candidate_Dashboard.html.

Enhancements included:
  1. Dark mode toggle (persisted in localStorage)
  2. GPA range slider (min/max dual range filter)
  3. Export CSV button (exports filtered + searched rows)
  4. Salary histogram (Analysis tab)
  5. Job function breakdown chart (Analysis tab)
  6. Top-earner row highlighting (top 10% = orange stripe, top 25% = green stripe)
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
XLSX = BASE / "MBA Grads.xlsx"
SVG_PATH = BASE / "pwc-logo.svg"
OUT = BASE / "Candidate_Dashboard.html"


def load_svg_inline() -> str:
    raw = SVG_PATH.read_text(encoding="utf-8")
    if raw.strip().startswith("<?xml"):
        raw = raw.split(">", 1)[1].strip()
    return raw


def main() -> None:
    df = pd.read_excel(XLSX, "Offers")
    rows = df.replace({float("nan"): None}).to_dict(orient="records")
    payload = json.dumps(rows, default=str, separators=(",", ":"))
    svg = load_svg_inline()

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>PwC · Candidate Profiler · MBA Offers</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600&family=Inter+Tight:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Outfit:wght@400;500;600&display=swap" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --app-chrome: 11.5rem;
    --chart-h: clamp(110px, 16vh, 200px);
    --chart-short: clamp(88px, 12vh, 140px);
    --ion-radius: 14px;
    --bc-navy: #2b2b2b;
    --bc-blue: #d04a02;
    --bc-blue-light: #e8e8e8;
    --bc-red: #c0392b;
    --ink: #f7f5f4;
    --line: rgba(43, 43, 43, 0.12);
    --line-2: rgba(43, 43, 43, 0.2);
    --cream: #2b2b2b;
    --muted: #707070;
    --muted-2: #4a5378;
    --gold: #d04a02;
    --green: #1a7f5c;
    --red: #c0392b;
    --header-text: #f7f5f4;
    --on-accent: #ffffff;
    --ion-glow: 0 0 0 1px rgba(43, 43, 43, 0.06), 0 10px 32px rgba(43, 43, 43, 0.08);
    --panel-bg: linear-gradient(180deg, #ffffff 0%, #fafcfd 100%);
    --panel-border: rgba(43, 43, 43, 0.2);
    --table-bg: #fff;
    --table-hd-bg: linear-gradient(180deg, #fafcfd 0%, #f0f2f8 100%);
    --table-row-hover: rgba(208, 74, 2, 0.06);
    --tab-bg: rgba(255, 255, 255, 0.92);
    --search-bg: #ffffff;
    --search-border: rgba(43, 43, 43, 0.2);
    --search-color: #2b2b2b;
    --snap-bg: #e8eef9;
    --pager-btn-bg: #ffffff;
  }}
  html[data-theme="dark"] {{
    --ink: #13141a;
    --cream: #e8e6e3;
    --muted: #9a9a9a;
    --line: rgba(255,255,255,0.10);
    --line-2: rgba(255,255,255,0.14);
    --ion-glow: 0 0 0 1px rgba(255,255,255,0.06), 0 10px 32px rgba(0,0,0,0.45);
    --panel-bg: linear-gradient(180deg, #1e2030 0%, #191c2a 100%);
    --panel-border: rgba(255,255,255,0.11);
    --table-bg: #1a1d2b;
    --table-hd-bg: linear-gradient(180deg, #22263a 0%, #1d2035 100%);
    --table-row-hover: rgba(208,74,2,0.12);
    --tab-bg: rgba(28,31,46,0.97);
    --search-bg: #1a1d2b;
    --search-border: rgba(255,255,255,0.14);
    --search-color: #e8e6e3;
    --snap-bg: rgba(34,39,94,0.3);
    --pager-btn-bg: #1e2030;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    background: var(--ink);
    color: var(--cream);
    font-family: 'Inter Tight', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    height: 100%;
    overflow: hidden;
    transition: background 0.25s, color 0.25s;
  }}
  body {{
    background:
      radial-gradient(1000px 520px at 92% -8%, rgba(208, 74, 2, 0.14), transparent 55%),
      radial-gradient(800px 480px at -5% 105%, rgba(217, 217, 217, 0.45), transparent 50%),
      var(--ink);
  }}
  html[data-theme="dark"] body {{
    background:
      radial-gradient(1000px 520px at 92% -8%, rgba(208, 74, 2, 0.07), transparent 55%),
      radial-gradient(800px 480px at -5% 105%, rgba(30,30,60,0.55), transparent 50%),
      var(--ink);
  }}
  .shell {{
    max-width: 1600px;
    margin: 0 auto;
    padding: 10px 20px 8px;
    height: 100vh;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .dashboard-body {{ flex: 1; min-height: 0; position: relative; }}
  header.top {{
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    padding: 10px 14px 12px;
    margin: 0 -4px 6px;
    border-bottom: 1px solid rgba(217, 217, 217, 0.35);
    background: linear-gradient(165deg, #242a66 0%, #2b2b2b 48%, #161a4a 100%);
    backdrop-filter: blur(14px);
    border-radius: 0 0 var(--ion-radius) var(--ion-radius);
    flex-shrink: 0;
    color: var(--header-text);
  }}
  .brand-row {{ display: flex; align-items: flex-start; gap: 14px; margin-bottom: 4px; }}
  .bc-logo-link {{ flex-shrink: 0; line-height: 0; border-radius: 10px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2); }}
  .bc-logo-wrap {{
    width: 44px; height: 44px;
    background: #fff;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px;
  }}
  .bc-logo-wrap svg {{ width: 100%; height: auto; max-height: 32px; }}
  .crumb {{
    font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase;
    color: rgba(247, 245, 244, 0.68);
    font-weight: 500;
  }}
  h1.title {{
    font-family: 'Fraunces', serif;
    font-weight: 400;
    font-size: clamp(1.25rem, 2.2vw, 1.75rem);
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: #ffffff;
  }}
  h1.title em {{ font-style: italic; color: var(--bc-blue); font-weight: 400; }}
  .subtitle {{
    margin-top: 4px;
    font-size: 11px;
    color: rgba(247, 245, 244, 0.82);
    max-width: 44rem;
    line-height: 1.4;
  }}
  .ctrl-cluster {{ display: flex; flex-direction: column; align-items: flex-end; gap: 8px; }}
  .filter-row {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: flex-end; }}
  .sel-label {{ font-size: 10px; color: rgba(247, 245, 244, 0.72); letter-spacing: 0.1em; text-transform: uppercase; }}
  .sel {{
    background: #f7f5f4;
    color: #2b2b2b;
    border: 1px solid rgba(43, 43, 43, 0.22);
    padding: 6px 28px 6px 12px;
    font-size: 12px;
    border-radius: 4px;
    font-family: inherit;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'%3E%3Cpath fill='%232B2B2B' d='M5 7L1 3h8z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
    cursor: pointer;
  }}
  .sel:hover {{ border-color: rgba(208, 74, 2, 0.65); }}
  .gpa-filter {{
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .gpa-filter input[type=range] {{
    width: 68px;
    accent-color: #d04a02;
    cursor: pointer;
  }}
  .gpa-val {{
    font-size: 11px;
    color: rgba(247,245,244,0.9);
    font-family: 'JetBrains Mono', monospace;
    min-width: 26px;
    text-align: center;
  }}
  .btn-reset {{
    background: var(--bc-red);
    color: #fff;
    border: 0;
    padding: 6px 14px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
  }}
  .btn-reset:hover {{ filter: brightness(1.08); }}
  .btn-dark {{
    background: rgba(255,255,255,0.14);
    color: #fff;
    border: 1px solid rgba(255,255,255,0.28);
    padding: 5px 11px;
    font-size: 14px;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    line-height: 1;
    transition: background 0.2s;
  }}
  .btn-dark:hover {{ background: rgba(255,255,255,0.24); }}
  .btn-export {{
    background: var(--green);
    color: #fff;
    border: 0;
    padding: 7px 14px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
  }}
  .btn-export:hover {{ filter: brightness(1.1); }}
  nav.tabs {{
    display: flex;
    gap: 4px;
    padding: 4px;
    margin: 0 0 6px;
    border: 1px solid var(--line-2);
    border-radius: 12px;
    background: var(--tab-bg);
    overflow-x: auto;
    flex-shrink: 0;
    scrollbar-width: thin;
    box-shadow: 0 1px 0 rgba(43, 43, 43, 0.04);
    transition: background 0.25s;
  }}
  nav.tabs button {{
    background: transparent;
    border: 0;
    color: var(--muted);
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.04em;
    cursor: pointer;
    white-space: nowrap;
    font-family: inherit;
    transition: color 0.18s;
  }}
  nav.tabs button:hover {{ color: var(--cream); }}
  nav.tabs button.active {{ color: var(--cream); position: relative; }}
  nav.tabs button.active::after {{
    content: '';
    position: absolute;
    left: 10px; right: 10px; bottom: 4px;
    height: 2px;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--bc-blue), var(--bc-red));
  }}
  .tab-panel {{
    display: none;
    position: absolute;
    inset: 0;
    overflow: hidden;
    flex-direction: column;
  }}
  .tab-panel.active {{ display: flex; animation: fade 0.22s ease; }}
  .tab-scroll {{
    flex: 1;
    min-height: 0;
    overflow: auto;
    padding: 0 4px 8px;
    scrollbar-width: thin;
    scrollbar-color: rgba(208, 74, 2, 0.4) transparent;
  }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
  .kpi-strip {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    border: 1px solid rgba(217, 217, 217, 0.35);
    border-radius: var(--ion-radius);
    overflow: hidden;
    margin-bottom: 10px;
    background: linear-gradient(135deg, #22275e 0%, #2b2b2b 55%, #161a4a 100%);
    box-shadow: var(--ion-glow);
    color: var(--header-text);
  }}
  @media (max-width: 900px) {{
    .kpi-strip {{ grid-template-columns: repeat(2, 1fr); }}
  }}
  .kpi {{
    padding: 10px 14px;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
  }}
  .kpi:last-child {{ border-right: 0; }}
  .kpi .klabel {{
    font-size: 10px;
    color: rgba(247, 245, 244, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
  }}
  .kpi .kval {{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: clamp(1.2rem, 2.2vw, 1.65rem);
    color: #ffffff;
    letter-spacing: -0.02em;
    line-height: 1;
  }}
  .kpi .ksub {{
    font-size: 11px;
    color: rgba(247, 245, 244, 0.72);
    margin-top: 8px;
  }}
  .panel-grid {{
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 10px;
    margin-bottom: 10px;
  }}
  .panel {{
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    border-radius: var(--ion-radius);
    padding: 10px 12px;
    box-shadow: var(--ion-glow);
    transition: background 0.25s, border-color 0.25s;
  }}
  .panel.accent-left {{
    border-left: 3px solid var(--bc-red);
    box-shadow: inset 0 0 0 1px rgba(208, 74, 2, 0.08), var(--ion-glow);
  }}
  .panel-head {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--line);
  }}
  .panel-title {{
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: clamp(0.95rem, 1.2vw, 1.05rem);
    color: var(--cream);
  }}
  .panel-sub {{
    font-size: 10px;
    color: var(--muted);
    margin-top: 3px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }}
  .panel-tag {{
    font-size: 9px;
    padding: 3px 8px;
    border-radius: 3px;
    background: rgba(208, 74, 2, 0.12);
    color: var(--cream);
    border: 1px solid rgba(208, 74, 2, 0.35);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
  }}
  .col-6 {{ grid-column: span 6; }}
  .col-12 {{ grid-column: span 12; }}
  @media (max-width: 960px) {{
    .col-6 {{ grid-column: span 12; }}
  }}
  .chart-box {{ position: relative; height: var(--chart-h); min-height: 0; }}
  .chart-box.short {{ height: var(--chart-short); max-height: var(--chart-short); }}
  .chart-box.tall {{ height: clamp(150px, 24vh, 280px); }}
  .search-bar {{
    margin-bottom: 8px;
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
  }}
  .search-bar input {{
    flex: 1;
    min-width: 200px;
    padding: 8px 12px;
    border: 1px solid var(--search-border);
    border-radius: 8px;
    font-family: inherit;
    font-size: 13px;
    background: var(--search-bg);
    color: var(--search-color);
    transition: background 0.25s, color 0.25s, border-color 0.25s;
  }}
  .tier-legend {{
    display: flex;
    gap: 16px;
    font-size: 11px;
    color: var(--muted);
    margin-bottom: 8px;
    align-items: center;
  }}
  .tier-dot {{
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 2px;
    margin-right: 4px;
    vertical-align: middle;
  }}
  .table-wrap {{
    border: 1px solid var(--line-2);
    border-radius: var(--ion-radius);
    overflow: auto;
    max-height: min(52vh, 480px);
    background: var(--table-bg);
    box-shadow: var(--ion-glow);
    transition: background 0.25s;
  }}
  table.data {{
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
  }}
  table.data th {{
    position: sticky;
    top: 0;
    background: var(--table-hd-bg);
    text-align: left;
    padding: 8px 10px;
    border-bottom: 1px solid var(--line-2);
    font-weight: 600;
    color: var(--cream);
    white-space: nowrap;
    z-index: 1;
  }}
  table.data td {{
    padding: 7px 10px;
    border-bottom: 1px solid rgba(43,43,43,0.08);
    vertical-align: top;
    color: var(--cream);
  }}
  html[data-theme="dark"] table.data td {{ border-bottom: 1px solid rgba(255,255,255,0.06); }}
  table.data tr:hover td {{ background: var(--table-row-hover) !important; }}
  table.data tr.tier-top10 td {{
    background: rgba(208,74,2,0.09);
    border-left: 3px solid #d04a02;
  }}
  table.data tr.tier-top25 td {{
    background: rgba(26,127,92,0.08);
    border-left: 3px solid #1a7f5c;
  }}
  .pager {{
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: flex-end;
    margin-top: 10px;
    font-size: 12px;
    color: var(--muted);
  }}
  .pager button {{
    background: var(--pager-btn-bg);
    border: 1px solid var(--line-2);
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    color: var(--cream);
    transition: background 0.2s;
  }}
  .pager button:disabled {{ opacity: 0.45; cursor: not-allowed; }}
  .snapshot-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }}
  @media (max-width: 700px) {{ .snapshot-grid {{ grid-template-columns: 1fr; }} }}
  .snap-item {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 12px 14px;
    background: var(--snap-bg);
    border-radius: 8px;
    border-left: 3px solid var(--bc-blue);
    transition: background 0.25s;
  }}
  .snap-label {{ font-size: 11px; color: var(--muted); }}
  .snap-val {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    color: var(--cream);
    font-weight: 500;
  }}
</style>
</head>
<body>
<div class="shell">
  <header class="top">
    <div>
      <div class="brand-row">
        <div class="bc-logo-link" aria-hidden="true">
          <div class="bc-logo-wrap">{svg}</div>
        </div>
        <div>
          <div class="crumb">People analytics · <b>MBA pipeline</b></div>
          <h1 class="title">Candidate Profiler · <em>MBA Offers</em></h1>
          <p class="subtitle">Interactive view of simulated MBA graduate outcomes—school mix, post-MBA roles, compensation, and offer flags. Adjust filters to explore cohorts.</p>
        </div>
      </div>
    </div>
    <div class="ctrl-cluster">
      <div class="filter-row">
        <span class="sel-label">Year</span>
        <select id="f-year" class="sel" aria-label="Graduation year"></select>
        <span class="sel-label">School</span>
        <select id="f-school" class="sel" aria-label="School"></select>
        <span class="sel-label">Industry</span>
        <select id="f-industry" class="sel" aria-label="Post-MBA industry"></select>
        <span class="sel-label">Program</span>
        <select id="f-program" class="sel" aria-label="Program type"></select>
        <span class="sel-label">GPA</span>
        <div class="gpa-filter">
          <input type="range" id="f-gpa-min" min="2.0" max="4.0" step="0.1" value="2.0" aria-label="Min GPA" />
          <span class="gpa-val" id="gpa-min-lbl">2.0</span>
          <span class="sel-label">–</span>
          <input type="range" id="f-gpa-max" min="2.0" max="4.0" step="0.1" value="4.0" aria-label="Max GPA" />
          <span class="gpa-val" id="gpa-max-lbl">4.0</span>
        </div>
        <button type="button" class="btn-reset" id="btn-reset">Reset</button>
        <button type="button" class="btn-dark" id="btn-dark" aria-label="Toggle dark mode" title="Toggle dark mode">🌙</button>
      </div>
    </div>
  </header>
  <nav class="tabs" role="tablist" aria-label="Dashboard sections">
    <button type="button" class="active" role="tab" aria-selected="true" data-tab="t1">Overview</button>
    <button type="button" role="tab" aria-selected="false" data-tab="t2">Offer mix</button>
    <button type="button" role="tab" aria-selected="false" data-tab="t3">School bench</button>
    <button type="button" role="tab" aria-selected="false" data-tab="t4">Analysis</button>
    <button type="button" role="tab" aria-selected="false" data-tab="t5">Directory</button>
  </nav>
  <div class="dashboard-body">
    <section id="t1" class="tab-panel active" role="tabpanel">
      <div class="tab-scroll">
        <div class="kpi-strip" id="kpi-strip"></div>
        <div class="panel-grid">
          <div class="panel accent-left col-6">
            <div class="panel-head">
              <div>
                <div class="panel-title">Post-MBA industry</div>
                <div class="panel-sub">Where graduates land</div>
              </div>
              <span class="panel-tag">mix</span>
            </div>
            <div class="chart-box"><canvas id="chart-industry"></canvas></div>
          </div>
          <div class="panel col-6">
            <div class="panel-head">
              <div>
                <div class="panel-title">School distribution</div>
                <div class="panel-sub">Share of filtered cohort</div>
              </div>
              <span class="panel-tag">%</span>
            </div>
            <div class="chart-box short"><canvas id="chart-school"></canvas></div>
          </div>
          <div class="panel col-6">
            <div class="panel-head">
              <div>
                <div class="panel-title">Graduation year</div>
                <div class="panel-sub">Headcount by year</div>
              </div>
              <span class="panel-tag">time</span>
            </div>
            <div class="chart-box"><canvas id="chart-year"></canvas></div>
          </div>
          <div class="panel accent-left col-6">
            <div class="panel-head">
              <div>
                <div class="panel-title">GPA vs post-MBA salary</div>
                <div class="panel-sub">Filtered sample (max 400 pts)</div>
              </div>
              <span class="panel-tag">scatter</span>
            </div>
            <div class="chart-box"><canvas id="chart-scatter"></canvas></div>
          </div>
        </div>
      </div>
    </section>
    <section id="t2" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel-grid">
          <div class="panel col-12">
            <div class="panel-head">
              <div>
                <div class="panel-title">Flagged offers</div>
                <div class="panel-sub">Share answering "Yes" for Big Tech, Consulting, and Big Banks</div>
              </div>
              <span class="panel-tag">rates</span>
            </div>
            <div class="chart-box"><canvas id="chart-offers"></canvas></div>
          </div>
          <div class="panel col-12">
            <div class="panel-head">
              <div>
                <div class="panel-title">Internship pathway</div>
                <div class="panel-sub">Internship completed vs not (filtered)</div>
              </div>
              <span class="panel-tag">intern</span>
            </div>
            <div class="chart-box short"><canvas id="chart-intern"></canvas></div>
          </div>
        </div>
      </div>
    </section>
    <section id="t3" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel-grid">
          <div class="panel accent-left col-6">
            <div class="panel-head">
              <div>
                <div class="panel-title">Avg post-MBA salary by school</div>
                <div class="panel-sub">Mean compensation</div>
              </div>
              <span class="panel-tag">$</span>
            </div>
            <div class="chart-box"><canvas id="chart-sal-school"></canvas></div>
          </div>
          <div class="panel col-6">
            <div class="panel-head">
              <div>
                <div class="panel-title">Avg GMAT by school</div>
                <div class="panel-sub">Admissions signal</div>
              </div>
              <span class="panel-tag">exam</span>
            </div>
            <div class="chart-box"><canvas id="chart-gmat-school"></canvas></div>
          </div>
          <div class="panel col-12">
            <div class="panel-head">
              <div>
                <div class="panel-title">Snapshot</div>
                <div class="panel-sub">Filtered cohort (same filters as header)</div>
              </div>
            </div>
            <div class="snapshot-grid" id="bench-snap"></div>
          </div>
        </div>
      </div>
    </section>
    <section id="t4" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel-grid">
          <div class="panel col-12">
            <div class="panel-head">
              <div>
                <div class="panel-title">Salary distribution</div>
                <div class="panel-sub">Histogram of post-MBA compensation (filtered cohort)</div>
              </div>
              <span class="panel-tag">histogram</span>
            </div>
            <div class="chart-box tall"><canvas id="chart-sal-hist"></canvas></div>
          </div>
          <div class="panel accent-left col-12">
            <div class="panel-head">
              <div>
                <div class="panel-title">Job function breakdown</div>
                <div class="panel-sub">Headcount by post-MBA function</div>
              </div>
              <span class="panel-tag">function</span>
            </div>
            <div class="chart-box tall"><canvas id="chart-function"></canvas></div>
          </div>
        </div>
      </div>
    </section>
    <section id="t5" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel col-12" style="margin-bottom:10px">
          <div class="search-bar">
            <input type="search" id="table-search" placeholder="Search name, school, industry, location, function…" autocomplete="off" />
            <span class="panel-tag" id="table-count"></span>
            <button type="button" class="btn-export" id="btn-export">⬇ Export CSV</button>
          </div>
          <div class="tier-legend">
            <span><span class="tier-dot" style="background:#d04a02"></span>Top 10% salary</span>
            <span><span class="tier-dot" style="background:#1a7f5c"></span>Top 11–25% salary</span>
          </div>
          <div class="table-wrap">
            <table class="data" id="data-table">
              <thead><tr id="data-thead"></tr></thead>
              <tbody id="data-tbody"></tbody>
            </table>
          </div>
          <div class="pager">
            <span id="page-info"></span>
            <button type="button" id="page-prev">Prev</button>
            <button type="button" id="page-next">Next</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</div>
<script>
window.__MBA_DATA = {payload};
(function () {{
  const DATA = window.__MBA_DATA;
  const COLORS = {{
    primary: '#d04a02',
    secondary: '#c0392b',
    navy: '#2b2b2b',
    teal: '#1580b0',
    green: '#1a7f5c',
    muted: ['#d04a02','#c0392b','#1580b0','#2b2b2b','#5c6bc0','#1a7f5c','#707070'],
  }};
  let charts = {{}};
  const PAGE_SIZE = 40;
  let page = 0;
  let tableRows = [];

  // ── Dark mode ────────────────────────────────────────────────────────────────
  const htmlEl = document.documentElement;
  const btnDark = document.getElementById('btn-dark');
  (function () {{
    const saved = localStorage.getItem('mba-theme');
    if (saved) {{ htmlEl.setAttribute('data-theme', saved); btnDark.textContent = saved === 'dark' ? '☀️' : '🌙'; }}
  }})();
  btnDark.addEventListener('click', () => {{
    const next = htmlEl.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    htmlEl.setAttribute('data-theme', next);
    btnDark.textContent = next === 'dark' ? '☀️' : '🌙';
    localStorage.setItem('mba-theme', next);
  }});

  // ── GPA sliders ──────────────────────────────────────────────────────────────
  const gpaMinEl  = document.getElementById('f-gpa-min');
  const gpaMaxEl  = document.getElementById('f-gpa-max');
  const gpaMinLbl = document.getElementById('gpa-min-lbl');
  const gpaMaxLbl = document.getElementById('gpa-max-lbl');

  function syncGPA() {{
    let mn = parseFloat(gpaMinEl.value);
    let mx = parseFloat(gpaMaxEl.value);
    if (mn > mx) {{ const t = mn; mn = mx; mx = t; gpaMinEl.value = mn; gpaMaxEl.value = mx; }}
    gpaMinLbl.textContent = mn.toFixed(1);
    gpaMaxLbl.textContent = mx.toFixed(1);
  }}

  // ── Helpers ──────────────────────────────────────────────────────────────────
  function uniq(col) {{
    const s = new Set();
    DATA.forEach(r => {{ if (r[col] != null && r[col] !== '') s.add(String(r[col])); }});
    return Array.from(s).sort();
  }}

  function fillSelect(el, values) {{
    el.innerHTML = '<option value="all">All</option>' +
      values.map(v => '<option value="' + String(v).replace(/"/g, '&quot;') + '">' + v + '</option>').join('');
  }}

  function initFilters() {{
    fillSelect(document.getElementById('f-year'),     uniq('Graduation Year').sort((a,b)=>Number(a)-Number(b)));
    fillSelect(document.getElementById('f-school'),   uniq('School'));
    fillSelect(document.getElementById('f-industry'), uniq('Post-MBA Industry'));
    fillSelect(document.getElementById('f-program'),  uniq('Program Type'));
    const gpas = DATA.map(r => Number(r['GPA'])).filter(x => isFinite(x));
    const gMin = (Math.floor(Math.min(...gpas) * 10) / 10).toFixed(1);
    const gMax = (Math.ceil(Math.max(...gpas)  * 10) / 10).toFixed(1);
    gpaMinEl.min = gMin; gpaMinEl.max = gMax; gpaMinEl.value = gMin;
    gpaMaxEl.min = gMin; gpaMaxEl.max = gMax; gpaMaxEl.value = gMax;
    syncGPA();
  }}

  function filtered() {{
    const y    = document.getElementById('f-year').value;
    const s    = document.getElementById('f-school').value;
    const ind  = document.getElementById('f-industry').value;
    const p    = document.getElementById('f-program').value;
    const gMin = parseFloat(gpaMinEl.value);
    const gMax = parseFloat(gpaMaxEl.value);
    return DATA.filter(r => {{
      if (y   !== 'all' && String(r['Graduation Year'])  !== y)   return false;
      if (s   !== 'all' && r['School']                  !== s)   return false;
      if (ind !== 'all' && r['Post-MBA Industry']        !== ind) return false;
      if (p   !== 'all' && r['Program Type']             !== p)   return false;
      const g = Number(r['GPA']);
      if (isFinite(g) && (g < gMin || g > gMax)) return false;
      return true;
    }});
  }}

  function fmtMoney(n) {{
    if (n == null || n === '') return '—';
    const x = Number(n);
    if (!isFinite(x)) return '—';
    return '$' + Math.round(x).toLocaleString();
  }}

  function pctYes(rows, col) {{
    if (!rows.length) return 0;
    return Math.round((rows.filter(r => String(r[col]).toLowerCase() === 'yes').length / rows.length) * 1000) / 10;
  }}

  function mean(nums) {{
    const a = nums.filter(x => x != null && isFinite(Number(x))).map(Number);
    if (!a.length) return null;
    return a.reduce((s, x) => s + x, 0) / a.length;
  }}

  function countBy(rows, col) {{
    const m = {{}};
    rows.forEach(r => {{ const k = r[col] == null ? 'Unknown' : String(r[col]); m[k] = (m[k] || 0) + 1; }});
    return m;
  }}

  function destroyChart(id) {{
    if (charts[id]) {{ charts[id].destroy(); delete charts[id]; }}
  }}

  function palette(n) {{
    const base = COLORS.muted;
    return Array.from({{length: n}}, (_, i) => base[i % base.length]);
  }}

  function emptyChart(id, type) {{
    destroyChart(id);
    const el = document.getElementById('chart-' + id);
    charts[id] = new Chart(el, {{
      type: type || 'bar',
      data: {{ labels: ['—'], datasets: [{{ data: [0], backgroundColor: '#e8e8e8' }}] }},
      options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ display: false }}, y: {{ display: false }} }} }}
    }});
  }}

  // ── KPI strip ────────────────────────────────────────────────────────────────
  function renderKPI(rows) {{
    const avgSal = mean(rows.map(r => r['Post-MBA Salary']));
    const avgG   = mean(rows.map(r => r['GMAT']));
    const pTech  = pctYes(rows, 'Offer in Big Tech');
    document.getElementById('kpi-strip').innerHTML =
      kpiCard('Profiles',          rows.length.toLocaleString(), 'in filtered cohort') +
      kpiCard('Avg post-MBA salary', avgSal != null ? fmtMoney(avgSal) : '—', 'mean compensation') +
      kpiCard('Avg GMAT',           avgG   != null ? Math.round(avgG)  : '—', 'exam score') +
      kpiCard('Big Tech offer',     pTech + '%', 'share answering Yes');
  }}

  function kpiCard(label, val, sub) {{
    return '<div class="kpi"><div class="klabel">' + label + '</div><div class="kval">' + val + '</div><div class="ksub">' + sub + '</div></div>';
  }}

  // ── Overview charts ──────────────────────────────────────────────────────────
  function renderOverviewCharts(rows) {{
    ['industry','school','year','scatter'].forEach(id => destroyChart(id));
    if (!rows.length) {{
      ['industry','year'].forEach(id => emptyChart(id, 'bar'));
      emptyChart('school', 'doughnut');
      emptyChart('scatter', 'scatter');
      return;
    }}
    const byInd = countBy(rows, 'Post-MBA Industry');
    const labI  = Object.keys(byInd).sort((a,b) => byInd[b]-byInd[a]);
    charts.industry = new Chart(document.getElementById('chart-industry'), {{
      type: 'bar',
      data: {{ labels: labI, datasets: [{{ label: 'Count', data: labI.map(k=>byInd[k]), backgroundColor: palette(labI.length), borderWidth: 0 }}] }},
      options: {{ indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ display:false }} }}, scales:{{ x:{{ ticks:{{ color:'#707070' }}, grid:{{ color:'rgba(43,43,43,0.08)' }} }}, y:{{ ticks:{{ color:var_cream() }}, grid:{{ display:false }} }} }} }}
    }});
    const bySch = countBy(rows, 'School');
    const labS  = Object.keys(bySch);
    charts.school = new Chart(document.getElementById('chart-school'), {{
      type: 'doughnut',
      data: {{ labels: labS, datasets: [{{ data: labS.map(k=>bySch[k]), backgroundColor: palette(labS.length), borderWidth:1, borderColor:'#fff' }}] }},
      options: {{ responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ position:'right', labels:{{ color:var_cream(), boxWidth:12 }} }} }} }}
    }});
    const byY  = countBy(rows, 'Graduation Year');
    const labY = Object.keys(byY).sort((a,b)=>Number(a)-Number(b));
    charts.year = new Chart(document.getElementById('chart-year'), {{
      type: 'bar',
      data: {{ labels: labY, datasets: [{{ label:'Headcount', data:labY.map(k=>byY[k]), backgroundColor:'rgba(208,74,2,0.55)', borderColor:'#d04a02', borderWidth:1 }}] }},
      options: {{ responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ display:false }} }}, scales:{{ y:{{ beginAtZero:true, ticks:{{ color:'#707070' }}, grid:{{ color:'rgba(43,43,43,0.08)' }} }}, x:{{ ticks:{{ color:var_cream() }}, grid:{{ display:false }} }} }} }}
    }});
    const sample = rows.filter(r => r['GPA'] != null && r['Post-MBA Salary'] != null).slice(0, 400);
    charts.scatter = new Chart(document.getElementById('chart-scatter'), {{
      type: 'scatter',
      data: {{ datasets: [{{ label:'Candidates', data:sample.map(r=>({{ x:Number(r['GPA']), y:Number(r['Post-MBA Salary']) }})), backgroundColor:'rgba(192,57,43,0.35)', borderColor:'#c0392b', pointRadius:3, pointHoverRadius:5 }}] }},
      options: {{ responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ display:false }} }}, scales:{{ x:{{ title:{{ display:true, text:'GPA', color:'#707070' }}, ticks:{{ color:'#707070' }}, grid:{{ color:'rgba(43,43,43,0.08)' }} }}, y:{{ title:{{ display:true, text:'Salary', color:'#707070' }}, ticks:{{ callback:v=>'$'+Number(v)/1000+'k', color:'#707070' }}, grid:{{ color:'rgba(43,43,43,0.08)' }} }} }} }}
    }});
  }}

  // ── Offer charts ─────────────────────────────────────────────────────────────
  function renderOfferCharts(rows) {{
    ['offers','intern'].forEach(id => destroyChart(id));
    if (!rows.length) {{
      emptyChart('offers','bar'); emptyChart('intern','pie'); return;
    }}
    const vals   = ['Offer in Big Tech','Offer in Consulting','Offer in Big Banks'].map(c => pctYes(rows,c));
    charts.offers = new Chart(document.getElementById('chart-offers'), {{
      type: 'bar',
      data: {{ labels:['Big Tech','Consulting','Big Banks'], datasets:[{{ label:'% Yes', data:vals, backgroundColor:['rgba(208,74,2,0.75)','rgba(192,57,43,0.75)','rgba(21,128,176,0.75)'], borderWidth:0 }}] }},
      options: {{ responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ display:false }} }}, scales:{{ y:{{ max:100, beginAtZero:true, ticks:{{ callback:v=>v+'%', color:'#707070' }}, grid:{{ color:'rgba(43,43,43,0.08)' }} }}, x:{{ ticks:{{ color:var_cream() }}, grid:{{ display:false }} }} }} }}
    }});
    const intern = countBy(rows, 'Internship Completed');
    const ik = Object.keys(intern);
    charts.intern = new Chart(document.getElementById('chart-intern'), {{
      type: 'pie',
      data: {{ labels:ik, datasets:[{{ data:ik.map(k=>intern[k]), backgroundColor:['#1580b0','#d04a02','#707070'], borderWidth:1, borderColor:'#fff' }}] }},
      options: {{ responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ position:'right', labels:{{ color:var_cream() }} }} }} }}
    }});
  }}

  // ── School bench ─────────────────────────────────────────────────────────────
  function renderBench(rows) {{
    ['sal-school','gmat-school'].forEach(id => destroyChart(id));
    const snap = document.getElementById('bench-snap');
    if (!rows.length) {{
      snap.innerHTML = '<div class="snap-item"><span class="snap-label">Cohort</span><span class="snap-val">No rows</span></div>';
      emptyChart('sal-school','bar'); emptyChart('gmat-school','bar'); return;
    }}
    const schools = [...new Set(rows.map(r=>r['School']).filter(Boolean))].sort();
    const avgBy = col => Object.fromEntries(schools.map(sch => [sch, mean(rows.filter(r=>r['School']===sch).map(r=>r[col]))]));
    const sal = avgBy('Post-MBA Salary');
    const gm  = avgBy('GMAT');
    charts['sal-school'] = new Chart(document.getElementById('chart-sal-school'), {{
      type:'bar',
      data:{{ labels:schools, datasets:[{{ label:'Avg salary', data:schools.map(s=>sal[s]), backgroundColor:'rgba(34,39,94,0.75)', borderWidth:0 }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ display:false }}, tooltip:{{ callbacks:{{ label:c=>fmtMoney(c.parsed.y) }} }} }}, scales:{{ y:{{ ticks:{{ callback:v=>'$'+Number(v)/1000+'k', color:'#707070' }}, grid:{{ color:'rgba(43,43,43,0.08)' }} }}, x:{{ ticks:{{ color:var_cream() }}, grid:{{ display:false }} }} }} }}
    }});
    charts['gmat-school'] = new Chart(document.getElementById('chart-gmat-school'), {{
      type:'bar',
      data:{{ labels:schools, datasets:[{{ label:'Avg GMAT', data:schools.map(s=>gm[s]), backgroundColor:'rgba(208,74,2,0.55)', borderColor:'#d04a02', borderWidth:1 }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ display:false }} }}, scales:{{ y:{{ beginAtZero:false, ticks:{{ color:'#707070' }}, grid:{{ color:'rgba(43,43,43,0.08)' }} }}, x:{{ ticks:{{ color:var_cream() }}, grid:{{ display:false }} }} }} }}
    }});
    const avgGPA = mean(rows.map(r=>r['GPA']));
    const avgWrk = mean(rows.map(r=>r['Work Experience (Years)']));
    snap.innerHTML =
      '<div class="snap-item"><span class="snap-label">Avg GPA</span><span class="snap-val">' + (avgGPA!=null ? avgGPA.toFixed(2) : '—') + '</span></div>' +
      '<div class="snap-item"><span class="snap-label">Avg work yrs (pre)</span><span class="snap-val">' + (avgWrk!=null ? avgWrk.toFixed(1) : '—') + '</span></div>' +
      '<div class="snap-item"><span class="snap-label">% Big Tech offer</span><span class="snap-val">' + pctYes(rows,'Offer in Big Tech') + '%</span></div>' +
      '<div class="snap-item"><span class="snap-label">% Consulting offer</span><span class="snap-val">' + pctYes(rows,'Offer in Consulting') + '%</span></div>';
  }}

  // ── Analysis tab: histogram + function breakdown ──────────────────────────────
  function renderAnalysis(rows) {{
    ['sal-hist','function'].forEach(id => destroyChart(id));
    // Salary histogram
    const sals = rows.map(r=>Number(r['Post-MBA Salary'])).filter(x=>isFinite(x)&&x>0);
    const BIN_COUNT = 12;
    let histLabels = ['No data'], histData = [0];
    if (sals.length > 1) {{
      const minS = Math.min(...sals), maxS = Math.max(...sals);
      const binW = (maxS - minS) / BIN_COUNT;
      histData   = Array(BIN_COUNT).fill(0);
      histLabels = Array.from({{length: BIN_COUNT}}, (_, i) => {{
        const lo = minS + i * binW;
        return '$' + Math.round(lo/1000) + 'k';
      }});
      sals.forEach(s => {{
        let idx = Math.floor((s - minS) / binW);
        if (idx >= BIN_COUNT) idx = BIN_COUNT - 1;
        histData[idx]++;
      }});
    }}
    charts['sal-hist'] = new Chart(document.getElementById('chart-sal-hist'), {{
      type: 'bar',
      data: {{ labels: histLabels, datasets: [{{ label: 'Candidates', data: histData, backgroundColor: 'rgba(208,74,2,0.65)', borderColor: '#d04a02', borderWidth: 1 }}] }},
      options: {{ responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ display:false }} }}, scales:{{ y:{{ beginAtZero:true, ticks:{{ color:'#707070' }}, grid:{{ color:'rgba(43,43,43,0.08)' }} }}, x:{{ ticks:{{ color:var_cream(), maxRotation:40, minRotation:20 }}, grid:{{ display:false }} }} }} }}
    }});
    // Job function breakdown
    const byFunc = countBy(rows, 'Job Function');
    const labF   = Object.keys(byFunc).sort((a,b)=>byFunc[b]-byFunc[a]);
    if (!labF.length) {{ emptyChart('function','bar'); return; }}
    charts['function'] = new Chart(document.getElementById('chart-function'), {{
      type: 'bar',
      data: {{ labels: labF, datasets: [{{ label:'Count', data:labF.map(k=>byFunc[k]), backgroundColor:palette(labF.length), borderWidth:0 }}] }},
      options: {{ indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{{ legend:{{ display:false }} }}, scales:{{ x:{{ ticks:{{ color:'#707070' }}, grid:{{ color:'rgba(43,43,43,0.08)' }} }}, y:{{ ticks:{{ color:var_cream() }}, grid:{{ display:false }} }} }} }}
    }});
  }}

  // ── Directory table ───────────────────────────────────────────────────────────
  const TABLE_COLS = [
    'Student ID','School','Concentration','GPA','GMAT','Graduation Year','Program Type',
    'Post-MBA Salary','Post-MBA Industry','Job Function','Job Location',
    'Offer in Big Tech','Offer in Consulting','Offer in Big Banks'
  ];

  function salaryTiers(rows) {{
    const sals = rows.map(r=>Number(r['Post-MBA Salary'])).filter(x=>isFinite(x)&&x>0).sort((a,b)=>a-b);
    if (sals.length < 4) return {{ p75: Infinity, p90: Infinity }};
    return {{
      p75: sals[Math.floor(sals.length * 0.75)],
      p90: sals[Math.floor(sals.length * 0.90)],
    }};
  }}

  function renderTable() {{
    const q    = (document.getElementById('table-search').value || '').trim().toLowerCase();
    const rows = filtered().filter(r => !q || TABLE_COLS.some(c => String(r[c]??'').toLowerCase().includes(q)));
    tableRows  = rows;
    const {{ p75, p90 }} = salaryTiers(rows);
    page = Math.min(page, Math.max(0, Math.ceil(rows.length / PAGE_SIZE) - 1));
    document.getElementById('data-thead').innerHTML = TABLE_COLS.map(c => '<th>' + c + '</th>').join('');
    const start = page * PAGE_SIZE;
    document.getElementById('data-tbody').innerHTML = rows.slice(start, start + PAGE_SIZE).map(r => {{
      const sal = Number(r['Post-MBA Salary']);
      const cls = isFinite(sal) ? (sal >= p90 ? 'tier-top10' : sal >= p75 ? 'tier-top25' : '') : '';
      return '<tr class="' + cls + '">' +
        TABLE_COLS.map(c => '<td>' + (c==='Post-MBA Salary' ? fmtMoney(r[c]) : (r[c]==null?'':String(r[c]))) + '</td>').join('') +
        '</tr>';
    }}).join('');
    document.getElementById('table-count').textContent = rows.length.toLocaleString() + ' rows';
    document.getElementById('page-info').textContent   = rows.length ? 'Page '+(page+1)+' of '+Math.ceil(rows.length/PAGE_SIZE) : 'No rows';
    document.getElementById('page-prev').disabled = page <= 0;
    document.getElementById('page-next').disabled = start + PAGE_SIZE >= rows.length;
  }}

  // ── CSV export ────────────────────────────────────────────────────────────────
  document.getElementById('btn-export').addEventListener('click', () => {{
    const q    = (document.getElementById('table-search').value || '').trim().toLowerCase();
    const rows = filtered().filter(r => !q || TABLE_COLS.some(c => String(r[c]??'').toLowerCase().includes(q)));
    const esc  = v => '"' + String(v??'').replace(/"/g,'""') + '"';
    const csv  = [TABLE_COLS.map(esc).join(','), ...rows.map(r => TABLE_COLS.map(c=>esc(r[c])).join(','))].join('\\n');
    const a    = Object.assign(document.createElement('a'), {{ href: URL.createObjectURL(new Blob([csv], {{type:'text/csv'}})), download:'mba_candidates_filtered.csv' }});
    a.click(); URL.revokeObjectURL(a.href);
  }});

  // Helper: read CSS cream color for chart text
  function var_cream() {{
    return getComputedStyle(htmlEl).getPropertyValue('--cream').trim() || '#2b2b2b';
  }}

  // ── Refresh all ──────────────────────────────────────────────────────────────
  function refresh() {{
    const rows = filtered();
    renderKPI(rows);
    renderOverviewCharts(rows);
    renderOfferCharts(rows);
    renderBench(rows);
    renderAnalysis(rows);
    renderTable();
  }}

  // ── Event listeners ──────────────────────────────────────────────────────────
  document.querySelectorAll('nav.tabs button').forEach(btn => {{
    btn.addEventListener('click', () => {{
      document.querySelectorAll('nav.tabs button').forEach(b => {{ b.classList.remove('active'); b.setAttribute('aria-selected','false'); }});
      btn.classList.add('active');
      btn.setAttribute('aria-selected','true');
      const id = btn.getAttribute('data-tab');
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.id === id));
    }});
  }});

  ['f-year','f-school','f-industry','f-program'].forEach(id =>
    document.getElementById(id).addEventListener('change', () => {{ page = 0; refresh(); }})
  );
  [gpaMinEl, gpaMaxEl].forEach(el =>
    el.addEventListener('input', () => {{ syncGPA(); page = 0; refresh(); }})
  );
  document.getElementById('btn-reset').addEventListener('click', () => {{
    ['f-year','f-school','f-industry','f-program'].forEach(id => {{ document.getElementById(id).value = 'all'; }});
    const gpas = DATA.map(r=>Number(r['GPA'])).filter(x=>isFinite(x));
    gpaMinEl.value = (Math.floor(Math.min(...gpas)*10)/10).toFixed(1);
    gpaMaxEl.value = (Math.ceil(Math.max(...gpas)*10)/10).toFixed(1);
    syncGPA(); page = 0; refresh();
  }});
  document.getElementById('table-search').addEventListener('input',  () => {{ page = 0; renderTable(); }});
  document.getElementById('page-prev').addEventListener('click', () => {{ page = Math.max(0, page-1); renderTable(); }});
  document.getElementById('page-next').addEventListener('click', () => {{ page++; renderTable(); }});

  initFilters();
  refresh();
}})();
</script>
</body>
</html>"""

    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
