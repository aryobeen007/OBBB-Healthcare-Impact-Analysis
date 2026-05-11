# Data Sources

## OBBB Healthcare Impact Analysis

All data used in this project was retrieved from the following official government and nonpartisan policy research publications. Every number in the Python datasets, Jupyter Notebook, and interactive dashboard traces directly back to one of these sources.

---

### 1. Congressional Budget Office (CBO)

**Official Website:** [cbo.gov](https://www.cbo.gov)

The CBO is the nonpartisan official budget and economic analysis agency of the U.S. Congress. All national-level financial projections in this project come from CBO published estimates.

| Publication | Date | Data Retrieved |
|---|---|---|
| [Estimated Budgetary Effects of Public Law 119-21](https://www.cbo.gov/publication/61569) | July 21, 2025 | $1.06T total health cuts, $990B Medicaid cuts, $325.6B work requirements savings, $191.1B provider tax freeze savings, $149.4B state-directed payments cap |
| [Health Coverage Projections](https://www.cbo.gov) | August 2025 | 11.8M people losing Medicaid, 2.1M losing ACA marketplace coverage, 14.2M total losing coverage |

---

### 2. Kaiser Family Foundation (KFF)

**Official Website:** [kff.org](https://www.kff.org)

KFF is a leading nonpartisan health policy research organization. KFF provided all state-level data used in this project by allocating CBO national totals across individual states based on Medicaid enrollment and spending shares.

| Publication | Date | Data Retrieved |
|---|---|---|
| [How Will the 2025 Reconciliation Law Affect the Uninsured Rate in Each State?](https://www.kff.org/uninsured/how-will-the-2025-reconciliation-law-affect-the-uninsured-rate-in-each-state/) | August 20, 2025 | Percentage point increase in uninsured rate for all 50 states + DC |
| [Allocating CBO's Estimates of Federal Medicaid Spending Reductions Across the States](https://www.kff.org) | July 23, 2025 | Federal Medicaid funding loss in billions for all 50 states + DC |
| [Status of Medicaid Expansion Decisions by State](https://www.kff.org/medicaid/issue-brief/status-of-state-medicaid-expansion-decisions-interactive-map/) | 2025 | Medicaid expansion status (Yes/No) for each state |

---

### 3. Center for Medicare Advocacy

**Official Website:** [medicareadvocacy.org](https://www.medicareadvocacy.org)

| Publication | Date | Data Retrieved |
|---|---|---|
| [Impact of the Big Bill on Medicare](https://www.medicareadvocacy.org) | July 24, 2025 | $120B SNAP food aid cuts figure |

---

### 4. Center for American Progress (CAP)

**Official Website:** [americanprogress.org](https://www.americanprogress.org)

| Publication | Date | Data Retrieved |
|---|---|---|
| [The Truth About the One Big Beautiful Bill Act's Cuts to Medicaid and Medicare](https://www.americanprogress.org) | August 5, 2025 | 300+ rural hospitals at immediate risk of closure |

---

## How Each Source Was Used in the Code

```python
# df_national -- 12 rows of national metrics
# Source for every value: CBO July 21 and August 2025

# df_states -- 50 rows of state-level metrics
# funding_loss_b    -> KFF July 23, 2025
# uninsured_pct     -> KFF August 20, 2025
# people_losing     -> KFF state shares applied to CBO national totals
# expansion         -> KFF Medicaid Expansion Status 2025
# severity          -> Calculated from the above metrics
```

---

*All figures are CBO projections as of August 2025.*
*State-level figures are KFF allocations of CBO national totals.*
*Data was entered manually from published reports after automated downloads were blocked by the source websites.*
