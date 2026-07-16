from datetime import datetime

class PreGameSnapshot:
    def __init__(self, game_id, date, player, features):
        self.game_id = game_id
        self.date = date
        self.player = player
        self.features = features  # Dictionary of predictive stats
        # Use a real timestamp to ensure accuracy
        self.timestamp_captured = datetime.now().isoformat() 
