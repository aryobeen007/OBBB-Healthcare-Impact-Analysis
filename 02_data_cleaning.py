# ================================================================
# FILE:    02_data_cleaning.py
# PROJECT: OBBB Healthcare Impact Analysis
# PURPOSE: Clean and process the raw state-level dataset into
#          an analysis-ready DataFrame for visualization
#
# INPUT:   df_states (from 01_data_collection.py)
# OUTPUT:  df_clean  (validated, enriched, and sorted DataFrame)
#
# CLEANING STEPS:
#   1. Validate both datasets for completeness
#   2. Create a working copy of df_states
#   3. Add calculated columns for chart-ready formatting
#   4. Map severity text labels to numeric scores
#   5. Sort by severity score then funding loss
# ================================================================

import pandas as pd
from src.data_collection import build_national_dataset, build_state_dataset


# ================================================================
# STEP 1 -- DATA VALIDATION
# Run these checks before any transformation begins
# ================================================================

def validate_datasets(df_national, df_states):
    """
    Validates both datasets for completeness and basic correctness.
    Prints a full validation report.
    Returns True if all checks pass.
    """

    print("DATA VALIDATION REPORT")
    print("=" * 40)
    print()

    all_passed = True

    # ── National dataset checks ───────────────────────────────
    print("NATIONAL DATASET")
    print("  Rows         : " + str(len(df_national)))
    print("  Columns      : " + str(list(df_national.columns)))

    # isnull().any().any() checks every single cell for missing values
    # False means no missing values -- the dataset is complete
    missing_national = df_national.isnull().any().any()
    print("  Missing vals : " + str(missing_national))

    if missing_national:
        print("  WARNING -- Missing values found in national dataset")
        all_passed = False

    print()

    # ── State dataset checks ──────────────────────────────────
    print("STATE DATASET")
    print("  Rows         : " + str(len(df_states)))
    print("  Columns      : " + str(list(df_states.columns)))

    missing_states = df_states.isnull().any().any()
    print("  Missing vals : " + str(missing_states))

    if missing_states:
        print("  WARNING -- Missing values found in state dataset")
        all_passed = False

    # Check all 50 states + DC are present
    if len(df_states) != 51:
        print("  WARNING -- Expected 51 rows (50 states + DC), found: "
              + str(len(df_states)))
        all_passed = False

    print()

    # ── Statistical summary ───────────────────────────────────
    # describe() shows min, max, mean, and quartiles for each numeric column
    # This helps spot any obviously incorrect values
    print("SUMMARY STATISTICS -- State Dataset")
    print(df_states.describe().round(2))
    print()

    # ── Category counts ───────────────────────────────────────
    # value_counts() tallies how many states fall in each severity level
    print("STATES BY SEVERITY LEVEL")
    print(df_states["severity"].value_counts())
    print()

    print("STATES BY MEDICAID EXPANSION STATUS")
    print(df_states["expansion"].value_counts())
    print()

    print("=" * 40)

    if all_passed:
        print("VALIDATION PASSED -- Data is clean and ready")
    else:
        print("VALIDATION FAILED -- See warnings above")

    return all_passed


# ================================================================
# STEP 2-5 -- CLEANING PIPELINE
# ================================================================

def clean_state_dataset(df_states):
    """
    Applies the full cleaning pipeline to the state dataset.
    Returns df_clean -- the analysis-ready DataFrame.

    Transformations applied:
        - Working copy created (original preserved)
        - people_losing_thousands: raw count / 1000 for chart labels
        - funding_loss_m: billions * 1000 = millions for small states
        - severity_score: text -> integer for correct sort behavior
        - Sorted: severity_score desc, funding_loss_b desc
        - Index reset: clean sequential row numbers after sort
    """

    # ── Step 2: Create working copy ───────────────────────────
    # Always work on a copy -- never modify the original raw data
    df_clean = df_states.copy()

    # ── Step 3: Add calculated columns ────────────────────────

    # people_losing_thousands
    # Divides raw coverage loss by 1000 for cleaner chart labels
    # Example: 1,800,000 becomes 1800.0 (thousands)
    df_clean["people_losing_thousands"] = (
        df_clean["people_losing"] / 1000
    ).round(1)

    # funding_loss_m
    # Converts billions to millions for small-state comparisons
    # Example: 1 billion becomes 1000.0 million
    df_clean["funding_loss_m"] = (
        df_clean["funding_loss_b"] * 1000
    ).round(0)

    # ── Step 4: Map severity text to numeric score ─────────────
    # Python cannot sort text labels in the correct severity order
    # by default ("Critical", "High", "Low" would sort alphabetically)
    # We convert text to integers so sort works correctly
    # .map() replaces each text value using the dictionary as a lookup
    severity_map = {
        "Critical": 4,   # most severe
        "High":     3,
        "Medium":   2,
        "Lower":    1    # least severe
    }

    df_clean["severity_score"] = df_clean["severity"].map(
        severity_map
    ).astype(int)   # explicit int cast prevents category-type sort errors

    # ── Step 5: Sort ──────────────────────────────────────────
    # Sort by severity_score descending first
    # then by funding_loss_b descending within each severity group
    # This ensures most critically impacted states appear at the top
    df_clean = df_clean.sort_values(
        ["severity_score", "funding_loss_b"],
        ascending=[False, False]
    ).reset_index(drop=True)   # drop=True discards the old index numbers

    return df_clean


# ================================================================
# MAIN -- Run the full cleaning pipeline
# ================================================================

if __name__ == "__main__":
    print("OBBB DATA CLEANING PIPELINE")
    print("=" * 50)
    print()

    # Load raw datasets
    df_national = build_national_dataset()
    df_states   = build_state_dataset()
    print()

    # Validate before cleaning
    validate_datasets(df_national, df_states)
    print()

    # Run cleaning pipeline
    print("Running cleaning pipeline...")
    df_clean = clean_state_dataset(df_states)

    print()
    print("CLEANING COMPLETE")
    print("=" * 50)
    print("Final shape: " + str(df_clean.shape[0]) + " rows x "
          + str(df_clean.shape[1]) + " columns")
    print()
    print("Columns in df_clean:")
    for col in df_clean.columns:
        print("  " + col.ljust(28) + str(df_clean[col].dtype))
    print()
    print("TOP 5 MOST IMPACTED STATES:")
    print()
    print(df_clean[[
        "state", "funding_loss_b", "uninsured_pct",
        "people_losing_thousands", "severity"
    ]].head().to_string(index=False))
