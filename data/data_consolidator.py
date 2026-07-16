import pandas as pd
import glob
import os

def consolidate_player_metrics(input_folder='data', output_file='data/master_player_metrics.csv'):
    """
    Consolidates player performance files into a master CSV.
    Aligns metrics across different data sources.
    """
    all_files = glob.glob(os.path.join(input_folder, "*.csv"))
    
    # 1. Filter out the master file if it exists to avoid infinite appending
    files_to_process = [f for f in all_files if os.path.basename(f) != os.path.basename(output_file)]
    
    if not files_to_process:
        print("No player metric files found to consolidate.")
        return

    df_list = []
    for filename in files_to_process:
        try:
            df = pd.read_csv(filename)
            # 2. Standardize column names (e.g., ensure 'wrc_plus' vs 'wRC+' are mapped)
            df.columns = [col.lower().replace(' ', '_').replace('+', '') for col in df.columns]
            df_list.append(df)
            print(f"Processed: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    # 3. Concatenate and clean
    master_df = pd.concat(df_list, axis=0, ignore_index=True)
    
    # Ensure standard date formatting for longitudinal player tracking
    if 'date' in master_df.columns:
        master_df['date'] = pd.to_datetime(master_df['date'])
        master_df = master_df.sort_values(['player_id', 'date'])
    
    # 4. Save
    master_df.to_csv(output_file, index=False)
    print(f"---")
    print(f"Master Player Metrics created: {output_file}")
    print(f"Total records: {len(master_df)}")

if __name__ == "__main__":
    consolidate_player_metrics()
