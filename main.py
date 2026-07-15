import sys
import os

# Get the absolute path to the project root (one level up from 'data')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ensure the root is in the path
if project_root not in sys.path:
    sys.path.append(project_root)

# Now it can find 'audit.sharplays'
from audit.sharplays import SharplaysAudit
