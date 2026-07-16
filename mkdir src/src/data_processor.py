import json
from pathlib import Path

# Set paths relative to project root (up one level from src)
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / 'data' / 'today_matchups.json'
OUTPUT_FILE = BASE_DIR / 'data' / 'processed_matchups.json'

def process_matchup_data():
    """Reads raw matchups and processes them for the dashboard."""
    try:
        # Load the raw data
        with open(INPUT_FILE, 'r') as f:
            raw_data = json.load(f)
            
        # Example processing: Extracting only the necessary fields
        # Adjust this logic based on your specific dashboard requirements
        processed_list = []
        
        # Accessing data_points from the JSON structure
        games = raw_data.get('payload', {}).get('data_points', [])
        
        for game in games:
            # Clean or format the data here
            clean_game = {
                "matchup": f"{game.get('away_team')} @ {game.get('home_team')}",
                "status": game.get('status', 'Unknown')
            }
            processed_list.append(clean_game)
            
        # Save the processed data
        with open(OUTPUT_FILE, 'w') as f:
            json.dump({"matchups": processed_list}, f, indent=4)
            
        print(f"Successfully processed {len(processed_list)} games to {OUTPUT_FILE}")
        
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Ensure scraper has run.")
    except Exception as e:
        print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    process_matchup_data()
