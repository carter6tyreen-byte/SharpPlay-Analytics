import logging
from data.data_collector import run_ingestion
from data.results_collector import fetch_yesterdays_results
from simulations.simulator import MonteCarloSimulator
from analytics.matchup_engine import analyze_matchups
from database.recorder import archive_prediction
from analytics.tuner import tune_team_ratings
from analytics.exporter import export_to_frontend

def run_pipeline():
    # 1. Audit & Tune
    actuals = fetch_yesterdays_results()
    if actuals:
        adjustments = tune_team_ratings(previous_predictions, actuals)
        # Apply adjustments logic here
    
    # 2. Ingest & Simulate
    data = run_ingestion()
    simulator = MonteCarloSimulator(iterations=10000)
    sim_results = simulator.run(data)
    
    # 3. Decide & Archive
    final_picks = analyze_matchups(sim_results)
    for pick in final_picks:
        archive_prediction(pick)
        
    # 4. Publish
    export_to_frontend()

if __name__ == "__main__":
    run_pipeline()
