# ================================================================
# FILE:    03_data_visualization.py
# PROJECT: OBBB Healthcare Impact Analysis
# PURPOSE: Generate all four professional matplotlib visualizations
#
# CHARTS:
#   chart1_funding_loss_bar()      -- Top 15 states by funding loss
#   chart2_uninsured_rate_bar()    -- Top 25 states by uninsured rate
#   chart3_coverage_breakdown_pie()-- National coverage loss breakdown
#   chart4_scatter_plot()          -- Funding loss vs uninsured rate
#
# SHARED DESIGN:
#   Background    : #0F1117 (outer), #1A1F35 (chart area)
#   Color encoding: Critical=#DC2626, High=#F97316,
#                   Medium=#EAB308, Lower=#22C55E
#   Accent        : #A78BFA (purple) for reference lines
# ================================================================

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.lines as mlines
import numpy as np
from matplotlib.patches import Patch


# ── Shared color map used across all four charts ───────────────
COLOR_MAP = {
    "Critical": "#DC2626",   # red
    "High":     "#F97316",   # orange
    "Medium":   "#EAB308",   # yellow
    "Lower":    "#22C55E"    # green
}


# ================================================================
# CHART 1 -- VERTICAL BAR CHART
# Question: Which states lose the most federal Medicaid funding?
# ================================================================

