import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_raw_api_data(raw_json):
    """
    Parses raw API JSON into a clean DataFrame with basic validation.
    """
    if not raw_json:
        logging.warning("Received empty JSON data.")
        return pd.DataFrame()

    try:
        df = pd.DataFrame(raw_json)
        
        # 1. Basic Cleaning
        df = df.dropna(how='all')
        
        # 2. Date conversion
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            
        logging.info(f"Successfully processed DataFrame with {len(df)} rows.")
        return df

    except Exception as e:
        logging.error(f"Error processing API data: {e}")
        return pd.DataFrame()

def filter_starworld_criteria(df):
    """
    Filters the DataFrame based on strict Starworld quality thresholds.
    """
    if df.empty:
        return df

    initial_count = len(df)
    
    # Apply strict validation filters
    mask = (
        (df['lineup_confirmed'] == True) &
        (df['injury_status'] == "Healthy") &
        (df['projected_plate_appearances'] >= 4) &
        (df['confidence'] >= 0.70) &
        (df['data_quality'] >= 0.90)
    )
    
    filtered_df = df[mask].copy()
    
    dropped_count = initial_count - len(filtered_df)
    logging.info(f"Starworld Filter: Dropped {dropped_count} entries. {len(filtered_df)} remain.")
    
    return filtered_df
