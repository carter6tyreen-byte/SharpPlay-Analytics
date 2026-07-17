import pandas as pd
# Assuming you have your existing API setup here

class AnalyticsEngine:
    def __init__(self):
        # Your existing initialization
        pass

    def get_pitcher_data(self):
        # Your existing logic for fetching/processing pitcher stats
        # Ensure this returns a clean pandas DataFrame
        return pd.DataFrame(...) 

    def get_batter_data(self):
        # Logic to fetch hitting stats (OPS, AVG, HR, RBI, ISO)
        # Use a different endpoint or filter for 'hitter'
        return pd.DataFrame(...)

