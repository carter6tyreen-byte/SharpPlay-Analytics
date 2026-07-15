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
