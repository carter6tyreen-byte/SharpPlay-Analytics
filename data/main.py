import logging
from data.data_collector import run_ingestion
from simulations.simulator import MonteCarloSimulator
from analytics.matchup_engine import analyze_matchups

# Configure logging for GitHub Actions visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    logging.info("--- Starting SharpPLAY Analytics Pipeline ---")
    
    try:
        # 1. Ingestion: Fetch data from your collectors
        data = run_ingestion()
        
        # 2. Simulation: Use the new class-based simulator
        # Running 10,000 iterations per game for high confidence
        simulator = MonteCarloSimulator(iterations=10000)
        sim_results = simulator.run(data)
        
        # 3. Decision: Analyze simulations for +EV opportunities
        final_picks = analyze_matchups(sim_results)
        
        # 4. Output: Log results for GitHub Actions/Dashboard
        for pick in final_picks:
            logging.info(f"Analysis Complete: {pick['game']} | Edge: {pick['edge']}% | Action: {pick['action']}")
            
        logging.info("--- Pipeline Completed Successfully ---")
        
    except Exception as e:
        logging.error(f"Pipeline failed at execution: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()
