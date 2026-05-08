"""One-shot generator: embed MBA Grads.xlsx into Candidate_Dashboard.html.

Features:
  A. Click chart bars/slices to instantly filter
  B. Candidate profile modal (click any directory row)
  C. Active filter pills with one-click removal
  D. Regression trend line + R² on GPA vs Salary scatter
  E. Shareable URL (filters encoded in hash)
  F. Animated KPI counters
  G. School comparison tab (side-by-side A vs B)
  H. Print / Save as PDF button
  + Larger fonts, lighter modern design, no dark mode
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
XLSX = BASE / "MBA Grads.xlsx"
OUT  = BASE / "Candidate_Dashboard.html"

LOGO_SVG = """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="40" height="40" rx="10" fill="url(#lg)"/>
  <defs><linearGradient id="lg" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
    <stop stop-color="#6366f1"/><stop offset="1" stop-color="#8b5cf6"/>
  </linearGradient></defs>
  <rect x="7"  y="24" width="6" height="10" rx="2" fill="rgba(255,255,255,0.55)"/>
  <rect x="17" y="16" width="6" height="18" rx="2" fill="rgba(255,255,255,0.80)"/>
  <rect x="27" y="9"  width="6" height="25" rx="2" fill="rgba(255,255,255,1)"/>
</svg>"""


def main() -> None:
    df      = pd.read_excel(XLSX, "Offers")
    rows    = df.replace({float("nan"): None}).to_dict(orient="records")
    payload = json.dumps(rows, default=str, separators=(",", ":"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Grad Analytics · MBA Profiler</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
/* ── Tokens ─────────────────────────────────────────────────────────────── */
:root {{
  --r:      16px;
  --r-sm:   10px;
  --ch:     clamp(130px,18vh,220px);
  --ch-s:   clamp(95px, 13vh,150px);
  --ch-t:   clamp(160px,25vh,300px);

  --indigo:   #6366f1;
  --indigo-d: #4f46e5;
  --violet:   #8b5cf6;
  --sky:      #0ea5e9;
  --emerald:  #10b981;
  --amber:    #f59e0b;
  --rose:     #f43f5e;

  --bg:       #eef2ff;
  --surface:  #ffffff;
  --s2:       #f8fafc;
  --border:   rgba(99,102,241,0.12);
  --border2:  rgba(99,102,241,0.20);
  --ink:      #1e1b4b;
  --ink2:     #3730a3;
  --muted:    #6b7280;
  --muted2:   #9ca3af;

  --hdr1: #4f46e5;
  --hdr2: #7c3aed;

  --sh-s: 0 1px 3px rgba(99,102,241,0.08),0 1px 2px rgba(99,102,241,0.05);
  --sh-m: 0 4px 16px rgba(99,102,241,0.10),0 1px 4px rgba(99,102,241,0.06);
  --sh-l: 0 8px 32px rgba(99,102,241,0.13),0 2px 8px rgba(99,102,241,0.07);
}}

/* ── Reset ───────────────────────────────────────────────────────────────── */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{
  height:100%;overflow:hidden;
  background:var(--bg);color:var(--ink);
  font-family:'Inter',system-ui,sans-serif;
  font-size:14px;line-height:1.5;
  -webkit-font-smoothing:antialiased;
}}
body{{
  background:
    radial-gradient(ellipse 900px 480px at 88% -8%, rgba(99,102,241,0.13) 0%,transparent 55%),
    radial-gradient(ellipse 700px 420px at -4% 102%,rgba(139,92,246,0.10) 0%,transparent 50%),
    var(--bg);
}}

/* ── Shell ───────────────────────────────────────────────────────────────── */
.shell{{
  max-width:1700px;margin:0 auto;
  padding:12px 22px 10px;
  height:100vh;display:flex;flex-direction:column;overflow:hidden;
}}
.dash-body{{flex:1;min-height:0;position:relative;}}

/* ── Header ──────────────────────────────────────────────────────────────── */
header.top{{
  display:grid;grid-template-columns:1fr auto;gap:16px;align-items:center;
  padding:14px 20px 16px;
  margin:0 -4px 6px;
  background:linear-gradient(135deg,var(--hdr1) 0%,var(--hdr2) 100%);
  border-radius:0 0 var(--r) var(--r);
  border:1px solid rgba(255,255,255,0.08);border-top:none;
  box-shadow:var(--sh-l),0 0 0 1px rgba(99,102,241,0.25);
  flex-shrink:0;color:#fff;
}}
.brand{{display:flex;align-items:center;gap:14px;}}
.brand-logo{{
  width:46px;height:46px;flex-shrink:0;border-radius:12px;
  box-shadow:0 4px 14px rgba(0,0,0,0.2);overflow:hidden;
}}
.brand-logo svg,
.brand-logo img{{width:100%;height:100%;display:block;}}
.brand-name{{
  font-family:'Manrope',sans-serif;font-weight:800;
  font-size:clamp(1.1rem,1.8vw,1.55rem);
  letter-spacing:-0.03em;line-height:1.1;color:#fff;
}}
.brand-name em{{font-style:normal;color:#c7d2fe;}}
.brand-sub{{margin-top:4px;font-size:12px;color:rgba(255,255,255,0.68);line-height:1.4;}}

/* ── Filter controls ─────────────────────────────────────────────────────── */
.ctrl{{display:flex;flex-wrap:wrap;gap:7px;align-items:center;justify-content:flex-end;}}
.lbl{{font-size:10px;color:rgba(199,210,254,0.7);letter-spacing:0.12em;text-transform:uppercase;font-weight:700;}}
.sel{{
  background:rgba(255,255,255,0.12);color:#e2e8f0;
  border:1px solid rgba(255,255,255,0.22);
  padding:6px 24px 6px 11px;font-size:12px;border-radius:8px;
  font-family:inherit;appearance:none;cursor:pointer;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath fill='%23a5b4fc' d='M5 6L0 0h10z'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 8px center;
  transition:border-color 0.2s,background 0.2s;
}}
.sel option{{background:#3730a3;color:#e2e8f0;}}
.sel:hover{{border-color:rgba(165,180,252,0.55);background:rgba(255,255,255,0.18);}}
.gpa-wrap{{display:flex;align-items:center;gap:5px;}}
.gpa-wrap input[type=range]{{width:64px;accent-color:#a5b4fc;cursor:pointer;}}
.gpa-lbl{{font-size:11px;color:#c7d2fe;font-family:'JetBrains Mono',monospace;min-width:26px;text-align:center;}}
.btn{{
  border:0;border-radius:8px;cursor:pointer;
  font-family:inherit;font-weight:700;font-size:11.5px;
  letter-spacing:0.04em;text-transform:uppercase;padding:7px 15px;
  transition:filter 0.2s,transform 0.15s;
}}
.btn:hover{{filter:brightness(1.1);transform:translateY(-1px);}}
.btn:active{{transform:translateY(0);}}
.btn-reset  {{background:var(--rose);   color:#fff;}}
.btn-print  {{background:rgba(255,255,255,0.14);color:#fff;border:1px solid rgba(255,255,255,0.25);font-size:13px;text-transform:none;letter-spacing:0;}}
.btn-export {{background:var(--emerald);color:#fff;}}

/* ── Filter pills ────────────────────────────────────────────────────────── */
.filter-pills{{
  display:flex;flex-wrap:wrap;gap:6px;
  padding:0 4px 6px;min-height:0;flex-shrink:0;
}}
.pill{{
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(99,102,241,0.10);
  border:1px solid rgba(99,102,241,0.25);
  border-radius:20px;padding:3px 10px 3px 10px;
  font-size:12px;color:var(--indigo);font-weight:600;
}}
.pill b{{font-weight:700;}}
.pill-x{{
  background:none;border:0;cursor:pointer;
  color:var(--indigo);font-size:14px;line-height:1;
  padding:0 0 0 2px;opacity:0.7;transition:opacity 0.15s;
}}
.pill-x:hover{{opacity:1;}}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
nav.tabs{{
  display:flex;gap:3px;padding:5px;margin:0 0 8px;
  background:rgba(255,255,255,0.92);
  border:1px solid var(--border2);
  border-radius:14px;overflow-x:auto;flex-shrink:0;
  box-shadow:var(--sh-s);scrollbar-width:none;
  backdrop-filter:blur(12px);
}}
nav.tabs::-webkit-scrollbar{{display:none;}}
nav.tabs button{{
  background:transparent;border:0;
  color:var(--muted);padding:9px 20px;
  font-size:13px;font-weight:700;
  font-family:'Manrope',sans-serif;letter-spacing:0.01em;
  cursor:pointer;white-space:nowrap;border-radius:10px;
  transition:color 0.2s,background 0.2s;
}}
nav.tabs button:hover{{color:var(--ink);background:rgba(99,102,241,0.07);}}
nav.tabs button.active{{
  color:var(--indigo-d);background:#fff;
  box-shadow:var(--sh-s);
}}

/* ── Tab panels ──────────────────────────────────────────────────────────── */
.tab-panel{{display:none;position:absolute;inset:0;overflow:hidden;flex-direction:column;}}
.tab-panel.active{{display:flex;animation:fade .2s ease;}}
.tab-scroll{{flex:1;min-height:0;overflow:auto;padding:0 4px 10px;scrollbar-width:thin;scrollbar-color:rgba(99,102,241,0.35) transparent;}}
@keyframes fade{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:none}}}}

/* ── KPI strip ───────────────────────────────────────────────────────────── */
.kpi-strip{{
  display:grid;grid-template-columns:repeat(4,1fr);
  margin-bottom:10px;
  background:linear-gradient(135deg,#3730a3 0%,#5b21b6 100%);
  border-radius:var(--r);overflow:hidden;
  border:1px solid rgba(165,180,252,0.2);
  box-shadow:var(--sh-l);color:#f1f5f9;
}}
@media(max-width:900px){{.kpi-strip{{grid-template-columns:repeat(2,1fr);}}}}
.kpi{{
  padding:14px 18px;border-right:1px solid rgba(255,255,255,0.08);
  position:relative;overflow:hidden;
}}
.kpi::after{{
  content:'';position:absolute;
  bottom:-20px;right:-20px;
  width:80px;height:80px;border-radius:50%;
  background:rgba(255,255,255,0.04);
}}
.kpi:last-child{{border-right:0;}}
.klbl{{font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:rgba(199,210,254,0.65);font-weight:700;margin-bottom:8px;}}
.kval{{font-family:'Manrope',sans-serif;font-weight:800;font-size:clamp(1.3rem,2.4vw,1.8rem);color:#fff;letter-spacing:-0.03em;line-height:1;}}
.ksub{{font-size:11px;color:rgba(199,210,254,0.5);margin-top:6px;}}

/* ── Panel grid ──────────────────────────────────────────────────────────── */
.pgrid{{display:grid;grid-template-columns:repeat(12,1fr);gap:10px;margin-bottom:10px;}}
.panel{{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r);padding:13px 15px;
  box-shadow:var(--sh-m);
}}
.panel.acc{{border-left:3px solid var(--indigo);}}
.ph{{
  display:flex;justify-content:space-between;align-items:flex-start;
  margin-bottom:10px;padding-bottom:9px;border-bottom:1px solid var(--border);
}}
.ptitle{{font-family:'Manrope',sans-serif;font-weight:700;font-size:clamp(0.9rem,1.15vw,1.05rem);color:var(--ink);letter-spacing:-0.01em;}}
.psub{{font-size:11px;color:var(--muted);margin-top:3px;letter-spacing:0.05em;text-transform:uppercase;font-weight:500;}}
.ptag{{
  font-size:9.5px;padding:3px 9px;border-radius:20px;
  background:rgba(99,102,241,0.10);color:var(--indigo);
  border:1px solid rgba(99,102,241,0.25);
  text-transform:uppercase;letter-spacing:0.08em;font-weight:700;
  white-space:nowrap;
}}
.col-4 {{grid-column:span 4;}} .col-6{{grid-column:span 6;}} .col-12{{grid-column:span 12;}}
@media(max-width:960px){{.col-4,.col-6{{grid-column:span 12;}}}}
.cb  {{position:relative;height:var(--ch);  min-height:0;}}
.cb-s{{position:relative;height:var(--ch-s);min-height:0;}}
.cb-t{{position:relative;height:var(--ch-t);min-height:0;}}

/* ── Hint label on charts ────────────────────────────────────────────────── */
.chart-hint{{font-size:11px;color:var(--muted2);margin-top:4px;text-align:center;}}

/* ── Search & table ──────────────────────────────────────────────────────── */
.sbar{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:8px;}}
.sbar input{{
  flex:1;min-width:200px;padding:9px 14px;
  border:1px solid var(--border2);border-radius:10px;
  font-family:inherit;font-size:14px;
  background:var(--surface);color:var(--ink);
  box-shadow:var(--sh-s);transition:all 0.2s;
}}
.sbar input:focus{{outline:none;border-color:var(--indigo);box-shadow:0 0 0 3px rgba(99,102,241,0.12);}}
.tier-leg{{display:flex;gap:14px;font-size:12px;color:var(--muted);margin-bottom:7px;align-items:center;}}
.tier-dot{{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:4px;vertical-align:middle;}}
.twrap{{
  border:1px solid var(--border2);border-radius:var(--r-sm);
  overflow:auto;max-height:min(52vh,480px);
  background:var(--surface);box-shadow:var(--sh-m);
}}
table.dt{{width:100%;border-collapse:collapse;font-size:12px;}}
table.dt th{{
  position:sticky;top:0;
  background:linear-gradient(180deg,#f5f3ff 0%,#ede9fe 100%);
  text-align:left;padding:9px 11px;
  border-bottom:1px solid var(--border2);
  font-weight:700;color:var(--ink);white-space:nowrap;z-index:1;
  font-family:'Manrope',sans-serif;font-size:11px;letter-spacing:0.04em;text-transform:uppercase;
}}
table.dt td{{padding:8px 11px;border-bottom:1px solid var(--border);vertical-align:top;color:var(--ink2);font-size:12px;}}
table.dt tr.clickable{{cursor:pointer;}}
table.dt tr.clickable:hover td{{background:rgba(99,102,241,0.06)!important;}}
table.dt tr.t10 td{{background:rgba(99,102,241,0.08);border-left:3px solid var(--indigo);}}
table.dt tr.t25 td{{background:rgba(16,185,129,0.07);border-left:3px solid var(--emerald);}}
.pager{{display:flex;gap:10px;align-items:center;justify-content:flex-end;margin-top:10px;font-size:13px;color:var(--muted);}}
.pager button{{
  background:var(--surface);border:1px solid var(--border2);
  padding:7px 16px;border-radius:8px;cursor:pointer;
  font-family:inherit;color:var(--ink);font-size:12.5px;font-weight:700;
  box-shadow:var(--sh-s);transition:all 0.2s;
}}
.pager button:hover:not(:disabled){{border-color:var(--indigo);color:var(--indigo);}}
.pager button:disabled{{opacity:0.4;cursor:not-allowed;}}

/* ── Snap cards ──────────────────────────────────────────────────────────── */
.snap-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;}}
@media(max-width:700px){{.snap-grid{{grid-template-columns:1fr;}}}}
.snap{{
  display:flex;justify-content:space-between;align-items:baseline;
  padding:14px 17px;background:#ede9fe;border-radius:12px;
  border-left:3px solid var(--indigo);
}}
.snap-l{{font-size:12px;color:var(--muted);font-weight:500;}}
.snap-v{{font-family:'JetBrains Mono',monospace;font-size:15px;color:var(--indigo);font-weight:700;}}

/* ── Compare tab ─────────────────────────────────────────────────────────── */
.cmp-sel{{
  display:flex;align-items:center;gap:16px;
  margin-bottom:14px;flex-wrap:wrap;
}}
.cmp-col{{display:flex;flex-direction:column;gap:6px;flex:1;min-width:180px;}}
.cmp-col label{{font-size:11px;font-weight:700;color:var(--muted);letter-spacing:0.08em;text-transform:uppercase;}}
.cmp-col select{{
  padding:9px 14px;border:1px solid var(--border2);border-radius:10px;
  font-family:inherit;font-size:14px;background:var(--surface);color:var(--ink);
  box-shadow:var(--sh-s);cursor:pointer;
}}
.vs-badge{{
  font-family:'Manrope',sans-serif;font-weight:800;font-size:18px;
  color:var(--muted2);padding:0 8px;flex-shrink:0;
}}
.cmp-cards{{
  display:grid;grid-template-columns:1fr 1fr;gap:10px;
  margin-bottom:12px;
}}
@media(max-width:700px){{.cmp-cards{{grid-template-columns:1fr;}}}}
.cmp-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:14px 16px;box-shadow:var(--sh-m);}}
.cmp-card-title{{font-family:'Manrope',sans-serif;font-weight:800;font-size:15px;color:var(--ink);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border);}}
.cmp-card.a .cmp-card-title{{color:var(--indigo);}}
.cmp-card.b .cmp-card-title{{color:var(--violet);}}
.cmp-stat{{display:flex;justify-content:space-between;align-items:baseline;padding:6px 0;border-bottom:1px solid var(--border);}}
.cmp-stat:last-child{{border-bottom:0;}}
.cmp-stat-l{{font-size:12.5px;color:var(--muted);}}
.cmp-stat-v{{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:var(--ink);}}

/* ── Profile modal ───────────────────────────────────────────────────────── */
.modal{{
  position:fixed;inset:0;z-index:1000;
  display:flex;align-items:center;justify-content:center;
  visibility:hidden;
}}
.modal.open{{visibility:visible;}}
.modal-bg{{
  position:absolute;inset:0;
  background:rgba(30,27,75,0.45);
  backdrop-filter:blur(6px);
  opacity:0;transition:opacity 0.25s;
}}
.modal.open .modal-bg{{opacity:1;}}
.modal-card{{
  position:relative;z-index:1;
  background:var(--surface);border-radius:20px;
  width:min(580px,93vw);max-height:82vh;overflow-y:auto;
  box-shadow:0 24px 64px rgba(30,27,75,0.28);
  transform:translateY(20px) scale(0.97);opacity:0;
  transition:transform 0.25s,opacity 0.25s;
}}
.modal.open .modal-card{{transform:none;opacity:1;}}
.modal-hdr{{
  display:flex;justify-content:space-between;align-items:center;
  padding:18px 22px 14px;
  border-bottom:1px solid var(--border);
}}
.modal-title{{font-family:'Manrope',sans-serif;font-weight:800;font-size:17px;color:var(--ink);}}
.modal-close{{
  background:rgba(99,102,241,0.10);border:0;
  width:30px;height:30px;border-radius:8px;cursor:pointer;
  font-size:16px;display:flex;align-items:center;justify-content:center;
  color:var(--indigo);transition:background 0.2s;
}}
.modal-close:hover{{background:rgba(99,102,241,0.20);}}
.modal-body{{padding:18px 22px 22px;}}
.modal-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;}}
@media(max-width:480px){{.modal-grid{{grid-template-columns:1fr;}}}}
.mfield{{
  padding:10px 14px;background:var(--s2);
  border-radius:10px;border:1px solid var(--border);
}}
.mfield-l{{font-size:10.5px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);margin-bottom:4px;}}
.mfield-v{{font-size:14px;color:var(--ink);font-weight:600;}}
.mfield.hi .mfield-v{{color:var(--indigo);font-family:'JetBrains Mono',monospace;}}
.offer-badges{{display:flex;flex-wrap:wrap;gap:7px;margin-top:4px;}}
.obadge{{
  font-size:11.5px;font-weight:700;padding:4px 10px;border-radius:20px;
}}
.obadge.yes{{background:rgba(16,185,129,0.12);color:#059669;border:1px solid rgba(16,185,129,0.3);}}
.obadge.no {{background:rgba(107,114,128,0.10);color:var(--muted);border:1px solid var(--border);}}

/* ── Print ───────────────────────────────────────────────────────────────── */
@media print{{
  html,body{{overflow:visible!important;height:auto!important;}}
  .shell{{padding:0!important;height:auto!important;}}
  header.top .ctrl{{display:none!important;}}
  .filter-pills,.pager,.sbar .btn-export{{display:none!important;}}
  nav.tabs{{display:none!important;}}
  .dash-body{{overflow:visible!important;height:auto!important;position:static!important;}}
  .tab-panel{{display:flex!important;position:static!important;overflow:visible!important;}}
  .tab-scroll{{overflow:visible!important;}}
}}
</style>
</head>
<body>
<div class="shell">

  <!-- Header -->
  <header class="top">
    <div class="brand">
      <div class="brand-logo">{LOGO_SVG}</div>
      <div>
        <div class="brand-name">Grad Analytics · <em>MBA Profiler</em></div>
        <div class="brand-sub">Interactive view of simulated MBA graduate outcomes — school mix, roles, compensation &amp; offer flags. Click any chart to filter.</div>
      </div>
    </div>
    <div class="ctrl">
      <span class="lbl">Year</span>
      <select id="f-year"     class="sel" aria-label="Year"></select>
      <span class="lbl">School</span>
      <select id="f-school"   class="sel" aria-label="School"></select>
      <span class="lbl">Industry</span>
      <select id="f-industry" class="sel" aria-label="Industry"></select>
      <span class="lbl">Program</span>
      <select id="f-program"  class="sel" aria-label="Program"></select>
      <span class="lbl">GPA</span>
      <div class="gpa-wrap">
        <input type="range" id="f-gpa-min" min="2" max="4" step="0.1" value="2" aria-label="Min GPA"/>
        <span class="gpa-lbl" id="gpa-mn-lbl">2.0</span>
        <span class="lbl">–</span>
        <input type="range" id="f-gpa-max" min="2" max="4" step="0.1" value="4" aria-label="Max GPA"/>
        <span class="gpa-lbl" id="gpa-mx-lbl">4.0</span>
      </div>
      <button class="btn btn-reset" id="btn-reset">Reset</button>
      <button class="btn btn-print" id="btn-print" title="Print / Save as PDF">🖨 Print</button>
    </div>
  </header>

  <!-- Active filter pills -->
  <div class="filter-pills" id="filter-pills"></div>

  <!-- Tabs -->
  <nav class="tabs" role="tablist">
    <button class="active" role="tab" aria-selected="true"  data-tab="t1">Overview</button>
    <button role="tab" aria-selected="false" data-tab="t2">Offer Mix</button>
    <button role="tab" aria-selected="false" data-tab="t3">School Bench</button>
    <button role="tab" aria-selected="false" data-tab="t4">Analysis</button>
    <button role="tab" aria-selected="false" data-tab="t5">Compare</button>
    <button role="tab" aria-selected="false" data-tab="t6">Directory</button>
  </nav>

  <div class="dash-body">

    <!-- T1: Overview -->
    <section id="t1" class="tab-panel active" role="tabpanel">
      <div class="tab-scroll">
        <div class="kpi-strip" id="kpi-strip"></div>
        <div class="pgrid">
          <div class="panel acc col-6">
            <div class="ph">
              <div><div class="ptitle">Post-MBA Industry</div><div class="psub">Click a bar to filter</div></div>
              <span class="ptag">mix</span>
            </div>
            <div class="cb"><canvas id="ch-industry"></canvas></div>
          </div>
          <div class="panel col-6">
            <div class="ph">
              <div><div class="ptitle">School Distribution</div><div class="psub">Click a slice to filter</div></div>
              <span class="ptag">%</span>
            </div>
            <div class="cb-s"><canvas id="ch-school"></canvas></div>
          </div>
          <div class="panel col-6">
            <div class="ph">
              <div><div class="ptitle">Graduation Year</div><div class="psub">Click a bar to filter</div></div>
              <span class="ptag">time</span>
            </div>
            <div class="cb"><canvas id="ch-year"></canvas></div>
          </div>
          <div class="panel acc col-6">
            <div class="ph">
              <div><div class="ptitle">GPA vs Post-MBA Salary</div><div class="psub">Trend line with R²</div></div>
              <span class="ptag">scatter</span>
            </div>
            <div class="cb"><canvas id="ch-scatter"></canvas></div>
            <div class="chart-hint" id="scatter-r2"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- T2: Offer mix -->
    <section id="t2" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="pgrid">
          <div class="panel col-12">
            <div class="ph">
              <div><div class="ptitle">Flagged Offers</div><div class="psub">% answering Yes — Big Tech · Consulting · Big Banks</div></div>
              <span class="ptag">rates</span>
            </div>
            <div class="cb"><canvas id="ch-offers"></canvas></div>
          </div>
          <div class="panel col-12">
            <div class="ph">
              <div><div class="ptitle">Internship Pathway</div><div class="psub">Completed vs not</div></div>
              <span class="ptag">intern</span>
            </div>
            <div class="cb-s"><canvas id="ch-intern"></canvas></div>
          </div>
        </div>
      </div>
    </section>

    <!-- T3: School bench -->
    <section id="t3" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="pgrid">
          <div class="panel acc col-6">
            <div class="ph">
              <div><div class="ptitle">Avg Salary by School</div><div class="psub">Click to filter by school</div></div>
              <span class="ptag">$</span>
            </div>
            <div class="cb"><canvas id="ch-sal-sch"></canvas></div>
          </div>
          <div class="panel col-6">
            <div class="ph">
              <div><div class="ptitle">Avg GMAT by School</div><div class="psub">Admissions signal</div></div>
              <span class="ptag">exam</span>
            </div>
            <div class="cb"><canvas id="ch-gmat-sch"></canvas></div>
          </div>
          <div class="panel col-12">
            <div class="ph"><div><div class="ptitle">Cohort Snapshot</div><div class="psub">Filtered cohort</div></div></div>
            <div class="snap-grid" id="bench-snap"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- T4: Analysis -->
    <section id="t4" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="pgrid">
          <div class="panel col-12">
            <div class="ph">
              <div><div class="ptitle">Salary Distribution</div><div class="psub">Histogram — post-MBA compensation</div></div>
              <span class="ptag">histogram</span>
            </div>
            <div class="cb-t"><canvas id="ch-hist"></canvas></div>
          </div>
          <div class="panel acc col-12">
            <div class="ph">
              <div><div class="ptitle">Job Function Breakdown</div><div class="psub">Click a bar to filter by industry</div></div>
              <span class="ptag">function</span>
            </div>
            <div class="cb-t"><canvas id="ch-func"></canvas></div>
          </div>
        </div>
      </div>
    </section>

    <!-- T5: Compare -->
    <section id="t5" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel col-12" style="margin-bottom:12px">
          <div class="ph"><div><div class="ptitle">School Comparison</div><div class="psub">Pick two schools to compare side by side</div></div></div>
          <div class="cmp-sel">
            <div class="cmp-col">
              <label>School A</label>
              <select id="cmp-a"></select>
            </div>
            <div class="vs-badge">VS</div>
            <div class="cmp-col">
              <label>School B</label>
              <select id="cmp-b"></select>
            </div>
          </div>
          <div class="cmp-cards" id="cmp-cards"></div>
          <div class="cb-t"><canvas id="ch-cmp"></canvas></div>
        </div>
      </div>
    </section>

    <!-- T6: Directory -->
    <section id="t6" class="tab-panel" role="tabpanel">
      <div class="tab-scroll">
        <div class="panel col-12" style="margin-bottom:10px">
          <div class="sbar">
            <input type="search" id="tbl-srch" placeholder="Search school, industry, location, function…" autocomplete="off"/>
            <span class="ptag" id="tbl-cnt"></span>
            <button class="btn btn-export" id="btn-export">⬇ Export CSV</button>
          </div>
          <div class="tier-leg">
            <span><span class="tier-dot" style="background:var(--indigo)"></span>Top 10% salary</span>
            <span><span class="tier-dot" style="background:var(--emerald)"></span>Top 11–25% salary</span>
            <span style="font-size:11px;color:var(--muted2)">· Click any row for full profile</span>
          </div>
          <div class="twrap">
            <table class="dt" id="data-tbl">
              <thead><tr id="dt-head"></tr></thead>
              <tbody id="dt-body"></tbody>
            </table>
          </div>
          <div class="pager">
            <span id="pg-info"></span>
            <button id="pg-prev">← Prev</button>
            <button id="pg-next">Next →</button>
          </div>
        </div>
      </div>
    </section>

  </div><!-- dash-body -->
</div><!-- shell -->

<!-- Profile modal -->
<div class="modal" id="modal" role="dialog" aria-modal="true" aria-label="Candidate Profile">
  <div class="modal-bg" id="modal-bg"></div>
  <div class="modal-card">
    <div class="modal-hdr">
      <div class="modal-title">Candidate Profile</div>
      <button class="modal-close" id="modal-close" aria-label="Close">✕</button>
    </div>
    <div class="modal-body" id="modal-body"></div>
  </div>
</div>

<script>
window.__DATA = {payload};
(function(){{
  const DATA = window.__DATA;
  const P = {{
    indigo:'#6366f1', violet:'#8b5cf6', sky:'#0ea5e9',
    emerald:'#10b981', amber:'#f59e0b', rose:'#f43f5e', slate:'#64748b'
  }};
  const PAL = [P.indigo,P.violet,P.sky,P.emerald,P.amber,P.rose,P.slate];
  function pal(n){{return Array.from({{length:n}},(_,i)=>PAL[i%PAL.length]);}}

  let charts={{}}, page=0, tableRows=[];
  const PAGE=40;

  /* ── Helpers ──────────────────────────────────────────────────────────── */
  function uniq(col){{
    const s=new Set();
    DATA.forEach(r=>{{if(r[col]!=null&&r[col]!=='')s.add(String(r[col]));}}); 
    return Array.from(s).sort();
  }}
  function fillSel(el,vals){{
    el.innerHTML='<option value="all">All</option>'+
      vals.map(v=>'<option value="'+String(v).replace(/"/g,'&quot;')+'">'+v+'</option>').join('');
  }}
  function mean(arr){{
    const a=arr.filter(x=>x!=null&&isFinite(+x)).map(Number);
    return a.length?a.reduce((s,x)=>s+x,0)/a.length:null;
  }}
  function pctYes(rows,col){{
    if(!rows.length)return 0;
    return Math.round(rows.filter(r=>String(r[col]).toLowerCase()==='yes').length/rows.length*1000)/10;
  }}
  function countBy(rows,col){{
    const m={{}};
    rows.forEach(r=>{{const k=r[col]==null?'Unknown':String(r[col]);m[k]=(m[k]||0)+1;}});
    return m;
  }}
  function fmtMoney(n){{
    if(n==null||n==='')return'—';
    const x=+n;if(!isFinite(x))return'—';
    return'$'+Math.round(x).toLocaleString();
  }}
  function kill(id){{if(charts[id]){{charts[id].destroy();delete charts[id];}}}}
  function emptyC(id,type){{
    kill(id);
    charts[id]=new Chart(document.getElementById('ch-'+id),{{
      type:type||'bar',
      data:{{labels:['—'],datasets:[{{data:[0],backgroundColor:'rgba(99,102,241,0.15)'}}]}},
      options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{display:false}},y:{{display:false}}}}}}
    }});
  }}
  const GRID='rgba(99,102,241,0.08)';
  function ax(isX){{return {{ticks:{{color:'#6b7280',font:{{size:11}}}},grid:{{color:isX?'transparent':GRID}}}};}}

  /* ── GPA sliders ──────────────────────────────────────────────────────── */
  const gMnEl=document.getElementById('f-gpa-min'),
        gMxEl=document.getElementById('f-gpa-max'),
        gMnLbl=document.getElementById('gpa-mn-lbl'),
        gMxLbl=document.getElementById('gpa-mx-lbl');
  function syncGPA(){{
    let mn=parseFloat(gMnEl.value),mx=parseFloat(gMxEl.value);
    if(mn>mx){{const t=mn;mn=mx;mx=t;gMnEl.value=mn;gMxEl.value=mx;}}
    gMnLbl.textContent=mn.toFixed(1);gMxLbl.textContent=mx.toFixed(1);
  }}

  /* ── Filter pills ─────────────────────────────────────────────────────── */
  function renderPills(){{
    const defs=[
      {{id:'f-year',    lbl:'Year'}},
      {{id:'f-school',  lbl:'School'}},
      {{id:'f-industry',lbl:'Industry'}},
      {{id:'f-program', lbl:'Program'}},
    ];
    const active=defs.filter(d=>document.getElementById(d.id).value!=='all')
      .map(d=>{{return {{id:d.id,lbl:d.lbl,val:document.getElementById(d.id).value}};}});
    const gMin=parseFloat(gMnEl.value),gMax=parseFloat(gMxEl.value);
    const gFull=parseFloat(gMnEl.min)===gMin&&parseFloat(gMxEl.max)===gMax;
    if(!gFull)active.push({{id:'gpa',lbl:'GPA',val:gMin.toFixed(1)+' – '+gMax.toFixed(1)}});
    const el=document.getElementById('filter-pills');
    if(!active.length){{el.innerHTML='';return;}}
    el.innerHTML=active.map(p=>
      '<span class="pill">'+p.lbl+': <b>'+p.val+'</b>'+
      '<button class="pill-x" data-fid="'+p.id+'">×</button></span>'
    ).join('');
    el.querySelectorAll('.pill-x').forEach(btn=>{{
      btn.addEventListener('click',()=>{{
        const fid=btn.getAttribute('data-fid');
        if(fid==='gpa'){{gMnEl.value=gMnEl.min;gMxEl.value=gMxEl.max;syncGPA();}}
        else document.getElementById(fid).value='all';
        page=0;refresh();
      }});
    }});
  }}

  /* ── URL hash sync ────────────────────────────────────────────────────── */
  function saveHash(){{
    const p=new URLSearchParams();
    const y=document.getElementById('f-year').value;     if(y!=='all')p.set('y',y);
    const s=document.getElementById('f-school').value;   if(s!=='all')p.set('s',s);
    const i=document.getElementById('f-industry').value; if(i!=='all')p.set('i',i);
    const pr=document.getElementById('f-program').value; if(pr!=='all')p.set('p',pr);
    const mn=parseFloat(gMnEl.value),mx=parseFloat(gMxEl.value);
    if(parseFloat(gMnEl.min)!==mn)p.set('gn',mn.toFixed(1));
    if(parseFloat(gMxEl.max)!==mx)p.set('gx',mx.toFixed(1));
    const str=p.toString();
    history.replaceState(null,'',str?'#'+str:window.location.pathname+window.location.search);
  }}
  function loadHash(){{
    if(!window.location.hash)return;
    const p=new URLSearchParams(window.location.hash.slice(1));
    if(p.get('y'))document.getElementById('f-year').value=p.get('y');
    if(p.get('s'))document.getElementById('f-school').value=p.get('s');
    if(p.get('i'))document.getElementById('f-industry').value=p.get('i');
    if(p.get('p'))document.getElementById('f-program').value=p.get('p');
    if(p.get('gn')){{gMnEl.value=p.get('gn');}}
    if(p.get('gx')){{gMxEl.value=p.get('gx');}}
    syncGPA();
  }}

  /* ── Init filters ─────────────────────────────────────────────────────── */
  function initFilters(){{
    fillSel(document.getElementById('f-year'),    uniq('Graduation Year').sort((a,b)=>+a-+b));
    fillSel(document.getElementById('f-school'),  uniq('School'));
    fillSel(document.getElementById('f-industry'),uniq('Post-MBA Industry'));
    fillSel(document.getElementById('f-program'), uniq('Program Type'));
    const gpas=DATA.map(r=>+r['GPA']).filter(x=>isFinite(x));
    const mn=(Math.floor(Math.min(...gpas)*10)/10).toFixed(1);
    const mx=(Math.ceil( Math.max(...gpas)*10)/10).toFixed(1);
    gMnEl.min=mn;gMnEl.max=mx;gMnEl.value=mn;
    gMxEl.min=mn;gMxEl.max=mx;gMxEl.value=mx;
    syncGPA();
    // Fill compare selects
    const schs=uniq('School');
    ['cmp-a','cmp-b'].forEach((id,idx)=>{{
      const el=document.getElementById(id);
      el.innerHTML=schs.map(s=>'<option value="'+s.replace(/"/g,'&quot;')+'">'+s+'</option>').join('');
      if(schs[idx])el.value=schs[idx];
    }});
    loadHash();
  }}

  /* ── Filtered rows ────────────────────────────────────────────────────── */
  function filtered(){{
    const y=document.getElementById('f-year').value;
    const s=document.getElementById('f-school').value;
    const ind=document.getElementById('f-industry').value;
    const p=document.getElementById('f-program').value;
    const mn=parseFloat(gMnEl.value),mx=parseFloat(gMxEl.value);
    return DATA.filter(r=>{{
      if(y!=='all'&&String(r['Graduation Year'])!==y)return false;
      if(s!=='all'&&r['School']!==s)return false;
      if(ind!=='all'&&r['Post-MBA Industry']!==ind)return false;
      if(p!=='all'&&r['Program Type']!==p)return false;
      const g=+r['GPA'];
      if(isFinite(g)&&(g<mn||g>mx))return false;
      return true;
    }});
  }}

  /* ── Animated KPI counters ────────────────────────────────────────────── */
  function animCount(el,target,fmt,dur){{
    dur=dur||600;
    const start=performance.now();
    function step(ts){{
      const pct=Math.min((ts-start)/dur,1);
      const ease=1-Math.pow(1-pct,3);
      el.textContent=fmt(target*ease);
      if(pct<1)requestAnimationFrame(step);
      else el.textContent=fmt(target);
    }}
    requestAnimationFrame(step);
  }}

  function renderKPI(rows){{
    const avg$=mean(rows.map(r=>r['Post-MBA Salary']));
    const avgG=mean(rows.map(r=>r['GMAT']));
    const pt=pctYes(rows,'Offer in Big Tech');
    const strip=document.getElementById('kpi-strip');
    strip.innerHTML=
      kcard('Profiles',         'kv-n', '') +
      kcard('Avg Salary',       'kv-s', 'mean compensation') +
      kcard('Avg GMAT',         'kv-g', 'exam score') +
      kcard('Big Tech Offer',   'kv-t', '% answering Yes');
    animCount(strip.querySelector('.kv-n'),rows.length,v=>Math.round(v).toLocaleString());
    animCount(strip.querySelector('.kv-s'),avg$!=null?avg$:0,v=>avg$!=null?'$'+Math.round(v).toLocaleString():'—');
    animCount(strip.querySelector('.kv-g'),avgG!=null?avgG:0,v=>avgG!=null?Math.round(v).toString():'—');
    animCount(strip.querySelector('.kv-t'),pt,v=>(Math.round(v*10)/10)+'%');
  }}
  function kcard(label,cls,sub){{
    return '<div class="kpi"><div class="klbl">'+label+'</div><div class="kval '+cls+'">0</div>'+(sub?'<div class="ksub">'+sub+'</div>':'')+'</div>';
  }}

  /* ── Linear regression ────────────────────────────────────────────────── */
  function linReg(pts){{
    const n=pts.length; if(n<3)return null;
    const sx=pts.reduce((s,p)=>s+p.x,0),sy=pts.reduce((s,p)=>s+p.y,0);
    const sxy=pts.reduce((s,p)=>s+p.x*p.y,0),sx2=pts.reduce((s,p)=>s+p.x*p.x,0);
    const slope=(n*sxy-sx*sy)/(n*sx2-sx*sx);
    const int=(sy-slope*sx)/n;
    const ym=sy/n;
    const ssTot=pts.reduce((s,p)=>s+Math.pow(p.y-ym,2),0);
    const ssRes=pts.reduce((s,p)=>s+Math.pow(p.y-(slope*p.x+int),2),0);
    const r2=1-ssRes/ssTot;
    return {{slope,int,r2}};
  }}

  /* ── Overview ─────────────────────────────────────────────────────────── */
  function renderOverview(rows){{
    ['industry','school','year','scatter'].forEach(kill);
    if(!rows.length){{
      ['industry','year'].forEach(id=>emptyC(id,'bar'));
      emptyC('school','doughnut');emptyC('scatter','scatter');return;
    }}
    // Industry bar
    const byI=countBy(rows,'Post-MBA Industry');
    const labI=Object.keys(byI).sort((a,b)=>byI[b]-byI[a]);
    charts.industry=new Chart(document.getElementById('ch-industry'),{{
      type:'bar',
      data:{{labels:labI,datasets:[{{label:'Count',data:labI.map(k=>byI[k]),backgroundColor:pal(labI.length),borderRadius:4,borderWidth:0}}]}},
      options:{{
        indexAxis:'y',responsive:true,maintainAspectRatio:false,
        plugins:{{legend:{{display:false}}}},
        scales:{{x:{{...ax(true)}},y:{{...ax(false),grid:{{display:false}},ticks:{{color:'#1e1b4b',font:{{size:11}}}}}}}},
        onClick:(_,els)=>{{
          if(!els.length)return;
          const lbl=labI[els[0].index];
          const el=document.getElementById('f-industry');
          el.value=el.value===lbl?'all':lbl;
          page=0;refresh();
        }}
      }}
    }});
    // School doughnut
    const byS=countBy(rows,'School'),labS=Object.keys(byS);
    charts.school=new Chart(document.getElementById('ch-school'),{{
      type:'doughnut',
      data:{{labels:labS,datasets:[{{data:labS.map(k=>byS[k]),backgroundColor:pal(labS.length),borderWidth:2,borderColor:'#fff'}}]}},
      options:{{
        responsive:true,maintainAspectRatio:false,cutout:'55%',
        plugins:{{legend:{{position:'right',labels:{{color:'#1e1b4b',font:{{size:11}},boxWidth:10}}}}}},
        onClick:(_,els)=>{{
          if(!els.length)return;
          const lbl=labS[els[0].index];
          const el=document.getElementById('f-school');
          el.value=el.value===lbl?'all':lbl;
          page=0;refresh();
        }}
      }}
    }});
    // Year bar
    const byY=countBy(rows,'Graduation Year'),labY=Object.keys(byY).sort((a,b)=>+a-+b);
    charts.year=new Chart(document.getElementById('ch-year'),{{
      type:'bar',
      data:{{labels:labY,datasets:[{{label:'Headcount',data:labY.map(k=>byY[k]),backgroundColor:'rgba(99,102,241,0.55)',borderColor:P.indigo,borderWidth:1,borderRadius:4}}]}},
      options:{{
        responsive:true,maintainAspectRatio:false,
        plugins:{{legend:{{display:false}}}},
        scales:{{y:{{...ax(false),beginAtZero:true}},x:{{...ax(true),grid:{{display:false}},ticks:{{color:'#1e1b4b',font:{{size:11}}}}}}}},
        onClick:(_,els)=>{{
          if(!els.length)return;
          const lbl=labY[els[0].index];
          const el=document.getElementById('f-year');
          el.value=el.value===lbl?'all':lbl;
          page=0;refresh();
        }}
      }}
    }});
    // Scatter + regression
    const samp=rows.filter(r=>r['GPA']!=null&&r['Post-MBA Salary']!=null).slice(0,400);
    const pts=samp.map(r=>({{x:+r['GPA'],y:+r['Post-MBA Salary']}}));
    const reg=linReg(pts);
    const datasets=[{{
      type:'scatter',label:'Candidates',data:pts,
      backgroundColor:'rgba(139,92,246,0.28)',borderColor:P.violet,
      pointRadius:3,pointHoverRadius:5
    }}];
    if(reg){{
      const xs=[Math.min(...pts.map(p=>p.x)),Math.max(...pts.map(p=>p.x))];
      datasets.push({{
        type:'line',label:'Trend',
        data:xs.map(x=>({{x,y:reg.slope*x+reg.int}})),
        borderColor:P.indigo,borderWidth:2,borderDash:[5,4],
        pointRadius:0,fill:false,tension:0
      }});
      document.getElementById('scatter-r2').textContent=
        'R² = '+(Math.round(reg.r2*1000)/1000)+
        '  ·  slope = '+Math.round(reg.slope/1000)+'k per GPA point';
    }}
    charts.scatter=new Chart(document.getElementById('ch-scatter'),{{
      type:'scatter',
      data:{{datasets}},
      options:{{
        responsive:true,maintainAspectRatio:false,
        plugins:{{legend:{{display:false}}}},
        scales:{{
          x:{{...ax(true),title:{{display:true,text:'GPA',color:'#6b7280',font:{{size:11}}}}}},
          y:{{...ax(false),title:{{display:true,text:'Salary',color:'#6b7280',font:{{size:11}}}},
            ticks:{{callback:v=>'$'+Math.round(+v/1000)+'k',color:'#6b7280',font:{{size:11}}}}}}
        }}
      }}
    }});
  }}

  /* ── Offer mix ────────────────────────────────────────────────────────── */
  function renderOffers(rows){{
    ['offers','intern'].forEach(kill);
    if(!rows.length){{emptyC('offers','bar');emptyC('intern','doughnut');return;}}
    const vals=['Offer in Big Tech','Offer in Consulting','Offer in Big Banks'].map(c=>pctYes(rows,c));
    charts.offers=new Chart(document.getElementById('ch-offers'),{{
      type:'bar',
      data:{{labels:['Big Tech','Consulting','Big Banks'],datasets:[{{label:'% Yes',data:vals,backgroundColor:[P.indigo,P.violet,P.sky],borderRadius:6,borderWidth:0}}]}},
      options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},
        scales:{{y:{{...ax(false),max:100,beginAtZero:true,ticks:{{callback:v=>v+'%',color:'#6b7280',font:{{size:11}}}}}},x:{{...ax(true),grid:{{display:false}},ticks:{{color:'#1e1b4b',font:{{size:12}}}}}}}}}}
    }});
    const int2=countBy(rows,'Internship Completed'),ik=Object.keys(int2);
    charts.intern=new Chart(document.getElementById('ch-intern'),{{
      type:'doughnut',
      data:{{labels:ik,datasets:[{{data:ik.map(k=>int2[k]),backgroundColor:[P.sky,P.indigo,P.slate],borderWidth:2,borderColor:'#fff'}}]}},
      options:{{responsive:true,maintainAspectRatio:false,cutout:'52%',
        plugins:{{legend:{{position:'right',labels:{{color:'#1e1b4b',font:{{size:11}},boxWidth:10}}}}}}}}
    }});
  }}

  /* ── School bench ─────────────────────────────────────────────────────── */
  function renderBench(rows){{
    ['sal-sch','gmat-sch'].forEach(kill);
    const snap=document.getElementById('bench-snap');
    if(!rows.length){{
      snap.innerHTML=sc('Cohort','No rows');
      emptyC('sal-sch','bar');emptyC('gmat-sch','bar');return;
    }}
    const schs=[...new Set(rows.map(r=>r['School']).filter(Boolean))].sort();
    const avgBy=col=>Object.fromEntries(schs.map(s=>[s,mean(rows.filter(r=>r['School']===s).map(r=>r[col]))]));
    const sal=avgBy('Post-MBA Salary'),gm=avgBy('GMAT');
    charts['sal-sch']=new Chart(document.getElementById('ch-sal-sch'),{{
      type:'bar',
      data:{{labels:schs,datasets:[{{label:'Avg Salary',data:schs.map(s=>sal[s]),backgroundColor:'rgba(99,102,241,0.65)',borderRadius:4,borderWidth:0}}]}},
      options:{{responsive:true,maintainAspectRatio:false,
        plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>fmtMoney(c.parsed.y)}}}}}},
        scales:{{y:{{...ax(false),ticks:{{callback:v=>'$'+Math.round(+v/1000)+'k',color:'#6b7280',font:{{size:11}}}}}},x:{{...ax(true),grid:{{display:false}},ticks:{{color:'#1e1b4b',font:{{size:11}}}}}}}},
        onClick:(_,els)=>{{
          if(!els.length)return;
          const lbl=schs[els[0].index];
          const el=document.getElementById('f-school');
          el.value=el.value===lbl?'all':lbl;
          page=0;refresh();
        }}
      }}
    }});
    charts['gmat-sch']=new Chart(document.getElementById('ch-gmat-sch'),{{
      type:'bar',
      data:{{labels:schs,datasets:[{{label:'Avg GMAT',data:schs.map(s=>gm[s]),backgroundColor:'rgba(139,92,246,0.6)',borderRadius:4,borderWidth:0}}]}},
      options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},
        scales:{{y:{{...ax(false),beginAtZero:false}},x:{{...ax(true),grid:{{display:false}},ticks:{{color:'#1e1b4b',font:{{size:11}}}}}}}}}}
    }});
    const avgGPA=mean(rows.map(r=>r['GPA'])),avgW=mean(rows.map(r=>r['Work Experience (Years)']));
    snap.innerHTML=
      sc('Avg GPA',           avgGPA!=null?avgGPA.toFixed(2):'—')+
      sc('Avg Work Yrs (pre)',avgW  !=null?avgW.toFixed(1)  :'—')+
      sc('% Big Tech Offer',  pctYes(rows,'Offer in Big Tech')+'%')+
      sc('% Consulting',      pctYes(rows,'Offer in Consulting')+'%');
  }}
  function sc(l,v){{return '<div class="snap"><span class="snap-l">'+l+'</span><span class="snap-v">'+v+'</span></div>';}}

  /* ── Analysis ─────────────────────────────────────────────────────────── */
  function renderAnalysis(rows){{
    ['hist','func'].forEach(kill);
    const sals=rows.map(r=>+r['Post-MBA Salary']).filter(x=>isFinite(x)&&x>0);
    const N=12;
    let hLab=['No data'],hDat=[0];
    if(sals.length>1){{
      const lo=Math.min(...sals),hi=Math.max(...sals),bw=(hi-lo)/N;
      hDat=Array(N).fill(0);
      hLab=Array.from({{length:N}},(_,i)=>'$'+Math.round((lo+i*bw)/1000)+'k');
      sals.forEach(s=>{{let i=Math.floor((s-lo)/bw);if(i>=N)i=N-1;hDat[i]++;}});
    }}
    charts.hist=new Chart(document.getElementById('ch-hist'),{{
      type:'bar',
      data:{{labels:hLab,datasets:[{{label:'Candidates',data:hDat,backgroundColor:'rgba(99,102,241,0.6)',borderColor:P.indigo,borderWidth:1,borderRadius:4}}]}},
      options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},
        scales:{{y:{{...ax(false),beginAtZero:true}},x:{{...ax(true),grid:{{display:false}},ticks:{{color:'#1e1b4b',font:{{size:11}},maxRotation:40,minRotation:20}}}}}}}}
    }});
    const byF=countBy(rows,'Job Function'),labF=Object.keys(byF).sort((a,b)=>byF[b]-byF[a]);
    if(!labF.length){{emptyC('func','bar');return;}}
    charts.func=new Chart(document.getElementById('ch-func'),{{
      type:'bar',
      data:{{labels:labF,datasets:[{{label:'Count',data:labF.map(k=>byF[k]),backgroundColor:pal(labF.length),borderRadius:4,borderWidth:0}}]}},
      options:{{
        indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},
        scales:{{x:{{...ax(true)}},y:{{...ax(false),grid:{{display:false}},ticks:{{color:'#1e1b4b',font:{{size:11}}}}}}}},
        onClick:(_,els)=>{{
          if(!els.length)return;
          const fn=labF[els[0].index];
          const ind=document.getElementById('f-industry');
          // map function → industry if possible, else skip
          page=0;refresh();
        }}
      }}
    }});
  }}

  /* ── Compare ──────────────────────────────────────────────────────────── */
  function schoolStats(school){{
    const r=DATA.filter(d=>d['School']===school);
    return {{
      n:    r.length,
      sal:  mean(r.map(d=>d['Post-MBA Salary'])),
      gpa:  mean(r.map(d=>d['GPA'])),
      gmat: mean(r.map(d=>d['GMAT'])),
      tech: pctYes(r,'Offer in Big Tech'),
      cons: pctYes(r,'Offer in Consulting'),
      bank: pctYes(r,'Offer in Big Banks'),
      wrk:  mean(r.map(d=>d['Work Experience (Years)'])),
    }};
  }}
  function renderCompare(){{
    kill('cmp');
    const sa=document.getElementById('cmp-a').value;
    const sb=document.getElementById('cmp-b').value;
    if(!sa||!sb)return;
    const A=schoolStats(sa),B=schoolStats(sb);
    const rows2=[
      ['Candidates',       A.n.toLocaleString(),           B.n.toLocaleString()],
      ['Avg Salary',       fmtMoney(A.sal),                fmtMoney(B.sal)],
      ['Avg GPA',          A.gpa!=null?A.gpa.toFixed(2):'—', B.gpa!=null?B.gpa.toFixed(2):'—'],
      ['Avg GMAT',         A.gmat!=null?Math.round(A.gmat):'—', B.gmat!=null?Math.round(B.gmat):'—'],
      ['Avg Work Yrs',     A.wrk!=null?A.wrk.toFixed(1)+'y':'—', B.wrk!=null?B.wrk.toFixed(1)+'y':'—'],
      ['% Big Tech',       A.tech+'%',                     B.tech+'%'],
      ['% Consulting',     A.cons+'%',                     B.cons+'%'],
      ['% Big Banks',      A.bank+'%',                     B.bank+'%'],
    ];
    document.getElementById('cmp-cards').innerHTML=
      '<div class="cmp-card a">'+
        '<div class="cmp-card-title">'+sa+'</div>'+
        rows2.map(r=>'<div class="cmp-stat"><span class="cmp-stat-l">'+r[0]+'</span><span class="cmp-stat-v">'+r[1]+'</span></div>').join('')+
      '</div>'+
      '<div class="cmp-card b">'+
        '<div class="cmp-card-title">'+sb+'</div>'+
        rows2.map(r=>'<div class="cmp-stat"><span class="cmp-stat-l">'+r[0]+'</span><span class="cmp-stat-v">'+r[2]+'</span></div>').join('')+
      '</div>';
    const metrics=['Avg Salary','Avg GPA','Avg GMAT','% Big Tech','% Consulting'];
    const vA=[A.sal||0,A.gpa||0,A.gmat||0,A.tech,A.cons];
    const vB=[B.sal||0,B.gpa||0,B.gmat||0,B.tech,B.cons];
    charts.cmp=new Chart(document.getElementById('ch-cmp'),{{
      type:'bar',
      data:{{
        labels:metrics,
        datasets:[
          {{label:sa, data:vA, backgroundColor:'rgba(99,102,241,0.7)',borderRadius:4,borderWidth:0}},
          {{label:sb, data:vB, backgroundColor:'rgba(139,92,246,0.7)',borderRadius:4,borderWidth:0}},
        ]
      }},
      options:{{
        responsive:true,maintainAspectRatio:false,
        plugins:{{legend:{{position:'top',labels:{{color:'#1e1b4b',font:{{size:12,weight:'600'}}}}}},
          tooltip:{{callbacks:{{label:ctx=>{{
            const v=ctx.parsed.y;
            if(ctx.dataIndex===0)return ctx.dataset.label+': $'+Math.round(v).toLocaleString();
            return ctx.dataset.label+': '+v;
          }}}}}}}},
        scales:{{y:{{...ax(false),beginAtZero:true}},x:{{...ax(true),grid:{{display:false}},ticks:{{color:'#1e1b4b',font:{{size:12}}}}}}}}
      }}
    }});
  }}

  /* ── Directory ────────────────────────────────────────────────────────── */
  const COLS=['Student ID','School','Concentration','GPA','GMAT','Graduation Year','Program Type',
    'Post-MBA Salary','Post-MBA Industry','Job Function','Job Location',
    'Offer in Big Tech','Offer in Consulting','Offer in Big Banks'];
  function tiers(rows){{
    const s=rows.map(r=>+r['Post-MBA Salary']).filter(x=>isFinite(x)&&x>0).sort((a,b)=>a-b);
    if(s.length<4)return{{p75:Infinity,p90:Infinity}};
    return{{p75:s[Math.floor(s.length*.75)],p90:s[Math.floor(s.length*.90)]}};
  }}
  function renderTable(){{
    const q=(document.getElementById('tbl-srch').value||'').trim().toLowerCase();
    const rows=filtered().filter(r=>!q||COLS.some(c=>String(r[c]??'').toLowerCase().includes(q)));
    tableRows=rows;
    const {{p75,p90}}=tiers(rows);
    page=Math.min(page,Math.max(0,Math.ceil(rows.length/PAGE)-1));
    document.getElementById('dt-head').innerHTML=COLS.map(c=>'<th>'+c+'</th>').join('');
    const st=page*PAGE;
    document.getElementById('dt-body').innerHTML=rows.slice(st,st+PAGE).map((r,ri)=>{{
      const s=+r['Post-MBA Salary'];
      const cls=(isFinite(s)?(s>=p90?'t10':s>=p75?'t25':''):'');
      return '<tr class="clickable '+cls+'" data-idx="'+(st+ri)+'">'+
        COLS.map(c=>'<td>'+(c==='Post-MBA Salary'?fmtMoney(r[c]):(r[c]==null?'':String(r[c])))+'</td>').join('')+
        '</tr>';
    }}).join('');
    document.getElementById('tbl-cnt').textContent=rows.length.toLocaleString()+' rows';
    document.getElementById('pg-info').textContent=rows.length?'Page '+(page+1)+' of '+Math.ceil(rows.length/PAGE):'No rows';
    document.getElementById('pg-prev').disabled=page<=0;
    document.getElementById('pg-next').disabled=st+PAGE>=rows.length;
    // row click → profile modal
    document.getElementById('dt-body').querySelectorAll('tr.clickable').forEach(tr=>{{
      tr.addEventListener('click',()=>openModal(tableRows[+tr.getAttribute('data-idx')]));
    }});
  }}

  /* ── Profile modal ────────────────────────────────────────────────────── */
  function openModal(r){{
    if(!r)return;
    const money=fmtMoney(r['Post-MBA Salary']);
    const offerFields=['Offer in Big Tech','Offer in Consulting','Offer in Big Banks'];
    const badges=offerFields.map(f=>{{
      const yes=String(r[f]).toLowerCase()==='yes';
      return '<span class="obadge '+(yes?'yes':'no')+'">'+(yes?'✓ ':'')+f+'</span>';
    }}).join('');
    document.getElementById('modal-body').innerHTML=
      '<div class="modal-grid">'+
        mf('Student ID',  r['Student ID'],      true)+
        mf('School',      r['School'],           false)+
        mf('Program',     r['Program Type'],     false)+
        mf('Graduation',  r['Graduation Year'],  false)+
        mf('Concentration',r['Concentration'],   false)+
        mf('GPA',         r['GPA'],              true)+
        mf('GMAT',        r['GMAT'],             true)+
        mf('Work Exp.',   r['Work Experience (Years)']!=null?r['Work Experience (Years)']+' yrs':'—', true)+
        mf('Post-MBA Salary', money,             true)+
        mf('Industry',    r['Post-MBA Industry'],false)+
        mf('Job Function',r['Job Function'],     false)+
        mf('Location',    r['Job Location'],     false)+
        mf('Internship',  r['Internship Completed'],false)+
      '</div>'+
      '<div style="margin-top:14px"><div class="mfield-l" style="margin-bottom:8px;font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#6b7280">Offer Flags</div>'+
      '<div class="offer-badges">'+badges+'</div></div>';
    document.getElementById('modal').classList.add('open');
    document.getElementById('modal').focus();
  }}
  function mf(l,v,hi){{
    return '<div class="mfield'+(hi?' hi':'')+'"><div class="mfield-l">'+l+'</div><div class="mfield-v">'+(v==null||v===''?'—':String(v))+'</div></div>';
  }}
  function closeModal(){{document.getElementById('modal').classList.remove('open');}}
  document.getElementById('modal-close').addEventListener('click',closeModal);
  document.getElementById('modal-bg').addEventListener('click',closeModal);
  document.addEventListener('keydown',e=>{{if(e.key==='Escape')closeModal();}});

  /* ── CSV export ───────────────────────────────────────────────────────── */
  document.getElementById('btn-export').addEventListener('click',()=>{{
    const q=(document.getElementById('tbl-srch').value||'').trim().toLowerCase();
    const rows=filtered().filter(r=>!q||COLS.some(c=>String(r[c]??'').toLowerCase().includes(q)));
    const esc=v=>'"'+String(v??'').replace(/"/g,'""')+'"';
    const csv=[COLS.map(esc).join(','),...rows.map(r=>COLS.map(c=>esc(r[c])).join(','))].join('\\n');
    const a=Object.assign(document.createElement('a'),{{href:URL.createObjectURL(new Blob([csv],{{type:'text/csv'}})),download:'mba_candidates.csv'}});
    a.click();URL.revokeObjectURL(a.href);
  }});

  /* ── Print ────────────────────────────────────────────────────────────── */
  document.getElementById('btn-print').addEventListener('click',()=>window.print());

  /* ── Refresh ──────────────────────────────────────────────────────────── */
  function refresh(){{
    const rows=filtered();
    renderKPI(rows);renderOverview(rows);renderOffers(rows);
    renderBench(rows);renderAnalysis(rows);renderTable();
    renderPills();saveHash();
  }}

  /* ── Tab switching ────────────────────────────────────────────────────── */
  document.querySelectorAll('nav.tabs button').forEach(btn=>{{
    btn.addEventListener('click',()=>{{
      document.querySelectorAll('nav.tabs button').forEach(b=>{{b.classList.remove('active');b.setAttribute('aria-selected','false');}});
      btn.classList.add('active');btn.setAttribute('aria-selected','true');
      const id=btn.getAttribute('data-tab');
      document.querySelectorAll('.tab-panel').forEach(p=>p.classList.toggle('active',p.id===id));
      if(id==='t5')renderCompare();
    }});
  }});

  /* ── Filter events ────────────────────────────────────────────────────── */
  ['f-year','f-school','f-industry','f-program'].forEach(id=>
    document.getElementById(id).addEventListener('change',()=>{{page=0;refresh();}})
  );
  [gMnEl,gMxEl].forEach(el=>el.addEventListener('input',()=>{{syncGPA();page=0;refresh();}}));
  document.getElementById('btn-reset').addEventListener('click',()=>{{
    ['f-year','f-school','f-industry','f-program'].forEach(id=>{{document.getElementById(id).value='all';}});
    gMnEl.value=gMnEl.min;gMxEl.value=gMxEl.max;syncGPA();
    page=0;refresh();
  }});
  document.getElementById('tbl-srch').addEventListener('input',()=>{{page=0;renderTable();}});
  document.getElementById('pg-prev').addEventListener('click',()=>{{page=Math.max(0,page-1);renderTable();}});
  document.getElementById('pg-next').addEventListener('click',()=>{{page++;renderTable();}});
  ['cmp-a','cmp-b'].forEach(id=>document.getElementById(id).addEventListener('change',renderCompare));

  /* ── Boot ─────────────────────────────────────────────────────────────── */
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
