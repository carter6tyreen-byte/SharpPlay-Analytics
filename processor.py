import pandas as pd
import logging

# Set up logging to track data issues in your GitHub Action logs
logging.basicConfig(level=logging.INFO)

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
        df = df.dropna(how='all') # Remove rows that are entirely empty
        
        # 2. Example: Convert a column to datetime if it exists
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            
        # 3. Example: Fill missing values for specific numeric columns
        # df['odds'] = df['odds'].fillna(0)
        
        logging.info(f"Successfully processed DataFrame with {len(df)} rows.")
        return df

    except Exception as e:
        logging.error(f"Error processing API data: {e}")
        return pd.DataFrame()
