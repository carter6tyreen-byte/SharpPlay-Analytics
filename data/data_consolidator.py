import pandas as pd
import glob
import os

def consolidate_data(input_folder, output_file):
    # Get list of all CSV/JSON files in the folder
    all_files = glob.glob(os.path.join(input_folder, "*.csv")) # Change to .json if needed
    
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
        
    master_df = pd.concat(li, axis=0, ignore_index=True)
    
    # Ensure standard sorting for the backtester
    master_df['date'] = pd.to_datetime(master_df['date'])
    master_df = master_df.sort_values('date')
    
    # Export to master file
    master_df.to_csv(output_file, index=False)
    print(f"Consolidation complete: {len(master_df)} rows saved to {output_file}")

if __name__ == "__main__":
    consolidate_data('data/', 'data/master_historical_data.csv')
