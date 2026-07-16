import sys
import os
import json

# Fix: Point Python to the root directory so it can find the 'analytics' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analytics.matchup_engine import AnalyticsEngine
from analytics.tuner import StarworldOptimizer
from analytics.exporter import save_analytics

def run_pipeline():
    print("Starting SharpPLAY Pipeline...")
    
    # 1. Fetch Data (Assume your scraper logic is already here)
    # raw_data = ... 
    
    # 2. Process Analytics
    engine = AnalyticsEngine(raw_data)
    edges = engine.analyze_matchups(raw_data)
    
    # 3. STARWORLD Optimization
    # Tuner selects the best combination based on risk and edge
    tuner = StarworldOptimizer(risk_tolerance=0.5, max_picks=3)
    portfolio = tuner.optimize_portfolio(edges)
    
    # 4. Export for Dashboard
    # This saves to data/analytics_data.json
    save_analytics(portfolio)
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()
