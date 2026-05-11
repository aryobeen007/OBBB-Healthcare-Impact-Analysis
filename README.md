# OBBB Healthcare Impact Analysis

A data analysis project examining the impact of the **One Big Beautiful Bill Act (OBBB)** on Medicaid and Medicare coverage across all 50 U.S. states. Built entirely in Python using publicly available data from the Congressional Budget Office (CBO) and Kaiser Family Foundation (KFF).

---

## Live Dashboard

> Open `OBBB_Impact_Dashboard_final.html` in any browser for the full interactive experience.

The dashboard includes six tabs:

| Tab                 | Contents                                          |
| ------------------- | ------------------------------------------------- |
| National Overview   | KPI cards + coverage loss breakdown chart         |
| Medicaid Deep Dive  | Provision-by-provision cost breakdown             |
| Medicare Impact     | Medicare-specific cuts and dual-eligible analysis |
| State-by-State      | Searchable and sortable table of all 50 states    |
| Timeline            | Annotated implementation timeline 2025-2034       |
| Plain-English Guide | Key terms and provisions explained simply         |

---

## Project Overview

On July 4, 2025, the One Big Beautiful Bill Act was signed into law — the largest cuts to the U.S. healthcare safety net in history. The law reduces federal spending on health programs by over **$1 trillion over ten years (2025-2034)**, primarily targeting Medicaid.

This project answers four analytical questions:

1. Which states lose the most federal Medicaid funding in dollar terms?
2. Which states see the largest increase in their uninsured rate?
3. Of the 14.2 million people projected to lose coverage, where does each group come from?
4. Is there a measurable relationship between funding loss and uninsured rate increase?

---

## Key Findings

| Metric                      | Value                                | Source                |
| --------------------------- | ------------------------------------ | --------------------- |
| Total health program cuts   | $1.06 trillion (2025-2034)           | CBO July 2025         |
| People losing Medicaid      | 11.8 million                         | CBO August 2025       |
| Total losing coverage       | 14.2 million                         | CBO + KFF August 2025 |
| Highest dollar impact state | California -- $110B loss             | KFF July 2025         |
| Highest rate impact state   | Washington -- +4.8% uninsured        | KFF August 2025       |
| Largest single provision    | Work requirements -- $325.6B savings | CBO July 2025         |
| Rural hospitals at risk     | 300+ facilities                      | CAP 2025              |

---

## Visualizations

### Chart 1 -- Top 15 States by Federal Funding Loss

Vertical bar chart showing which states lose the most federal Medicaid money. Color-coded by severity level.

### Chart 2 -- Top 25 States by Uninsured Rate Increase

Horizontal bar chart showing the largest percentage point increases in uninsured rate by 2034, with national average reference line.

### Chart 3 -- National Coverage Loss Breakdown

Pie chart with detail panel breaking down the 14.2 million projected coverage losses by category (Medicaid, ACA Marketplace, ACA Tax Credit Expiry, Medicare/Other).

### Chart 4 -- Funding Loss vs Uninsured Rate Scatter Plot

Multi-dimensional scatter plot encoding four variables simultaneously: funding loss (x), uninsured rate (y), people losing coverage (dot size), and severity (dot color). Includes trend line and quadrant analysis.

---

## Repository Structure

```
OBBB-Healthcare-Impact-Analysis/
|
|-- 04_OBBB_Impact_Analysis.ipynb       # Main Jupyter Notebook (8 sections)
|-- OBBB_Impact_Dashboard_final.html    # Interactive HTML dashboard
|-- OBBB_PROJECT_DOCUMENTATION.md       # Full project documentation
|-- 00_DATA_SOURCES.md                  # Data sources with citations and links
|-- 01_data_collection.py               # Data retrieval code (Plans A, B, C)
|-- 02_data_cleaning.py                 # Data cleaning and processing pipeline
|-- 03_data_visualization.py            # All four matplotlib chart functions
|-- README.md                           # This file
```

---

## Technology Stack

| Tool                     | Purpose                                         |
| ------------------------ | ----------------------------------------------- |
| Python 3.14              | Core programming language                       |
| pandas                   | Data manipulation and cleaning                  |
| NumPy                    | Numerical operations and trend line calculation |
| matplotlib               | All four professional static charts             |
| Jupyter Notebook         | Interactive analysis and documentation          |
| HTML / CSS / JavaScript  | Interactive dashboard structure and styling     |
| Chart.js                 | Charts inside the HTML dashboard                |
| requests / BeautifulSoup | Web scraping attempts (Plans A and B)           |

---

## Data Sources

All data comes from official government and nonpartisan policy research publications.

| Source                                                       | Publication                                                  | Date            |
| ------------------------------------------------------------ | ------------------------------------------------------------ | --------------- |
| [Congressional Budget Office](https://www.cbo.gov/publication/61569) | Estimated Budgetary Effects of Public Law 119-21             | July 21, 2025   |
| [Kaiser Family Foundation](https://www.kff.org/uninsured/how-will-the-2025-reconciliation-law-affect-the-uninsured-rate-in-each-state/) | How Will the 2025 Reconciliation Law Affect the Uninsured Rate in Each State? | August 20, 2025 |
| [Kaiser Family Foundation](https://www.kff.org)              | Allocating CBO Estimates of Federal Medicaid Spending Reductions Across the States | July 23, 2025   |
| [Center for Medicare Advocacy](https://www.medicareadvocacy.org) | Impact of the Big Bill on Medicare                           | July 24, 2025   |
| [Center for American Progress](https://www.americanprogress.org) | The Truth About the One Big Beautiful Bill Act's Cuts to Medicaid and Medicare | August 5, 2025  |

See [`00_DATA_SOURCES.md`](00_DATA_SOURCES.md) for the complete data source reference.

---

## How to Run

### Requirements

```bash
pip install pandas numpy matplotlib seaborn plotly requests beautifulsoup4
```

### Run the Notebook

1. Open `04_OBBB_Impact_Analysis.ipynb` in Jupyter Notebook
2. Select **Kernel --> Restart & Run All**
3. All four charts will render in sequence

### View the Dashboard

1. Download `OBBB_Impact_Dashboard_final.html`
2. Open it in Chrome, Edge, or Firefox
3. No internet connection or server required

### Run Individual Chart Functions

```python
from data_visualization import (
    chart1_funding_loss_bar,
    chart2_uninsured_rate_bar,
    chart3_coverage_breakdown_pie,
    chart4_scatter_plot
)

# Run any chart independently
chart1_funding_loss_bar(df_clean)
chart3_coverage_breakdown_pie()
```

---

## Project Documentation

Full step-by-step project documentation is available in [`OBBB_PROJECT_DOCUMENTATION.md`](OBBB_PROJECT_DOCUMENTATION.md), covering:

- Project overview and problem statement
- Data retrieval process (Plans A, B, and C)
- Data cleaning methodology
- Visualization design decisions
- Key findings and interpretation

---

*All figures are CBO projections as of August 2025. State-level figures are based on KFF allocations of CBO national totals.*
