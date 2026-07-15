import sys
import os

# 1. Dynamically add the project root to sys.path
# This allows 'import audit' to work even when running from within 'data/'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2. Now perform the import
from audit.sharplays import SharplaysAudit

def run_audit():
    """
    Main entry point for the Quantum Consensus Audit.
    """
    print("Starting Quantum Consensus Audit...")
    
    # Initialize your audit logic
    audit = SharplaysAudit()
    
    # Run your processes
    try:
        audit.run_analysis()
        print("Audit completed successfully.")
    except Exception as e:
        print(f"Error during audit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_audit()
