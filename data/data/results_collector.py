import requests
import datetime
import json
import logging

def fetch_yesterdays_results():
    """
    Fetches the final scores of games played yesterday to compare 
    against our archived predictions.
    """
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    logging.info(f"Fetching results for {yesterday}...")
    
    # Replace this URL with your specific API endpoint for game scores
    # Example: MLB Stats API or similar source
    url = f"https://api.your-sports-data.com/scores?date={yesterday}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
        
        # Structure the results for the Audit Loop
        formatted_results = []
        for game in results['games']:
            formatted_results.append({
                "game_id": game['id'],
                "actual_winner": game['winner'],
                "final_score": game['score'],
                "date": yesterday
            })
            
        return formatted_results
        
    except Exception as e:
        logging.error(f"Failed to fetch results: {e}")
        return []

if __name__ == "__main__":
    # Test execution
    data = fetch_yesterdays_results()
    print(json.dumps(data, indent=2))
