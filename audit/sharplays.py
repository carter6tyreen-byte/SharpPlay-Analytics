# audit/sharplays.py

class SharplaysAudit:
    def __init__(self):
        print("Audit engine initialized.")
            
    def run(self, data=None):
        print("Running consensus audit...")
        
        # Check if data exists and is not empty
        if not data or len(data) == 0:
            print("PIPELINE_WARNING: No data received for audit. Skipping.")
            return

        # Perform your logic here safely
        try:
            # Example: safely accessing the first game
            first_game = data[0]
            print(f"Auditing game: {first_game.get('GameID')}")
        except IndexError:
            print("PIPELINE_ERROR: Data format mismatch.")
            
        print("Consensus audit complete.")
