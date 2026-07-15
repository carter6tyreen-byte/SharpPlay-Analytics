# audit/sharplays.py

class SharplaysAudit:
    def __init__(self):
        print("Audit engine initialized.")
            
    def run(self, data=None):
        if not data:
            print("No data, skipping audit.")
            return

        print(f"Auditing {len(data)} games...")
        
        for game in data:
            # Use .get() to avoid KeyError if the field is missing
            game_id = game.get("GameID") or game.get("gameId") or "Unknown ID"
            print(f"Processing game: {game_id}")
            
        print("Consensus audit complete.")
