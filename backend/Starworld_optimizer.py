def calculate_closeness(game):
    # Closeness: Lower is tighter
    return abs(game.get("homeScore", 0) - game.get("awayScore", 0))

def calculate_pace(game):
    # Pace: Runs per inning (avoid division by zero)
    inning = game.get("inning", 1)
    total_runs = game.get("homeScore", 0) + game.get("awayScore", 0)
    return round(total_runs / inning, 2) if inning > 0 else 0

def calculate_intensity(game):
    # Intensity: High if late inning and close score
    inning = game.get("inning", 1)
    closeness = calculate_closeness(game)
    return "High" if inning >= 7 and closeness <= 2 else "Normal"

def run_optimizer(data):
    # 1. Defensive Extraction
    dates = data.get("dates", [])
    if not dates: return []
    games = dates[0].get("games", [])
    if not games: return []

    # 2. Transformation & Enrichment
    processed_games = []
    for game in games:
        # Standardize the game data
        game_data = {
            "homeTeam": game.get("teams", {}).get("home", {}).get("team", {}).get("name", "Home"),
            "awayTeam": game.get("teams", {}).get("away", {}).get("team", {}).get("name", "Away"),
            "homeScore": game.get("teams", {}).get("home", {}).get("score", 0),
            "awayScore": game.get("teams", {}).get("away", {}).get("score", 0),
            "status": game.get("status", {}).get("detailedState", "Scheduled"),
            "inning": game.get("linescore", {}).get("currentInning", 1)
        }

        # 3. Apply the Analysis Suite
        game_data["analytics"] = {
            "closeness": calculate_closeness(game_data),
            "pace": calculate_pace(game_data),
            "intensity": calculate_intensity(game_data)
        }
        
        processed_games.append(game_data)
        
    return processed_games
