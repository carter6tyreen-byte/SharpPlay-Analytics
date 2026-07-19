import requests
import datetime
import json
import logging
import os

# Configure logging for GitHub Actions visibility
logging.basicConfig(level=logging.INFO)

def fetch_yesterdays_results():
    """
    Fetches game results and saves them to the data/ directory.
    """
    # Calculate yesterday's date
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    logging.info(f"Fetching results for {yesterday}...")
    
    # API configuration
    url = f"https://api.your-sports-data.com/scores?date={yesterday}"
    
    try:
        # Request with timeout to prevent hanging workflows
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Ensure the 'data' directory exists in the root
        os.makedirs('data', exist_ok=True)
        
        # Define flat path (no nested directories)
        output_path = os.path.join('data', 'audit_results.json')
        
        # Save results
        with open(output_path, 'w') as f:
            # We assume 'games' is the key; adjust if your API structure differs
            games = data.get('games', [])
            json.dump(games, f, indent=2)
            
        logging.info(f"Results successfully saved to {output_path}")
        return games
        
    except Exception as e:
        logging.error(f"Failed to fetch results: {e}")
        return []

if __name__ == "__main__":
    fetch_yesterdays_results()
