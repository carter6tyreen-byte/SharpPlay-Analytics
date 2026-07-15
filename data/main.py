import logging
from data.data_collector import run_ingestion
from simulations.simulator import run_monte_carlo
from analytics.matchup_engine import analyze_matchups
# Import new modules as you build them

# Configure logging for GitHub Actions visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_orchestrator():
    try:
        logging.info("--- Starting SharpPLAY Pipeline ---")
        
        # 1. Ingestion
        data = run_ingestion()
        
        # 2. Simulation
        sim_results = run_monte_carlo(data)
        
        # 3. Decision & Analytics
        final_picks = analyze_matchups(sim_results)
        
        # 4. Publication
        # publish_to_github_pages(final_picks)
        
        logging.info("--- Pipeline Completed Successfully ---")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        # Here, you could add an alert trigger (e.g., email or Discord notification)
        raise

if __name__ == "__main__":
    run_orchestrator()
