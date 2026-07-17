import json
import os

def save_analytics(data):
    """
    Saves the processed analytics data to a JSON file.
    """
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save the data
    output_path = os.path.join('data', 'analytics_data.json')
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Analytics successfully saved to {output_path}")
