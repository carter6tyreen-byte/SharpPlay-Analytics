import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / 'data' / 'today_matchups.json'
OUTPUT_FILE = BASE_DIR / 'data' / 'processed_matchups.json'

def process_matchup_data():
    with open(INPUT_FILE, 'r') as f:
        raw = json.load(f)
    
    processed = []
    for d in raw.get('dates', []):
        for g in d.get('games', []):
            processed.append({"game_pk": g['gamePk'], "away": g['teams']['away']['team']['name'], "home": g['teams']['home']['team']['name']})
            
    with open(OUTPUT_FILE, 'w') as f:
        json.dump({"matchups": processed}, f, indent=4)
    print("Processing complete.")
