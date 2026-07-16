import pandas as pd

def process_raw_api_data(raw_data):
    """
    Takes raw JSON data from the API and cleans it for analysis.
    """
    # Check if raw_data is empty
    if not raw_data:
        return pd.DataFrame()
    
    # Convert list of dicts to a DataFrame
    df = pd.DataFrame(raw_data)
    
    # Ensure numeric columns exist (convert where necessary)
    numeric_cols = ['at_bats', 'hr_count']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Feature Engineering: Calculate Home Run Rate
    # We add a small constant to prevent division by zero
    df['hr_rate'] = df['hr_count'] / (df['at_bats'] + 1)
    
    return df
