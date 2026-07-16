import sys
import os

# This adds the current folder to the path, even if GitHub moves the runner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets
