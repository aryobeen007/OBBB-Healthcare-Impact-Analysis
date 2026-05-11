# OBBB Healthcare Impact Analysis
## Project Documentation

**Author:** Independent Policy Data Analyst
**Date:** February 2026
**Tools:** Python 3.14 · pandas · NumPy · matplotlib · Jupyter Notebook · HTML · CSS · JavaScript · Chart.js

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Data Sources](#2-data-sources)
3. [Data Retrieval Process](#3-data-retrieval-process)
4. [Data Collection Code](#4-data-collection-code)
5. [Data Cleaning Process](#5-data-cleaning-process)
6. [Data Cleaning Code](#6-data-cleaning-code)
7. [Data Visualization Process](#7-data-visualization-process)
8. [Data Visualization Code](#8-data-visualization-code)
9. [Final Deliverables](#9-final-deliverables)

---

## 1. Project Overview

### What This Project Is About

On July 4, 2025, the One Big Beautiful Bill Act (OBBB) was signed into law — the largest cuts to the U.S. healthcare safety net in history. The law reduces federal spending on health programs by over $1 trillion over ten years (2025–2034), primarily targeting Medicaid, the program that provides health insurance to low-income families, children, elderly people in nursing homes, and people with disabilities.

The purpose of this project is to translate the raw numbers published by official government and policy research organizations into clear, accessible visualizations that anyone can understand — not just policy experts.

### The Problem I Am Analyzing

Most Americans have no way to quickly understand what $1 trillion in cuts actually means for real people. Numbers at that scale are abstract. I set out to answer four concrete questions:

1. Which states lose the most federal Medicaid funding in dollar terms?
2. Which states see the largest increase in their uninsured rate as a result?
3. Of the 14.2 million people projected to lose coverage, where does each group come from?
4. Is there a measurable relationship between how much funding a state loses and how badly its uninsured rate rises?

### The Final Goal

The project produces two complete deliverables:

- **A Jupyter Notebook** (`OBBB_Impact_Analysis.ipynb`) containing the full data pipeline — library setup, data retrieval attempts, verified dataset construction, validation, cleaning, and four professional matplotlib visualizations — with every step explained in plain language.
- **An interactive HTML dashboard** (`OBBB_Impact_Dashboard_Final.html`) that any non-technical reader can open in a browser to explore the data across six tabbed views, including a searchable and sortable state-by-state table, KPI cards, charts, an implementation timeline, and a plain-English explainer guide.

---

## 2. Data Sources

All data used in this project comes from official government agencies and nonpartisan policy research organizations. Every number in the analysis traces back to a published report listed below.

| # | Organization | Publication | Date | Description | Link |
|---|---|---|---|---|---|
| 1 | Congressional Budget Office (CBO) | Estimated Budgetary Effects of Public Law 119-21 | July 21, 2025 | Primary source for all national financial projections: $1.06T total cuts, $990B Medicaid cuts, $325.6B work requirements savings, $191.1B provider tax freeze, $149.4B state-directed payments cap, 11.8M Medicaid coverage loss | [cbo.gov/publication/61569](https://www.cbo.gov/publication/61569) |
| 2 | Congressional Budget Office (CBO) | Health Coverage Projections Update | August 2025 | Updated coverage loss figures including 14.2M total uninsured projection and 2.1M ACA marketplace loss | [cbo.gov](https://www.cbo.gov) |
| 3 | Kaiser Family Foundation (KFF) | How Will the 2025 Reconciliation Law Affect the Uninsured Rate in Each State? | August 20, 2025 | State-by-state uninsured rate increase projections. Source for all percentage point increase figures by state | [kff.org](https://www.kff.org/uninsured/how-will-the-2025-reconciliation-law-affect-the-uninsured-rate-in-each-state/) |
| 4 | Kaiser Family Foundation (KFF) | Allocating CBO Estimates of Federal Medicaid Spending Reductions Across the States | July 23, 2025 | State-by-state allocation of CBO national Medicaid cut estimates. Source for all state-level federal funding loss figures | [kff.org](https://www.kff.org) |
| 5 | Kaiser Family Foundation (KFF) | Status of Medicaid Expansion by State | 2025 | Current Medicaid expansion status for each state | [kff.org](https://www.kff.org/medicaid/issue-brief/status-of-state-medicaid-expansion-decisions-interactive-map/) |
| 6 | Center for Medicare Advocacy | Impact of the Big Bill on Medicare | July 24, 2025 | Source for $120B SNAP food aid cuts figure and Medicare-specific impact analysis | [medicareadvocacy.org](https://www.medicareadvocacy.org) |
| 7 | Center for American Progress (CAP) | The Truth About the One Big Beautiful Bill Act's Cuts to Medicaid and Medicare | August 5, 2025 | Source for 300+ rural hospitals at risk of closure figure | [americanprogress.org](https://www.americanprogress.org) |

---

## 3. Data Retrieval Process

I attempted to retrieve the data programmatically before resorting to manual entry. My retrieval process went through three plans in sequence.

### Plan A — Web Scraping with BeautifulSoup

I first tried to scrape the data directly from the KFF website using Python's `requests` library to fetch the page and `BeautifulSoup` to parse its HTML content. I connected successfully to the KFF URL and received a status 200 response, confirming the page loaded. However, when I searched the raw HTML for the data tables, I found none. I discovered that KFF loads its state-by-state data tables dynamically using JavaScript after the initial page renders. Since `BeautifulSoup` only reads the raw HTML that arrives before JavaScript executes, it had no way to see the actual data. Plan A was not viable.

### Plan B — Direct File Download

I then attempted to download KFF and CBO data files directly by URL, targeting known file paths for their published Excel and CSV exports. I tried three separate URLs using `requests.get()` with a browser-style User-Agent header. All three returned either a 403 (Access Denied) or 404 (Not Found) status code, indicating the websites block automated file downloads. Plan B was not viable.

### Plan C — Manual Entry from Verified Primary Sources

I built both datasets manually by reading the published CBO and KFF reports directly and entering every number by hand into Python dictionaries, which I then converted into pandas DataFrames. This is standard professional practice in policy research when automated retrieval is blocked. Every value is cited to its exact source publication and date inside the code. No numbers were estimated or interpolated — each one appears verbatim in the cited report.

**Source code:** [`src/01_data_collection.py`](src/01_data_collection.py)

---

## 4. Data Collection Code

The data collection code is saved in a separate file for reuse and version control.

**File:** [`src/01_data_collection.py`](src/01_data_collection.py)

This file contains:
- Plan A: the web scraping attempt using `requests` and `BeautifulSoup`
- Plan B: the direct file download attempt with fallback URLs
- Plan C: the verified manual dataset construction for both `df_national` and `df_states`

See the source file for full commented code. Below is a summary of the two datasets produced:

**`df_national`** — 12 rows × 4 columns

| Column | Description |
|---|---|
| `Metric` | Name of the national metric |
| `Value` | Numeric value |
| `Unit` | Unit of measurement (Billion USD, Million People, Hospitals) |
| `Source` | Citation for that specific number |

**`df_states`** — 50 rows × 5 columns

| Column | Description |
|---|---|
| `state` | State name |
| `funding_loss_b` | Federal Medicaid funding loss in billions USD (KFF, July 2025) |
| `uninsured_pct` | Percentage point increase in uninsured rate by 2034 (KFF, August 2025) |
| `people_losing` | Estimated number of people losing coverage |
| `expansion` | Whether the state expanded Medicaid under the ACA (Yes/No) |
| `severity` | Impact severity rating: Critical, High, Medium, or Lower |

---

## 5. Data Cleaning Process

After constructing both datasets, I put them through a structured cleaning and processing pipeline before any visualization work began.

### Step 1 — Data Validation

I validated both datasets before touching them. I checked for missing values using `isnull().any().any()`, which returned `False` for both datasets — confirming zero missing values. I used `describe()` to verify that all numeric ranges were realistic (for example, confirming that funding loss values fell between $1B and $110B as expected). I used `value_counts()` to confirm the correct number of states in each severity category, and verified that all 50 states plus DC were present.

### Step 2 — Creating a Working Copy

I created `df_clean` as a copy of `df_states` using `.copy()` so that the original raw dataset remained untouched throughout all subsequent transformations. This is a professional best practice — never modify the original source data.

### Step 3 — Adding Calculated Columns

I added three calculated columns to `df_clean`:

- `people_losing_thousands` — divided the raw `people_losing` values by 1,000 to produce cleaner, more readable numbers for chart labels. For example, 1,800,000 became 1800.0.
- `funding_loss_m` — converted `funding_loss_b` from billions to millions by multiplying by 1,000, useful for small-state comparisons.
- `severity_score` — mapped the text severity labels to integers using a dictionary (Critical=4, High=3, Medium=2, Lower=1) so Python could sort them correctly. I then cast this column to integer type explicitly to prevent category-type sorting errors.

### Step 4 — Sorting

I sorted `df_clean` by two columns simultaneously: `severity_score` descending first, then `funding_loss_b` descending within each severity group. This ensures that the most critically impacted states appear at the top of every chart. I followed the sort with `reset_index(drop=True)` to give the sorted DataFrame clean sequential row numbers.

**Source code:** [`src/02_data_cleaning.py`](src/02_data_cleaning.py)

---

## 6. Data Cleaning Code

The full cleaning pipeline is saved in a separate source file.

**File:** [`src/02_data_cleaning.py`](src/02_data_cleaning.py)

This file contains the complete cleaning pipeline that produces `df_clean` from `df_states`, including all validation checks, calculated columns, severity mapping, and sorting logic.

---

## 7. Data Visualization Process

I created four charts in matplotlib inside the Jupyter Notebook. Each chart answers a different analytical question about the data. All four charts share a consistent dark theme (`#0F1117` background), the same color encoding system (red = Critical, orange = High, yellow = Medium, green = Lower), and the same data source citation in each title.

### Chart 1 — Vertical Bar Chart: Top 15 States by Federal Funding Loss

**Question answered:** Which states lose the most federal Medicaid money under OBBB?

I chose a vertical bar chart because it is the most intuitive format for comparing a single value across many categories — the taller the bar, the greater the loss. I took the top 15 rows from `df_clean`, which was already sorted by severity and then funding loss, so the most impacted states naturally appear first. I color-coded each bar by severity level using a color map dictionary. I added dollar-formatted value labels above each bar using `ax.text()`, formatted the y-axis as `$110B` using `mticker.FuncFormatter`, and built a manual legend using `Patch` objects.

**Key finding:** California leads at $110B in projected losses, more than 50% higher than the second-ranked state (New York at $72B).

### Chart 2 — Horizontal Bar Chart: Top 25 States by Uninsured Rate Increase

**Question answered:** Which states see the largest percentage increase in their uninsured rate?

I chose a horizontal bar chart because state names are long — the horizontal orientation gives enough space for readable labels on the left side without rotation. I sorted `df_clean` by `uninsured_pct` ascending and used `.tail(25)` to retrieve the 25 highest values, which appear at the top of the chart after the ascending sort. I added a purple dashed vertical reference line using `axvline()` showing the national average increase, making it immediately visible which states are above and below average.

**Key finding:** Washington state (+4.8%) ranks highest — a different story from Chart 1, where California ranked first. This demonstrates that smaller states can be proportionally harder hit even when their dollar losses are lower.

### Chart 3 — Pie Chart with Detail Panel: National Coverage Loss Breakdown

**Question answered:** Of the 14.2 million people losing coverage, where does each group come from?

I chose a pie chart because I am showing parts of a whole — all four slices add up to 14.2 million people. I created a two-panel figure using `plt.subplots(1, 2)` with `gridspec_kw` controlling the width ratio between panels. The left panel holds the pie chart with `autopct` for automatic percentage labels, an `explode` value to pull the largest slice slightly outward for emphasis, and center text showing the total. The right panel uses `ax.transAxes` positioning to display colored circle dots with exact counts and percentages for each category.

**Key finding:** Medicaid loss from OBBB provisions alone accounts for 52.8% of all projected coverage loss — more than half the total.

### Chart 4 — Scatter Plot: Funding Loss vs Uninsured Rate Increase

**Question answered:** Is there a measurable relationship between funding loss and uninsured rate increase across states?

I chose a scatter plot because it encodes four variables simultaneously: x-position (funding loss), y-position (uninsured rate), dot size (people losing coverage), and dot color (severity). I used `np.sqrt()` on the dot size values to prevent California's very large population from producing a dot so large it dominates the chart. I calculated a trend line using `np.polyfit()` with degree 1 (straight line) and drew it with `np.poly1d()`. I added horizontal and vertical average reference lines using `axhline()` and `axvline()` to divide the chart into four labeled quadrants. I selectively labeled only the highest-impact states using `ax.annotate()` to keep the chart readable.

**Key finding:** A positive correlation exists between funding loss and uninsured rate increase, but the relationship is not perfectly linear. Some smaller states fall in the upper-left quadrant — high uninsured rate increase despite lower dollar losses — showing they are proportionally more vulnerable.

**Source code:** [`src/03_data_visualization.py`](src/03_data_visualization.py)

---

## 8. Data Visualization Code

The full visualization code for all four charts is saved in a separate source file.

**File:** [`src/03_data_visualization.py`](src/03_data_visualization.py)

This file contains the complete code for all four charts. Each chart is wrapped in a clearly labeled function so individual charts can be run independently:

- `chart1_funding_loss_bar(df_clean)` — vertical bar chart
- `chart2_uninsured_rate_bar(df_clean)` — horizontal bar chart
- `chart3_coverage_breakdown_pie()` — pie chart with detail panel
- `chart4_scatter_plot(df_clean)` — scatter plot with trend line

---

## 9. Final Deliverables

| File | Description |
|---|---|
| `OBBB_Impact_Analysis.ipynb` | Main Jupyter Notebook — complete 8-section analysis pipeline |
| `OBBB_Impact_Dashboard_Final.html` | Self-contained interactive HTML dashboard — six tabs, Chart.js, live search/filter/sort |
| `src/01_data_collection.py` | Data retrieval code — Plans A, B, and C |
| `src/02_data_cleaning.py` | Data cleaning and processing pipeline |
| `src/03_data_visualization.py` | All four matplotlib chart functions |
| `docs/HEALTHCARE_PORTFOLIO_BLUEPRINT.md` | Full project blueprint and strategy document |
| `docs/DATA_SOURCES.md` | Master data sources reference with citations and links |
| `docs/OBBB_PROJECT_DOCUMENTATION.md` | This file |

---

## Repository Structure

```
obbb-healthcare-impact/
|
|-- README.md
|-- requirements.txt
|-- OBBB_Impact_Analysis.ipynb
|-- OBBB_Impact_Dashboard_Final.html
|
|-- src/
|   |-- 01_data_collection.py
|   |-- 02_data_cleaning.py
|   |-- 03_data_visualization.py
|
|-- docs/
|   |-- OBBB_PROJECT_DOCUMENTATION.md
|   |-- HEALTHCARE_PORTFOLIO_BLUEPRINT.md
|   |-- DATA_SOURCES.md
```

---

*All figures are CBO projections as of August 2025. State-level figures are based on KFF allocations of CBO national totals.*
