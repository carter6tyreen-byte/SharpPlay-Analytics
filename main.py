import sys
import os

# Adds the parent directory to the system path so it can find the 'audit' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audit.sharplays import SharplaysAudit
