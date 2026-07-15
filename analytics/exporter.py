import json
import glob
import os

def export_to_frontend():
    """
    Consolidates raw archive data into a clean JSON for the website.
    """
    archive_files = sorted(glob.glob("archive/predictions_*.json"))
    frontend_data = {"dates": [], "scores": []}
    
    for file in archive_files:
        # Extract date from filename
        date = file.split('_')[-1].replace('.json', '')
        
        with open(file, 'r') as f:
            lines = [json.loads(line) for line in f]
            # Calculate daily average Brier score for the chart
            scores = [(l['win_prob'] - 1)**2 for l in lines] # simplified for demo
            avg_score = sum(scores) / len(scores)
            
            frontend_data['dates'].append(date)
            frontend_data['scores'].append(round(avg_score, 3))
            
    with open('public/data.json', 'w') as f:
        json.dump(frontend_data, f)
