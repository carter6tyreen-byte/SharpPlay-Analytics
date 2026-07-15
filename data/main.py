import logging
from data.data_collector import run_ingestion
from data.results_collector import fetch_yesterdays_results
from simulations.simulator import MonteCarloSimulator
from analytics.matchup_engine import analyze_matchups
from database.recorder import archive_prediction, reconcile_performance

def run_pipeline():
    logging.info("--- SharpPLAY Analytics: Pipeline Cycle Initiated ---")
    
    try:
        # STEP 1: AUDIT & RECONCILE (Learning Loop)
        # Fetch yesterday's actuals and compare to yesterday's archived predictions
        logging.info("Reconciling yesterday's performance...")
        actuals = fetch_yesterdays_results()
        reconcile_performance(actuals) # Updates accuracy metrics/Brier score
        
        # STEP 2: INGESTION (Fresh Data)
        data = run_ingestion()
        
        # STEP 3: SIMULATION (Predictive Phase)
        simulator = MonteCarloSimulator(iterations=10000)
        sim_results = simulator.run(data)
        
        # STEP 4: DECISION ENGINE (+EV Analysis)
        final_picks = analyze_matchups(sim_results)
        
        # STEP 5: ARCHIVE (Theory Stored for Tomorrow's Audit)
        for pick in final_picks:
            archive_prediction(pick)
            logging.info(f"Archived prediction for: {pick['game']}")
            
        logging.info("--- Pipeline Completed: Cycle Closed ---")
        
    except Exception as e:
        logging.error(f"Critical Pipeline Failure: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()
