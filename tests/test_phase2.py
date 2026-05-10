# tests/test_phase2.py
from data.powerbi_connector import PowerBIConnector
from data.mock_sales_data import get_current_week, get_historical_baseline

def test_data_layer():
    connector = PowerBIConnector()
    df = connector.fetch_weekly_sales()

    print(f"\nData loaded: {len(df)} rows")
    print(f"Weeks: {df['week_start_date'].nunique()}")
    print(f"Categories: {df['category'].unique().tolist()}")
    print(f"Regions: {df['region'].unique().tolist()}")
    print(f"\nSample rows:")
    print(df.head(6).to_string())

    current = get_current_week(df)
    print(f"\nCurrent week total sales: ${current['sales_amount'].sum():,.2f}")

    baseline = get_historical_baseline(df)
    print(f"Baseline rows: {len(baseline)}")

    # Sanity checks
    assert len(df) == 156, f"Expected 156 rows, got {len(df)}"
    assert df['sales_amount'].min() > 0, "Sales amount should never be 0 or negative"
    assert df['week_start_date'].nunique() == 13, "Should have 13 unique weeks"
    print("\nAll assertions passed.")

if __name__ == "__main__":
    test_data_layer()
