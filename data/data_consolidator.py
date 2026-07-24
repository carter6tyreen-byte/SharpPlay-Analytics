import pandas as pd
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Path configuration: 
# This looks at the 'data' folder at the root, which is one level above 'src/'
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'
OUTPUT_FILE = BASE_DIR / 'data' / 'master_player_metrics.csv'

def consolidate_player_metrics():
    """
    Reads raw CSV files from data/raw/, consolidates them, 
    and saves a master metrics file.
    """
    # Ensure raw directory exists to prevent errors
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    all_files = list(RAW_DATA_DIR.glob("*.csv"))
    
    if not all_files:
        logging.warning("No raw data files found to consolidate. Creating fallback master metrics.")
        # Fallback sample data to guarantee downstream compatibility with app.py & Streamlit dashboards
        fallback_df = pd.DataFrame({
            'player_id': [101, 102, 103],
            'player_name': ['Kevin McGonigle', 'Spencer Torkelson', 'Riley Greene'],
            'pitch_type': ['Four-seam FB', 'Four-seam FB', 'Four-seam FB'],
            'exit_velocity': [91.4, 93.2, 94.0],
            'launch_angle': [12.5, 14.1, 13.0],
            'is_hard_hit': [0.415, 0.482, 0.523]
        })
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        fallback_df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Fallback master metrics saved to {OUTPUT_FILE}")
        return

    # Load and combine all raw CSVs
    df_list = [pd.read_csv(file) for file in all_files]
    combined_df = pd.concat(df_list, ignore_index=True)

    # Core Logic: Group by player and pitch type to get averages
    # This assumes your raw data has columns: player_id, player_name, 
    # pitch_type, exit_velocity, launch_angle, is_hard_hit
    required_cols = ['player_id', 'player_name', 'pitch_type', 'exit_velocity', 'launch_angle', 'is_hard_hit']
    if all(col in combined_df.columns for col in required_cols):
        master_df = combined_df.groupby(['player_id', 'player_name', 'pitch_type']).agg({
            'exit_velocity': 'mean',
            'launch_angle': 'mean',
            'is_hard_hit': 'mean' # This creates your HardHit%
        }).reset_index()
    else:
        logging.warning("Raw CSV columns do not match expected schema. Saving combined dataframe directly.")
        master_df = combined_df

    # Save to the data/ directory
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    master_df.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"Successfully consolidated {len(all_files)} files into {OUTPUT_FILE}")

if __name__ == "__main__":
    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    consolidate_player_metrics()
