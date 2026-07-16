import json
from pathlib import Path

# Set paths relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / 'data' / 'today_matchups.json'
OUTPUT_FILE = BASE_DIR / 'data' / 'processed_matchups.json'

def process_matchup_data():
    """Reads raw matchups and processes them for the dashboard."""
    try:
        with open(INPUT_FILE, 'r') as f:
            raw_data = json.load(f)
            
        processed_list = []
        # Accessing data based on MLB API schedule structure
        for date_data in raw_data.get('dates', []):
            for game in date_data.get('games', []):
                processed_list.append({
                    "game_pk": game.get('gamePk'),
                    "away_team": game['teams']['away']['team']['name'],
                    "home_team": game['teams']['home']['team']['name'],
                    "status": game['status']['detailedState']
                })
            
        with open(OUTPUT_FILE, 'w') as f:
            json.dump({"matchups": processed_list}, f, indent=4)
            
        print(f"Successfully processed {len(processed_list)} games to {OUTPUT_FILE}")
        
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Ensure the scraper has run.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_matchup_data()
