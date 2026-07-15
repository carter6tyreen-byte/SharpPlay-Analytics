import requests
import sys

def fetch_mlb_data():
    try:
        response = requests.get("YOUR_API_ENDPOINT", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"PIPELINE_ERROR: Stage 1 Ingestion failed: {e}")
        return None

def main():
    data = fetch_mlb_data()
    if not data:
        sys.exit(1)
    
    # Simple check for critical fields required by Stage 2
    if 'no_vig_prob' not in data:
        print("MARKET_GATE_ERROR: Missing no-vig probability.")
        sys.exit(1)
        
    print("Stage 1 & 2: Pipeline clear for Quantum Encoding.")

if __name__ == "__main__":
    main()
