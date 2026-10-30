"""expenditure_anomaly_detector.py - Missouri expenditure anomaly project.

Author: Angie Crews
Date: 2026-10-29

This project analyzes Missouri state expenditure data to identify
unusually large travel expenditures that may warrant further review.
"""

from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import polars as pl

# === DECLARE FILE PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"
IMAGES_DIR: Final[Path] = ROOT_DIR / "docs" / "images"

DATA_FILE: Final[Path] = DATA_DIR / "2026_State_Expenditures_20261029.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "missouri_travel_anomalies.csv"
CHART_FILE: Final[Path] = IMAGES_DIR / "travel_anomalies_by_agency.png"


def main() -> None:
    """Analyze Missouri travel expenditures and identify anomalies."""
    # ----------------------------------------------------
    # STEP 1: LOAD THE MISSOURI EXPENDITURE DATA
    # ----------------------------------------------------

    df: pl.DataFrame = pl.read_csv(DATA_FILE)

    print(f"Loaded {df.height:,} expenditure records")

    # ----------------------------------------------------
    # STEP 2: CONVERT PAYMENT AMOUNTS TO NUMERIC VALUES
    # ----------------------------------------------------

    # Keep the original Payments Total column and create
    # a numeric version that can be used for calculations.
    df = df.with_columns(
        pl.col("Payments Total")
        .str.replace_all(",", "")
        .cast(pl.Float64)
        .alias("payment_amount")
    )

    # ----------------------------------------------------
    # STEP 3: KEEP ONLY TRAVEL EXPENDITURES
    # ----------------------------------------------------

    travel_df = df.filter(pl.col("Category Description") == "TRAVEL")

    # ----------------------------------------------------
    # STEP 4: CALCULATE THE ANOMALY THRESHOLD
    # ----------------------------------------------------

    # Use the 99th percentile of travel expenditures
    # as the threshold for unusually large payments.
    threshold = travel_df.select(pl.col("payment_amount").quantile(0.99)).item()

    # ----------------------------------------------------
    # STEP 5: IDENTIFY UNUSUALLY LARGE TRAVEL EXPENDITURES
    # ----------------------------------------------------

    # Flag travel expenditures at or above the 99th percentile.
    anomalies_df = travel_df.filter(pl.col("payment_amount") >= threshold)

    # ----------------------------------------------------
    # STEP 6: SUMMARIZE ANOMALIES BY AGENCY
    # ----------------------------------------------------

    # Count flagged travel expenditures by agency.
    agency_counts = (
        anomalies_df.group_by("Agency Name").len().sort("len", descending=True)
    )

    # Keep the top 10 agencies for the visualization.
    top_agencies = agency_counts.head(10)

    # ----------------------------------------------------
    # STEP 7: SAVE ANOMALIES AS EVIDENCE
    # ----------------------------------------------------

    # Ensure the artifacts folder exists.
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # Save the flagged records as a CSV file.
    anomalies_df.write_csv(OUTPUT_FILE)

    # ----------------------------------------------------
    # STEP 8: CREATE THE VISUALIZATION
    # ----------------------------------------------------

    # Ensure the documentation images folder exists.
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Reverse the order so the agency with the largest count
    # appears at the top of the horizontal bar chart.
    agency_names = top_agencies["Agency Name"].to_list()[::-1]
    anomaly_counts = top_agencies["len"].to_list()[::-1]

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(agency_names, anomaly_counts)

    ax.set_title("Top 10 Agencies by Flagged Travel Expenditures")
    ax.set_xlabel("Number of Flagged Expenditures")
    ax.set_ylabel("Agency")

    # Add the count at the end of each bar.
    for bar, count in zip(bars, anomaly_counts, strict=True):
        ax.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            str(count),
            va="center",
        )

    fig.tight_layout()
    fig.savefig(CHART_FILE, dpi=150)
    plt.close(fig)

    # ----------------------------------------------------
    # STEP 9: DISPLAY RESULTS
    # ----------------------------------------------------

    print(f"Travel expenditure records: {travel_df.height:,}")
    print(f"99th percentile threshold: ${threshold:,.2f}")
    print(f"Anomalies found: {anomalies_df.height:,}")
    print(f"Results saved to: {OUTPUT_FILE}")
    print(f"Chart saved to: {CHART_FILE}")
    print("Anomalies by agency:")
    print(agency_counts)


if __name__ == "__main__":
    main()
