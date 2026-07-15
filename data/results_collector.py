import requests
import datetime
import logging

# Configure logging for pipeline visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_yesterdays_results():
    """
    Retrieves the final outcomes of games from the previous calendar day.
    Returns a list of dictionaries structured for the reconciliation engine.
    """
    # Calculate yesterday's date
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    logging.info(f"Initiating data collection for: {yesterday}")
    
    # NOTE: Replace 'YOUR_API_ENDPOINT' with your actual MLB data source.
    # Ensure the structure matches your simulator's game_id identifiers.
    url = f"https://api.your-sports-data.com/v1/scores?date={yesterday}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        reconciled_data = []
        
        # Parse the JSON response
        for game in data.get('games', []):
            reconciled_data.append({
                "game_id": game['id'],
                "winner": "HOME" if game['home_score'] > game['away_score'] else "AWAY",
                "home_score": game['home_score'],
                "away_score": game['away_score'],
                "date": yesterday
            })
            
        logging.info(f"Successfully retrieved {len(reconciled_data)} game results.")
        return reconciled_data
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching results from API: {e}")
        return []

if __name__ == "__main__":
    # Allows for standalone testing of the data collector
    results = fetch_yesterdays_results()
    for entry in results:
        print(f"Game ID: {entry['game_id']} | Winner: {entry['winner']}")
