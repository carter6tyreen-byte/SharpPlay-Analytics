import sys
import os

# Adds the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audit.sharplays import SharplaysAudit

from mlb_stats import fetch_mlb_data
from audit.sharplays import SharplaysAudit

def main():
    print("Starting pipeline...")
    data = fetch_mlb_data()
    
    # Pass data to the audit engine
    audit_engine = SharplaysAudit()
    audit_engine.run(data=data)
    print("Pipeline complete.")

if __name__ == "__main__":
    main()
