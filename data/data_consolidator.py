import pandas as pd
from pathlib import Path

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
    all_files = list(RAW_DATA_DIR.glob("*.csv"))
    
    if not all_files:
        print("No raw data files found to consolidate.")
        return

    # Load and combine all raw CSVs
    df_list = [pd.read_csv(file) for file in all_files]
    combined_df = pd.concat(df_list, ignore_index=True)

    # Core Logic: Group by player and pitch type to get averages
    # This assumes your raw data has columns: player_id, player_name, 
    # pitch_type, exit_velocity, launch_angle, is_hard_hit
    master_df = combined_df.groupby(['player_id', 'player_name', 'pitch_type']).agg({
        'exit_velocity': 'mean',
        'launch_angle': 'mean',
        'is_hard_hit': 'mean' # This creates your HardHit%
    }).reset_index()

    # Save to the data/ directory
    master_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Successfully consolidated {len(all_files)} files into {OUTPUT_FILE}")

if __name__ == "__main__":
    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    consolidate_player_metrics()
