import os
import sys

# --- ROBUST PATH INJECTION ---
# This ensures that even in restricted CI/CD environments, 
# the interpreter finds the 'backend' folder as a package.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# -----------------------------

import json
from datetime import datetime, timedelta

# Now these imports will resolve correctly
from backend.data_collector import run_ingestion
from backend.Starworld_optimizer import run_optimizer
from backend.core_analytics import check_alert_threshold

# ... rest of your code ...
