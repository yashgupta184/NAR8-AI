# data/mock_sales_data.py
"""
NAR8 AI — Mock Sales Data Generator

Generates realistic weekly sales data that exactly mimics what the
Power BI REST API would return from a real semantic model.

Why mock data?
  - Lets the project work without a real Power BI account
  - Gives full control over the data (we can plant specific anomalies)
  - Swapping to real API data requires only changing USE_MOCK_DATA=false
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config.settings import Config


def generate_mock_sales_data(
    weeks: int = None,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates a realistic weekly sales DataFrame.

    Planted anomalies (intentional — so detection always has something to find):
      - Week 8: Electronics – North → 145% sales SPIKE (flash sale event)
      - Week 10: Apparel – South → 72% sales DROP (supply chain issue)
      - Week 12: Sports – West → 65% sales SPIKE (influencer campaign)

    Args:
        weeks: Number of weeks to generate. Defaults to Config.WEEKS_OF_DATA (13)
        seed: Random seed for reproducibility

    Returns:
        pandas DataFrame with columns:
        week_start_date, week_number, category, region,
        sales_amount, units_sold, avg_order_value, returns_amount
    """
    if weeks is None:
        weeks = Config.WEEKS_OF_DATA

    np.random.seed(seed)

    # Base weekly sales per category (realistic retail numbers in USD)
    BASE_SALES = {
        "Electronics":   85000,
        "Apparel":       42000,
        "Home & Garden": 31000,
        "Sports":        28000,
    }

    # Regional multipliers (North is strongest market)
    REGION_FACTOR = {"North": 1.20, "South": 0.90, "West": 1.10}

    # Start date: 13 weeks ago from a fixed reference date
    base_date = datetime(2025, 1, 6)  # A Monday

    records = []

    for week_num in range(weeks):
        week_date = base_date + timedelta(weeks=week_num)

        for category in Config.PRODUCT_CATEGORIES:
            for region in Config.REGIONS:

                # Natural random variation week to week (±15%)
                variation = np.random.normal(1.0, 0.12)

                # Slight upward trend over time (0.8% growth per week)
                trend = 1.0 + (week_num * 0.008)

                # Seasonal effect — slight dip in middle weeks
                seasonal = 1.0 - 0.04 * abs(week_num - (weeks / 2)) / (weeks / 2)

                # ── PLANT ANOMALY 1 ──────────────────────────────
                # Week 8 (index 7): Electronics North — massive spike
                if week_num == 7 and category == "Electronics" and region == "North":
                    variation = 2.45   # +145% above normal

                # ── PLANT ANOMALY 2 ──────────────────────────────
                # Week 10 (index 9): Apparel South — sharp drop
                if week_num == 9 and category == "Apparel" and region == "South":
                    variation = 0.28   # -72% below normal

                # ── PLANT ANOMALY 3 ──────────────────────────────
                # Week 12 (index 11): Sports West — significant spike
                if week_num == 11 and category == "Sports" and region == "West":
                    variation = 1.65   # +65% above normal

                # Calculate final sales
                sales = round(
                    BASE_SALES[category]
                    * variation
                    * trend
                    * seasonal
                    * REGION_FACTOR[region],
                    2
                )
                sales = max(sales, 500)  # Floor at $500

                # Derived metrics
                avg_price = np.random.uniform(45, 150)
                units = max(1, int(sales / avg_price))
                avg_order = round(sales / units, 2)
                returns = round(sales * np.random.uniform(0.01, 0.06), 2)

                records.append({
                    "week_start_date": week_date,
                    "week_number":     week_num + 1,
                    "category":        category,
                    "region":          region,
                    "sales_amount":    sales,
                    "units_sold":      units,
                    "avg_order_value": avg_order,
                    "returns_amount":  returns,
                })

    df = pd.DataFrame(records)
    df["week_start_date"] = pd.to_datetime(df["week_start_date"])
    df = df.sort_values(["week_start_date", "category", "region"]).reset_index(drop=True)

    return df


def get_current_week(df: pd.DataFrame) -> pd.DataFrame:
    """Returns only the most recent week's data."""
    return df[df["week_start_date"] == df["week_start_date"].max()].copy()


def get_previous_week(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the second most recent week's data."""
    weeks = sorted(df["week_start_date"].unique())
    if len(weeks) < 2:
        return pd.DataFrame()
    return df[df["week_start_date"] == weeks[-2]].copy()


def get_historical_baseline(df: pd.DataFrame, lookback: int = 8) -> pd.DataFrame:
    """Returns historical data (excluding current week) for baseline comparison."""
    all_weeks = sorted(df["week_start_date"].unique())
    if len(all_weeks) <= 1:
        return pd.DataFrame()
    historical_weeks = all_weeks[-(lookback + 1):-1]  # Exclude current week
    return df[df["week_start_date"].isin(historical_weeks)].copy()
