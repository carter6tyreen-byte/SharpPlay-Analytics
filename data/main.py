# main.py
import logging
from data.data_collector import fetch_all_data
from simulations.simulator import run_monte_carlo
# from decision.ai_engine import run_decision_layer  # Upcoming module

def run_pipeline():
    logging.info("Starting SharpPLAY Analytics Pipeline...")
    
    # 1. Ingestion
    raw_data = fetch_all_data()
    
    # 2. Simulation
    simulation_results = run_monte_carlo(raw_data)
    
    # 3. Decision (Placeholder for future)
    # recommendations = run_decision_layer(simulation_results)
    
    # 4. Publication
    # publish_to_dashboard(recommendations)
    
    logging.info("Pipeline completed successfully.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()