def chart1_funding_loss_bar(df_clean):
    """
    Draws a vertical bar chart of the top 15 states by federal
    Medicaid funding loss under OBBB (2025-2034).

    Parameters:
        df_clean (DataFrame): Cleaned and sorted state dataset
    """

    # ── Prepare data ──────────────────────────────────────────
    # df_clean is already sorted by severity then funding loss
    # so the top 15 rows are the most impacted states
    top15 = df_clean.head(15).copy()

    # Build a color list -- one color per bar based on severity
    colors = [COLOR_MAP[s] for s in top15["severity"]]

    # ── Create figure ─────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 7))

    # ── Draw bars ─────────────────────────────────────────────
    bars = ax.bar(
        top15["state"],          # x axis: state names
        top15["funding_loss_b"], # y axis: funding loss in billions
        color=colors,
        edgecolor="white",
        linewidth=0.8,
        width=0.7
    )

    # ── Add value labels above each bar ───────────────────────
    # zip() pairs each bar object with its corresponding value
    for bar, value in zip(bars, top15["funding_loss_b"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # x: center of bar
            bar.get_height() + 1,                # y: just above bar
            "$" + str(int(value)) + "B",
            ha="center", va="bottom",
            fontsize=9, fontweight="bold", color="white"
        )

    # ── Apply dark theme ──────────────────────────────────────
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#1A1F35")

    ax.set_title(
        "Top 15 States - Federal Medicaid Funding Loss Under OBBB\n"
        "10-Year Projection 2025-2034  |  Source: CBO and KFF 2025",
        fontsize=14, fontweight="bold", color="white", pad=20
    )
    ax.set_xlabel("State", fontsize=11, color="#94A3B8", labelpad=10)
    ax.set_ylabel("Federal Funding Loss (Billions USD)",
                  fontsize=11, color="#94A3B8", labelpad=10)

    ax.tick_params(colors="white")
    plt.xticks(rotation=35, ha="right", fontsize=9, color="white")
    plt.yticks(color="white")

    # Format y-axis as "$50B" instead of plain "50"
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, p: "$" + str(int(x)) + "B")
    )

    ax.grid(axis="y", color="#2D3456", linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_edgecolor("#2D3456")

    # ── Add legend ────────────────────────────────────────────
    legend_items = [
        Patch(facecolor="#DC2626", label="Critical Impact"),
        Patch(facecolor="#F97316", label="High Impact"),
        Patch(facecolor="#EAB308", label="Medium Impact"),
        Patch(facecolor="#22C55E", label="Lower Impact")
    ]
    ax.legend(handles=legend_items, loc="upper right",
              framealpha=0.3, facecolor="#1A1F35",
              edgecolor="#2D3456", labelcolor="white", fontsize=9)

    plt.tight_layout()
    plt.show()
    print("Chart 1 complete!")


# ================================================================
# CHART 2 -- HORIZONTAL BAR CHART
# Question: Which states have the highest uninsured rate increase?
# ================================================================

def chart2_uninsured_rate_bar(df_clean):
    """
    Draws a horizontal bar chart of the top 25 states by uninsured
    rate increase under OBBB.

    Horizontal orientation chosen because state names are long --
    horizontal bars provide space for readable left-side labels.

    Parameters:
        df_clean (DataFrame): Cleaned and sorted state dataset
    """

    # ── Prepare data ──────────────────────────────────────────
    # Sort ascending and take tail(25) to get the 25 HIGHEST values
    # appearing at the TOP of the horizontal chart
    df_uninsured = df_clean.sort_values(
        "uninsured_pct", ascending=True
    ).tail(25)

    colors = [COLOR_MAP[s] for s in df_uninsured["severity"]]

    # ── Create figure ─────────────────────────────────────────
    # Taller than wide because 25 states stack vertically
    fig, ax = plt.subplots(figsize=(12, 10))

    # ── Draw horizontal bars ──────────────────────────────────
    bars = ax.barh(
        df_uninsured["state"],
        df_uninsured["uninsured_pct"],
        color=colors,
        edgecolor="white", linewidth=0.6, height=0.7
    )

    # ── Add value labels at end of each bar ───────────────────
    for bar, value in zip(bars, df_uninsured["uninsured_pct"]):
        ax.text(
            value + 0.05,                             # just right of bar
            bar.get_y() + bar.get_height() / 2,       # middle of bar
            "+" + str(value) + "%",
            va="center", ha="left",
            fontsize=8, color="white", fontweight="bold"
        )

    # ── Add national average reference line ───────────────────
    # Purple dashed vertical line shows where the national average falls
    national_avg = round(df_clean["uninsured_pct"].mean(), 2)
    ax.axvline(
        x=national_avg,
        color="#A78BFA",
        linewidth=1.5,
        linestyle="--",
        label="National Average +" + str(national_avg) + "%"
    )

    # ── Apply dark theme ──────────────────────────────────────
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#1A1F35")

    ax.set_title(
        "Top 25 States - Uninsured Rate Increase Under OBBB\n"
        "Percentage Point Increase by 2034  |  Source: KFF August 2025",
        fontsize=13, fontweight="bold", color="white", pad=20
    )
    ax.set_xlabel("Percentage Point Increase in Uninsured Rate",
                  fontsize=11, color="#94A3B8", labelpad=10)

    ax.tick_params(colors="white")
    plt.xticks(color="white")
    plt.yticks(fontsize=9, color="white")

    # Format x-axis as "+3.5%" instead of plain "3.5"
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, p: "+" + str(round(x, 1)) + "%")
    )

    ax.grid(axis="x", color="#2D3456", linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_edgecolor("#2D3456")

    # ── Add legend ────────────────────────────────────────────
    legend_items = [
        Patch(facecolor="#DC2626", label="Critical Impact"),
        Patch(facecolor="#F97316", label="High Impact"),
        Patch(facecolor="#EAB308", label="Medium Impact"),
        Patch(facecolor="#22C55E", label="Lower Impact"),
        mlines.Line2D([], [], color="#A78BFA", linewidth=1.5,
                      linestyle="--",
                      label="National Average +" + str(national_avg) + "%")
    ]
    ax.legend(handles=legend_items, loc="lower right",
              framealpha=0.3, facecolor="#1A1F35",
              edgecolor="#2D3456", labelcolor="white", fontsize=9)

    plt.tight_layout()
    plt.show()
    print("Chart 2 complete!")
    print("National average: +" + str(national_avg) + "%")
    print("Highest: Washington state at +4.8%")


# ================================================================
# CHART 3 -- PIE CHART WITH DETAIL PANEL
# Question: How does the 14.2M coverage loss break down by group?
# ================================================================

def chart3_coverage_breakdown_pie():
    """
    Draws a two-panel figure: pie chart on the left showing
    national coverage loss breakdown, detail panel on the right
    with exact counts and percentages per category.

    Data sourced directly from CBO August 2025.
    No DataFrame parameter needed -- uses hardcoded CBO figures.
    """

    # ── Data -- CBO August 2025 ───────────────────────────────
    categories = [
        "Medicaid Loss\n(OBBB Provisions)",
        "ACA Marketplace\n(OBBB Provisions)",
        "ACA Tax Credit\nExpiry",
        "Medicare and\nOther Changes"
    ]
    values = [7.5, 2.1, 4.2, 0.4]  # millions of people
    colors = ["#DC2626", "#F97316", "#EAB308", "#3B82F6"]

    # explode pulls the largest slice (Medicaid) slightly outward
    explode = (0.05, 0.02, 0.02, 0.02)

    # ── Create two-panel figure ───────────────────────────────
    # gridspec_kw controls the relative width of each panel
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(14, 7),
        gridspec_kw={"width_ratios": [1.5, 1]}
    )

    # ── Draw pie chart ────────────────────────────────────────
    # autopct automatically calculates and formats percentages
    # pctdistance positions labels 75% from the center
    wedges, texts, autotexts = ax1.pie(
        values, explode=explode, colors=colors,
        autopct="%1.1f%%", startangle=90, pctdistance=0.75,
        wedgeprops={"edgecolor": "#0F1117", "linewidth": 2}
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
        autotext.set_fontsize(11)

    # ── Add center text (donut style) ─────────────────────────
    ax1.text(0, 0.1, "14.2M",
             ha="center", va="center",
             fontsize=28, fontweight="bold", color="white")
    ax1.text(0, -0.2, "Total People\nLosing Coverage",
             ha="center", va="center", fontsize=10, color="#94A3B8")

    # ── Build right detail panel ──────────────────────────────
    ax2.set_facecolor("#1A1F35")
    ax2.axis("off")

    ax2.text(0.1, 0.95, "Coverage Loss Breakdown",
             transform=ax2.transAxes,
             fontsize=13, fontweight="bold", color="white", va="top")
    ax2.text(0.1, 0.87, "Source: CBO August 2025",
             transform=ax2.transAxes, fontsize=9, color="#64748B", va="top")

    # Each row: colored dot + label + count + percentage
    row_items = [
        ("Medicaid Loss - OBBB",   "7.5M people", "52.8%", "#DC2626"),
        ("ACA Marketplace - OBBB", "2.1M people", "14.8%", "#F97316"),
        ("ACA Tax Credit Expiry",  "4.2M people", "29.6%", "#EAB308"),
        ("Medicare and Other",     "0.4M people",  "2.8%", "#3B82F6"),
    ]

    y_pos = 0.72
    for label, count, pct, color in row_items:
        ax2.add_patch(plt.Circle(
            (0.08, y_pos), 0.025, transform=ax2.transAxes,
            color=color, zorder=5
        ))
        ax2.text(0.16, y_pos + 0.01, label,
                 transform=ax2.transAxes, fontsize=10,
                 fontweight="bold", color="white", va="center")
        ax2.text(0.16, y_pos - 0.04, count + "  |  " + pct + " of total",
                 transform=ax2.transAxes, fontsize=9,
                 color="#94A3B8", va="center")
        y_pos -= 0.18

    ax2.text(0.1, 0.08, "TOTAL: 14.2 Million Americans",
             transform=ax2.transAxes, fontsize=11,
             fontweight="bold", color="#A78BFA", va="center")
    ax2.text(0.1, 0.02, "will lose health coverage by 2034",
             transform=ax2.transAxes, fontsize=9, color="#64748B", va="center")

    # ── Apply dark theme ──────────────────────────────────────
    fig.patch.set_facecolor("#0F1117")
    ax1.set_facecolor("#0F1117")

    fig.suptitle(
        "OBBB National Health Coverage Loss Breakdown\n"
        "14.2 Million Americans Projected to Lose Coverage by 2034",
        fontsize=14, fontweight="bold", color="white", y=1.02
    )

    plt.tight_layout()
    plt.show()
    print("Chart 3 complete!")
    print("Largest share: Medicaid (52.8%) -- 7.5M people")
    print("Second: ACA Tax Credit Expiry (29.6%) -- 4.2M people")


# ================================================================
# CHART 4 -- SCATTER PLOT
# Question: Does funding loss correlate with uninsured rate increase?
# ================================================================

def chart4_scatter_plot(df_clean):
    """
    Draws a multi-dimensional scatter plot with four encoded variables:
        x position  = federal funding loss (billions)
        y position  = uninsured rate increase (percentage points)
        dot size    = people losing coverage (sqrt-scaled)
        dot color   = severity level

    Also includes a trend line (np.polyfit degree 1) and quadrant
    reference lines at the national averages.

    Parameters:
        df_clean (DataFrame): Cleaned and sorted state dataset
    """

    df_scatter = df_clean.copy()

    # ── Set up colors and dot sizes ───────────────────────────
    dot_colors = [COLOR_MAP[s] for s in df_scatter["severity"]]

    # np.sqrt() prevents very large states from dominating the chart
    # Without sqrt, California (1800K) would be ~200x larger than Wyoming (9K)
    # With sqrt, sizes remain meaningful but visually balanced
    dot_sizes = np.sqrt(df_scatter["people_losing_thousands"]) * 30

    # ── Create figure ─────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 8))

    # ── Draw scatter dots ─────────────────────────────────────
    # alpha=0.85 = slightly transparent so overlapping dots remain visible
    ax.scatter(
        df_scatter["funding_loss_b"],
        df_scatter["uninsured_pct"],
        s=dot_sizes,
        c=dot_colors,
        alpha=0.85,
        edgecolors="white",
        linewidths=0.8,
        zorder=5
    )

    # ── Label high-impact states ──────────────────────────────
    # Only label states above key thresholds to avoid clutter
    for _, row in df_scatter.iterrows():
        if row["funding_loss_b"] >= 18 or row["uninsured_pct"] >= 3.8:
            ax.annotate(
                row["state"],
                xy=(row["funding_loss_b"], row["uninsured_pct"]),
                xytext=(8, 4),
                textcoords="offset points",
                fontsize=8, color="white", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#1A1F35",
                          edgecolor="#2D3456", alpha=0.8)
            )

    # ── Calculate and draw trend line ─────────────────────────
    # np.polyfit(x, y, 1) fits a degree-1 straight line through the data
    # Returns [slope, intercept] of the best-fit line
    z = np.polyfit(df_scatter["funding_loss_b"], df_scatter["uninsured_pct"], 1)
    p = np.poly1d(z)

    # 100 evenly spaced x values for a smooth line
    x_line = np.linspace(
        df_scatter["funding_loss_b"].min(),
        df_scatter["funding_loss_b"].max(),
        100
    )
    ax.plot(x_line, p(x_line),
            color="#A78BFA", linewidth=2, linestyle="--",
            alpha=0.8, zorder=3)

    # ── Add quadrant reference lines at national averages ─────
    avg_funding   = df_scatter["funding_loss_b"].mean()
    avg_uninsured = df_scatter["uninsured_pct"].mean()

    ax.axhline(y=avg_uninsured, color="#60A5FA", linewidth=1,
               linestyle=":", alpha=0.6)
    ax.axvline(x=avg_funding,   color="#34D399", linewidth=1,
               linestyle=":", alpha=0.6)

    # ── Add quadrant labels ───────────────────────────────────
    ax.text(avg_funding + 2, avg_uninsured + 0.15,
            "HIGH FUNDING LOSS\nHIGH UNINSURED INCREASE",
            fontsize=7, color="#94A3B8", alpha=0.7)
    ax.text(1, avg_uninsured + 0.15,
            "LOWER FUNDING LOSS\nHIGH UNINSURED INCREASE",
            fontsize=7, color="#94A3B8", alpha=0.7)
    ax.text(avg_funding + 2, 1.65,
            "HIGH FUNDING LOSS\nLOWER UNINSURED INCREASE",
            fontsize=7, color="#94A3B8", alpha=0.7)
    ax.text(1, 1.65,
            "LOWER FUNDING LOSS\nLOWER UNINSURED INCREASE",
            fontsize=7, color="#94A3B8", alpha=0.7)

    # ── Apply dark theme ──────────────────────────────────────
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#1A1F35")

    ax.set_title(
        "OBBB Impact - Federal Funding Loss vs Uninsured Rate Increase by State\n"
        "Dot size = people losing coverage  |  Color = severity level  "
        "|  Source: CBO and KFF 2025",
        fontsize=13, fontweight="bold", color="white", pad=20
    )
    ax.set_xlabel("Federal Medicaid Funding Loss (Billions USD)",
                  fontsize=11, color="#94A3B8", labelpad=10)
    ax.set_ylabel("Uninsured Rate Increase (Percentage Points by 2034)",
                  fontsize=11, color="#94A3B8", labelpad=10)

    ax.tick_params(colors="white")
    plt.xticks(color="white")
    plt.yticks(color="white")

    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, p: "$" + str(int(x)) + "B"))
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, p: "+" + str(round(x, 1)) + "%"))

    ax.grid(color="#2D3456", linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_edgecolor("#2D3456")

    # ── Add legend ────────────────────────────────────────────
    legend_items = [
        Patch(facecolor="#DC2626", label="Critical Impact"),
        Patch(facecolor="#F97316", label="High Impact"),
        Patch(facecolor="#EAB308", label="Medium Impact"),
        Patch(facecolor="#22C55E", label="Lower Impact"),
        mlines.Line2D([], [], color="#A78BFA", linewidth=2,
                      linestyle="--", label="Trend Line"),
        mlines.Line2D([], [], color="#60A5FA", linewidth=1,
                      linestyle=":", label="Avg Uninsured Increase"),
        mlines.Line2D([], [], color="#34D399", linewidth=1,
                      linestyle=":", label="Avg Funding Loss")
    ]
    ax.legend(handles=legend_items, loc="upper left",
              framealpha=0.3, facecolor="#1A1F35",
              edgecolor="#2D3456", labelcolor="white", fontsize=9)

    ax.text(0.98, 0.05,
            "Note: Dot size represents\nnumber of people losing coverage",
            transform=ax.transAxes, fontsize=8, color="#64748B",
            ha="right", va="bottom")

    plt.tight_layout()
    plt.show()

    print("Chart 4 complete!")
    print()
    print("HOW TO READ THIS CHART:")
    print("  Each dot = one U.S. state")
    print("  Further RIGHT  = more federal funding lost")
    print("  Further UP     = higher uninsured rate increase")
    print("  Bigger dot     = more people losing coverage")
    print("  Red dots       = Critical severity states")
    print("  Dashed line    = overall trend direction")


# ================================================================
# MAIN -- Generate all four charts in sequence
# ================================================================

if __name__ == "__main__":
    from src.data_collection import build_state_dataset
    from src.data_cleaning import clean_state_dataset

    print("OBBB VISUALIZATION PIPELINE")
    print("=" * 50)
    print()

    df_states = build_state_dataset()
    df_clean  = clean_state_dataset(df_states)

    print()
    print("Generating Chart 1...")
    chart1_funding_loss_bar(df_clean)

    print("Generating Chart 2...")
    chart2_uninsured_rate_bar(df_clean)

    print("Generating Chart 3...")
    chart3_coverage_breakdown_pie()

    print("Generating Chart 4...")
    chart4_scatter_plot(df_clean)

    print()
    print("All four charts complete!")
