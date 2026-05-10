# tests/test_phase4.py
import json
from data.powerbi_connector import PowerBIConnector
from engine.anomaly_detector import AnomalyDetector
from engine.llm_narrator import LLMNarrator

def test_narrative_generation():
    print("1. Fetching mock data...")
    connector = PowerBIConnector()
    df = connector.fetch_weekly_sales()

    print("2. Running anomaly detection...")
    detector = AnomalyDetector()
    report = detector.detect(df)
    
    print(f"   Found {report.total_anomalies} anomalies.")

    print("3. Generating AI narrative...")
    narrator = LLMNarrator()
    narrative_dict = narrator.generate_narrative(report)

    print("\n[SUCCESS] Narrative successfully generated and parsed into JSON!")
    print("\n--- Executive Summary ---")
    print(f"Headline: {narrative_dict['executive_summary']['headline']}")
    print(f"TLDR:     {narrative_dict['executive_summary']['tldr']}")
    print(f"Sentiment:{narrative_dict['executive_summary']['sentiment']}")
    
    print("\n--- Detected Anomalies (Slide 3) ---")
    for card in narrative_dict['slide_3_anomalies']['cards']:
        print(f"[{card['severity']}] {card['segment']}: {card['finding']}")
        print(f"  -> Hypothesis: {card['hypothesis']}")
        print(f"  -> Action:     {card['action']}\n")

if __name__ == "__main__":
    test_narrative_generation()
