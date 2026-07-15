import sys
import os

# 1. ADD THIS: Tell Python to look in the parent folder (the repository root)
# This allows the script to find the 'audit' folder even when inside 'data/'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2. NOW you can import your modules normally
from audit.sharplays import SharplaysAudit

def main():
    print("--- Quantum Consensus Audit Starting ---")
    
    # Initialize the audit class
    audit_engine = SharplaysAudit()
    
    # Example logic: Load your data (you might need to adjust the path if files are also in data/)
    # For now, we pass empty data or a placeholder
    sample_data = [] 
    
    # Run the audit
    audit_engine.run(data=sample_data)
    
    print("--- Audit Process Finished ---")

if __name__ == "__main__":
    main()
