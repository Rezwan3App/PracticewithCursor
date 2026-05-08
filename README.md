# Candidate Profiler · MBA Offers Dashboard

An interactive analytics dashboard built from simulated MBA graduate data. Created as a class exercise using GenAI coding agents (Cursor / Claude).

**Live link:** https://raw.githack.com/Rezwan3App/PracticewithCursor/main/docs/index.html

---

## What's in this repo

| File | Description |
|------|-------------|
| `Candidate Profiler/Candidate Profiler/Candidate_Dashboard.html` | Self-contained interactive dashboard (open directly in browser) |
| `Candidate Profiler/Candidate Profiler/MBA Grads.xlsx` | Simulated MBA graduate dataset |
| `Candidate Profiler/Candidate Profiler/MBA GradsOffers.docx` | Prompt used during the class demo |
| `Candidate Profiler/Candidate Profiler/build_candidate_dashboard.py` | Python script that regenerates the HTML from the Excel file |
| `Candidate Profiler/Candidate Profiler/pwc-logo.svg` | Logo asset |
| `docs/index.html` | Copy of the dashboard for GitHub Pages hosting |

---

## How to open the dashboard

**Option A — locally (zero setup):**
Download `Candidate_Dashboard.html` and double-click it. Everything is embedded — no server required.

**Option B — live link (shareable with anyone):**
https://raw.githack.com/Rezwan3App/PracticewithCursor/main/docs/index.html

**Option C — GitHub Pages:**
In repo Settings → Pages, set source to `main` branch, `/docs` folder.
URL: `https://rezwan3app.github.io/PracticewithCursor/`

---

## Changes made by the GenAI coding agent

### Features added
1. **Dark mode toggle** — 🌙/☀️ button in the header; switches light/dark theme and remembers your preference in `localStorage`
2. **GPA range slider** — dual min/max range inputs that filter all charts and the directory in real time
3. **Export CSV** — "⬇ Export CSV" button in the Directory tab downloads the currently filtered and searched rows as a `.csv` file
4. **Analysis tab** — new tab with two charts:
   - *Salary Distribution* — 12-bin histogram of post-MBA compensation
   - *Job Function Breakdown* — horizontal bar chart of headcount by job function
5. **Top-earner row highlighting** — in the Directory, rows are color-striped by salary tier: indigo = top 10%, green = top 11–25%

### Design refresh
6. **New color palette** — moved from PwC orange to a modern indigo/violet primary (`#6366f1`), sky-blue accent (`#0ea5e9`), and emerald green (`#10b981`)
7. **Modern UI** — pill-style tabs, glassmorphism header with deep indigo gradient, rounded cards, improved shadows, Manrope font for headings, smoother transitions throughout
8. **Dark mode design** — full dark-surface treatment (`#0b0f1a` background, `#141928` cards) with adapted borders and chart colors

### Original tabs (unchanged in structure, updated visually)
- **Overview** — industry mix, school distribution doughnut, graduation year bar, GPA vs salary scatter
- **Offer Mix** — Big Tech / Consulting / Banks offer rates, internship pathway doughnut
- **School Bench** — avg salary by school, avg GMAT by school, cohort snapshot stats

---

## Class exercise (optional — not graded)

1. Open `MBA GradsOffers.docx` and copy the prompt the professor used. Paste it into ChatGPT or Claude with the `MBA Grads.xlsx` dataset and compare your output to the dashboard above.
2. Think about additional enhancements to the dashboard, then use a GenAI coding agent (Cursor, Claude Code, Codex) to build them — just point the agent at `Candidate_Dashboard.html` and describe what you want.
3. Try the same request in a chat tool (ChatGPT, ClaudeChat) and compare the quality of results.
