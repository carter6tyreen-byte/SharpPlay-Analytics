import sys
import os

# Force the audit directory into the path if standard imports fail
sys.path.append(os.path.join(os.getcwd(), 'audit'))

from sharplays import SharplaysAudit
# In your main.py
from audit.sharplays import SharplaysAudit
