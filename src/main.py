import sys
import os

# Ensure the root directory is in the path to find the 'analytics' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports
from matchup_scraper import fetch_matchup_data
from analytics.matchup_engine import AnalyticsEngine
from analytics.tuner import StarworldOptimizer
from analytics.exporter import save_analytics

def run_pipeline():
    print("Starting SharpPLAY Pipeline...")
    
    # 1. Fetch Data
    print("Phase 1: Fetching matchups...")
    raw_data = fetch_matchup_data() 
    
    # Diagnostic Check: Ensure data exists before proceeding
    if raw_data is None:
        print("ERROR: fetch_matchup_data() returned None. Check your scraper!")
        return 
        
    print(f"DEBUG: Successfully fetched {len(raw_data)} records.")
    
    # 2. Process Analytics
    print("Phase 2: Processing analytics...")
    engine = AnalyticsEngine(raw_data)
    edges = engine.analyze_matchups(raw_data)
    
    # 3. STARWORLD Optimization
    print("Phase 3: Running STARWORLD Engine...")
    tuner = StarworldOptimizer(risk_tolerance=0.5, max_picks=3)
    portfolio = tuner.optimize_portfolio(edges)
    
    # 4. Export for Dashboard
    save_analytics(portfolio)
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()

# Example logic for main.py
# After fetching game info, for each team (home/away):
# pitcher_stats = fetch_pitcher_data(pitcher_id) 

game_data = {
    "matchup": f"{away_name} vs {home_name}",
    "teams": {
        "home": {
            "name": home_name,
            "pitcher_stats": {
                "name": home_pitcher_name,
                "era": home_era,
                "whip": home_whip,
                "k_per_9": home_k9
            }
        },
        "away": {
            "name": away_name,
            "pitcher_stats": {
                "name": away_pitcher_name,
                "era": away_era,
                "whip": away_whip,
                "k_per_9": away_k9
            }
        }
    }
}
# Write this to today_matchups.json
