import pandas as pd
import glob
import os

def consolidate_player_metrics(input_folder='data', output_file='data/master_player_metrics.csv'):
    all_files = glob.glob(os.path.join(input_folder, "*.csv"))
    files_to_process = [f for f in all_files if os.path.basename(f) != os.path.basename(output_file)]
    
    if not files_to_process:
        print("No files found.")
        return

    df_list = []
    for filename in files_to_process:
        df = pd.read_csv(filename)
        
        # 1. Calculate 'is_hard_hit' dynamically if exit_velocity exists
        if 'exit_velocity' in df.columns:
            df['is_hard_hit'] = (df['exit_velocity'] >= 95).astype(int)
        
        df_list.append(df)
            
    # 2. Concatenate all data
    master_df = pd.concat(df_list, axis=0, ignore_index=True)
    
    # 3. Aggregate by player and pitch type
    # This creates the granular view needed for your Trend Scanner
    groupby_cols = ['player_id', 'pitch_type']
    
    agg_df = master_df.groupby(groupby_cols).agg({
        'exit_velocity': 'mean',
        'is_hard_hit': 'mean',  # This now represents your HardHit%
        'launch_angle': 'mean'
    }).reset_index()
    
    # Rename columns for clarity
    agg_df.rename(columns={'is_hard_hit': 'hard_hit_rate'}, inplace=True)
    
    # 4. Save
    agg_df.to_csv(output_file, index=False)
    print(f"Master file updated with granular pitch data: {output_file}")

if __name__ == "__main__":
    consolidate_player_metrics()
