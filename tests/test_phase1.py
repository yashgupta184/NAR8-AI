# tests/test_phase1.py
from config.settings import Config

def test_config():
    print(f"App Name: {Config.APP_NAME}")
    print(f"LLM Provider: {Config.LLM_PROVIDER}")
    print(f"LLM Model: {Config.LLM_MODEL}")
    print(f"Mock Data Mode: {Config.USE_MOCK_DATA}")
    print(f"Output Dir: {Config.OUTPUT_DIR}")

    warnings = Config.validate()
    if warnings:
        print("\n⚠ Warnings:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("\n✅ All configuration checks passed.")

if __name__ == "__main__":
    test_config()
