# --- Corrected main.py Logic ---

# 1. First, extract the names from your API data structure
away_name = game['teams']['away']['team']['name']
home_name = game['teams']['home']['team']['name']

# 2. Then, define the pitcher data (example paths; adjust to your API source)
home_pitcher = game['teams']['home'].get('pitcher', {})
away_pitcher = game['teams']['away'].get('pitcher', {})

# 3. Now construct the dictionary using the defined variables
game_data = {
    "matchup": f"{away_name} vs {home_name}",
    "teams": {
        "home": {
            "name": home_name,
            "pitcher_stats": {
                "name": home_pitcher.get('fullName', 'N/A'),
                "era": home_pitcher.get('era', '0.00'),
                "whip": home_pitcher.get('whip', '0.00'),
                "k_per_9": home_pitcher.get('kPer9', '0.0')
            }
        },
        "away": {
            "name": away_name,
            "pitcher_stats": {
                "name": away_pitcher.get('fullName', 'N/A'),
                "era": away_pitcher.get('era', '0.00'),
                "whip": away_pitcher.get('whip', '0.00'),
                "k_per_9": away_pitcher.get('kPer9', '0.0')
            }
        }
    }
}
