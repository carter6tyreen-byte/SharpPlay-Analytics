# Import your scraper function (adjust the import based on your filename)
from src.matchup_scraper import fetch_matchup_data 

def run_pipeline():
    print("Starting SharpPLAY Pipeline...")
    
    # 1. Fetch Data: This creates the 'raw_data' variable
    print("Phase 1: Fetching matchups...")
    raw_data = fetch_matchup_data() 
    
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
