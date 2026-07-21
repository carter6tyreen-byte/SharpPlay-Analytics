import json
import glob
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
                try:
                    data = json.loads(line)
                    if 'actual_outcome' in data and 'win_prob' in data:
                        score = (float(data['win_prob']) - float(data['actual_outcome']))**2
                        total_brier += score
                        count += 1
                except json.JSONDecodeError:
                    continue
    
    avg_brier = total_brier / count if count > 0 else 0
    logging.info(f"--- Weekly Performance Report ---")
    logging.info(f"Average Brier Score: {avg_brier:.3f}")
    logging.info(f"Interpretation: {'Excellent (<0.20)' if avg_brier < 0.2 else 'Needs Tuning (>0.25)'}")
    
    return avg_brier

if __name__ == "__main__":
    calculate_weekly_brier()
