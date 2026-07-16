import pandas as pd

def process_raw_api_data(raw_json):
    # Logic to parse JSON into a clean DataFrame
    df = pd.DataFrame(raw_json)
    # Perform cleaning: fill NAs, format dates, etc.
    return df
