import json
import glob
import logging

def calculate_weekly_brier():
    """
    Scans the archive/ directory and calculates the average Brier Score
    to provide a 'sharpness' report for the week.
    """
    archive_files = glob.glob("archive/predictions_*.json")
    total_brier = 0
    count = 0
    
    for file in archive_files:
        with open(file, 'r') as f:
            for line in f:
                data = json.loads(line)
                # Brier Score = (predicted_prob - actual_outcome)^2
                # Note: 'actual' must be reconciled from your results_collector
                if 'actual_outcome' in data:
                    score = (data['win_prob'] - data['actual_outcome'])**2
                    total_brier += score
                    count += 1
    
    avg_brier = total_brier / count if count > 0 else 0
    logging.info(f"--- Weekly Performance Report ---")
    logging.info(f"Average Brier Score: {avg_brier:.3f}")
    logging.info(f"Interpretation: {'Excellent' if avg_brier < 0.2 else 'Needs Tuning'}")
    
    return avg_brier

# Interpretation guide:
# 0.0 = Perfect prediction
# 0.25 = Equivalent to a random guess (0.5 probability)
