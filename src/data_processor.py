import pandas as pd

def process_raw_api_data(raw_data):
    """
    Converts raw JSON into a clean Pandas DataFrame.
    This makes it easy to perform math on the stats.
    """
    # Assuming 'raw_data' is a list of player stats
    df = pd.DataFrame(raw_data)
    
    # 1. Handle missing values
    df = df.fillna(0)
    
    # 2. Select only the columns you need for the HR model
    cols_to_keep = ['player_name', 'hr_count', 'at_bats', 'launch_angle']
    clean_df = df[cols_to_keep]
    
    return clean_df
