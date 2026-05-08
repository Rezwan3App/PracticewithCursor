"""One-shot generator: embed MBA Grads.xlsx + pwc-logo.svg into Candidate_Dashboard.html.

Enhancements over base version:
  1.  Dark mode toggle (persisted in localStorage)
  2.  GPA range slider (min/max dual range filter)
  3.  Export CSV button (exports filtered + searched rows)
  4.  Salary histogram (Analysis tab)
  5.  Job function breakdown chart (Analysis tab)
  6.  Top-earner row highlighting (top 10% / top 25%)
  7.  Refreshed color palette — indigo/violet primary, sky-blue accent, emerald green
  8.  Modern UI — pill tabs, glassmorphism header, refined shadows, improved typography
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

BASE     = Path(__file__).resolve().parent
XLSX     = BASE / "MBA Grads.xlsx"
SVG_PATH = BASE / "pwc-logo.svg"
OUT      = BASE / "Candidate_Dashboard.html"


def load_svg_inline() -> str:
    raw = SVG_PATH.read_text(encoding="utf-8")
    if raw.strip().startswith("<?xml"):
        raw = raw.split(">", 1)[1].strip()
    return raw


def main() -> None:
    df   = pd.read_excel(XLSX, "Offers")
    rows = df.replace({float("nan"): None}).to_dict(orient="records")
    payload = json.dumps(rows, default=str, separators=(",", ":"))
    svg = load_svg_inline()

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Candidate Profiler · MBA Offers</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  /* ── Design tokens ──────────────────────────────────────────────────────── */
  :root {{
    --radius:     18px;
    --radius-sm:  10px;
    --chart-h:    clamp(120px, 17vh, 210px);
    --chart-short:clamp(90px,  12vh, 140px);
    --chart-tall: clamp(160px, 24vh, 290px);

    /* palette */
    --indigo:     #6366f1;
    --indigo-dark:#4f46e5;
    --violet:     #8b5cf6;
    --sky:        #0ea5e9;
    --emerald:    #10b981;
    --amber:      #f59e0b;
    --rose:       #f43f5e;

    /* light-mode surfaces */
    --bg:         #f1f5f9;
    --surface:    #ffffff;
    --surface-2:  #f8fafc;
    --border:     rgba(100,116,139,0.14);
    --border-2:   rgba(100,116,139,0.22);
    --ink:        #0f172a;
    --ink-2:      #334155;
    --muted:      #64748b;
    --muted-2:    #94a3b8;

    /* header */
    --hdr-from:   #1e1b4b;
    --hdr-mid:    #312e81;
    --hdr-to:     #1e1b4b;
    --hdr-text:   #f1f5f9;
    --hdr-sub:    rgba(241,245,249,0.7);

    /* kpi strip */
    --kpi-from:   #1e1b4b;
    --kpi-to:     #4c1d95;

    /* tabs */
    --tab-bg:     rgba(255,255,255,0.95);
    --tab-active: #ffffff;
    --tab-text:   #64748b;
    --tab-active-text: #1e1b4b;

    /* shadows */
    --shadow-sm:  0 1px 3px rgba(15,23,42,0.06), 0 1px 2px rgba(15,23,42,0.04);
    --shadow-md:  0 4px 16px rgba(15,23,42,0.08), 0 1px 4px rgba(15,23,42,0.05);
    --shadow-lg:  0 8px 32px rgba(15,23,42,0.10), 0 2px 8px rgba(15,23,42,0.06);

    /* misc */
    --snap-bg:    #ede9fe;
    --pager-bg:   #ffffff;
    --search-bg:  #ffffff;
    --tbl-bg:     #ffffff;
    --tbl-hd-bg:  linear-gradient(180deg,#f8fafc 0%,#f1f5f9 100%);
    --tbl-hover:  rgba(99,102,241,0.05);
    --tier-orange-bg: rgba(99,102,241,0.08);
    --tier-green-bg:  rgba(16,185,129,0.07);
  }}

  html[data-theme="dark"] {{
    --bg:         #0b0f1a;
    --surface:    #141928;
    --surface-2:  #1a2035;
    --border:     rgba(255,255,255,0.07);
    --border-2:   rgba(255,255,255,0.12);
    --ink:        #e2e8f0;
    --ink-2:      #94a3b8;
    --muted:      #64748b;
    --muted-2:    #475569;

    --hdr-from:   #0d0b1f;
    --hdr-mid:    #1a1740;
    --hdr-to:     #0d0b1f;

    --kpi-from:   #0d0b1f;
    --kpi-to:     #2e1065;

    --tab-bg:     rgba(20,25,40,0.97);
    --tab-active: #1a2035;
    --tab-text:   #64748b;
    --tab-active-text: #c7d2fe;

    --shadow-sm:  0 1px 3px rgba(0,0,0,0.3);
    --shadow-md:  0 4px 16px rgba(0,0,0,0.4);
    --shadow-lg:  0 8px 32px rgba(0,0,0,0.5);

    --snap-bg:    rgba(99,102,241,0.12);
    --pager-bg:   #1a2035;
    --search-bg:  #141928;
    --tbl-bg:     #141928;
    --tbl-hd-bg:  linear-gradient(180deg,#1a2035 0%,#141928 100%);
    --tbl-hover:  rgba(99,102,241,0.10);
    --tier-orange-bg: rgba(99,102,241,0.14);
    --tier-green-bg:  rgba(16,185,129,0.10);
  }}

  /* ── Reset / base ───────────────────────────────────────────────────────── */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    height: 100%;
    overflow: hidden;
    background: var(--bg);
    color: var(--ink);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 13px;
    -webkit-font-smoothing: antialiased;
    transition: background 0.3s, color 0.3s;
  }}
  body {{
    background:
      radial-gradient(ellipse 900px 500px at 90% -5%,  rgba(99,102,241,0.12) 0%, transparent 55%),
      radial-gradient(ellipse 700px 400px at -5% 100%, rgba(139,92,246,0.09) 0%, transparent 50%),
      var(--bg);
  }}
  html[data-theme="dark"] body {{
    background:
      radial-gradient(ellipse 900px 500px at 90% -5%,  rgba(99,102,241,0.08) 0%, transparent 55%),
      radial-gradient(ellipse 700px 400px at -5% 100%, rgba(139,92,246,0.07) 0%, transparent 50%),
      var(--bg);
  }}

  /* ── Shell ──────────────────────────────────────────────────────────────── */
  .shell {{
    max-width: 1680px;
    margin: 0 auto;
    padding: 12px 22px 10px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .dashboard-body {{ flex: 1; min-height: 0; position: relative; }}

  /* ── Header ─────────────────────────────────────────────────────────────── */
  header.top {{
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    gap: 16px;
    padding: 12px 18px 14px;
    margin: 0 -4px 8px;
    background: linear-gradient(135deg, var(--hdr-from) 0%, var(--hdr-mid) 50%, var(--hdr-to) 100%);
    border-radius: 0 0 var(--radius) var(--radius);
    border: 1px solid rgba(255,255,255,0.06);
    border-top: none;
    box-shadow: var(--shadow-lg), 0 0 0 1px rgba(99,102,241,0.2);
    backdrop-filter: blur(20px);
    flex-shrink: 0;
    color: var(--hdr-text);
  }}
  .brand-row {{ display: flex; align-items: center; gap: 14px; margin-bottom: 6px; }}
  .logo-wrap {{
    width: 46px; height: 46px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    padding: 7px;
    backdrop-filter: blur(8px);
    flex-shrink: 0;
  }}
  .logo-wrap svg {{ width: 100%; height: auto; max-height: 30px; }}
  .crumb {{
    font-size: 10px; letter-spacing: 0.16em; text-transform: uppercase;
    color: rgba(199,210,254,0.7); font-weight: 600;
    margin-bottom: 4px;
  }}
  h1.title {{
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: clamp(1.15rem, 2vw, 1.6rem);
    line-height: 1.15;
    letter-spacing: -0.03em;
    color: #ffffff;
  }}
  h1.title em {{ font-style: normal; color: #a5b4fc; }}
  .subtitle {{
    margin-top: 4px;
    font-size: 11px;
    color: var(--hdr-sub);
    max-width: 48rem;
    line-height: 1.5;
  }}

  /* ── Filter controls ────────────────────────────────────────────────────── */
  .ctrl-cluster {{ display: flex; flex-direction: column; align-items: flex-end; gap: 8px; }}
  .filter-row {{ display: flex; flex-wrap: wrap; gap: 7px; align-items: center; justify-content: flex-end; }}
  .sel-label {{ font-size: 9.5px; color: rgba(199,210,254,0.65); letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600; }}
  .sel {{
    background: rgba(255,255,255,0.10);
    color: #e2e8f0;
    border: 1px solid rgba(255,255,255,0.18);
    padding: 6px 26px 6px 10px;
    font-size: 11.5px;
    border-radius: 8px;
    font-family: inherit;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath fill='%23a5b4fc' d='M5 6L0 0h10z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 9px center;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    backdrop-filter: blur(8px);
  }}
  .sel option {{ background: #1e1b4b; color: #e2e8f0; }}
  .sel:hover {{ border-color: rgba(165,180,252,0.5); background: rgba(255,255,255,0.15); }}
  .gpa-filter {{ display: flex; align-items: center; gap: 5px; }}
  .gpa-filter input[type=range] {{ width: 66px; accent-color: #a5b4fc; cursor: pointer; }}
  .gpa-val {{
    font-size: 10.5px; color: #c7d2fe;
    font-family: 'JetBrains Mono', monospace;
    min-width: 26px; text-align: center;
  }}
  .btn {{
    border: 0; border-radius: 8px; cursor: pointer;
    font-family: inherit; font-weight: 600;
    font-size: 11px; letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: filter 0.2s, transform 0.15s;
    padding: 6px 14px;
  }}
  .btn:hover {{ filter: brightness(1.1); transform: translateY(-1px); }}
  .btn:active {{ transform: translateY(0); }}
  .btn-reset  {{ background: var(--rose);    color: #fff; }}
  .btn-dark   {{
    background: rgba(255,255,255,0.12);
    color: #fff; border: 1px solid rgba(255,255,255,0.22);
    font-size: 13px; letter-spacing: 0; text-transform: none;
    padding: 5px 10px;
    backdrop-filter: blur(8px);
  }}
  .btn-export {{ background: var(--emerald); color: #fff; }}

  /* ── Tabs ───────────────────────────────────────────────────────────────── */
  nav.tabs {{
    display: flex;
    gap: 3px;
    padding: 5px;
    margin: 0 0 8px;
    background: var(--tab-bg);
    border: 1px solid var(--border-2);
    border-radius: 14px;
    overflow-x: auto;
    flex-shrink: 0;
    box-shadow: var(--shadow-sm);
    scrollbar-width: none;
    transition: background 0.3s;
  }}
  nav.tabs::-webkit-scrollbar {{ display: none; }}
  nav.tabs button {{
    background: transparent;
    border: 0;
    color: var(--tab-text);
    padding: 8px 18px;
    font-size: 12px;
    font-weight: 600;
    font-family: 'Manrope', sans-serif;
    letter-spacing: 0.02em;
    cursor: pointer;
    white-space: nowrap;
    border-radius: 10px;
    transition: color 0.2s, background 0.2s;
  }}
  nav.tabs button:hover {{ color: var(--tab-active-text); background: rgba(99,102,241,0.06); }}
  nav.tabs button.active {{
    color: var(--tab-active-text);
    background: var(--tab-active);
    box-shadow: var(--shadow-sm);
  }}
  html[data-theme="dark"] nav.tabs button.active {{ background: var(--tab-active); }}

  /* ── Tab panels ─────────────────────────────────────────────────────────── */
  .tab-panel {{
    display: none; position: absolute; inset: 0;
    overflow: hidden; flex-direction: column;
  }}
  .tab-panel.active {{ display: flex; animation: fade 0.2s ease; }}
  .tab-scroll {{
    flex: 1; min-height: 0; overflow: auto;
    padding: 0 4px 10px;
    scrollbar-width: thin;
    scrollbar-color: rgba(99,102,241,0.4) transparent;
  }}
  @keyframes fade {{ from {{ opacity:0; transform:translateY(5px); }} to {{ opacity:1; transform:none; }} }}

  /* ── KPI strip ──────────────────────────────────────────────────────────── */
  .kpi-strip {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    margin-bottom: 10px;
    background: linear-gradient(135deg, var(--kpi-from) 0%, var(--kpi-to) 100%);
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid rgba(165,180,252,0.15);
    box-shadow: var(--shadow-lg), 0 0 0 1px rgba(99,102,241,0.15);
    color: #f1f5f9;
  }}
  @media (max-width:900px) {{ .kpi-strip {{ grid-template-columns:repeat(2,1fr); }} }}
  .kpi {{
    padding: 12px 16px;
    border-right: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
  }}
  .kpi::before {{
    content:''; position:absolute; inset:0;
    background: radial-gradient(circle at 0% 50%, rgba(165,180,252,0.05), transparent 70%);
  }}
  .kpi:last-child {{ border-right: 0; }}
  .klabel {{
    font-size: 9.5px; letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(199,210,254,0.65); font-weight: 700;
    margin-bottom: 8px;
  }}
  .kval {{
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: clamp(1.25rem, 2.2vw, 1.7rem);
    color: #ffffff;
    letter-spacing: -0.03em;
    line-height: 1;
  }}
  .ksub {{
    font-size: 10.5px; color: rgba(199,210,254,0.55);
    margin-top: 6px;
  }}

  /* ── Panel grid ─────────────────────────────────────────────────────────── */
  .panel-grid {{
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 10px;
    margin-bottom: 10px;
  }}
  .panel {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 14px;
    box-shadow: var(--shadow-md);
    transition: background 0.3s, border-color 0.3s;
  }}
  .panel.accent {{
    border-left: 3px solid var(--indigo);
  }}
  .panel-head {{
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 10px; padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }}
  .panel-title {{
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    font-size: clamp(0.88rem, 1.1vw, 1rem);
    color: var(--ink);
    letter-spacing: -0.01em;
  }}
  .panel-sub {{
    font-size: 10px; color: var(--muted);
    margin-top: 2px; letter-spacing: 0.06em; text-transform: uppercase;
    font-weight: 500;
  }}
  .panel-tag {{
    font-size: 9px; padding: 3px 8px; border-radius: 20px;
    background: rgba(99,102,241,0.10);
    color: var(--indigo);
    border: 1px solid rgba(99,102,241,0.25);
    text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;
  }}
  html[data-theme="dark"] .panel-tag {{
    background: rgba(99,102,241,0.15);
    color: #a5b4fc;
  }}
  .col-6  {{ grid-column: span 6; }}
  .col-12 {{ grid-column: span 12; }}
  @media (max-width:960px) {{ .col-6 {{ grid-column: span 12; }} }}

  /* ── Chart boxes ────────────────────────────────────────────────────────── */
  .chart-box       {{ position:relative; height:var(--chart-h);     min-height:0; }}
  .chart-box.short {{ height:var(--chart-short); max-height:var(--chart-short); }}
  .chart-box.tall  {{ height:var(--chart-tall); }}

  /* ── Search / table ─────────────────────────────────────────────────────── */
  .search-bar {{
    display: flex; gap: 8px; align-items: center;
    flex-wrap: wrap; margin-bottom: 8px;
  }}
  .search-bar input {{
    flex: 1; min-width: 200px;
    padding: 9px 14px;
    border: 1px solid var(--border-2);
    border-radius: 10px;
    font-family: inherit; font-size: 13px;
    background: var(--search-bg); color: var(--ink);
    transition: all 0.2s;
    box-shadow: var(--shadow-sm);
  }}
  .search-bar input:focus {{
    outline: none;
    border-color: var(--indigo);
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12);
  }}
  .tier-legend {{
    display: flex; gap: 14px; font-size: 11px;
    color: var(--muted); margin-bottom: 8px; align-items: center;
  }}
  .tier-dot {{
    display: inline-block; width: 10px; height: 10px;
    border-radius: 3px; margin-right: 4px; vertical-align: middle;
  }}
  .table-wrap {{
    border: 1px solid var(--border-2);
    border-radius: var(--radius-sm);
    overflow: auto;
    max-height: min(52vh, 480px);
    background: var(--tbl-bg);
    box-shadow: var(--shadow-md);
    transition: background 0.3s;
  }}
  table.data {{ width:100%; border-collapse:collapse; font-size:11px; }}
  table.data th {{
    position:sticky; top:0;
    background: var(--tbl-hd-bg);
    text-align:left; padding:8px 10px;
    border-bottom:1px solid var(--border-2);
    font-weight:700; color:var(--ink);
    white-space:nowrap; z-index:1;
    font-family:'Manrope',sans-serif; font-size:10.5px; letter-spacing:0.02em;
  }}
  table.data td {{
    padding:7px 10px;
    border-bottom:1px solid var(--border);
    vertical-align:top; color:var(--ink-2);
  }}
  table.data tr:hover td {{ background: var(--tbl-hover) !important; }}
  table.data tr.tier-top10 td {{
    background: var(--tier-orange-bg);
    border-left: 3px solid var(--indigo);
  }}
  table.data tr.tier-top25 td {{
    background: var(--tier-green-bg);
    border-left: 3px solid var(--emerald);
  }}
  .pager {{
    display:flex; gap:10px; align-items:center;
    justify-content:flex-end; margin-top:10px;
    font-size:12px; color:var(--muted);
  }}
  .pager button {{
    background:var(--pager-bg); border:1px solid var(--border-2);
    padding:6px 14px; border-radius:8px; cursor:pointer;
    font-family:inherit; color:var(--ink); font-size:11.5px;
    font-weight:600; transition:all 0.2s;
    box-shadow:var(--shadow-sm);
  }}
  .pager button:hover:not(:disabled) {{ border-color:var(--indigo); color:var(--indigo); }}
  .pager button:disabled {{ opacity:0.4; cursor:not-allowed; }}

  /* ── Snapshot grid ──────────────────────────────────────────────────────── */
  .snapshot-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
  @media (max-width:700px) {{ .snapshot-grid {{ grid-template-columns:1fr; }} }}
  .snap-item {{
    display:flex; justify-content:space-between; align-items:baseline;
    padding:13px 16px;
    background: var(--snap-bg);
    border-radius: 12px;
    border-left: 3px solid var(--indigo);
    transition: background 0.3s;
  }}
  .snap-label {{ font-size:11px; color:var(--muted); font-weight:500; }}
  .snap-val {{
    font-family:'JetBrains Mono',monospace;
    font-size:14px; color:var(--indigo); font-weight:700;
  }}
  html[data-theme="dark"] .snap-val {{ color:#a5b4fc; }}
</style>
</head>
<body>
<div class="shell">

  <header class="top">
    <div>
      <div class="brand-row">
        <div class="logo-wrap" aria-hidden="true">{svg}</div>
        <div>
          <div class="crumb">People Analytics · MBA Pipeline</div>
          <h1 class="title">Candidate Profiler · <em>MBA Offers</em></h1>
          <p class="subtitle">Interactive view of simulated MBA graduate outcomes — school mix, post-MBA roles, compensation, and offer flags.</p>
        </div>
      </div>
    </div>
    <div class="ctrl-cluster">
      <div class="filter-row">
        <span class="sel-label">Year</span>
        <select id="f-year"     class="sel" aria-label="Graduation year"></select>
        <span class="sel-label">School</span>
        <select id="f-school"   class="sel" aria-label="School"></select>
        <span class="sel-label">Industry</span>
        <select id="f-industry" class="sel" aria-label="Post-MBA industry"></select>
        <span class="sel-label">Program</span>
        <select id="f-program"  class="sel" aria-label="Program type"></select>
        <span class="sel-label">GPA</span>
        <div class="gpa-filter">
          <input type="range" id="f-gpa-min" min="2.0" max="4.0" step="0.1" value="2.0" aria-label="Min GPA" />
          <span class="gpa-val" id="gpa-min-lbl">2.0</span>
          <span class="sel-label">–</span>
          <input type="range" id="f-gpa-max" min="2.0" max="4.0" step="0.1" value="4.0" aria-label="Max GPA" />
          <span class="gpa-val" id="gpa-max-lbl">4.0</span>
        </div>
        <button class="btn btn-reset" id="btn-reset">Reset</button>
        <button class="btn btn-dark"  id="btn-dark"  aria-label="Toggle dark mode" title="Toggle dark mode">🌙</button>
      </div>
    </div>
  </header>

  <nav class="tabs" role="tablist" aria-label="Dashboard sections">
    <button type="button" class="active" role="tab" aria-selected="true"  data-tab="t1">Overview</button>
    <button type="button" role="tab" aria-selected="false" data-tab="t2">Offer Mix</button>
    <button type="button" role="tab" aria-selected="false" data-tab="t3">School Bench</button>
    <button type="button" role="tab" aria-selected="false" data-tab="t4">Analysis</button>
    <button type="button" role="tab" aria-selected="false" data-tab="t5">Directory</button>
  </nav>

  <div class="dashboard-body">

    <!-- Overview -->
    <section id="t1" class="tab-panel active" role="tabpanel">
      <div class="tab-scroll">
        <div class="kpi-strip" id="kpi-strip"></div>
        <div class="panel-grid">
          <div class="panel accent col-6">
            <div class="panel-head">
              <div><div class="panel-title">Post-MBA Industry</div><div class="panel-sub">Where graduates land</div></div>
              <span class="panel-tag">mix</span>
            </div>
            <div class="chart-box"><canvas id="chart-industry"></canvas></div>
          </div>
          <div class="panel col-6">
            <div class="panel-head">
              <div><div class="panel-title">School Distribution</div><div class="panel-sub">Share of filtered cohort</div></div>
              <span class="panel-tag">%</span>
            </div>
            <div class="chart-box short"><canvas id="chart-school"></canvas></div>
          </div>
          <div class="panel col-6">
            <div class="panel-head">
              <div><div class="panel-title">Graduation Year</div><div class="panel-sub">Headcount by year</div></div>
              <span class="panel-tag">time</span>
            </div>
            <div class="chart-box"><canvas id="chart-year"></canvas></div>
          </div>
          <div class="panel accent col-6">
            <div class="panel-head">
              <div><div class="panel-title">GPA vs Post-MBA Salary</div><div class="panel-sub">Filtered sample · max 400 pts</div></div>
              <span class="panel-tag">scatter</span>
            </div>
            <div class="chart-box"><canvas id="chart-scatter"></canvas></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Offer mix -->
    <section id="t2" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel-grid">
          <div class="panel col-12">
            <div class="panel-head">
              <div><div class="panel-title">Flagged Offers</div><div class="panel-sub">% answering Yes — Big Tech · Consulting · Big Banks</div></div>
              <span class="panel-tag">rates</span>
            </div>
            <div class="chart-box"><canvas id="chart-offers"></canvas></div>
          </div>
          <div class="panel col-12">
            <div class="panel-head">
              <div><div class="panel-title">Internship Pathway</div><div class="panel-sub">Completed vs not (filtered cohort)</div></div>
              <span class="panel-tag">intern</span>
            </div>
            <div class="chart-box short"><canvas id="chart-intern"></canvas></div>
          </div>
        </div>
      </div>
    </section>

    <!-- School bench -->
    <section id="t3" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel-grid">
          <div class="panel accent col-6">
            <div class="panel-head">
              <div><div class="panel-title">Avg Post-MBA Salary by School</div><div class="panel-sub">Mean compensation</div></div>
              <span class="panel-tag">$</span>
            </div>
            <div class="chart-box"><canvas id="chart-sal-school"></canvas></div>
          </div>
          <div class="panel col-6">
            <div class="panel-head">
              <div><div class="panel-title">Avg GMAT by School</div><div class="panel-sub">Admissions signal</div></div>
              <span class="panel-tag">exam</span>
            </div>
            <div class="chart-box"><canvas id="chart-gmat-school"></canvas></div>
          </div>
          <div class="panel col-12">
            <div class="panel-head">
              <div><div class="panel-title">Cohort Snapshot</div><div class="panel-sub">Filtered cohort — same filters as header</div></div>
            </div>
            <div class="snapshot-grid" id="bench-snap"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Analysis -->
    <section id="t4" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel-grid">
          <div class="panel col-12">
            <div class="panel-head">
              <div><div class="panel-title">Salary Distribution</div><div class="panel-sub">Histogram of post-MBA compensation · filtered cohort</div></div>
              <span class="panel-tag">histogram</span>
            </div>
            <div class="chart-box tall"><canvas id="chart-sal-hist"></canvas></div>
          </div>
          <div class="panel accent col-12">
            <div class="panel-head">
              <div><div class="panel-title">Job Function Breakdown</div><div class="panel-sub">Headcount by post-MBA function</div></div>
              <span class="panel-tag">function</span>
            </div>
            <div class="chart-box tall"><canvas id="chart-function"></canvas></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Directory -->
    <section id="t5" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel col-12" style="margin-bottom:10px">
          <div class="search-bar">
            <input type="search" id="table-search" placeholder="Search name, school, industry, location, function…" autocomplete="off" />
            <span class="panel-tag" id="table-count"></span>
            <button class="btn btn-export" id="btn-export">⬇ Export CSV</button>
          </div>
          <div class="tier-legend">
            <span><span class="tier-dot" style="background:var(--indigo)"></span>Top 10% salary</span>
            <span><span class="tier-dot" style="background:var(--emerald)"></span>Top 11–25% salary</span>
          </div>
          <div class="table-wrap">
            <table class="data" id="data-table">
              <thead><tr id="data-thead"></tr></thead>
              <tbody id="data-tbody"></tbody>
            </table>
          </div>
          <div class="pager">
            <span id="page-info"></span>
            <button type="button" id="page-prev">← Prev</button>
            <button type="button" id="page-next">Next →</button>
          </div>
        </div>
      </div>
    </section>

  </div>
</div>

<script>
window.__MBA_DATA = {payload};
(function () {{
  const DATA  = window.__MBA_DATA;
  const P = {{
    indigo:  '#6366f1', violet: '#8b5cf6', sky:    '#0ea5e9',
    emerald: '#10b981', amber:  '#f59e0b', rose:   '#f43f5e',
    slate:   '#64748b',
  }};
  const PALETTE = [P.indigo, P.violet, P.sky, P.emerald, P.amber, P.rose, P.slate];

  let charts   = {{}};
  const PAGE_SIZE = 40;
  let page = 0, tableRows = [];

  /* ── Dark mode ──────────────────────────────────────────────────────────── */
  const html   = document.documentElement;
  const btnDrk = document.getElementById('btn-dark');
  (function () {{
    const s = localStorage.getItem('mba-theme');
    if (s) {{ html.setAttribute('data-theme', s); btnDrk.textContent = s === 'dark' ? '☀️' : '🌙'; }}
  }})();
  btnDrk.addEventListener('click', () => {{
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    btnDrk.textContent = next === 'dark' ? '☀️' : '🌙';
    localStorage.setItem('mba-theme', next);
  }});

  /* ── GPA sliders ────────────────────────────────────────────────────────── */
  const gpaMinEl  = document.getElementById('f-gpa-min');
  const gpaMaxEl  = document.getElementById('f-gpa-max');
  const gpaMinLbl = document.getElementById('gpa-min-lbl');
  const gpaMaxLbl = document.getElementById('gpa-max-lbl');
  function syncGPA() {{
    let mn = parseFloat(gpaMinEl.value), mx = parseFloat(gpaMaxEl.value);
    if (mn > mx) {{ const t = mn; mn = mx; mx = t; gpaMinEl.value = mn; gpaMaxEl.value = mx; }}
    gpaMinLbl.textContent = mn.toFixed(1);
    gpaMaxLbl.textContent = mx.toFixed(1);
  }}

  /* ── Helpers ────────────────────────────────────────────────────────────── */
  function uniq(col) {{
    const s = new Set();
    DATA.forEach(r => {{ if (r[col] != null && r[col] !== '') s.add(String(r[col])); }});
    return Array.from(s).sort();
  }}
  function fillSel(el, vals) {{
    el.innerHTML = '<option value="all">All</option>' +
      vals.map(v => '<option value="' + String(v).replace(/"/g,'&quot;') + '">' + v + '</option>').join('');
  }}
  function initFilters() {{
    fillSel(document.getElementById('f-year'),     uniq('Graduation Year').sort((a,b)=>+a- +b));
    fillSel(document.getElementById('f-school'),   uniq('School'));
    fillSel(document.getElementById('f-industry'), uniq('Post-MBA Industry'));
    fillSel(document.getElementById('f-program'),  uniq('Program Type'));
    const gpas = DATA.map(r=>+r['GPA']).filter(x=>isFinite(x));
    const mn = (Math.floor(Math.min(...gpas)*10)/10).toFixed(1);
    const mx = (Math.ceil( Math.max(...gpas)*10)/10).toFixed(1);
    gpaMinEl.min = mn; gpaMinEl.max = mx; gpaMinEl.value = mn;
    gpaMaxEl.min = mn; gpaMaxEl.max = mx; gpaMaxEl.value = mx;
    syncGPA();
  }}
  function filtered() {{
    const y   = document.getElementById('f-year').value;
    const s   = document.getElementById('f-school').value;
    const ind = document.getElementById('f-industry').value;
    const p   = document.getElementById('f-program').value;
    const mn  = parseFloat(gpaMinEl.value), mx = parseFloat(gpaMaxEl.value);
    return DATA.filter(r => {{
      if (y   !== 'all' && String(r['Graduation Year']) !== y)   return false;
      if (s   !== 'all' && r['School']                 !== s)   return false;
      if (ind !== 'all' && r['Post-MBA Industry']       !== ind) return false;
      if (p   !== 'all' && r['Program Type']            !== p)   return false;
      const g = +r['GPA'];
      if (isFinite(g) && (g < mn || g > mx)) return false;
      return true;
    }});
  }}
  function fmtMoney(n) {{
    if (n == null || n === '') return '—';
    const x = +n; if (!isFinite(x)) return '—';
    return '$' + Math.round(x).toLocaleString();
  }}
  function pctYes(rows, col) {{
    if (!rows.length) return 0;
    return Math.round(rows.filter(r=>String(r[col]).toLowerCase()==='yes').length/rows.length*1000)/10;
  }}
  function mean(nums) {{
    const a = nums.filter(x=>x!=null&&isFinite(+x)).map(Number);
    return a.length ? a.reduce((s,x)=>s+x,0)/a.length : null;
  }}
  function countBy(rows, col) {{
    const m = {{}};
    rows.forEach(r=>{{ const k = r[col]==null?'Unknown':String(r[col]); m[k]=(m[k]||0)+1; }});
    return m;
  }}
  function pal(n) {{ return Array.from({{length:n}},(_,i)=>PALETTE[i%PALETTE.length]); }}
  function ink()  {{ return getComputedStyle(html).getPropertyValue('--ink').trim() || '#0f172a'; }}
  function muted(){{ return getComputedStyle(html).getPropertyValue('--muted').trim()||'#64748b'; }}

  function killChart(id) {{ if (charts[id]) {{ charts[id].destroy(); delete charts[id]; }} }}
  function emptyC(id, type) {{
    killChart(id);
    charts[id] = new Chart(document.getElementById('chart-'+id), {{
      type: type||'bar',
      data: {{ labels:['—'], datasets:[{{ data:[0], backgroundColor:'rgba(99,102,241,0.15)' }}] }},
      options: {{ responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}}}, scales:{{x:{{display:false}},y:{{display:false}}}} }}
    }});
  }}

  /* ── KPI ────────────────────────────────────────────────────────────────── */
  function renderKPI(rows) {{
    const avg$ = mean(rows.map(r=>r['Post-MBA Salary']));
    const avgG = mean(rows.map(r=>r['GMAT']));
    const pt   = pctYes(rows,'Offer in Big Tech');
    const card = (l,v,s) => '<div class="kpi"><div class="klabel">'+l+'</div><div class="kval">'+v+'</div><div class="ksub">'+s+'</div></div>';
    document.getElementById('kpi-strip').innerHTML =
      card('Profiles',            rows.length.toLocaleString(),          'in filtered cohort') +
      card('Avg Post-MBA Salary', avg$!=null ? fmtMoney(avg$) : '—',    'mean compensation')  +
      card('Avg GMAT',            avgG!=null ? Math.round(avgG) : '—',   'exam score')         +
      card('Big Tech Offer',      pt+'%',                                 'share answering Yes');
  }}

  /* chart global defaults */
  const GRID = 'rgba(100,116,139,0.10)';
  function axOpts(axis) {{
    return {{ ticks:{{color:muted(),font:{{size:10}}}}, grid:{{color: axis==='x'?'transparent':GRID}} }};
  }}

  /* ── Overview ───────────────────────────────────────────────────────────── */
  function renderOverview(rows) {{
    ['industry','school','year','scatter'].forEach(killChart);
    if (!rows.length) {{
      ['industry','year'].forEach(id=>emptyC(id,'bar'));
      emptyC('school','doughnut'); emptyC('scatter','scatter'); return;
    }}
    const byInd = countBy(rows,'Post-MBA Industry');
    const labI  = Object.keys(byInd).sort((a,b)=>byInd[b]-byInd[a]);
    charts.industry = new Chart(document.getElementById('chart-industry'), {{
      type:'bar',
      data:{{ labels:labI, datasets:[{{ label:'Count', data:labI.map(k=>byInd[k]), backgroundColor:pal(labI.length), borderRadius:4, borderWidth:0 }}] }},
      options:{{ indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}}}, scales:{{ x:{{...axOpts('x'),ticks:{{...axOpts('x').ticks}}}}, y:{{...axOpts('y'),grid:{{display:false}},ticks:{{color:ink(),font:{{size:10}}}}}} }} }}
    }});
    const bySch = countBy(rows,'School'), labS = Object.keys(bySch);
    charts.school = new Chart(document.getElementById('chart-school'), {{
      type:'doughnut',
      data:{{ labels:labS, datasets:[{{ data:labS.map(k=>bySch[k]), backgroundColor:pal(labS.length), borderWidth:2, borderColor:getComputedStyle(html).getPropertyValue('--surface').trim()||'#fff' }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, cutout:'58%', plugins:{{ legend:{{ position:'right', labels:{{color:ink(),font:{{size:10}},boxWidth:10}} }} }} }}
    }});
    const byY = countBy(rows,'Graduation Year'), labY = Object.keys(byY).sort((a,b)=>+a-+b);
    charts.year = new Chart(document.getElementById('chart-year'), {{
      type:'bar',
      data:{{ labels:labY, datasets:[{{ label:'Headcount', data:labY.map(k=>byY[k]), backgroundColor:'rgba(99,102,241,0.55)', borderColor:P.indigo, borderWidth:1, borderRadius:4 }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}}}, scales:{{ y:{{...axOpts('y'),beginAtZero:true}}, x:{{...axOpts('x'),grid:{{display:false}},ticks:{{color:ink(),font:{{size:10}}}}}} }} }}
    }});
    const samp = rows.filter(r=>r['GPA']!=null&&r['Post-MBA Salary']!=null).slice(0,400);
    charts.scatter = new Chart(document.getElementById('chart-scatter'), {{
      type:'scatter',
      data:{{ datasets:[{{ label:'Candidates', data:samp.map(r=>({{x:+r['GPA'],y:+r['Post-MBA Salary']}})), backgroundColor:'rgba(139,92,246,0.3)', borderColor:P.violet, pointRadius:3, pointHoverRadius:5 }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}}},
        scales:{{ x:{{...axOpts('x'),title:{{display:true,text:'GPA',color:muted(),font:{{size:10}}}}}}, y:{{...axOpts('y'),title:{{display:true,text:'Salary',color:muted(),font:{{size:10}}}},ticks:{{callback:v=>'$'+Math.round(+v/1000)+'k',color:muted(),font:{{size:10}}}}}} }} }}
    }});
  }}

  /* ── Offers ─────────────────────────────────────────────────────────────── */
  function renderOffers(rows) {{
    ['offers','intern'].forEach(killChart);
    if (!rows.length) {{ emptyC('offers','bar'); emptyC('intern','pie'); return; }}
    const vals = ['Offer in Big Tech','Offer in Consulting','Offer in Big Banks'].map(c=>pctYes(rows,c));
    charts.offers = new Chart(document.getElementById('chart-offers'), {{
      type:'bar',
      data:{{ labels:['Big Tech','Consulting','Big Banks'], datasets:[{{ label:'% Yes', data:vals, backgroundColor:[P.indigo,P.violet,P.sky], borderRadius:6, borderWidth:0 }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}}},
        scales:{{ y:{{...axOpts('y'),max:100,beginAtZero:true,ticks:{{callback:v=>v+'%',color:muted(),font:{{size:10}}}}}}, x:{{...axOpts('x'),grid:{{display:false}},ticks:{{color:ink(),font:{{size:11}}}}}} }} }}
    }});
    const int2 = countBy(rows,'Internship Completed'), ik = Object.keys(int2);
    charts.intern = new Chart(document.getElementById('chart-intern'), {{
      type:'doughnut',
      data:{{ labels:ik, datasets:[{{ data:ik.map(k=>int2[k]), backgroundColor:[P.sky,P.indigo,P.slate], borderWidth:2, borderColor:getComputedStyle(html).getPropertyValue('--surface').trim()||'#fff' }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, cutout:'52%', plugins:{{ legend:{{ position:'right', labels:{{color:ink(),font:{{size:10}},boxWidth:10}} }} }} }}
    }});
  }}

  /* ── School bench ───────────────────────────────────────────────────────── */
  function renderBench(rows) {{
    ['sal-school','gmat-school'].forEach(killChart);
    const snap = document.getElementById('bench-snap');
    if (!rows.length) {{
      snap.innerHTML = '<div class="snap-item"><span class="snap-label">Cohort</span><span class="snap-val">No rows</span></div>';
      emptyC('sal-school','bar'); emptyC('gmat-school','bar'); return;
    }}
    const schs = [...new Set(rows.map(r=>r['School']).filter(Boolean))].sort();
    const avgBy = col => Object.fromEntries(schs.map(sc=>[sc,mean(rows.filter(r=>r['School']===sc).map(r=>r[col]))]));
    const sal = avgBy('Post-MBA Salary'), gm = avgBy('GMAT');
    charts['sal-school'] = new Chart(document.getElementById('chart-sal-school'), {{
      type:'bar',
      data:{{ labels:schs, datasets:[{{ label:'Avg Salary', data:schs.map(s=>sal[s]), backgroundColor:'rgba(99,102,241,0.65)', borderRadius:4, borderWidth:0 }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>fmtMoney(c.parsed.y)}}}}}},
        scales:{{ y:{{...axOpts('y'),ticks:{{callback:v=>'$'+Math.round(+v/1000)+'k',color:muted(),font:{{size:10}}}}}}, x:{{...axOpts('x'),grid:{{display:false}},ticks:{{color:ink(),font:{{size:10}}}}}} }} }}
    }});
    charts['gmat-school'] = new Chart(document.getElementById('chart-gmat-school'), {{
      type:'bar',
      data:{{ labels:schs, datasets:[{{ label:'Avg GMAT', data:schs.map(s=>gm[s]), backgroundColor:'rgba(139,92,246,0.6)', borderRadius:4, borderWidth:0 }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}}},
        scales:{{ y:{{...axOpts('y'),beginAtZero:false}}, x:{{...axOpts('x'),grid:{{display:false}},ticks:{{color:ink(),font:{{size:10}}}}}} }} }}
    }});
    const avgGPA = mean(rows.map(r=>r['GPA'])), avgW = mean(rows.map(r=>r['Work Experience (Years)']));
    snap.innerHTML =
      snapCard('Avg GPA',           avgGPA!=null?avgGPA.toFixed(2):'—') +
      snapCard('Avg Work Yrs (pre)',avgW  !=null?avgW.toFixed(1)  :'—') +
      snapCard('% Big Tech Offer',  pctYes(rows,'Offer in Big Tech')+'%') +
      snapCard('% Consulting Offer',pctYes(rows,'Offer in Consulting')+'%');
  }}
  function snapCard(l,v) {{
    return '<div class="snap-item"><span class="snap-label">'+l+'</span><span class="snap-val">'+v+'</span></div>';
  }}

  /* ── Analysis ───────────────────────────────────────────────────────────── */
  function renderAnalysis(rows) {{
    ['sal-hist','function'].forEach(killChart);
    const sals = rows.map(r=>+r['Post-MBA Salary']).filter(x=>isFinite(x)&&x>0);
    const N = 12;
    let hLabels = ['No data'], hData = [0];
    if (sals.length > 1) {{
      const lo = Math.min(...sals), hi = Math.max(...sals), bw = (hi-lo)/N;
      hData = Array(N).fill(0);
      hLabels = Array.from({{length:N}},(_,i)=>'$'+Math.round((lo+i*bw)/1000)+'k');
      sals.forEach(s=>{{ let i=Math.floor((s-lo)/bw); if(i>=N)i=N-1; hData[i]++; }});
    }}
    charts['sal-hist'] = new Chart(document.getElementById('chart-sal-hist'), {{
      type:'bar',
      data:{{ labels:hLabels, datasets:[{{ label:'Candidates', data:hData,
        backgroundColor:'rgba(99,102,241,0.55)', borderColor:P.indigo, borderWidth:1, borderRadius:4 }}] }},
      options:{{ responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}}},
        scales:{{ y:{{...axOpts('y'),beginAtZero:true}}, x:{{...axOpts('x'),grid:{{display:false}},ticks:{{color:ink(),font:{{size:10}},maxRotation:40,minRotation:20}}}} }} }}
    }});
    const byF = countBy(rows,'Job Function'), labF = Object.keys(byF).sort((a,b)=>byF[b]-byF[a]);
    if (!labF.length) {{ emptyC('function','bar'); return; }}
    charts['function'] = new Chart(document.getElementById('chart-function'), {{
      type:'bar',
      data:{{ labels:labF, datasets:[{{ label:'Count', data:labF.map(k=>byF[k]), backgroundColor:pal(labF.length), borderRadius:4, borderWidth:0 }}] }},
      options:{{ indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}}},
        scales:{{ x:{{...axOpts('x')}}, y:{{...axOpts('y'),grid:{{display:false}},ticks:{{color:ink(),font:{{size:10}}}}}} }} }}
    }});
  }}

  /* ── Directory ──────────────────────────────────────────────────────────── */
  const COLS = ['Student ID','School','Concentration','GPA','GMAT','Graduation Year','Program Type',
    'Post-MBA Salary','Post-MBA Industry','Job Function','Job Location',
    'Offer in Big Tech','Offer in Consulting','Offer in Big Banks'];

  function tiers(rows) {{
    const s = rows.map(r=>+r['Post-MBA Salary']).filter(x=>isFinite(x)&&x>0).sort((a,b)=>a-b);
    if (s.length < 4) return {{p75:Infinity,p90:Infinity}};
    return {{p75:s[Math.floor(s.length*.75)], p90:s[Math.floor(s.length*.90)]}};
  }}
  function renderTable() {{
    const q = (document.getElementById('table-search').value||'').trim().toLowerCase();
    const rows = filtered().filter(r=>!q||COLS.some(c=>String(r[c]??'').toLowerCase().includes(q)));
    tableRows = rows;
    const {{p75,p90}} = tiers(rows);
    page = Math.min(page, Math.max(0, Math.ceil(rows.length/PAGE_SIZE)-1));
    document.getElementById('data-thead').innerHTML = COLS.map(c=>'<th>'+c+'</th>').join('');
    const st = page*PAGE_SIZE;
    document.getElementById('data-tbody').innerHTML = rows.slice(st,st+PAGE_SIZE).map(r=>{{
      const s = +r['Post-MBA Salary'];
      const cls = isFinite(s)?(s>=p90?'tier-top10':s>=p75?'tier-top25':''):'';
      return '<tr class="'+cls+'">'+COLS.map(c=>'<td>'+(c==='Post-MBA Salary'?fmtMoney(r[c]):(r[c]==null?'':String(r[c])))+'</td>').join('')+'</tr>';
    }}).join('');
    document.getElementById('table-count').textContent = rows.length.toLocaleString()+' rows';
    document.getElementById('page-info').textContent   = rows.length?'Page '+(page+1)+' of '+Math.ceil(rows.length/PAGE_SIZE):'No rows';
    document.getElementById('page-prev').disabled = page<=0;
    document.getElementById('page-next').disabled = st+PAGE_SIZE>=rows.length;
  }}

  /* ── CSV export ─────────────────────────────────────────────────────────── */
  document.getElementById('btn-export').addEventListener('click',()=>{{
    const q = (document.getElementById('table-search').value||'').trim().toLowerCase();
    const rows = filtered().filter(r=>!q||COLS.some(c=>String(r[c]??'').toLowerCase().includes(q)));
    const esc  = v=>'"'+String(v??'').replace(/"/g,'""')+'"';
    const csv  = [COLS.map(esc).join(','),...rows.map(r=>COLS.map(c=>esc(r[c])).join(','))].join('\\n');
    const a = Object.assign(document.createElement('a'),{{href:URL.createObjectURL(new Blob([csv],{{type:'text/csv'}})),download:'mba_candidates_filtered.csv'}});
    a.click(); URL.revokeObjectURL(a.href);
  }});

  /* ── Refresh ────────────────────────────────────────────────────────────── */
  function refresh() {{
    const rows = filtered();
    renderKPI(rows); renderOverview(rows); renderOffers(rows);
    renderBench(rows); renderAnalysis(rows); renderTable();
  }}

  /* ── Events ─────────────────────────────────────────────────────────────── */
  document.querySelectorAll('nav.tabs button').forEach(btn=>{{
    btn.addEventListener('click',()=>{{
      document.querySelectorAll('nav.tabs button').forEach(b=>{{b.classList.remove('active');b.setAttribute('aria-selected','false');}});
      btn.classList.add('active'); btn.setAttribute('aria-selected','true');
      const id = btn.getAttribute('data-tab');
      document.querySelectorAll('.tab-panel').forEach(p=>p.classList.toggle('active',p.id===id));
    }});
  }});
  ['f-year','f-school','f-industry','f-program'].forEach(id=>
    document.getElementById(id).addEventListener('change',()=>{{page=0;refresh();}})
  );
  [gpaMinEl,gpaMaxEl].forEach(el=>el.addEventListener('input',()=>{{syncGPA();page=0;refresh();}}));
  document.getElementById('btn-reset').addEventListener('click',()=>{{
    ['f-year','f-school','f-industry','f-program'].forEach(id=>{{document.getElementById(id).value='all';}});
    const gpas=DATA.map(r=>+r['GPA']).filter(x=>isFinite(x));
    gpaMinEl.value=(Math.floor(Math.min(...gpas)*10)/10).toFixed(1);
    gpaMaxEl.value=(Math.ceil( Math.max(...gpas)*10)/10).toFixed(1);
    syncGPA(); page=0; refresh();
  }});
  document.getElementById('table-search').addEventListener('input',()=>{{page=0;renderTable();}});
  document.getElementById('page-prev').addEventListener('click',()=>{{page=Math.max(0,page-1);renderTable();}});
  document.getElementById('page-next').addEventListener('click',()=>{{page++;renderTable();}});

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
