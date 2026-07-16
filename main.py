import os
import sys

# Force the project root into the Python path
sys.path.insert(0, os.getcwd())

# Now imports will resolve correctly
from backend.data_collector import run_ingestion
from backend.Starworld_optimizer import run_optimizer
from backend.core_analytics import check_alert_threshold

# --- Rest of your main.py logic ---
