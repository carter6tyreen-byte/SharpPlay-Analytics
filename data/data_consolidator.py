from pathlib import Path
import pandas as pd

# The current file is in 'src/', so we go to parent (..) then into 'data/'
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
MASTER_FILE = DATA_DIR / 'master_player_metrics.csv'

def consolidate_player_metrics():
    # Now you can access your raw data safely
    all_files = list(RAW_DATA_DIR.glob("*.csv"))
    # ... rest of your consolidation logic
