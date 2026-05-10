# tests/test_phase3.py
from data.powerbi_connector import PowerBIConnector
from engine.anomaly_detector import AnomalyDetector

def test_anomaly_detection():
    connector = PowerBIConnector()
    df = connector.fetch_weekly_sales()

    detector = AnomalyDetector()
    report = detector.detect(df)

    print(f"\nWeek analyzed: {report.week_analyzed}")
    print(f"Total anomalies: {report.total_anomalies}")
    print(f"High severity:   {report.high_severity_count}")
    print(f"Medium severity: {report.medium_severity_count}")
    print(f"Overall sales:   ${report.overall_week_sales:,.2f}")
    print(f"WoW change:      {report.wow_change_pct:+.1f}%")
    print(f"\nTop segment:    {report.top_segment}")
    print(f"Bottom segment: {report.bottom_segment}")

    print(f"\n-- Anomaly Details --")
    for a in report.anomalies:
        print(f"  [{a.severity}] {a.description}")

    assert report.total_anomalies >= 1, "Should detect at least 1 anomaly in mock data"
    assert all(a.severity in ["HIGH", "MEDIUM", "LOW"] for a in report.anomalies)
    print("\nAll assertions passed.")

if __name__ == "__main__":
    test_anomaly_detection()
