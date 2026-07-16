import json
from pathlib import Path

# Set paths relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / 'data' / 'today_matchups.json'
OUTPUT_FILE = BASE_DIR / 'data' / 'processed_matchups.json'

def process_matchup_data():
    """Reads raw matchups and processes them with additional metrics."""
    try:
        with open(INPUT_FILE, 'r') as f:
            raw_data = json.load(f)
            
        processed_list = []
        
        # Accessing the schedule data
        for date_data in raw_data.get('dates', []):
            for game in date_data.get('games', []):
                # Core game info
                game_info = {
                    "game_pk": game.get('gamePk'),
                    "away_team": game['teams']['away']['team']['name'],
                    "home_team": game['teams']['home']['team']['name'],
                    "status": game['status']['detailedState'],
                    
                    # Placeholder for your specific analytics metrics
                    "expected_hr_probability": "TBD", # You can calculate this here
                    "pitcher_data": "Pending Analysis", # Placeholder for your pitcher data
                    "betting_market": "Data Loading..."  # Placeholder for betting market integration
                }
                processed_list.append(game_info)
            
        with open(OUTPUT_FILE, 'w') as f:
            json.dump({"matchups": processed_list}, f, indent=4)
            
        print(f"Successfully processed {len(processed_list)} games.")
        
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Ensure the scraper has run.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_matchup_data()
